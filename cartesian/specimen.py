"""Specimen module.

This module contains the class `Specimen` returned to the user after the
evolution concludes as well as the `RawSpecimen` used for the internal
evolutionary algorithm.
"""

from copy import deepcopy as copy
from random import randint, random


class RawSpecimen():
    """The class `RawSpecimen` used during the evolutionary process.

    Unlike the `Specimen` it does not contain a function lookup table (in order
    to save some memory) and therefore cannot be used 'as is'. It exists for
    implementation purpouses only.

    Attributes:
        genotype (list) : array of integers used to construct the phenotype.
        node_len (int) : length of a single node in the genome.
        inp (int) : number of input values taken by a specimen.
        out (int) : number of output values produced by a specimen.
    """
    def __init__(self, inp, out, node_size, dna_len, fn_tab_size):
        """Create a `Raw Specimen` with random genotype.

        Args:
            inp (int) : number of input values taken by a specimen.
            out (int) : number of output values produced by a specimen.
            node_size (int) : size of a single node.
            dna_len (int) : desired number of nodes.
            fn_tab_size (int) : size of function lookup table.
        """

        self.inp = inp
        self.out = out
        self.fns = fn_tab_size
        self.node_size = node_size
        self.genotype = list()
        if dna_len is None:
            # This means we want an 'empty' genotype
            return
        # TODO: Build a random genotype with randint

    def mutate(self, mutation_p):
        """Mutate into an offspring instance of `RawSpecimen`.

        Args:
            mutation_p (float) : probability of mutating a given gene.

        Returns:
            Offspring, a correctly mutated instance of `RawSpecimen`.
        """
        offspring = copy(self)
        for gene in offspring.genotype:
            if random() <= mutation_p:
                # Mutate
                pass
        return offspring


class Specimen(RawSpecimen):
    """The class `Specimen` produced by the evolutionary algorithm.

    It is capable of being used on its own and calculate the outcome of
    the phenotype given any input.

    Attributes:
        fn_tab (tuple) : function lookup table used to decode a genotype.
        genotype (list) : array of integers used to construct the phenotype.
        node_size (int) : length of a single node in the genome.
        inp : number of input values taken by a specimen.
        out : number of output values produced by a specimen.
    """
    def __init__(self, raw, fn_tab):
        """Create an instance of usable `Specimen` from a raw one.

        Args:
            raw (RawSpecimen) : specimen to convert.
            fn_tab (tuple) : function lookup table used to decode a genotype.
        """
        super().__init__(
            raw.inp,
            raw.out,
            raw.node_size,
            None,    # Since we want an empty genotype
            raw.fns)
        self.genotype = raw.geontype
        self.fn_tab_size = len(fn_tab)
        self.fn_tab = fn_tab
