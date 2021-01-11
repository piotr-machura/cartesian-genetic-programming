"""Cartesian genetic programming implementation library.

The main interface is the `evolve` function which returns an instance of
`Specimen` best fit to a given fit function.
"""
from inspect import signature, isfunction
from specimen import Specimen


def evolve(function_table, fit_function, inputs_num, outputs_num, **kwargs):
    """Evolve a `Specimen` according to the provided fit function.

    Args:
        function_table (tuple) : lookup table of functions to compose specimen
                                 from.
        fit_function (callable) : function evaluating fit, **see note below**.
        inputs_num (int) : number of input values taken by a specimen.
        outputs (int) : number of output values produced by a specimen.
        **kwargs : optional keyword arguments:
            desired_fit (float) : terminate evolution if fit >= (default None).
            generations_num(int) : number of generations (default 100).
            population_size (int) : per-generation population size (defalut 5).
            nodes_num (int) : number of nodes in the genome (default 100).
            mutation_prob (float) : probability of mutation (default 0.01).
            mutation_num (int) : max number of nodes that can be mutated in a
                                 single generation (default 1).

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
    desired_fit = kwargs.get('desired_fit', None)
    generations_num = kwargs.get('generations_num', 100)
    population_size = kwargs.get('population_size', 5)
    nodes_num = kwargs.get('nodes_num', 100)
    mutation_prob = kwargs.get('mutation_prob', 0.01)
    mutation_num = kwargs.get('mutation_num', 1)

    # Handle incorrect user input
    if inputs_num < 1 or int(inputs_num) != inputs_num:
        raise ValueError('Wrong or non-integer number of inputs.')
    if outputs_num < 1 or int(outputs_num) != outputs_num:
        raise ValueError('Wrong or non-integer number of outputs.')
    if nodes_num < 1 or int(nodes_num) != nodes_num:
        raise ValueError('Wrong number of nodes.')
    if generations_num < 1 or int(generations_num) != generations_num:
        raise ValueError('Wrong or non-integer number of generations.')
    if population_size < 1 or int(population_size) != population_size:
        raise ValueError('Wrong or non-integer population size.')
    if not isfunction(fit_function) or isinstance(fit_function) == type(print):
        raise TypeError(f'Not a valid fit function: {fit_function}.')
    if mutation_prob > 1 or mutation_prob < 0:
        raise ValueError('Probability of mutation must be (0, 1).')
    for function in function_table:
        if not isfunction(function) or isinstance(function) == type(print):
            raise TypeError(f'Not a valid function: {function}.')

    # Create a random population
    population = [
        Specimen(
            inputs_num,
            outputs_num,
            nodes_num,
            function_table,
            mutation_prob,
            mutation_num,
        ) for _ in range(population_size)
    ]

    # No parent for now since we are just starting
    parent = None
    parent_fit = None

    # Begin the process of evolution
    for _ in range(generations_num):
        # Find a specimen as (or more) fit as the current parent
        for specimen in population:
            # Provide a callable generating outputs from inputs and feed it to
            # the user's fit function
            sp_fit = fit_function(specimen.outputs)
            if parent_fit is None or parent_fit <= sp_fit:
                parent_fit = sp_fit
                parent = specimen
            # If the desired fit has been acheived we can terminate
            if desired_fit is not None and parent_fit >= desired_fit:
                return parent
        # Recreate the population by mutating the new parent
        population = [
            parent.mutate(mutation_prob) for _ in range(population_size)
        ]

    # Return the best we achieved by evolving
    return parent
