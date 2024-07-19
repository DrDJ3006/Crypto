from aes import *
aes = Aes(256)
f = open(r"C:\Users\do\Downloads\Ankama Launcher-Setup.exe", mode="rb")
data=f.read()
f.close()
key = b'Ma Super cle de la mort qui tue'
ct = aes.decrypt(key,data,enc_mod="ecb")
f = open(r"C:\Users\do\Downloads\Ankama Launcher-Setup.exe", mode="wb")
data=f.write(ct)
f.close()


