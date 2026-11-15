import unicodedata, re

ZERO_WIDTH = ["\u200b", "\u200c", "\u200d", "\ufeff"]

def canonical(text):
    text = unicodedata.normalize("NFKC", text)
    # fold look-alikes
    for z in ZERO_WIDTH:
        text = text.replace(z, "")
    # drop invisibles
    text = re.sub(r"\s+", " ", text).strip()
    # collapse spaces
    return text
user_input = "Hello,   this  is   a   test\tinput   for cybersecurity!"
clean = canonical(user_input)

print("Original Input :", repr(user_input))
print("Cleaned Output :", repr(clean))