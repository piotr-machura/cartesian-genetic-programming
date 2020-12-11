"""Cartesian genetic programming implementation library.

The main interface is the `evolve` function which returns an instance of
`Specimen` best fit to a given fit function.
"""

from inspect import signature
from specimen import RawSpecimen, Specimen, gen_outputs, mutate


def evolve(fn_tab, fit_fn, inp, out, **kwargs):
    """Evolve a `Specimen` according to the provided fit function.

    Args:
        fn_tab (tuple) : lookup table of functions to compose specimen from.
        fit_fn (callable) : function evaluating fit, **see note below**.
        inp (int) : number of input values taken by a specimen.
        out (int) : number of output values produced by a specimen.
        **kwargs : optional keyword arguments:
            desired_fit (float) : terminate evolution if fit >= (default None).
            gen (int) : number of generations (default 100).
            pop_size (int) : per-generation population size (defalut 100).
            n_of_nodes (int) : number of nodes in the genome (default 100).
            mutation_p (float) : probability of mutation (default 0.01).

    Returns:
        A `Specimen` with desired fit OR the best fit after `gen` generations.

    **Note**: the `fit_fn` should accept a `callable` as it's argument, and
    utilize it like so:
    `
    def example_fit_function(get_outputs: callable): -> float
        inputs = ...
        expected_outputs = ...
        actual_outputs = get_outputs(inputs)
        # Return fit based on how good the outputs are
    `
    The return value of `fit_fn` doesn't have to be `float`, but should be
    comparable and never `None`.
    """
    desired_fit = kwargs.get('desired_fit', None)
    gen = kwargs.get('gen', 100)
    pop_size = kwargs.get('pop_size', 100)
    n_of_nodes = kwargs.get('n_of_nodes', 100)
    mutation_p = kwargs.get('mutation_p', 0.01)

    # Size of a single node is the maximum amount of args taken by functions
    # from fn_tab + a single 'which function am I' gene
    node_size = max(len(signature(fn).parameters) for fn in fn_tab) + 1

    # Create a random population
    population = [
        RawSpecimen(inp, out, node_size, n_of_nodes, len(fn_tab))
        for _ in range(pop_size)
    ]

    # No parent for now since we are just starting
    parent = None
    parent_fit = None

    # Begin the process of evolution
    for _ in range(gen):
        # Find a specimen as (or more) fit as the current parent
        for specimen in population:
            # Provide a callable generating outputs from inputs and feed it to
            # the user's fit function
            sp_fit = fit_fn(lambda inp: gen_outputs(specimen, fn_tab, inp))
            if parent_fit is None or parent_fit <= sp_fit:
                parent_fit = sp_fit
                parent = specimen
            # If the desired fit has been acheived we can terminate
            if desired_fit is not None and parent_fit >= desired_fit:
                return Specimen(parent, fn_tab)
        # Recreate the population by mutating the new parent
        population = [mutate(parent, mutation_p) for _ in range(pop_size)]

    # Return what we achieved by evolving
    return Specimen(parent, fn_tab)
