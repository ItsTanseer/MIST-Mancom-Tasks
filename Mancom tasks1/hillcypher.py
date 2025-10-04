# Hill Cipher (2x2) — encryption, decryption, and brute-force for 2x2 keys
from math import gcd
from itertools import product

ALPH = "abcdefghijklmnopqrstuvwxyz"
M = 26

def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a, m):
    g, x, y = egcd(a % m, m)
    if g != 1:
        return None
    return x % m

def text_to_nums(text):
    text = "".join(c for c in text.lower() if c.isalpha())
    return [ALPH.index(c) for c in text]

def nums_to_text(nums):
    return "".join(ALPH[n % M] for n in nums)

def pad_nums(nums, block=2, pad_char='x'):
    pad_val = ALPH.index(pad_char)
    while len(nums) % block != 0:
        nums.append(pad_val)
    return nums

def matrix_det_2x2(mat):
    return (mat[0][0]*mat[1][1] - mat[0][1]*mat[1][0]) % M

def matrix_inv_2x2(mat):
    det = matrix_det_2x2(mat)
    inv_det = modinv(det, M)
    if inv_det is None:
        return None
    a, b = mat[0]
    c, d = mat[1]
    inv = [[( d * inv_det) % M, ((-b) * inv_det) % M],
           [((-c) * inv_det) % M, ( a * inv_det) % M]]
    return inv

def mat_vec_mul(mat, vec):
    return [ (mat[0][0]*vec[0] + mat[0][1]*vec[1]) % M,
             (mat[1][0]*vec[0] + mat[1][1]*vec[1]) % M ]

def encrypt(plaintext, key_matrix):
    nums = text_to_nums(plaintext)
    nums = pad_nums(nums, block=2)
    cipher_nums = []
    for i in range(0, len(nums), 2):
        block = nums[i:i+2]
        out = mat_vec_mul(key_matrix, block)
        cipher_nums.extend(out)
    return nums_to_text(cipher_nums)

def decrypt(ciphertext, key_matrix):
    inv = matrix_inv_2x2(key_matrix)
    if inv is None:
        raise ValueError("Key matrix not invertible mod 26; cannot decrypt.")
    nums = text_to_nums(ciphertext)
    plain_nums = []
    for i in range(0, len(nums), 2):
        block = nums[i:i+2]
        out = mat_vec_mul(inv, block)
        plain_nums.extend(out)
    return nums_to_text(plain_nums).rstrip('x')

def make_key_from_tuple(t):
    return [[t[0]%M, t[1]%M],[t[2]%M, t[3]%M]]

def is_invertible_2x2(t):
    mat = make_key_from_tuple(t)
    det = matrix_det_2x2(mat)
    return gcd(det, M) == 1

def english_score(text):
    common = ["the","and","to","of","that","is","in","it","you","a"]
    score = 0
    low = text.lower()
    for w in common:
        if w in low:
            score += 5
    vowels = sum(1 for c in low if c in "aeiou")
    score += vowels * 0.5
    spaces = low.count(' ')
    score += spaces * 1.5
    return score

def brute_force_2x2(ciphertext, crib=None, top=10):
    nums = text_to_nums(ciphertext)
    if len(nums) % 2 != 0:
        raise ValueError("Ciphertext length (letters only) must be even for 2x2 Hill.")
    candidates = []
    for a,b,c,d in product(range(M), repeat=4):
        t = (a,b,c,d)
        if not is_invertible_2x2(t):
            continue
        key = make_key_from_tuple(t)
        try:
            pt = decrypt(ciphertext, key)
        except Exception:
            continue
        if crib:
            if crib.lower() in pt.lower():
                candidates.append((key, pt, None))
        else:
            sc = english_score(pt)
            candidates.append((key, pt, sc))
    if crib:
        return candidates
    candidates.sort(key=lambda x: -x[2])
    return candidates[:top]

# Demo (example)
if __name__ == "__main__":
    key = [[3,3],[2,5]]
    pt = "meet me by the park"
    ct = encrypt(pt, key)
    dec = decrypt(ct, key)
    print("Plaintext :", pt)
    print("Key matrix:", key)
    print("Ciphertext:", ct)
    print("Decrypted :", dec)
    print("\nBrute-force demo (looking for 'meet') on ciphertext:")
    bf = brute_force_2x2(ct, crib="meet")
    print(f"Found {len(bf)} keys that yield plaintext containing 'meet' (showing up to 5):")
    for k,p,s in bf[:5]:
        print("Key:", k, "->", p)
