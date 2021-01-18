"""Cartesian genetic programming implementation library.

The main interface is the `evolve` function which returns an instance of
`Specimen` best fit to a given fit function.
"""
from inspect import signature, isfunction
from threading import Thread
from specimen import Specimen


def evolve(
    function_table,
    fit_function,
    inputs_num,
    outputs_num,
    desired_fit=None,
    generations_num=100,
    population_size=5,
    nodes_num=100,
    mutation_prob=0.01,
    max_mutations=10,
):
    """Evolve a `Specimen` according to the provided fit function.

    Args:
        function_table (tuple) : lookup table of functions to compose specimen
                                 from.
        fit_function (callable) : function evaluating fit, **see note below**.
        inputs_num (int) : number of input values taken by a specimen.
        outputs_num (int) : number of output values produced by a specimen.
        desired_fit (float) : terminate evolution if fit >= (default None).
        generations_num(int) : number of generations (default 100).
        population_size (int) : per-generation population size (defalut 5).
        nodes_num (int) : number of nodes in the genome (default 100).
        mutation_prob (float) : probability of mutation (default 0.01).
        max_mutations (int) : number of genes that can be mutated in a single
                              application of the mutation operator (default 10).
                              Set to None to remove the limit.

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

    # Handle incorrect user input
    if inputs_num < 1 or int(inputs_num) != inputs_num:
        raise ValueError('Wrong or non-integer number of inputs.')
    if outputs_num < 1 or int(outputs_num) != outputs_num:
        raise ValueError('Wrong or non-integer number of outputs.')
    if nodes_num < 1 or int(nodes_num) != nodes_num:
        raise ValueError('Wrong nor non-integer umber of nodes.')
    if generations_num < 1 or int(generations_num) != generations_num:
        raise ValueError('Wrong or non-integer number of generations.')
    if population_size < 1 or int(population_size) != population_size:
        raise ValueError('Wrong or non-integer population size.')
    if not isfunction(fit_function) or isinstance(fit_function, type(print)):
        raise TypeError(f'Not a valid fit function: {fit_function}.')
    if mutation_prob > 1 or mutation_prob < 0:
        raise ValueError('Probability must be between 0 and 1.')
    if max_mutations is not None or max_mutations < 1 or int(
            max_mutations) != max_mutations:
        raise ValueError('Wrong or non-integer number of max mutations.')
    for function in function_table:
        if not isfunction(function) or isinstance(function, type(print)):
            msg = 'Your function table is invalid '
            msg += f'(not a valid function: {function}.'
            raise TypeError(msg)

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
        population = [
            parent.mutate(mutation_prob) for _ in range(population_size)
        ]

    # Return the best we achieved by evolving
    return parent
