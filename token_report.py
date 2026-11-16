import argparse
import unicodedata
import re
import tiktoken

# জিরো-উইডথ বা অদৃশ্য ক্যারেক্টারগুলোর লিস্ট (Normalization এর জন্য)
ZERO_WIDTH = ["\u200b", "\u200c", "\u200d", "\ufeff"]

def canonical(text):
    text = unicodedata.normalize("NFKC", text)
    for z in ZERO_WIDTH:
        text = text.replace(z, "")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def main():
    parser = argparse.ArgumentParser(description="CLI tool to analyze text files for LLM token usage.")
    parser.add_argument("file_path", type=str, help="Path to the text file to analyze.")
    parser.add_argument("--encoding", type=str, default="cl100k_base", help="Tiktoken encoding name (default: cl100k_base)")
    parser.add_argument("--viz", action="store_true", help="Visualize token pieces in brackets [piece]")
    
    args = parser.parse_args()

    # এনকোডার লোড করা
    try:
        enc = tiktoken.get_encoding(args.encoding)
    except Exception as e:
        print(f"Error loading encoding '{args.encoding}': {e}")
        return

    # ফাইল রিড করা
    try:
        with open(args.file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{args.file_path}'")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 4. Canonical প্রয়োগ করা (আগে এবং পরে টোকেন কাউন্ট তুলনা)
    clean_text = canonical(raw_text)

    raw_ids = enc.encode(raw_text)
    clean_ids = enc.encode(clean_text)

    # 2. মেট্রিকস হিসাব করা (Chars, Bytes, Tokens, Bytes/Token)
    raw_chars = len(raw_text)
    raw_bytes = len(raw_text.encode("utf-8"))
    raw_tokens = len(raw_ids)
    raw_bpt = raw_bytes / raw_tokens if raw_tokens > 0 else 0

    clean_chars = len(clean_text)
    clean_bytes = len(clean_text.encode("utf-8"))
    clean_tokens = len(clean_ids)
    clean_bpt = clean_bytes / clean_tokens if clean_tokens > 0 else 0

    # 5. খরচের হিসাব (যেমন: প্রতি ১ মিলিয়ন ইনপুট টোকেনের দাম $০.১৫)
    PRICE_IN_PER_1M = 0.15
    cost = (clean_tokens / 1_000_000) * PRICE_IN_PER_1M

    # রিপোর্ট প্রিন্ট করা
    print(f"\n--- TOKEN REPORT FOR: {args.file_path} ---")
    print(f"Encoding Used       : {args.encoding}")
    print("-" * 45)
    print(f"RAW TEXT STATS:")
    print(f"  - Characters      : {raw_chars:,}")
    print(f"  - Bytes           : {raw_bytes:,}")
    print(f"  - Tokens          : {raw_tokens:,}")
    print(f"  - Bytes/Token     : {raw_bpt:.2f}")
    print("-" * 45)
    print(f"CLEANED TEXT STATS (After canonical):")
    print(f"  - Characters      : {clean_chars:,}")
    print(f"  - Bytes           : {clean_bytes:,}")
    print(f"  - Tokens          : {clean_tokens:,} (Before: {raw_tokens:,})")
    print(f"  - Bytes/Token     : {clean_bpt:.2f}")
    print("-" * 45)
    print(f"ESTIMATED COST      : ${cost:.6f} (at ${PRICE_IN_PER_1M}/1M tokens)")
    print("=" * 45)

    # STRETCH: --viz ফ্ল্যাগ থাকলে টোকেন পিসগুলো ব্র্যাকেটে প্রিন্ট করা
    if args.viz:
        print("\nTOKEN VISUALIZATION (--viz):")
        out = []
        for tid in clean_ids:
            piece = enc.decode([tid])
            out.append(f"[{piece}]")
        print("".join(out))
        print()

if __name__ == "__main__":
    main()