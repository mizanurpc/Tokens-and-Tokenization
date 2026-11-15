import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def analyse(text):
    ids = enc.encode(text)
    pieces = [enc.decode([i]) for i in ids] # one token at a time
    print(f"{text!r}")
    print(f" chars={len(text)} bytes={len(text.encode())} tokens={len(ids)}")
    print(" pieces:", pieces)

for t in ["cybersecurity", "Cyber Security", "antidisestablishmentarianism", "GPT-40"]:
    analyse(t)
