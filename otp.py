import base64
from itertools import cycle

def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ k for d, k in zip(data, cycle(key)))

def encrypt_entry(username: str, password: str, notes: str, key: str) -> str:
    # Make a single plaintext block (you can change labels if you want)
    plaintext = f"USERNAME: {username}\nPASSWORD: {password}\nNOTES: {notes}"
    pt_bytes = plaintext.encode("utf-8")
    ct_bytes = xor_bytes(pt_bytes, key.encode("utf-8"))
    return base64.b64encode(ct_bytes).decode("ascii")

def decrypt_entry(cipher_b64: str, key: str) -> str:
    ct_bytes = base64.b64decode(cipher_b64.encode("ascii"))
    pt_bytes = xor_bytes(ct_bytes, key.encode("utf-8"))
    return pt_bytes.decode("utf-8", errors="strict")

def main():
    print("One-Time-Pad-Style Notebook (XOR + Base64)")
    print("[E]ncrypt  or  [D]ecrypt")
    mode = input("> ").strip().lower()

    if mode.startswith("e"):
        key = input("Enter KEY (can include spaces/symbols): ")
        username = input("Enter USERNAME: ")
        password = input("Enter PASSWORD: ")
        notes = input("Enter NOTES (can include spaces): ")
        cipher = encrypt_entry(username, password, notes, key)
        print("\n--- ENCRYPTED (Base64) ---")
        print(cipher)
        print("\nWrite that string in your notebook. Keep the KEY separate.")
    elif mode.startswith("d"):
        key = input("Enter KEY: ")
        cipher_b64 = input("Paste ENCRYPTED (Base64): ").strip()
        try:
            plaintext = decrypt_entry(cipher_b64, key)
            print("\n--- DECRYPTED ---")
            print(plaintext)
        except Exception as e:
            print("\n⚠️ Decryption failed. Check your key and ciphertext.")
    else:
        print("Choose E or D.")

if __name__ == "__main__":
    main()