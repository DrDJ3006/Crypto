from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')
shared_secret = 356899806282711561062694298246043922588995018141584959222520613500028332966666005946095780224234561634355230672437352473598384385292554847128730215416600399294049526336847022856785958799140087423032069156302102363271658996072604595325845961752322504230709012765296170897817723431876468273704177243506310454456048202185166487608895203810180371783436555541887563320820771745506878426276051923779701058430905629431752497774190149726218321724933475528999639741438358
iv = '8a6833c14663f859d572388597410cdc'
ciphertext = 'c6954f6891f7394f939415f327d2b0ab11e08f1c520f65405bc80e9e5249fa4c'

print(decrypt_flag(shared_secret, iv, ciphertext))
