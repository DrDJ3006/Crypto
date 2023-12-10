from genprimes import generate_primes,is_probably_prime
from datetime import datetime,timedelta
from hashlib import sha256
class _PublicKey:

    def __init__(self, bit_size: int, mod: int, public_exp: int):
        self.bit_size = bit_size
        self.mod = mod
        self.public_exp = public_exp

    def __str__(self) -> str:
        return (f'Public Key:\n\tBit Size: {self.bit_size}\n\tModulus: {hex(self.mod)}\n\t'
                f'Public Exponent: {hex(self.public_exp)}\n')

    def get_object_string(self) -> str:
        return f'{self.bit_size}{self.mod}{self.public_exp}'


class _Issuer_Subject:
    def __init__(self,Country,State,Locality,Organization,OrganizationalUnit,CommonName):
        self.country = Country
        self.state = State
        self.locality = Locality
        self.organization = Organization
        self.organizationalUnit = OrganizationalUnit
        self.commonName = CommonName
    
    def __str__(self) -> str:
        return f'C:{self.country}, S:{self.state}, L:{self.locality}, O:{self.organization}, OU:{self.organizationalUnit}, CN:{self.commonName}'

    def get_object_string(self):
        return f'{self.country}{self.state}{self.locality}{self.organization}{self.organizationalUnit}{self.commonName}'

class _CertReq:
    def __init__(self,Subject : _Issuer_Subject,Pubkey : _PublicKey):  
        self.subject=Subject
        self.pubkey=Pubkey

    def __str__(self) -> str:
        return f'Certificat Request: {str(self.subject)}\n {str(self.pubkey)}'
    
    def get_object_string(self):
        return f'{self.subject.get_object_string()}{self.pubkey.get_object_string()}' 
    
class _Cert:
    def __init__(self,Issuer : _Issuer_Subject, Subject : _Issuer_Subject ,Pubkey : _PublicKey,Ext : str, NotBefore : datetime, NotAfter : datetime):
        self.subject=Subject
        self.issuer=Issuer
        self.pubkey=Pubkey
        self.notBefore=NotBefore  
        self.notAfter=NotAfter
        self.ext=Ext
        self.signature=None

    def genPubkey(self):
        return self.pubkey
    
    def __str__(self) -> str:
        return f'Certificate : \n\tSubject:\n\t\t{str(self.subject)}\n\tIssuer:\n\t\t{str(self.issuer)}\n\tValid Not Before:{self.notBefore}\n\tNot After{self.notAfter}\n\tExt:\n\t\t{self.ext}\n{str(self.pubkey)}\n\tSignature:\n\t\t{self.signature}'
        
    def get_object_string(self):
        return f'{self.subject.get_object_string()}{self.issuer.get_object_string()}{self.pubkey.get_object_string()}{self.notBefore}{self.notBefore}{self.ext}'

class PrivateKey:
    def __init__(self,Bit_size,Prime1,Prime2,Mod,Public_exp,Private_exp) -> None:
        self.bit_size=int(Bit_size)
        self.prime1=int(Prime1)
        self.prime2=int(Prime2)
        self.mod=int(Mod)
        self.public_exp=int(Public_exp)
        self.private_exp=int(Private_exp)
        return

    def __str__(self) -> str:
        return (f'Private Key:\n\tBit Size: {self.bit_size}\n\tPrime 1: {hex(self.prime1)}\n\t'
                f'Prime 2: {hex(self.prime2)}\n\tModulus: {hex(self.mod)}\n\tPublic Exponent: {hex(self.public_exp)}\n\t'
                f'Private Exponent: {hex(self.private_exp)}\n')

    def generate_public_key(self):
        return _PublicKey(self.bit_size, self.mod, self.public_exp)

    def sign(self, data: bytes) -> hex:
        return hex(pow(int.from_bytes(data, 'big'), self.private_exp, self.mod))

    def sign_certificate_request(self, req, ca_cert=None, days=91, ext=None) -> _Cert:
        not_before = datetime.now()
        not_after = not_before + timedelta(days=days)
        if not ca_cert:
            issuer = req.subject
            ext = str(ext)+"/CA:TRUE"
        else:
            issuer = ca_cert.subject
            ext = None
        cert = _Cert(issuer, req.subject, req.pubkey, ext, not_before, not_after)
        cert_signature = sha256(cert.get_object_string().encode()).digest()
        cert.signature = self.sign(cert_signature)
        return cert

def genPrivateKey(byte_length: int, public_exp: int = 65537) -> PrivateKey:
    prime1,prime2,mod=generate_primes(byte_length)
    if  mod < public_exp:
        raise ValueError("Public exponent too large.")
    if not is_probably_prime(public_exp):
        raise ValueError("Public exponent is not prime.")
    phi = (prime1 - 1) * (prime2 - 1)
    private_exp = pow(public_exp, -1, phi)
    return PrivateKey(byte_length,prime1,prime2,mod,public_exp,private_exp)

def GenReqCert(Privkey : PrivateKey, Country : str, State: str,Locality: str,Organization: str,OrganizationalUnit: str,CommonName: str):
    return (_CertReq(_Issuer_Subject(Country,State,Locality,Organization,OrganizationalUnit,CommonName),Privkey.generate_public_key()))