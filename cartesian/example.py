"""This is a working example of using the library.

Our aim is to evolve an algorithm that will take in an unsigned integer
as a tuple of 3 bits and return its modulo 3 as a tuple of 2 bits. The
algorithm will achieve this by using the basic logic gates:
`BUFFOR`, `AND`, `OR`, `XOR` and `NOT`.
"""
import time
import sys
from evolve import evolve
# pylint: disable=redefined-outer-name,invalid-name,unnecessary-lambda


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


if __name__ == '__main__':
    function_table = (
        lambda x: int(x),    # BUFFOR
        lambda x, y: int(x and y),    # AND
        lambda x, y: int(x or y),    # OR
        lambda x, y: int((x or y) and not (x and y)),    # XOR
        lambda x: int(not x),    # NOT
    )
    print('Starting the process of evolution...')
    t_start = time.time()
    solution = evolve(
        function_table=function_table,
        fit_function=fit_modulo_2,
        inputs_num=3,
        outputs_num=2,
        nodes_num=25,
        mutation_prob=0.05,
        generations_num=10000,
        desired_fit=1,
        max_mutations=None,
    )
    delta_t = time.time() - t_start
    print('---------------------')
    print('Evolution terminated.')
    print(f'Achieved fit of {solution.fit}', end=' ')
    print(f'after {solution.generation} generations', end=' ')
    print(f'in {delta_t:.4} seconds.')
    print('Try it out!')
    while True:
        try:
            inp = int(input('Your number goes here -> '))
            if inp > 7:
                raise ValueError()
        except ValueError:
            print('Only 3-bit integers allowed!')
            continue
        except (KeyboardInterrupt, EOFError):
            print('\n---------------------')
            print('Goodbye!')
            sys.exit()
        # Convert the number to bit array
        inp_bits = [int(digit) for digit in bin(inp)[2:]]
        # Fill the front with 0s to always have 3 bits total
        while len(inp_bits) != 3:
            inp_bits.insert(0, False)
        result = solution.outputs(inp_bits)
        print(f'The algorithm says {inp} modulo 3 is', end=' ')
        print(result, end=' ')
        print('in binary and', end=' ')
        result_int = 0
        for bit in result:
            result_int = (result_int << 1) | bit
        print(f'and {result_int} in decimal.')
