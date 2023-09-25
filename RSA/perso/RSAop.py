from Crypto.Util.number import *
from hashlib import sha256
import datetime
import sys
import json
import os


def encrypt(keyfile,filein,fileout):
    with open(keyfile, "r") as infile:
            pubkey=json.load(infile)
    try :    
        modulus=int(pubkey["Modulus"],16)
        exp=int(pubkey["PublicExp"],16)
    except KeyError:
        modulus=int(int(pubkey["Certificate"]["PublicKey"]["Modulus"],16))
        exp=int(int(pubkey["Certificate"]["PublicKey"]["PublicExp"],16))
    if os.path.getsize(filein)*8 > int(modulus).bit_length():
            exit(f"[!] Data too big {os.path.getsize(filein)*8} > {int(modulus).bit_length()} bits")
    with open(filein, "rb") as binary_file:
        binary_data = binary_file.read()
    encryptedData=long_to_bytes(pow(bytes_to_long(binary_data),exp,modulus))
    with open(fileout, "wb") as binary_file:
        binary_file.write(encryptedData)

def decrypt(keyfile,filein,fileout):
    with open(keyfile, "r") as infile:
            privatekey=json.load(infile)
    try :    
        modulus=int(privatekey["Modulus"],16)
        exp=int(privatekey["PrivateExp"],16)
    except KeyError:
        exit("privkeyerror")
    with open(filein, "rb") as binary_file:
        binary_data = binary_file.read()
    decryptedData=long_to_bytes(pow(bytes_to_long(binary_data),exp,modulus))
    with open(fileout, "wb") as binary_file:
        binary_file.write(decryptedData)

def verify_cert(cacertfile,certfile):
    with open(cacertfile, "r") as infile:
            cacert=json.load(infile)
    with open(certfile, "r") as infile:
            cert=json.load(infile)
    hashed_certificate = bytes_to_long(sha256(json.dumps(cert["Certificate"], sort_keys=True).encode("utf-8")).digest())

    modulus=int(cacert['Certificate']['PublicKey']['Modulus'],16)
    exp=int(cacert['Certificate']['PublicKey']['PublicExp'],16)
    signature=int(cert['Signature']['SignatureValue'],16)
    signature_decrypt=pow(signature,exp,modulus)
    is_signed=True
    current_datetime = datetime.datetime.now()

    if(hashed_certificate!=signature_decrypt):
        is_signed=False
        print("Invalid Signature !")
    if(cacert['Certificate']['Extension']['CA']!=True):
        is_signed=False
    if(cert['Certificate']['Issuer']['C']!=cacert['Certificate']['Subject']['C']):
        is_signed=False
    if(cert['Certificate']['Issuer']['ST']!=cacert['Certificate']['Subject']['ST']):
        is_signed=False
    if(cert['Certificate']['Issuer']['O']!=cacert['Certificate']['Subject']['O']):
        is_signed=False
    if(cert['Certificate']['Issuer']['CN']!=cacert['Certificate']['Subject']['CN']):
        is_signed=False
    if(datetime.datetime.strptime(cert['Certificate']['Validity']['NotBefore'], "%Y-%m-%d %H:%M:%S")>current_datetime):
         print("Unvalid Date")
    if(datetime.datetime.strptime(cert['Certificate']['Validity']['NotAfter'], "%Y-%m-%d %H:%M:%S")<current_datetime):
         print("Unvalid Date")
    if(is_signed):
        print("Signature OK")
        return True
    else :
        print("Signature ERROR")
        return False
try:
    if sys.argv[1]=="-encrypt":
        encrypt(sys.argv[2],sys.argv[3],sys.argv[4])
    if sys.argv[1]=="-decrypt":
        decrypt(sys.argv[2],sys.argv[3],sys.argv[4])
    if sys.argv[1]=="-verify":
        if sys.argv[2]=="-cert":
            verify_cert(sys.argv[3],sys.argv[4])
         

except IndexError:
    exit("Args Error")
except FileNotFoundError as e:
    print(f"'{e}'")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")