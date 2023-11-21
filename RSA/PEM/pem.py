privkey_file=r'C:\Users\Do\Documents\Crypto\RSA\PEM\private.pem'
with open(privkey_file, 'rb') as source:
   privkey=source.read()

privkey=privkey.replace(b'-----BEGIN PRIVATE KEY-----\r\n',b'')
privkey=privkey.replace(b'\r\n-----END PRIVATE KEY-----\r\n',b'')
privkey=privkey.replace(b'\r\n',b'')
print(privkey)
