"""Specimen module.

This module contains the class `Specimen` used for the internal evolutionary
algorithm and returned to the user after the evolution concludes.

The method `outputs` of `Specimen` is of greatest interest for the end user.
"""
from copy import deepcopy
from random import random
from inspect import signature
from node import Node, OutputNode, InputNode


class Specimen():
    """The class `Specimen` used during the evolutionary process.

    To obtain the outputs use the method `outputs`.

    Attributes:
        genotype (list) : array of nodes used to calculate the output.
        function_table (tuple) : function lookup table.
        inputs_num (int) : number of input values taken by a specimen.
        outputs_num (int) : number of output values produced by a specimen.
        nodes_num (int) : number of gene nodes.
        mutation_prob (float) : probability of a applying the mutation
                                operator to a gene.
        max_mutations (int) : number of genes that can be mutated in a singe
                              application of the mutation operator.
        fit (object) : last fit assigned by the fit function.
        generation (int) : number of generations since the evolution started.
        total_mutations (int) : total number of mutations since the evolution
                                started.
    """
    def __init__(
        self,
        inputs_num,
        outputs_num,
        nodes_num,
        function_table,
        mutation_prob,
        max_mutations,
    ):
        """Create a `Specimen` with random genotype.

        Args:
            inputs_num (int) : number of input values taken by a specimen.
            outputs_num (int) : number of output values produced by a specimen.
            nodes_num (int) : number of gene nodes.
            function_table (tuple) : function lookup table.
            mutation_prob (float) : probability of a applying the mutation
                                    operator to a gene.
            max_mutations (int) : number of genes that can be mutated in a singe
                                  application of the mutation operator.
        """
        self.function_table = function_table
        self.mutation_prob = mutation_prob
        self.max_mutations = max_mutations
        self.inputs_num = inputs_num
        self.outputs_num = outputs_num
        self.nodes_num = nodes_num
        self.fit = None
        # Only the initial population is created by this constructor
        self.generation = 0
        self.total_mutations = 0
        # Size of a single node is the maximum amount of args taken by functions
        # from function_table
        node_size = max(
            len(signature(function).parameters)
            for function in self.function_table)

        self.genotype = [InputNode(self, i, i) for i in range(inputs_num)]
        self.genotype += [
            Node(self, i + inputs_num, node_size) for i in range(nodes_num)
        ]
        self.genotype += [
            OutputNode(self, i + inputs_num + nodes_num)
            for i in range(outputs_num)
        ]
        self._input_data = None    # For temporarily storing input data

    def outputs(self, input_data):
        """Generate output from input.

        Args:
            input_data (tuple) : input values from which outputs are obtained.

        Returns:
            Outputs of the algorithm encoded in the genotype.
        """
        self._input_data = input_data
        outputs = [
            node.calculate() for node in self.genotype[self.outputs_num:]
        ]
        self._input_data = None    # No need to keep it around after we're done
        return tuple(outputs)

    def mutate(self):
        """Mutate into an offspring instance of `Specimen`.

        Returns:
            Offspring, a correctly mutated instance of `Specimen` with the
            `generation` value increased by 1.
        """

        offspring = deepcopy(self)
        offspring.fit = None    # Reset offsprings' fit
        mutations = 0
        # Do not mutate the input nodes
        for node in offspring.genotype[offspring.inputs_num:]:
            if mutations < offspring.max_mutations:
                if random() <= offspring.mutation_prob:
                    mutations += 1
                    node.mutate()
        offspring.generation += 1
        offspring.total_mutations += mutations
        return offspring

    def to_raw(self):
        """Encode most of the information about the specimen as an array of
        integers (or floats when necessary).

        **WARNING:** This array doesn't contain any information about the
        `function_table`, which is **necessary** to reconstruct a specimen. Make
        sure to keep it around if you plan on decoding the array returned by
        this function.

        Returns:
            Tuple of integers (or floats) constructed as follows:
            [0] -> inputs_num
            [1] -> nodes_num
            [2] -> outputs_num
            [3] -> mutation_prob (float)
            [4] -> max_mutations
            [5] -> fit (float OR None if not convertible to float)
            [6] -> generation
            [7] -> total_mutations
            [...] -> nodes as sequences of integers, encoded by `Node.to_raw()`
        """
        raw = list()
        raw.append(self.inputs_num)
        raw.append(self.nodes_num)
        raw.append(self.outputs_num)
        raw.append(self.mutation_prob)
        raw.append(self.max_mutations)
        try:
            raw.append(float(self.fit))
        except ValueError:
            raw.append(None)
        raw.append(self.generation)
        raw.append(self.total_mutations)
        for node in self.genotype:
            raw += node.to_raw()
        return tuple(raw)

    @staticmethod
    def reconstruct_raw(raw_specimen_array, function_table):
        """Reconstruct the specimen from a previously generated array given
        the function lookup table.

        Args:
            raw_specimen_array (tuple) : tuple generated by the to_raw() method.
            function_table (tuple) : function lookup table.

        Returns:
            A reconstructed instance of `Specimen` ready to be used.
        """
        # TODO: decode the raw array
        raise NotImplementedError
