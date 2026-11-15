import tiktoken
enc = tiktoken.encoding_for_model("gpt-4o-mini")  # note: 'gpt-4o-mini' instead of 'gpt-40-mini'
chat = (
    "<|im_start|>system\nYou are a helpful bot.<|im_end|>\n"
    "<|im_start|>user\nHello!<|im_end|>"
)
ids = enc.encode(chat, allowed_special="all")
print(len(ids), "tokens incl. role markers")
print("vocab size:", enc.n_vocab)
