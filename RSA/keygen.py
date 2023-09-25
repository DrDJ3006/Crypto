from Cryptodome.Util.number import *
cli1=dict()
cli1["p"]=3992376397
cli1["q"]=4167607217
cli1["n"]=cli1["p"]*cli1["q"]
cli1["e"]=65537
cli1["d"]=pow(cli1["e"],-1,(cli1["p"]-1)*(cli1["q"]-1))

cli2=dict()
cli2["p"]=4034474069
cli2["q"]=3297996959
cli2["n"]=cli2["p"]*cli2["q"]
cli2["e"]=65537
cli2["d"]=pow(cli2["e"],-1,(cli2["p"]-1)*(cli2["q"]-1))

text=b"bon"
long_text=bytes_to_long(text)
common_n=cli2["n"]*cli1["n"]
signedText1=pow(long_text,cli1["d"],common_n)
print(signedText1)
signedText2=pow(long_text,cli2["d"],common_n)
print(signedText2)