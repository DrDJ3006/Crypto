from AES import Aes
aes = Aes()
matrix = aes.bytes2matrix(b"1234567891234567")
key = aes.bytes2matrix(b'9876543219876543')
ct = aes.mix_columns(matrix)
pt = aes.inv_mix_columns(ct)
text = aes.matrix2bytes(pt)
print(text)
