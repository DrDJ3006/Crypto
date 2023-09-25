def bytes2matrix(text):
    """Converts a 16-byte array into a 4x4 matrix."""
    matrix = []  # Initialize an empty matrix to store the result
    for i in range(0, 16, 4):
        # Take each set of 4 bytes from the input text and create a row in the matrix
        row = list(text[i:i+4])
        matrix.append(row)  # Add the row to the matrix
    return matrix  # Return the 4x4 matrix


text=b'Azerty1235689'

def matrix2bytes(matrix):
    """Converts a 4x4 matrix into a 16-byte array."""
    text = b""  # Initialize an empty bytes array to store the result
    for row in matrix:
        # Convert each row in the matrix to bytes and append to the result
        text += bytes(row)
    return text  # Return the 16-byte array




matrix = [
    [99, 114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97, 116],
    [114, 105, 120, 125],
]

print(matrix2bytes([[99, 114, 121, 112], [116, 111, 123, 108], [49, 110, 51, 52], [114, 108, 121, 125]]))
