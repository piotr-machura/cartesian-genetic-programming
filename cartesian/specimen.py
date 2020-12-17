"""Specimen module.

This module contains the class `Specimen` returned to the user after the
evolution concludes as well as the `RawSpecimen` used for the internal
evolutionary algorithm.

The method `outputs` of `Specimen` is of greatest interest for the end user.

The functions `gen_outputs` and `mutate` are not class methods to save on memory
in the case of very large populations.
"""
from copy import deepcopy as copy
from random import randint, random
from inspect import signature


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
        active_nodes (list) : array with adresses of nodes connected to outputs.
        fns (int) : number of functions in a lookup table.
    """
    def __init__(self, inp, out, node_size, n_of_nodes, fn_tab):
        """Create a `RawSpecimen` with random genotype.

        Args:
            inp (int) : number of input values taken by a specimen.
            out (int) : number of output values produced by a specimen.
            node_size (int) : size of a single node.
            n_of_nodes (int) : number of nodes. Leave empty genotype if `None`.
            fn_tab (tuple) : function lookup table.
        """
        self.inp = inp
        self.out = out
        self.fns = len(fn_tab)
        self.node_size = node_size
        self.genotype = list()
        if n_of_nodes is None:
            # This means we want an empty genotype and will fill it later
            return
        # TODO: Actually build a genotype
        self.genotype = [randint(0, 10) for _ in range(n_of_nodes * node_size)]
        # TODO: Replace this with @property
        self.active_nodes = _get_active_nodes(self, fn_tab)


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
        active_nodes (list) : array with adresses of nodes connected to outputs.
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
            None,    # <--- Do not bother contructing a genotype
            raw.fns)
        self.genotype = raw.genotype.copy()
        self.fns = len(fn_tab)
        self.fn_tab = fn_tab

    def outputs(self, inputs):
        """Return outputs of `Specimen` from provided inputs.

        This is a convinience method. Calls `decode_cgp` using  `self` and
        `self.fn_tab`, returning the outputs.

        Args:
            inputs (tuple) : input values to use in `decode_cgp`.
        """
        return gen_outputs(self, self.fn_tab, inputs)


def gen_outputs(specimen, fn_tab, inputs):
    """Decode the genotype and generate output from input.

    Args:
        specimen (RawSpecimen) : specimen with a genotype to decode.
        fn_tab (tuple) : function lookup table used to decode a genotype.
        inputs (tuple) : input values from which outputs are obtained.

    Returns:
        Outputs of the specimen.
    """
    # TODO: Construct the outputs
    outputs = None
    return outputs


def mutate(specimen, mutation_p, fn_tab):
    """Mutate into an offspring instance of `RawSpecimen`.

    Args:
        specimen (RawSpecimen) : specimen to mutate.
        mutation_p (float) : probability of mutating a given gene.

    Returns:
        Offspring, a correctly mutated instance of `RawSpecimen`.
    """
    offspring = copy(specimen)
    for gene in offspring.genotype:
        if random() <= mutation_p:
            # TODO: Actually mutate
            gene += 1
    offspring.active_nodes = _get_active_nodes(offspring, fn_tab)
    return offspring


def _get_active_nodes(specimen, fn_tab):
    """Get active nodes in a given genotype.

    Args:
        specimen (RawSpecimen) : specimen with the genotype to process.

    Returns:
        List with node indexes of active nodes. Note that theese are **NODE**
        indexes, eg. 4th node, 5th node etc., **NOT** the indexes in the
        genotype itself.
    """
    genotype_size = len(specimen.genotype)
    total_nodes = specimen.inp + specimen.node_size + specimen.out
    # Mark all nodes as inactive
    active_nodes = [False for _ in range(genotype_size)]

    # Activate outputs
    for out_index in range(genotype_size - specimen.out, genotype_size):
        active_nodes[out_index] = True
    # Iterate over the nodes from end to start of input nodes
    for node_indx in range(total_nodes, specimen.inp, -1):
        if active_nodes[node_indx]:    # Current node is active
            node_start = specimen.node_size * (node_indx - specimen.inp)
            node_end = node_start + specimen.node_size
            # Current node is the slice of genotype from node_start to node_end
            current_node = specimen.genotype[node_start:node_end]
            # Calculate how many inputs current node actually needs
            required_nodes = len(signature(fn_tab(current_node[-1])))
            for input_gene in current_node[0:required_nodes]:
                # Mark this many nodes as active
                active_nodes[input_gene] = True

    # Return an array with node indexes considered active
    return [
        node_indx for node_indx in range(specimen.inp, total_nodes)
        if active_nodes[node_indx]
    ]
