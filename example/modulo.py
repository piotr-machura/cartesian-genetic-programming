"""This is a working example of using the library.

Our aim is to evolve an algorithm that will take in an unsigned integer
as a tuple of 8 bits and return its modulo 7 as a tuple of 3 bits. The
algorithm will achieve this by using the basic logic gates:
`BUFFOR`, `AND`, `OR`, `XOR`, `NOT`, `NAND`, `NOR`, `XNOR`.
"""
# from cartesian import evolve

function_table = (
    lambda x: x,    # BUFFOR
    lambda x, y: x and y,    # AND
    lambda x, y: x or y,    # OR
    lambda x, y: (x or y) and not (x and y),    # XOR
    lambda x: not x,    # NOT
    lambda x, y: not (x and y),    # NAND
    lambda x, y: not (x or y),    # NOR
    lambda x, y: not ((x or y) and not (x and y)),    #XNOR
)

def fit_modulo_7(gen_outputs):
    bad = 1
    for integer in range(255):
        # Convert the number to bit array
        input_bits = [int(digit) for digit in bin(integer)[2:]]
        # Fill the front with 0s to always have 8 bits total
        while len(input_bits) != 8:
            input_bits.insert(0, 0)
        # Get the outputs from output-generating function
        returned_bits = gen_outputs(input_bits)
        # Convert returned bit array to int
        returned_int = 0
        for bit in returned_bits:
            returned_int = (returned_int << 1) | bit
        # Determine how bad the returned value is
        bad += ((integer % 7) - returned_int) ** 2
    return 1/bad
