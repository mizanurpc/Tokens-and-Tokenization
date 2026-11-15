import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

samples = {
    "English": "Cybersecurity keeps your data safe",
    "Bangla": "সাইবার নিরাপত্তা সবার দরকার",
    "Emoji": "🛡️🔒💻"
}

for name, s in samples.items():
    ids = enc.encode(s)
    bpt = len(s.encode()) / len(ids) if len(ids) > 0 else 0
    print(f"{name:8} chars={len(s):3} bytes={len(s.encode()):3} "
          f"tokens={len(ids):3} bytes/tok={bpt:.1f}")