from simpleECDSA import ECDSA
from aes import aes_cbc_decrypt, aes_cbc_encrypt
from hashlib import sha256
import base64

G=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
ecdsa=ECDSA(0,0,7,0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,G)
privkeyA, pubkeyA= ecdsa.generate_keys(31835986277580604944851190073686914159735306555305686455075655752709537897478)
privkeyB, pubkeyB= ecdsa.generate_keys(113301334314996466357389192410842361743485829184708351926417542737247143925437)


sharedKeyA = ecdsa.scalar_multiplication(privkeyA,pubkeyB)
sharedKeyB = ecdsa.scalar_multiplication(privkeyB,pubkeyA)
msg= b'mon message super secret'
key = sha256(sharedKeyA[0].to_bytes((sharedKeyA[0].bit_length() + 7) // 8, 'big')).digest()
enc = aes_cbc_encrypt(key,msg)
print(base64.encodebytes(enc))

key = sha256(sharedKeyB[0].to_bytes((sharedKeyB[0].bit_length() + 7) // 8, 'big')).digest()
dec = aes_cbc_decrypt(key,enc)
print(dec)