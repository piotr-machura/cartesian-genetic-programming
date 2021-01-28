"""Specimen module.

This module contains the class `Specimen` used for the internal evolutionary
algorithm and returned to the user after the evolution concludes.

The method `outputs` of `Specimen` is of greatest interest for the end user.

The instance of `Specimen` can be converted into 2 special tuples: one
containing the genotype (instance of `Specimen._Raw`) and another containing
the function lookup table (instance of `Specimen._FunctionTable`). Those can
then be used to fully reconstruct an instance of `Specimen`.
"""
from copy import deepcopy
from random import random
from inspect import signature
from node import Node, OutputNode, InputNode


class Specimen:
    """The class `Specimen` used during the evolutionary process.

    To obtain the outputs use the method `outputs`.

    Attributes:
        genotype (list) : list of nodes used to calculate the output.
        function_table (Specimen._FunctionTable) : function lookup table.
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
        self.function_table = self._FunctionTable(function_table)
        self.mutation_prob = mutation_prob
        self.max_mutations = max_mutations
        self.inputs_num = inputs_num
        self.outputs_num = outputs_num
        self.nodes_num = nodes_num
        self._input_data = None    # For temporarily storing input data
        self.fit = None
        # Only the initial population is created by this constructor
        self.generation = 0
        self.total_mutations = 0
        # Size of a single node is the maximum amount of args taken by functions
        # from function_table
        node_size = max(
            len(signature(function).parameters)
            for function in self.function_table)

        # Contruct the genotype
        self.genotype = [InputNode(self, i, i) for i in range(inputs_num)]
        nodes_start = self.inputs_num
        self.genotype += [
            Node(self, nodes_start + i, node_size) for i in range(nodes_num)
        ]
        outputs_start = nodes_start + self.nodes_num
        self.genotype += [
            OutputNode(self, outputs_start + i) for i in range(outputs_num)
        ]

    def outputs(self, input_data):
        """Generate output from input.

        Args:
            input_data (tuple) : input values from which outputs are obtained.

        Returns:
            Tuple of outputs of the algorithm encoded in the genotype.
        """
        self._input_data = input_data
        # Clear the cache from nodes
        for node in self.genotype:
            node._cached_data = None    # pylint: disable=protected-access
        outputs_start = self.inputs_num + self.nodes_num
        out = [node.calculate() for node in self.genotype[outputs_start:]]
        self._input_data = None    # No need to keep it around after we're done
        # Clear the cache from nodes again
        for node in self.genotype:
            node._cached_data = None    # pylint: disable=protected-access
        return tuple(out)

    def mutate(self):
        """Mutate into an offspring instance of `Specimen`.

        Returns:
            Offspring, a correctly mutated instance of `Specimen` with the
            `fit` reset and the `generation` number increased by 1.
        """

        offspring = deepcopy(self)
        offspring.fit = None    # Reset offsprings' fit
        mutations = 0
        max_mutations = offspring.max_mutations
        # Do not waste mutations on input nodes
        for node in offspring.genotype[offspring.inputs_num:]:
            if max_mutations is None or mutations < max_mutations:
                if random() <= offspring.mutation_prob:
                    mutations += 1
                    node.mutate()
            else:
                break
        offspring.generation += 1
        offspring.total_mutations += mutations
        return offspring

    def assign_fit(self, fit_function):
        """Assign fit based on the fit_function. This is used for concurency
        reasons (as target for the `threading.Thread` class).

        Args:
            fit_function (callable) : fit function to pipe outputs through.
        """

        self.fit = fit_function(self.outputs)
        if self.fit is None:
            raise TypeError('Fit function returned None.')

    class _FunctionTable(tuple):
        """This is a special tuple used to store the function lookup table.
        Using this reduces the probability that the function table will be
        accidentally messed up."""

    # NUMBER ARRAY REPRESENTATION
    # ---------------------------
    # This is a section dedicated to converting the specimen to/from a pair
    # of tuples.

    class _Raw(tuple):
        """This is a special tuple returned by the `to_raw()` class method which
        can be rebuilt into an instance of `Specimen` using `from_raw()`.
        """

    def to_raw(self):
        """Encode most of the information about the specimen as a special tuple
        of integers (or floats when necessary).

        **WARNING:** This tuple doesn't contain any information about the
        `function_table`, which is **necessary** to reconstruct a specimen. Make
        sure you keep it around and **do not tamper with it** if you plan on
        decoding the tuple returned by this function.

        Returns:
            A tuple of (`Specimen._Raw`, `Specimen._FunctionTable`).

            `_FunctionTable` is a tuple with functions used by the encoded
            algorithm. `_Raw` is a tuple of integers (or floats where necessary)
            constructed as follows:
            [0] -> inputs_num
            [1] -> outputs_num
            [2] -> nodes_num
            [3] -> mutation_prob (float)
            [4] -> max_mutations
            [5] -> fit (float OR None if not convertible to float)
            [6] -> generation
            [7] -> total_mutations
            [...] -> nodes as sequences of integers, encoded by `Node.to_raw()`
        """
        raw = list()
        raw.append(self.inputs_num)
        raw.append(self.outputs_num)
        raw.append(self.nodes_num)
        raw.append(self.mutation_prob)
        raw.append(self.max_mutations)
        try:
            raw.append(float(self.fit))
        except ValueError:    # The information about the fit is lost
            raw.append(None)
        raw.append(self.generation)
        raw.append(self.total_mutations)
        for node in self.genotype:
            raw += node.to_raw()
        return self._Raw(raw), self.function_table

    @classmethod
    def from_raw(cls, raw_specimen, function_table):
        """Reconstruct the specimen from the `Specimen._Raw` and
        `Specimen._FunctionTable` generated by the method `to_raw()`.

        **WARNING:** If you have tampered with the raw tuple OR the function
        table in any way expect this to (at best) generate random garbage, or
        (more likely) not work at all.

        Args:
            raw_specimen (Specimen._Raw) : special tuple generated by to_raw().
            function_table (Specimen._FunctionTable) : function lookup table.

        Returns:
            A reconstructed instance of `Specimen` ready to be used.
        """
        if not isinstance(raw_specimen, cls._Raw):
            raise TypeError('Cannot reconstruct a Specimen from arguments.')
        if not isinstance(function_table, cls._FunctionTable):
            raise TypeError('Cannot reconstruct a Specimen from arguments.')
        instance = cls(
            inputs_num=raw_specimen[0],
            outputs_num=raw_specimen[1],
            nodes_num=raw_specimen[2],
            function_table=function_table,
            mutation_prob=raw_specimen[3],
            max_mutations=raw_specimen[4],
        )
        instance.fit = raw_specimen[5]
        instance.generation = raw_specimen[6]
        instance.total_mutations = raw_specimen[7]
        raw_nodes = raw_specimen[8:]

        for i in range(inputs_num):
            instance.genotype += InputNode(instance, i, i)

        for i in range(len(raw_nodes)):
            if i >= len(raw_nodes) - instance.outputs_num:
                new_output_node = OutputNode(instance, i)
                new_output_node.input_addresses = raw_nodes[i]
                instance.genotype += new_output_node
            else:
                new_node = Node(instance, i, len(raw_nodes[i][1]))
                new_node.input_addresses = raw_nodes[i][1]
                new_node.inner_function_index = raw_nodes[i][0]
                new_node.inner_function = function_table[raw_nodes[i][0]]
                instance.genotype += new_node
        return instance
