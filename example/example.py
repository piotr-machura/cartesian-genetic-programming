"""This is a working example of using the library.

Our aim is to evolve an algorithm that will take in an unsigned integer
as a tuple of 3 bits and return its modulo 3 as a tuple of 2 bits. The
algorithm will achieve this by using the basic logic gates:
`BUFFOR`, `AND`, `OR`, `XOR` and `NOT`.
"""
# pylint: disable=redefined-outer-name,invalid-name,unnecessary-lambda
import sys
sys.path.append('../cartesian')    # Relative import without parent package
from evolve import evolve


def fit_modulo_2(gen_outputs):
    """Establish how bad the algorithm is at finding modulo 3 from a
    tuple of 4 bits."""
    bad = 1
    for integer in range(8):
        # Convert the number to bit array
        input_bits = [int(digit) for digit in bin(integer)[2:]]
        expected_bits = [int(digit) for digit in bin(integer % 3)[2:]]
        # Fill the front with 0s
        while len(input_bits) != 3:
            input_bits.insert(0, 0)
        while len(expected_bits) != 2:
            expected_bits.insert(0, 0)
        # Get the outputs from output-generating function
        returned_bits = gen_outputs(input_bits)
        # Compare the expected bit to returned bits
        for index, bit in enumerate(returned_bits):
            if bit != expected_bits[index]:
                bad += 1
    return 1 / bad


FUNCTION_TABLE = (
    lambda x: x,    # BUFFOR
    lambda x, y: x & y,    # AND
    lambda x, y: x | y,    # OR
    lambda x, y: x ^ y,    # XOR
    lambda x: ~x,    # NOT
)

INPUTS_NUM = 3
NODES_NUM = 100
OUTPUTS_NUM = 2
DESIRED_FIT = 1
GENERATIONS_NUM = 100000
