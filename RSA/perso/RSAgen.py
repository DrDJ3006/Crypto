from Crypto.Util.number import *
from hashlib import sha256
import json
import sys
import random
import sys
import datetime
def is_probably_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if num % 2 == 0:
            num += 1
        if is_probably_prime(num):
            return num

def generate_primes(numbits):
    prime1 = generate_prime(int(numbits/2))
    prime2 = generate_prime(int(numbits/2))
    product=prime1*prime2
    while int(product).bit_length() != numbits:
        prime1 = generate_prime(int(numbits/2))
        prime2 = generate_prime(int(numbits/2))
        product=prime1*prime2
    return(prime1,prime2)

def generate_privatekey(numbits,outfile):
    privkey = {}
    p,q=generate_primes(int(numbits))
    n=p*q
    phi=(q-1)*(p-1)
    e=65537
    d=pow(e,-1,phi)
    privkey["Modulus"]=hex(n)
    privkey["PublicExp"]=hex(e)
    privkey["PrivateExp"]=hex(d)
    privkey["Prime1"]=hex(p)
    privkey["Prime2"]=hex(q)
    with open(sys.argv[3], "w") as outfile:
        json.dump(privkey, outfile, indent=4)


def extract_publickey(privkey,certfile):
     with open(privkey, "r") as infile:
            key=json.load(infile)
            pubkey={}
            try :
                pubkey["Modulus"]=key["Modulus"]
                pubkey["PublicExp"]=key["PublicExp"]
            except Exception as e:
                pubkey["Modulus"]=key["Certificate"]["PublicKey"]["Modulus"]
                pubkey["PublicExp"]=key["Certificate"]["PublicKey"]["PublicExp"]
            with open(certfile, "w") as outfile:
                json.dump(pubkey, outfile, indent=4)

def generate_cert(privkey,outfile):
    with open(privkey, "r") as infile:
            privkey=json.load(infile)
    current_datetime = datetime.datetime.now()
    
    validity_days=input("Validity(days)[90]:")
    if validity_days == '':
        time_to_add = datetime.timedelta(days=90)
    else:
        time_to_add = datetime.timedelta(days=int(validity_days))
    NotAfter = current_datetime + time_to_add
    cert={}
    cert["Certificate"]={}
    cert["Certificate"]["SerialNumber"]=hex(1)
    cert["Certificate"]["Subject"]={}
    cert["Certificate"]["Validity"]={}
    cert["Certificate"]["Validity"]["NotBefore"]=current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    cert["Certificate"]["Validity"]["NotAfter"]=NotAfter.strftime("%Y-%m-%d %H:%M:%S")
    cert["Certificate"]["Issuer"]={}
    cert["Certificate"]["Issuer"]["C"]=cert["Certificate"]["Subject"]["C"]=input("Country[TV]:")
    if cert["Certificate"]["Subject"]["C"] == '':
        cert["Certificate"]["Issuer"]["C"]=cert["Certificate"]["Subject"]["C"]="TV" 
    cert["Certificate"]["Issuer"]["ST"]=cert["Certificate"]["Subject"]["ST"]=input("State[Neverland]:")
    if cert["Certificate"]["Subject"]["ST"] == '':
        cert["Certificate"]["Issuer"]["ST"]=cert["Certificate"]["Subject"]["ST"]="Neverland"
    cert["Certificate"]["Issuer"]["O"]=cert["Certificate"]["Subject"]["O"]=input("Organization[EvilCorp]:")
    if cert["Certificate"]["Subject"]["O"] == '':
        cert["Certificate"]["Issuer"]["O"]=cert["Certificate"]["Subject"]["O"]="EvilCorp"
    cert["Certificate"]["Issuer"]["CN"]=cert["Certificate"]["Subject"]["CN"]=input("Common Name[Certificate]:")
    if cert["Certificate"]["Subject"]["CN"] == '':
        cert["Certificate"]["Issuer"]["CN"]=cert["Certificate"]["Subject"]["CN"]="Certificate"
    cert["Certificate"]["Extension"]={}
    cert["Certificate"]["Extension"]["CA"]=True
    cert["Certificate"]["PublicKey"]={}
    cert["Certificate"]["PublicKey"]["Algorithm"]="rsaEncryption"
    cert["Certificate"]["PublicKey"]["Size"]=str(int(privkey["Modulus"],16).bit_length())+" bits"
    cert["Certificate"]["PublicKey"]["Modulus"]=privkey["Modulus"]
    cert["Certificate"]["PublicKey"]["PublicExp"]=privkey["PublicExp"]
    hashed_certificate = bytes_to_long(sha256(json.dumps(cert["Certificate"], sort_keys=True).encode("utf-8")).digest())
    if(int(privkey["Modulus"],16).bit_length()<int(hashed_certificate).bit_length()):
        exit("Error Mod too short for sign !")
        return False
    cert["Signature"]={}
    cert["Signature"]["SignatureAlgorithm"]="SHA256"
    cert["Signature"]["SignatureValue"]=hex(pow(hashed_certificate,int(privkey["PrivateExp"],16),int(privkey["Modulus"],16)))
    with open(outfile, "w") as outfile:
                json.dump(cert, outfile, indent=4)

def generate_req(privkey,outfile):
    with open(privkey, "r") as infile:
            privkey=json.load(infile)
    req={}
    req["CertificateRequest"]={}
    req["CertificateRequest"]["Subject"]={}
    req["CertificateRequest"]["Subject"]["C"]=input("Country[TV]:")
    if req["CertificateRequest"]["Subject"]["C"] == '':
        req["CertificateRequest"]["Subject"]["C"]="TV" 

    req["CertificateRequest"]["Subject"]["ST"]=input("State[Neverland]:")
    if req["CertificateRequest"]["Subject"]["ST"] == '':
        req["CertificateRequest"]["Subject"]["ST"]="Neverland"

    req["CertificateRequest"]["Subject"]["O"]=input("Organization[EvilCorp]:")
    if req["CertificateRequest"]["Subject"]["O"] == '':
        req["CertificateRequest"]["Subject"]["O"]="EvilCorp"

    req["CertificateRequest"]["Subject"]["CN"]=input("Common Name[Certificate]:")
    if req["CertificateRequest"]["Subject"]["CN"] == '':
        req["CertificateRequest"]["Subject"]["CN"]="Certificate"
    req["CertificateRequest"]["PublicKey"]={}    
    req["CertificateRequest"]["PublicKey"]["Algorithm"]="rsaEncryption"
    req["CertificateRequest"]["PublicKey"]["Size"]=str(int(privkey["Modulus"],16).bit_length())+" bits"
    req["CertificateRequest"]["PublicKey"]["Modulus"]=privkey["Modulus"]
    req["CertificateRequest"]["PublicKey"]["PublicExp"]=privkey["PublicExp"]

    hashed_certificate = bytes_to_long(sha256(json.dumps(req["CertificateRequest"], sort_keys=True).encode("utf-8")).digest())
    if(int(privkey["Modulus"],16).bit_length()<int(hashed_certificate).bit_length()):
        exit("Error Mod too short for sign !")
    req["Signature"]={}
    req["Signature"]["SignatureAlgorithm"]="SHA256"
    req["Signature"]["SignatureValue"]=hex(pow(hashed_certificate,int(privkey["PrivateExp"],16),int(privkey["Modulus"],16)))

    with open(outfile, "w") as outfile:
                json.dump(req, outfile, indent=4)

def sign_cert(cakeyfile,cacertfile,reqfile,outfile):
    with open(cakeyfile, "r") as infile:
            cakey=json.load(infile)
    with open(cacertfile, "r") as infile:
            cacert=json.load(infile)
    with open(reqfile, "r") as infile:
            req=json.load(infile)
    cert={}
    cert["Certificate"]={}
    cert["Certificate"]["SerialNumber"]=input("SerialNumber[1]:")
    cert["Certificate"]["Subject"]={}
    if cert["Certificate"]["SerialNumber"]== '':
        cert["Certificate"]["SerialNumber"]=hex(1)
    else :
        cert["Certificate"]["SerialNumber"] = hex(int(cert["Certificate"]["SerialNumber"]))
    cert["Certificate"]["Subject"]["C"]=req["CertificateRequest"]["Subject"]["C"]
    cert["Certificate"]["Subject"]["ST"]=req["CertificateRequest"]["Subject"]["ST"]
    cert["Certificate"]["Subject"]["O"]=req["CertificateRequest"]["Subject"]["O"]
    cert["Certificate"]["Subject"]["CN"]=req["CertificateRequest"]["Subject"]["CN"]
    current_datetime = datetime.datetime.now()
    validity_days=input("Validity(days)[90]:")
    if validity_days == '':
        time_to_add = datetime.timedelta(days=90)
    else:
        time_to_add = datetime.timedelta(days=int(validity_days))
    NotAfter = current_datetime + time_to_add
    cert["Certificate"]["Validity"]={}
    cert["Certificate"]["Validity"]["NotBefore"]=current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    cert["Certificate"]["Validity"]["NotAfter"]=NotAfter.strftime("%Y-%m-%d %H:%M:%S")
    cert["Certificate"]["Issuer"]={}
    cert["Certificate"]["Issuer"]["C"]=cacert["Certificate"]["Subject"]["C"]
    cert["Certificate"]["Issuer"]["ST"]=cacert["Certificate"]["Subject"]["ST"]
    cert["Certificate"]["Issuer"]["O"]=cacert["Certificate"]["Subject"]["O"]
    cert["Certificate"]["Issuer"]["CN"]=cacert["Certificate"]["Subject"]["CN"]
    isCA=input("CA (y/n)[n]:")
    if isCA=="y":
        cert["Certificate"]["Extension"]={}
        cert["Certificate"]["Extension"]["CA"]=True
    cert["Certificate"]["PublicKey"]={}
    cert["Certificate"]["PublicKey"]["Algorithm"]=req['CertificateRequest']['PublicKey']['Algorithm']
    cert["Certificate"]["PublicKey"]["Size"]=str(int(req['CertificateRequest']['PublicKey']['Modulus'],16).bit_length())+" bits"
    cert["Certificate"]["PublicKey"]["Modulus"]=req['CertificateRequest']['PublicKey']['Modulus']
    cert["Certificate"]["PublicKey"]["PublicExp"]=req['CertificateRequest']['PublicKey']['PublicExp']
    hashed_certificate = bytes_to_long(sha256(json.dumps(cert["Certificate"], sort_keys=True).encode("utf-8")).digest())
    if(int(cakey["Modulus"],16).bit_length()<int(hashed_certificate).bit_length()):
        exit("Error Mod too short for sign !")
        return False
    cert["Signature"]={}
    cert["Signature"]["SignatureAlgorithm"]="SHA256"
    cert["Signature"]["SignatureValue"]=hex(pow(hashed_certificate,int(cakey["PrivateExp"],16),int(cakey["Modulus"],16)))
    with open(outfile, "w") as outfile:
        json.dump(cert, outfile, indent=4)

try:
    if sys.argv[1] == '-genrsa':
        generate_privatekey(sys.argv[2],sys.argv[3])
    if sys.argv[1] == '-pubout':
       extract_publickey(sys.argv[2],sys.argv[3])
    if sys.argv[1] == '-cert':
       generate_cert(sys.argv[2],sys.argv[3])
    if sys.argv[1] == '-req':
       generate_req(sys.argv[2],sys.argv[3])
    if sys.argv[1] == '-sign':
       sign_cert(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])

except IndexError:
    exit("Args Error")
except FileNotFoundError:
    print(f"File not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")