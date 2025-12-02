import random

# --------------------------
#  ORIGINAL BASE ALGORITHM
# --------------------------
ALGORITHM = {
    # Vowels (safe)
    'a' : '6',
    'e' : '7',
    'i' : '0',
    'o' : '9',
    'u' : '5',

    # Consonants
    'b': 'qb$',
    'c': 'ac$',
    'd': 'zd$',
    'f': 'xf$',
    'g': 'sg$',
    'h': 'wh$',
    'j': 'dj$',
    'k': 'ek$',
    'l': 'cl$',
    'm': 'pm$',
    'n': 'mn?',
    'p': 'kp?',
    'q': 'oq?',
    'r': 'pr?',
    's': 'ls?',
    't': 'it?',
    'v': 'jv?',
    'w': 'nw?',
    'x': 'yx?',
    'y': 'ty?',
    'z': 'nz?',

    # Whitespace
    ' '  : '§',
    '\t' : '===',
    '\n' : '@!',

    # punctuation (wrapped)
    '!' : 'i.',
    '@' : '(a0)',
    '$' : 's|',
    ';' : ';;',
    ':' : '::',
    '<' : '<<',
    '>' : '>>',

    # passthrough
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

# Reverse map
REVERSE = {v: k for k, v in ALGORITHM.items()}

# --------------------------
#  UPGRADE COMPONENTS
# --------------------------

# Multiple wrappers
WRAPPERS = [
    ("¿", "¿"),
    ("¡", "!"),
    ("⧼", "⧽"),
]

# Noise tokens (ignored by decoder)
NOISE = {"¤0¤", "††", "øxø", "!!!", "+++", "//", "~~"}

# --------------------------
#      SHIFT HELPERS
# --------------------------

def shift_token(token: str, salt: int) -> str:
    """Shift ONLY digits inside token."""
    out = ""
    for ch in token:
        if ch.isdigit():
            out += str((int(ch) + salt) % 10)
        else:
            out += ch
    return out

def unshift_token(token: str, salt: int) -> str:
    """Reverse shifting."""
    out = ""
    for ch in token:
        if ch.isdigit():
            out += str((int(ch) - salt) % 10)
        else:
            out += ch
    return out

# --------------------------
#          ENCRYPT
# --------------------------
def encrypt(text: str) -> str:
    salt = random.randint(1, 9)
    output = str(salt)  # prefix salt

    for ch in text:
        base = ALGORITHM.get(ch, ch)
        shifted = shift_token(base, salt)

        # choose wrapper
        w1, w2 = random.choice(WRAPPERS)
        wrapped = f"{w1}{shifted}{w2}"
        output += wrapped

        # maybe sprinkle noise
        if random.random() < 0.25:
            output += random.choice(list(NOISE))

    return output

# --------------------------
#          DECRYPT
# --------------------------
def decrypt(cipher: str) -> str:
    if not cipher:
        return ""

    # read salt
    # If ciphertext does not start with a digit → treat it as plain text
    if not cipher or not cipher[0].isdigit():
        return cipher
    salt = int(cipher[0])
    i = 1
    L = len(cipher)
    result = []

    while i < L:
        # 1️⃣ Noise?
        for noise in NOISE:
            if cipher.startswith(noise, i):
                i += len(noise)
                break
        else:
            # Not noise → check wrappers
            pass
        if i >= L:
            break

        ch = cipher[i]

        # 2️⃣ Token wrappers
        wrapper = None
        for w1, w2 in WRAPPERS:
            if ch == w1:
                wrapper = (w1, w2)
                break

        if wrapper:
            w1, w2 = wrapper
            end = i + 1
            while end < L and cipher[end] != w2:
                end += 1

            if end < L:
                token = cipher[i+1:end]  # inside only
                real = unshift_token(token, salt)
                result.append(REVERSE.get(real, real))
                i = end + 1
                continue

        # fallback
        result.append(cipher[i])
        i += 1

    return "".join(result)
