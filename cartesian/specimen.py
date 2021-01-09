"""Specimen module.

This module contains the class `Specimen` used for the internal evolutionary
algorithm and returned to the user after the evolution concludes.

The method `outputs` of `Specimen` is of greatest interest for the end user.
"""
from copy import deepcopy as copy
from inspect import signature
from node import Node
from random import sample, random


class Specimen():
    # TODO: a contructor that takes a genome string so that we can load an existing specimen
    """The class `Specimen` used during the evolutionary process.

    To obtain the outputs use the method `outputs`.

    Attributes:
        genotype (list) : array of nodes used to calculate the output.
        inp (int) : number of input values taken by a specimen.
        out (int) : number of output values produced by a specimen.
        fn_tab (tuple) : function lookup table.
    """

    def __init__(self, inputs_num, outputs_num, nodes_num, function_table, mutation_prob, mutation_num):
        """Create a `Specimen` with random genotype.

        Args:
            inputs (int) : number of input values taken by a specimen.
            out (int) : number of output values produced by a specimen.
            fn_tab (tuple) : function lookup table.
            mutation_prob (float) : probability of a applying the mutation operator to a gene.
            mutation_num (int) : number of genes that can be mutated in a singe application of the mutation operator.
        """
        self.inputs = inputs_num
        self.outputs = outputs_num
        self.function_table = function_table
        self.mutation_prob = mutation_prob
        # Size of a single node is the maximum amount of args taken by functions
        # from fn_tab
        node_size = max(len(signature(function).parameters)
                        for function in self.functions_tables)
        self.genotype = [
            Node(self, i + inputs_num, node_size) for i in range(nodes_num)
        ]
        # Add output nodes to the end
        self.genotype += [
            Node(self, i, 1, True) for i in range(nodes_num, nodes_num + self.out)
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

    def mutate(self):
        """Mutate into an offspring instance of `Specimen`.
        Returns:
            Offspring, a correctly mutated instance of `Specimen`.
        """

        offspring = copy(self)
        for node in sample(offspring.genotype):
            if random() < offspring.mutation_prob:
                node.mutate()
        return offspring
