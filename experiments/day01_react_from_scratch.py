"""
Day 1 - ReAct from scratch (no framework).

Goal: implement a minimal ReAct (Reasoning + Acting) agent in ~200 lines,
using only the raw Anthropic / DeepSeek / OpenAI HTTP API, so we can
*see* every prompt and tool call.

The agent has three tools:
  - calc(expr)         : evaluate a Python arithmetic expression
  - read_file(path)    : read a local file
  - finish(answer)     : terminate with a final answer

Loop format (classic ReAct):
  Thought: ...
  Action: tool_name
  Action Input: <json>
  Observation: <tool result>
  ... (repeat) ...
  Thought: I now know the final answer
  Action: finish
  Action Input: {"answer": "..."}

Run:
  python experiments/day01_react_from_scratch.py "What is 17 * 23 + 5?"
  python experiments/day01_react_from_scratch.py --provider deepseek "..."
"""

from __future__ import annotations

import argparse
import ast
import json
import operator as op
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# ---------- safe arithmetic eval (no eval()) ----------

_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Mod: op.mod, ast.Pow: op.pow,
    ast.USub: op.neg, ast.UAdd: op.pos, ast.FloorDiv: op.floordiv,
}


def safe_calc(expr: str) -> float | int:
    def _eval(node: ast.AST) -> Any:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](_eval(node.operand))
        raise ValueError(f"Unsafe expression: {ast.dump(node)}")

    tree = ast.parse(expr.strip(), mode="eval")
    return _eval(tree.body)


# ---------- tool registry ----------

ToolFn = Callable[[dict], str]
TOOLS: dict[str, ToolFn] = {}


def tool(name: str) -> Callable[[ToolFn], ToolFn]:
    def deco(fn: ToolFn) -> ToolFn:
        TOOLS[name] = fn
        return fn
    return deco


@tool("calc")
def _calc(args: dict) -> str:
    try:
        return str(safe_calc(args["expr"]))
    except Exception as e:
        return f"ERROR: {e}"


@tool("read_file")
def _read_file(args: dict) -> str:
    p = Path(args["path"]).expanduser()
    if not p.is_file():
        return f"ERROR: not a file: {p}"
    return p.read_text()[:4000]


@tool("finish")
def _finish(args: dict) -> str:
    # Sentinel: the loop checks for this name and stops; payload is the answer.
    return args.get("answer", "")


# ---------- LLM providers (raw HTTP, no SDK abstractions) ----------

@dataclass
class LLMResponse:
    text: str
    usage: dict = field(default_factory=dict)


def call_anthropic(system: str, messages: list[dict], model: str | None = None) -> LLMResponse:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    model = model or os.getenv("DEFAULT_MODEL_CLAUDE", "claude-sonnet-4-5")
    resp = client.messages.create(
        model=model, system=system, messages=messages, max_tokens=1024
    )
    text = "".join(b.text for b in resp.content if b.type == "text")
    return LLMResponse(text=text, usage={"in": resp.usage.input_tokens, "out": resp.usage.output_tokens})


def call_openai_compatible(system: str, messages: list[dict], *, base_url: str, api_key: str, model: str) -> LLMResponse:
    import httpx
    msgs = [{"role": "system", "content": system}] + messages
    r = httpx.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": model, "messages": msgs, "max_tokens": 1024, "temperature": 0.2},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    return LLMResponse(text=data["choices"][0]["message"]["content"], usage=data.get("usage", {}))


def call_deepseek(system: str, messages: list[dict], model: str | None = None) -> LLMResponse:
    return call_openai_compatible(
        system, messages,
        base_url="https://api.deepseek.com/v1",
        api_key=os.environ["DEEPSEEK_API_KEY"],
        model=model or os.getenv("DEFAULT_MODEL_DEEPSEEK", "deepseek-chat"),
    )


def call_openai(system: str, messages: list[dict], model: str | None = None) -> LLMResponse:
    return call_openai_compatible(
        system, messages,
        base_url="https://api.openai.com/v1",
        api_key=os.environ["OPENAI_API_KEY"],
        model=model or os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o"),
    )


PROVIDERS = {
    "claude": call_anthropic,
    "deepseek": call_deepseek,
    "openai": call_openai,
}


# ---------- ReAct loop ----------

SYSTEM_PROMPT = """You are a ReAct agent. Solve the user's task step by step.

You have these tools:
  - calc(expr: str)            evaluate a Python arithmetic expression, e.g. {"expr": "17*23+5"}
  - read_file(path: str)       read a local text file (first 4KB), e.g. {"path": "./README.md"}
  - finish(answer: str)        ALWAYS call this last with your final answer

You MUST respond in EXACTLY this format, one block at a time:

Thought: <your reasoning in one short sentence>
Action: <one of: calc | read_file | finish>
Action Input: <a single-line JSON object>

After you emit one such block, STOP. The system will run the tool and append:
Observation: <tool output>

Then you continue with the next Thought/Action/Action Input.
When you have the answer, use Action: finish.
Do not include any other text outside this format."""


ACTION_RE = re.compile(
    r"Thought:\s*(.*?)\n+Action:\s*([a-zA-Z_]+)\s*\n+Action Input:\s*(\{.*?\})",
    re.DOTALL,
)


def parse_step(text: str) -> tuple[str, str, dict] | None:
    m = ACTION_RE.search(text)
    if not m:
        return None
    thought, action, raw_input = m.groups()
    try:
        args = json.loads(raw_input)
    except json.JSONDecodeError:
        # Try to extract first {...} on a single line
        try:
            args = json.loads(raw_input.strip().splitlines()[0])
        except Exception:
            return None
    return thought.strip(), action.strip(), args


def run_react(task: str, provider: str = "claude", max_steps: int = 8) -> str:
    call = PROVIDERS[provider]
    messages: list[dict] = [{"role": "user", "content": f"Task: {task}"}]
    print(f"\n=== Task: {task}    (provider={provider}) ===\n")

    for step in range(1, max_steps + 1):
        resp = call(SYSTEM_PROMPT, messages)
        print(f"--- step {step} | usage={resp.usage} ---")
        print(resp.text.strip())
        parsed = parse_step(resp.text)
        if not parsed:
            print("[!] could not parse step, stopping")
            return "(parse error)"

        thought, action, args = parsed
        if action == "finish":
            answer = args.get("answer", "")
            print(f"\n=== FINAL ANSWER ===\n{answer}\n")
            return answer

        if action not in TOOLS:
            obs = f"ERROR: unknown tool {action!r}"
        else:
            obs = TOOLS[action](args)

        print(f"Observation: {obs}\n")
        # Append the assistant turn and then the tool observation as a user turn,
        # so the model sees a clean alternating dialog.
        messages.append({"role": "assistant", "content": resp.text})
        messages.append({"role": "user", "content": f"Observation: {obs}"})

    return "(max steps reached)"


# ---------- CLI ----------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("task", nargs="+", help="task description")
    ap.add_argument("--provider", default=os.getenv("DEFAULT_PROVIDER", "claude"),
                    choices=list(PROVIDERS))
    ap.add_argument("--max-steps", type=int, default=8)
    args = ap.parse_args()

    task = " ".join(args.task)
    try:
        run_react(task, provider=args.provider, max_steps=args.max_steps)
    except KeyError as e:
        print(f"[!] missing API key in env: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
