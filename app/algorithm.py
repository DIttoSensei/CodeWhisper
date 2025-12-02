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
    result = ""
    i = 0
    L = len(cipher)

    while i < L:
        # Detect wrapped tokens: starts & ends with ¿
        if cipher[i] == '¿':
            end = cipher.find('¿', i+1)
            if end != -1:
                chunk = cipher[i:end+1]
                if chunk in REVERSE:
                    result += REVERSE[chunk]
                    i = end + 1
                    continue

        # Try vowels or single-char tokens
        found = False
        for val, key in REVERSE.items():
            if len(val) == 1 and cipher[i:i+1] == val:
                result += key
                i += 1
                found = True
                break

        if found:
            continue

        # Unknown character
        result += cipher[i]
        i += 1

    return result


# --------------------------
#         TEST
# --------------------------
text = input("Enter text to encode: ")
enc = encrypt(text.lower())
dec = decrypt(enc)

print("\nEncrypted:\n", enc)
print("\nDecrypted:\n", dec)
print("\nSuccess:", dec == text.lower())