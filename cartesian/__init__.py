"""Cartesian genetic programming implementation library.

The main interface is the `evolve` function which returns an instance of
`Specimen` best fit to a given fit function.
"""

from inspect import signature
from specimen import RawSpecimen, Specimen


def evolve(fn_tab, fit_fn, inp, out, **kwargs):
    """Evolve a `Specimen` according to the provided fit function.

    Args:
        fn_tab (tuple) : lookup table of functions to compose specimen from.
        fit_fn (callable) : function evaluating fit from phenotype.
        inp (int) : number of input values taken by a specimen.
        out (int) : number of output values produced by a specimen.
        **kwargs : optional keyword arguments :
            fit (float) : desired fit (default 1).
            gen (int) : number of generations (default 100).
            pop_size (int) : per-generation population size (defalut 100).
            dna_len (int) : number of nodes in a specimens genome (default 100).
            mutation_p (float) : probability of mutation (default 0.01).
    Returns:
        A `Specimen` with desired fit OR the best fit after `gen` generations.
    """

    fit = kwargs.get('fit', 1)
    gen = kwargs.get('gen', 100)
    pop_size = kwargs.get('pop_size', 100)
    dna_len = kwargs.get('dna_len', 100)
    mutation_p = kwargs.get('mutation_p', 0.01)

    # Size of a single node is the maximum amount of args taken by functions
    # from fn_tab + 1 'which function am I' gene
    node_size = max(len(signature(fn).parameters) for fn in fn_tab) + 1

    # Create an initial, random population
    population = [
        RawSpecimen(inp, out, node_size, dna_len, len(fn_tab))
        for _ in range(pop_size)
    ]

    # No parent for now since we are just starting
    parent_fit = 0
    parent = None

    for _ in range(gen):

        # Find a specimen as (or more) fit as the current parent
        for specimen in population:
            sp_phenotype = decode_genotype(specimen, fn_tab)
            sp_fit = fit_fn(sp_phenotype)
            if sp_fit >= parent_fit:
                parent_fit = sp_fit
                parent = specimen
            # If the desired fit has been acheived we can terminate
            if parent_fit >= fit:
                return Specimen(parent, fn_tab)

        # Recreate the population using the new parent
        population = [parent.mutate(mutation_p) for _ in range(pop_size)]

    # Return what we achieved by evolving
    return Specimen(parent, fn_tab)


def decode_genotype(specimen, fn_tab):
    """Decode the genotype into a usable phenotype.

    Args:
        specimen (RawSpecimen) : specmen with a genotype to decode.
        fn_tab (tuple) : function lookup table used to decode a genotype.

    Returns:
        Phenotype of the specimen, ready to be used.
    """
    # TODO: Construct the phenotype
    phenotype = None
    return phenotype
