state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]


def add_round_key(s, k):
    text=''
    for i in range(0,len(s)):
        for j in range(0,len(s[i])):
            text=text+chr(s[i][j]^k[i][j])
    return text

def bytes2matrix(text):
    """Converts a 16-byte array into a 4x4 matrix."""
    matrix = []  # Initialize an empty matrix to store the result
    textLong=[]
    for letter in text:
        textLong.append(ord(letter))
    for i in range(0, 16, 4):
        # Take each set of 4 bytes from the input text and create a row in the matrix
        row = list(textLong[i:i+4])
        matrix.append(row)  # Add the row to the matrix
    return matrix  # Return the 4x4 matrix


def add_round_text(t, k):
    textLong=bytes2matrix(t)
    for i in range(0,len(textLong)):
        for j in range(0,len(textLong[i])):
            print(f'{textLong[i][j]^k[i][j]}')
    pass

text='crypto{r0undk3y}'

add_round_text(text, round_key)
#print(add_round_key(state, round_key))

