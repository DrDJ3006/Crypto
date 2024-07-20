from rsa import *
import json

privkey1 = genPrivateKey(512)
pubkey=privkey1.generate_public_key()
req=GenReqCert(privkey1,'FR','Bretagne','Vannes','MOI','Moi','Autorite')

cert1=privkey1.sign_certificate_request(req)
privkey2 = genPrivateKey(512)
req=GenReqCert(privkey2,'FR','Bretagne','Vannes','MOI','Moi','Test client')
cert2=privkey1.sign_certificate_request(req,cert1)
print(cert2)
print(privkey2)