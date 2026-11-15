import tiktoken

enc = tiktoken.get_encoding("cl100k_base")	# GPT-3.5/4 family
ids = enc.encode("Stay Safe, Stay Secure")
print(ids)					#list of integer token ids
print(len(ids), "tokens")
print(enc.decode(ids))				#round-trips back to the text