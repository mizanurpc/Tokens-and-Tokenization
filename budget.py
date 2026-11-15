import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
CONTEXT = 128_000  # model context window (tokens)
PRICE_IN = 0.15 / 1_000_000  # $ per input token (example: $0.15 per 1M tokens)

system = open("system_prompt.txt", encoding="utf-8").read()
rag = open("retrieved.txt", encoding="utf-8").read()

used = len(enc.encode(system)) + len(enc.encode(rag))

print(f"prompt so far: {used:,} tokens")
print(f"room for reply: {CONTEXT - used:,} tokens")
print(f"input cost : ${used * PRICE_IN:.4f}")