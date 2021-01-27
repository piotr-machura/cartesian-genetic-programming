"""This is an interactive demo of the modulo 3 example."""
import time
from example import *

if __name__ == '__main__':
    print('Starting the process of evolution...')
    t_start = time.time()
    solution = evolve(
        function_table=FUNCTION_TABLE,
        fit_function=fit_modulo_2,
        inputs_num=INPUTS_NUM,
        nodes_num=NODES_NUM,
        outputs_num=OUTPUTS_NUM,
        desired_fit=DESIRED_FIT,
        generations_num=GENERATIONS_NUM,
        mutation_prob=0.1,
    )
    delta_t = time.time() - t_start
    print('---------------------')
    print(f'Evolution terminated (took {delta_t:.4} seconds).')
    print(
        f'Achieved fit of {solution.fit} ' +
        f'after {solution.generation} generations ' +
        f'and a total of {solution.total_mutations} mutations.',
    )
    print('Try it out!')
    while True:
        try:
            inp = int(input('Your 3-bit number -> '))
            if not 0 <= inp <= 7:
                raise ValueError()
        except ValueError:
            print('Only 3-bit unsigned integers allowed!')
            continue
        except (KeyboardInterrupt, EOFError):
            print('\n---------------------')
            print('Goodbye!')
            sys.exit()
        # Convert the number to bit list
        inp_bits = [int(digit) for digit in bin(inp)[2:]]
        # Fill the front with 0s to always have 3 bits total
        while len(inp_bits) != 3:
            inp_bits.insert(0, False)
        result = solution.outputs(inp_bits)
        print(f'It seems {inp} modulo 3 is', end=' ')
        print(result, end=' ')
        print('in binary and', end=' ')
        # Bitshift magic to turn bit tuple into int
        result_int = 0
        for bit in result:
            result_int = (result_int << 1) | bit
        print(f'and {result_int} in decimal.')
