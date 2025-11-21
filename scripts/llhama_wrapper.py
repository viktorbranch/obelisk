import sys
import json

# Simple wrapper that reads prompt from stdin and returns a JSON-free text response.
# It expects the full prompt (messages joined) on stdin and will print a short reply.

def main():
    prompt = sys.stdin.read()
    # Very simple heuristic: respond with first line + marker
    first_line = prompt.strip().splitlines()[0] if prompt.strip() else ""
    response = f"[LLHAMA-MOCK] Received prompt starting: {first_line}"
    # Print the response to stdout
    sys.stdout.write(response)

if __name__ == '__main__':
    main()
