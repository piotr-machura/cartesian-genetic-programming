"""Specimen module.

This module contains the class `Specimen` used for the internal evolutionary
algorithm and returned to the user after the evolution concludes.

The method `outputs` of `Specimen` is of greatest interest for the end user.
"""
from copy import deepcopy as copy
from inspect import signature
from node import Node


class Specimen():
    """The class `Specimen` used during the evolutionary process.

    To obtain the outputs use the method `outputs`.

    Attributes:
        genotype (list) : array of nodes used to calculate the output.
        inp (int) : number of input values taken by a specimen.
        out (int) : number of output values produced by a specimen.
        fn_tab (tuple) : function lookup table.
    """
    def __init__(self, inp, out, n_nodes, fn_tab):
        """Create a `Specimen` with random genotype.

        Args:
            inp (int) : number of input values taken by a specimen.
            out (int) : number of output values produced by a specimen.
            fn_tab (tuple) : function lookup table.
        """
        self.inp = inp
        self.out = out
        self.fn_tab = fn_tab
        # Size of a single node is the maximum amount of args taken by functions
        # from fn_tab
        node_size = max(len(signature(fn).parameters) for fn in self.fn_tab)
        self.genotype = [
            Node(self, i + inp, node_size) for i in range(n_nodes)
        ]
        # Add output nodes to the end
        self.genotype += [
            Node(self, i, 1, True) for i in range(n_nodes, n_nodes + self.out)
        ]

    def outputs(self, inputs):
        """Generate output from input.

        Args:
            inputs (tuple) : input values from which outputs are obtained.

        Returns:
            Outputs of the specimen.
        """
        # TODO: Construct the outputs
        outputs = None
        return outputs

    def mutate(self, mutation_p):
        """Mutate into an offspring instance of `Specimen`.

        Args:
            mutation_p (float) : probability of mutating a given gene.

        Returns:
            Offspring, a correctly mutated instance of `Specimen`.
        """
        offspring = copy(self)
        for node in offspring.genotype:
            node.mutate(mutation_p)
        return offspring
