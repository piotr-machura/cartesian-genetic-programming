"""This module contains the `evolve` function used to obtain an instance
of `Specimen` fit to the given fit function.
"""

from threading import Thread
from specimen import Specimen
from inspect import isfunction


def evolve(
    function_table,
    fit_function,
    inputs_num,
    nodes_num,
    outputs_num,
    desired_fit=None,
    generations_num=100,
    population_size=5,
    mutation_prob=0.01,
    max_mutations=None,
):
    """Evolve a `Specimen` according to the provided fit function.

    Args:
        function_table (tuple) : lookup table of functions to compose specimen
                                 from.
        fit_function (callable) : function evaluating fit, **see note below**.
        inputs_num (int) : number of input values taken by a specimen.
        nodes_num (int) : number of nodes in the genome.
        outputs_num (int) : number of output values produced by a specimen.
        desired_fit (float) : terminate evolution if fit >= (default None).
        generations_num(int) : number of generations (default 100).
        population_size (int) : per-generation population size (defalut 5).
        mutation_prob (float) : probability of mutation (default 0.01).
        max_mutations (int) : maximum number of genes that can be mutated in
                              a single application of the mutation operator
                              (default None).

    Returns:
        A `Specimen` with desired fit OR the best fit after `gen` generations.

    **Note**: the `fit_function` should accept a `callable` as it's argument,
    and utilize it like so:
    `
    def example_fit_function(get_outputs: callable): -> float
        inputs = ...
        expected_outputs = ...
        actual_outputs = get_outputs(inputs)
        # Return fit based on how good the outputs are
    `
    The return value of `fit_function` doesn't have to be `float`, but should be
    comparable and never `None`.
    """

    # Handle incorrect input
    if generations_num < 1 or int(generations_num) != generations_num:
        raise ValueError('Wrong or non-integer number of generations.')
    if population_size < 1 or int(population_size) != population_size:
        raise ValueError('Wrong or non-integer population size.')
    if not isfunction(fit_function) or isinstance(fit_function, type(print)):
        raise TypeError(f'Not a valid fit function: {fit_function}.')

    # Create a random population
    population = [
        Specimen(
            inputs_num,
            outputs_num,
            nodes_num,
            function_table,
            mutation_prob,
            max_mutations,
        ) for _ in range(population_size)
    ]

    # No parent for now since we are just starting
    parent = None

    # Begin the process of evolution
    for _ in range(generations_num):
        # Set up threads to assign fit in paralell
        threads = [
            Thread(target=specimen.assign_fit, args=(fit_function, ))
            for specimen in population
        ]
        for thread in threads:
            thread.start()
        # Wait for all threads to complete before proceeding
        for thread in threads:
            thread.join()
        # Find the specimen with fit >= parent fit
        for specimen in population:
            if parent is None or parent.fit <= specimen.fit:
                parent = specimen

            # If the desired fit has been acheived we can terminate
            if desired_fit is not None and parent.fit >= desired_fit:
                return parent
        # Recreate the population by mutating the new parent
        population = []
        threads = [
            Thread(
                target=lambda l: l.append(parent.mutate()),
                args=(population, )) for _ in range(population_size)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    # Return the best we achieved by evolving
    return parent
