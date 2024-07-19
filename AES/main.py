from aes import *
aes = Aes(256)
key = b'Ma Super cle de la mort qui tue'
source = r"C:\Users\do\Documents\GitHub\Crypto\AES\DriversCloudx64_12_0_24.msi"
dest =  r"C:\Users\do\Documents\GitHub\Crypto\AES\DriversCloudx64_12_0_24.msi.enc"
dest2 = r"C:\Users\do\Documents\GitHub\Crypto\AES\DriversCloudx64_12_0_24_dec.msi"
#aes.encrypt_file(key,source_file=source, dest_file=dest, enc_mod="cbc", initial_vector=None)
aes.decrypt_file(key,source_file=dest, dest_file=dest2, enc_mod="cbc")


