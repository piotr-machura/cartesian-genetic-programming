"""Specimen module.

This module contains the class `Specimen` returned to the user after the
evolution concludes as well as the `RawSpecimen` used for the internal
evolutionary algorithm.

The field `phenotype` of `Specimen` is of greatest interest for the end user.
"""

from copy import deepcopy as copy
from random import randint, random

from cartesian import decode_genotype


class RawSpecimen():
    """The class `RawSpecimen` used during the evolutionary process.

    Unlike the `Specimen` it does not contain a function lookup table nor the
    phenotype in order to save some memory, and therefore cannot be used
    'as is'. It exists for implementation purpouses only.

    Attributes:
        genotype (list) : array of integers used to construct the phenotype.
        node_size (int) : length of a single node in the genome.
        inp (int) : number of input values taken by a specimen.
        out (int) : number of output values produced by a specimen.
    """
    def __init__(self, inp, out, node_size, dna_len, fn_tab_size):
        """Create a `Raw Specimen` with random genotype.

        Args:
            inp (int) : number of input values taken by a specimen.
            out (int) : number of output values produced by a specimen.
            node_size (int) : size of a single node.
            dna_len (int) : number of nodes. Leave empty genotype if `None`.
            fn_tab_size (int) : size of function lookup table.
        """

        self.inp = inp
        self.out = out
        self.fns = fn_tab_size
        self.node_size = node_size
        self.genotype = list()
        if dna_len is None:
            # This means we want an empty genotype and will fill it later
            return
        # TODO: Actually build a genotype
        self.genotype = [randint(0, 10) for _ in range(dna_len * node_size)]

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
                # TODO: Actually mutate
                gene += 1
        return offspring


class Specimen(RawSpecimen):
    """The class `Specimen` produced by the evolutionary algorithm.

    Unlike `RawSpecimen` it contains the full phenotype and so it is capable
    of being used on its own.

    Attributes:
        fn_tab (tuple) : function lookup table used to decode a genotype.
        genotype (list) : array of integers used to construct the phenotype.
        node_size (int) : length of a single node in the genome.
        inp (int) : number of input values taken by a specimen.
        out (int) : number of output values produced by a specimen.
        phenotype (object) : the phenotype of the specimen.
    """
    def __init__(self, raw, fn_tab):
        """Create an instance of usable `Specimen` from a raw one.

        Args:
            raw (RawSpecimen) : specimen to convert.
            fn_tab (tuple) : function lookup table used to decode the genotype.
        """
        super().__init__(
            raw.inp,
            raw.out,
            raw.node_size,
            None,    # <--- We want an empty genotype
            raw.fns)
        self.genotype = raw.genotype.copy()
        self.fn_tab_size = len(fn_tab)
        self.phenotype = decode_genotype(self, fn_tab)
