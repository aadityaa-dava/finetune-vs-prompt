"""Call the local server with the same system prompt used in training. Usage: python src/client_demo.py "sentence" """
import json
import sys
import time
import urllib.request
sys.path.insert(0, "src")
from prompts import build_messages

text = sys.argv[1] if len(sys.argv) > 1 else "Pemphigus vulgaris precipitated by glibenclamide therapy."
body = json.dumps({"model": "fused_model/qwen25-3b-ade-r8", "messages": build_messages(text), "temperature": 0, "max_tokens": 256}).encode()
req = urllib.request.Request("http://127.0.0.1:8080/v1/chat/completions", data=body, headers={"Content-Type": "application/json"})
for i in range(3):
    t0 = time.perf_counter()
    r = json.load(urllib.request.urlopen(req))
    print(f"{time.perf_counter() - t0:.2f}s  {r['choices'][0]['message']['content']}")
