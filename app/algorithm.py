ALGORITHM = {
    # Vowels (safe)
    'a' : '¿6¿',
    'e' : '¿7¿',
    'i' : '¿0¿',
    'o' : '¿9¿',
    'u' : '¿5¿',

    # Consonants (already wrapped, kept exactly the same)
    'b': '¿qb$¿',
    'c': '¿ac$¿',
    'd': '¿zd$¿',
    'f': '¿xf$¿',
    'g': '¿sg$¿',
    'h': '¿wh$¿',
    'j': '¿dj$¿',
    'k': '¿ek$¿',
    'l': '¿cl$¿',
    'm': '¿pm$¿',
    'n': '¿mn?¿',
    'p': '¿kp?¿',
    'q': '¿oq?¿',
    'r': '¿pr?¿',
    's': '¿ls?¿',
    't': '¿it?¿',
    'v': '¿jv?¿',
    'w': '¿nw?¿',
    'x': '¿yx?¿',
    'y': '¿ty?¿',
    'z': '¿nz?¿',

    # Whitespace (wrapped)
    ' '  : '¿§¿',
    '\t' : '¿===¿',
    '\n' : '¿@!¿',

    # punctuation that needed wrapping
    '!' : '¿i.¿',
    '@' : '¿(a0)¿',
    '$' : '¿s|¿',
    ';' : '¿;;¿',
    ':' : '¿::¿',
    '<' : '¿<<¿',
    '>' : '¿>>¿',

    # single-char punctuation (safe as-is)
    '#' : '#',
    '%' : '%',
    '&' : '&',
    '*' : '*',
    '(' : '(',
    ')' : ')',
    '-' : '-',
    '_' : '_',
    '=' : '=',
    '+' : '+',
    '[' : '[',
    ']' : ']',
    '{' : '{',
    '}' : '}',
    '\\' : '\\',
    '|' : '|',
    "'" : "'",
    '"' : '"',
    ',' : ',',
    '.' : '.',
    '/' : '/',
    '?' : '?',
    '`' : '`',
}


# Reverse map for fast decoding
REVERSE = {v: k for k, v in ALGORITHM.items()}

# --------------------------
#         ENCRYPT
# --------------------------
def encrypt(text: str) -> str:
    out = ""
    for ch in text:
        out += ALGORITHM.get(ch, ch)
    return out

# --------------------------
#        DECRYPT
# --------------------------
def decrypt(cipher: str) -> str:
    result = []
    i = 0
    L = len(cipher)

    while i < L:
        # 1️⃣ Check for wrapped token start
        if cipher[i] == '¿':
            # find the next ¿ AFTER this one
            end = i + 1
            while end < L and cipher[end] != '¿':
                end += 1

            # include the ending ¿
            if end < L and cipher[end] == '¿':
                token = cipher[i:end+1]
                if token in REVERSE:
                    result.append(REVERSE[token])
                    i = end + 1
                    continue
                else:
                    # unknown wrapped token, just copy
                    result.append(token)
                    i = end + 1
                    continue
            else:
                # malformed, just copy the single ¿
                result.append(cipher[i])
                i += 1
                continue

        # 2️⃣ Single-character tokens
        ch = cipher[i]
        if ch in REVERSE:
            result.append(REVERSE[ch])
            i += 1
            continue

        # 3️⃣ Passthrough for unknown characters
        result.append(ch)
        i += 1

    return "".join(result)


# --------------------------
#         TEST
# --------------------------
#text = input("Enter text to encode: ")
#enc = encrypt(text.lower())
#dec = decrypt(enc)

#print("\nEncrypted:\n", enc)
#print("\nDecrypted:\n", dec)
#print("\nSuccess:", dec == text.lower())