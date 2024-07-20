from aes import *
aes = Aes(128)
key = b'Ma Super cle de la mort qui tue'
source = r"C:\Users\do\Downloads\Ankama Launcher-Setup.exe"
dest =  r"C:\Users\do\Downloads\Ankama Launcher-Setup.exe.enc"
dest2 = r"C:\Users\do\Downloads\Ankama Launcher-Setupd_ec.exe"
#aes.encrypt_file(key,source_file=source, dest_file=dest, enc_mod="cbc")
aes.decrypt_file(key,source_file=dest, dest_file=dest2, enc_mod="cbc")


