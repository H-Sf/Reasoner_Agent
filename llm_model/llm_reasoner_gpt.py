#!/usr/bin/env python3
"""
Return only the optimal placement in the format:
Service <id> -> Node <id>
(one per line, no extra text).
"""

import argparse
import json
import os
import sys
from openai import OpenAI

TEMPLATE_SYSTEM = (
    "You are a strict formatter. "
    "Given a placement problem, output ONLY lines like "
    "'Service <id> -> Node <id>' (one per line). "
    "No explanations, no extra text."
)

TEMPLATE_USER = "Here is the problem JSON:\n{problem_json}"

def main():
    parser = argparse.ArgumentParser(
        description="Generate optimal placement via OpenAI (GPT-5)."
    )
    parser.add_argument("--json_path", required=True, help="Path to the JSON input file.")
    parser.add_argument("--model", default="gpt-5", help="OpenAI model name (default: gpt-5).")
    args = parser.parse_args()

    try:
        with open(args.json_path, "r", encoding="utf-8") as f:
            problem = json.load(f)
    except Exception as e:
        print(f"Failed to read JSON: {e}", file=sys.stderr)
        sys.exit(1)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set. Do: export OPENAI_API_KEY='your_key'")

    client = OpenAI(api_key=api_key)

    system_msg = {"role": "system", "content": TEMPLATE_SYSTEM}
    user_msg = {
        "role": "user",
        "content": TEMPLATE_USER.format(
            problem_json=json.dumps(problem, ensure_ascii=False)
        ),
    }

    resp = client.chat.completions.create(
        model=args.model,
        messages=[system_msg, user_msg],
        temperature=0,
        max_tokens=1000,
    )

    content = resp.choices[0].message.content.strip()
    print(content)

if __name__ == "__main__":
    main()
