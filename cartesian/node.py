"""Node module. *(heh)*

Contains the class `Node` used as a container for a function and where it
should take inputs from. Output nodes are impelemnted as nodes of size 1 and
inner function of None.
"""
from random import choice, randint
from inspect import signature


class Node:
    """The class `Node` used as a container for a function and where it
    should take inputs from.

    Attributes:
        parent (Specimen) : the specimen to which the node belongs.
        index (int) : index in the parent's genotype
    """
    def __init__(self, parent, index, size, output_node=False):
        self.parent = parent
        self.index = index
        # TODO: make a standalone OutputNode class
        if output_node:
            self.inner_fn = None
            size = 1
        else:
            self.inner_fn = choice(parent.fn_tab)
        # Inputs can only be in front of the current node
        self.input_adresses = [randint(0, self.index - 1) for _ in range(size)]

    def calculate(self, g_inp):
        """Take input from `input_adresses` in 'parent.genotype'and return the
        output of `inner_fn`.

        The args needed for `inner_fn` are gathered recursively.
        Args:
            g_inp (tuple) : 'global' inputs from which outputs are obtained.

        Returns:
            Output of `inner_fn` OR the `args` if `inner_fn` is `None`.`
        """
        args = list()
        # Only take as many args as the function needs
        if self.inner_fn is not None:
            # TODO: the new OutputNode class should fix this mess
            needed = len(signature(self.inner_fn).parameters)
        else:
            needed = len(self.input_adresses)
        for i in self.input_adresses[:needed]:
            if i >= len(self.parent.inp):    # Take arguments from other nodes
                genotype_i = i - self.parent.inp    # Offset the index
                # Recursively get the arguments
                args.append(self.parent.genotype[genotype_i].calculate(g_inp))
            else:    # Take arguments from global inputs
                args.append(g_inp[i])
        if self.inner_fn is None:
            return args
        return self.inner_fn(*args)

    def mutate(self, mutation_p):
        """Randomly change the 'input_adresses' and `innner_fn`.

        Args:
            mutation_p (float) : probability of mutating any of the attributes.
        """
        # TODO: Actually mutate the node
        pass
