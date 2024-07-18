def generate_rcon():
    # Initialize the r_con array with the first value set to 0x01 (second value in typical AES implementations)
    r_con = [0x00] * 15  # Allocate space for 15 elements; r_con[0] is not used
    r_con[1] = 0x01  # Start with 1

    # Generate subsequent r_con values
    for i in range(2, 15):
        r_con[i] = r_con[i - 1] << 1
        if r_con[i - 1] & 0x80:  # Check if the left shift would cause a carry out of the byte
            r_con[i] ^= 0x11b  # XOR with the reduction polynomial

    return r_con

# Example of usage
r_con_values = generate_rcon()
print([hex(x) for x in r_con_values])
