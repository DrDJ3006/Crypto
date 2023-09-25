def add_round_key(s, k):
    matrix=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(0,len(s)):
        for j in range(0,len(s[i])):
            matrix[i][j]=s[i][j]^k[i][j]
    return matrix

def bytes2matrix(text):
    """Converts a 16-byte array into a 4x4 matrix."""
    matrix = []  # Initialize an empty matrix to store the result
    for i in range(0, 16, 4):
        # Take each set of 4 bytes from the input text and create a row in the matrix
        row = list(text[i:i+4])
        matrix.append(row)  # Add the row to the matrix
    return matrix  # Return the 4x4 matrix

text=b"AZERTYUIIOPQSDFG"
key=b"AZERTYUIIOPQSDFG"
key_matrix=bytes2matrix(key)
text_matrix=bytes2matrix(text)
print(add_round_key(text_matrix, key_matrix))