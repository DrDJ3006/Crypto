# importing the module
import base64
 
# assigning our sample to a variable
convertsample = "MBwCAQACAgCPAgEHAgFnAgELAgENAgEDAgEHAgEG="
# converting the base64 code into ascii characters
convertbytes = convertsample.encode("utf-8")
# converting into bytes from base64 system
convertedbytes = base64.b64decode(convertbytes)
# decoding the ASCII characters into alphabets
decodedsample = convertedbytes.decode("utf-8")
# displaying the result
print(f"The string after decoding is: {decodedsample}")