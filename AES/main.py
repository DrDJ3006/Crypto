from AES import *
aes = Aes(128)
data=b"Azerty123*"
ikm = b'Ma Super cle de la mort qui tue'
derived_key = hkdf(ikm,aes.key_bytes_size )
ct = aes.encrypt(derived_key,add_pkcs7_padding(data))
t = aes.decrypt(derived_key,ct)
print(ct)
print(t)


