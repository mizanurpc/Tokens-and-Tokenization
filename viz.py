import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def show(text):
    out = []
    for tid in enc.encode(text):
        piece = enc.decode([tid]).replace(" ", ".")
        out.append(f"[{piece}]")
    print("".join(out))

show("The quick brown fox.")
show("supercalifragilistic")
show("192.168.0.1")
# watch where the tokenizer splits numbers, dots and rare words
