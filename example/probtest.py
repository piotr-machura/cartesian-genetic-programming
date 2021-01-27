"""This module will test the average number of generations and mutations
required to achieve fit of 1 depending on the chosen mutation probability.

We will test every probability from 10% to 35% with step 2.5%.
"""
from statistics import stdev, sqrt, mean
from matplotlib import pyplot as plt
from example import *

if __name__ == '__main__':
    avg_gens = list()
    avg_muts = list()
    err_gens = list()
    err_muts = list()
    probabilities = [0.1 + i * 0.025 for i in range(10)]
    for prob in probabilities:
        gens = list()
        muts = list()
        for i in range(10):
            solution = evolve(
                function_table=FUNCTION_TABLE,
                fit_function=fit_modulo_2,
                inputs_num=INPUTS_NUM,
                nodes_num=NODES_NUM,
                outputs_num=OUTPUTS_NUM,
                desired_fit=DESIRED_FIT,
                generations_num=GENERATIONS_NUM,
                mutation_prob=prob,
            )
            gens.append(solution.generation)
            muts.append(solution.total_mutations)
        avg_gens.append(mean(gens))
        avg_muts.append(mean(muts))
        # Standard error is stdev/sqrt(N)
        err_gens.append(stdev(gens) / sqrt(10))
        err_muts.append(stdev(muts) / sqrt(10))

    # Save data to a text file
    with open('./sample_data.txt', mode='w') as f:
        for i, prob in enumerate(probabilities):
            f.write(
                f'{prob} {avg_gens[i]} {err_gens[i]} ' +
                f'{avg_muts[i]} {err_muts[i]}\n')

    # Draw a graph with matplotlib

    _, ax1 = plt.subplots(figsize=(12, 5))
    ax1.set_ylabel('Generations')
    ax1.set_xlabel('Probability')
    plt.errorbar(
        probabilities,
        avg_gens,
        yerr=err_gens,
        xerr=None,
        linestyle=None,
        fmt='o',
        elinewidth=0.5,
        capsize=5,
        color='black',
    )
    plt.show()

    _, ax1 = plt.subplots(figsize=(12, 5))
    ax1.set_ylabel('Mutations')
    ax1.set_xlabel('Probability')
    plt.errorbar(
        probabilities,
        avg_muts,
        yerr=err_muts,
        xerr=None,
        linestyle=None,
        fmt='o',
        elinewidth=0.5,
        capsize=5,
        color='black',
    )
    plt.show()
