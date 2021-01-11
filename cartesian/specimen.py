"""Specimen module.

This module contains the class `Specimen` used for the internal evolutionary
algorithm and returned to the user after the evolution concludes.

The method `outputs` of `Specimen` is of greatest interest for the end user.
"""
from copy import deepcopy as copy
from random import random
from inspect import isfunction, signature
from node import Node, OutputNode, InputNode


class Specimen():
    # TODO: a contructor that takes a genome string so that we can load
    # an existing specimen
    """The class `Specimen` used during the evolutionary process.

    To obtain the outputs use the method `outputs`.

    Attributes:
        genotype (list) : array of nodes used to calculate the output.
        inp (int) : number of input values taken by a specimen.
        out (int) : number of output values produced by a specimen.
        function_table (tuple) : function lookup table.
    """
    def __init__(
        self,
        inputs_num,
        outputs_num,
        nodes_num,
        function_table,
        mutation_prob,
        mutation_num,
    ):
        """Create a `Specimen` with random genotype.

        Args:
            inputs_num (int) : number of input values taken by a specimen.
            outputs_num (int) : number of output values produced by a specimen.
            nodes_num (int) : number of nodes to generate.
            function_table (tuple) : function lookup table.
            mutation_prob (float) : probability of a applying the mutation
                                    operator to a gene.
            mutation_num (int) : number of genes that can be mutated in a singe
                                 application of the mutation operator.
        """
        # TODO: implement exceptions
        if inputs_num < 1 or outputs_num < 1 or nodes_num < 1:
            raise Exception
        for function in function_table:
            if not isfunction(function) or isinstance(function) == type(print):
                raise Exception
        self.function_table = function_table
        self.inputs = None
        if mutation_prob > 1:
            raise Exception
        self.mutation_prob = mutation_prob
        if mutation_num > nodes_num:
            raise Exception
        self.mutation_num = mutation_num
        # Size of a single node is the maximum amount of args taken by functions
        # from fnunction_table
        node_size = max(
            len(signature(function).parameters)
            for function in self.function_table)
        # Create a random genotype
        self.genotype = [InputNode(self, i) for i in range(inputs_num)]
        self.genotype += [Node(self, node_size) for _ in range(nodes_num)]
        self.genotype += [OutputNode(self) for _ in range(outputs_num)]

    def outputs(self, inputs):
        """Generate output from input.

        Args:
            inputs (tuple) : input values from which outputs are obtained.

        Returns:
            Outputs of the specimen.
        """
        # TODO: Construct the outputs
        self.inputs = inputs
        outputs = None
        return outputs

    def mutate(self):
        """Mutate into an offspring instance of `Specimen`.
        Returns:
            Offspring, a correctly mutated instance of `Specimen`.
        """

        offspring = copy(self)
        for node in offspring.genotype:
            if random() < offspring.mutation_prob:
                node.mutate()
        return offspring
