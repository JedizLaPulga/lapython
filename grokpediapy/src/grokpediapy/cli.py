"""Simple command-line interface for grokpediapy."""

import argparse
import json
import sys

from .core import fetch, FetchError


def main(argv=None):
    parser = argparse.ArgumentParser(prog="grokpediapy")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout in seconds")
    args = parser.parse_args(argv)

    q = " ".join(args.query)
    try:
        res = fetch(q, timeout=args.timeout)
    except FetchError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        raise SystemExit(2)

    # Print JSON to stdout for easy scripting.
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
