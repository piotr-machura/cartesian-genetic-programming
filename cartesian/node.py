"""Node module. *(heh)*

Contains the class `Node` used as a container for a function and where it
should take inputs from. Output nodes are impelemnted as nodes of size 1 and
inner function of None.
"""
from random import choice, randint, random, randrange
from inspect import signature


class Node:
    # TODO: contructor that take in a gene string
    # TODO: better naming
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
            self.inner_function = None
            size = 1
        else:
            self.inner_function = choice(parent.function_table)
        # Inputs can only be in front of the current node
        self.input_addresses = [randint(0, self.index - 1)
                                for _ in range(size)]

    def calculate(self, global_inputs):
        """Take input from `input_addresses` in 'parent.genotype'and return the
        output of `inner_function`.

        The args needed for `inner_function` are gathered recursively.
        Args:
            global_inputs (tuple) : 'global' inputs from which outputs are obtained.

        Returns:
            Output of `inner_function` OR the `args` if `inner_function` is `None`.`
        """
        args = list()
        # Only take as many args as the function needs
        if self.inner_function is not None:
            # TODO: the new OutputNode class should fix this mess
            needed = len(signature(self.inner_function).parameters)
        else:
            needed = len(self.input_addresses)
        for i in self.input_addresses[:needed]:
            if i >= len(self.parent.inputs):    # Take arguments from other nodes
                genotype_i = i - self.parent.inputs    # Offset the index
                # Recursively get the arguments
                args.append(
                    self.parent.genotype[genotype_i].calculate(global_inputs))
            else:    # Take arguments from global inputs
                args.append(global_inputs[i])
        if self.inner_function is None:
            return args
        return self.inner_function(*args)

    def mutate(self):
        """Randomly change the 'input_addresses' and `innner_fn`.
        """
        if random() <= 0.5:
            last_function = self.inner_function
            while(self.inner_function == last_function):
                self.inner_function = choice(self.parent.function_table)
        else:
            self.input_addresses[randrange(len(self.input_addresses))] = randint(
                0, self.index - 1)
        pass
