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

    def __init__(self, parent, index, size):
        self.parent = parent
        self.index = index
        # TODO: make a standalone OutputNode class
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
        needed = len(signature(self.inner_function).parameters)
        for input_address in self.input_addresses[:needed]:
            # Take arguments from other nodes
            if input_address >= len(self.parent.inputs):
                genotype_index = input_address - self.parent.inputs    # Offset the index
                # Recursively get the arguments
                args.append(
                    self.parent.genotype[genotype_index].calculate(global_inputs))
            else:    # Take arguments from global inputs
                args.append(global_inputs[input_address])
        if self.inner_function is None:
            return args
        return self.inner_function(*args)

    def mutate(self):
        """Randomly change the an input address or `innner_fn`.
        """
        if random() < 1/(len(self.input_addresses)):
            last_function = self.inner_function
            while(self.inner_function == last_function):
                self.inner_function = choice(self.parent.function_table)
        else:
            self.input_addresses[randrange(len(self.input_addresses))] = randint(
                0, self.index - 1)


class OutputNode(Node):
    def __init__(self, parent, index):
        """The class `OutputNode` used as a container for the final output.

        Attributes:
            parent (Specimen) : the specimen to which the node belongs.
            index (int) : index in the parent's genotype
        """
        super().__init__(parent, index, 1)

    def calculate(self, global_inputs):
        """Take input from `input_addresses` in 'parent.genotype'and return them.

        Args:
            global_inputs (tuple) : 'global' inputs from which outputs are obtained.

        Returns:
            Output of `inner_function` OR the `args` if `inner_function` is `None`.`
        """
        args = list()
        needed = len(self.input_addresses)
        for input_address in self.input_addresses[:needed]:
            # Take arguments from other nodes
            if input_address >= len(self.parent.inputs):
                genotype_index = input_address - self.parent.inputs    # Offset the index
                # Recursively get the arguments
                args.append(
                    self.parent.genotype[genotype_index].calculate(global_inputs))
            else:    # Take arguments from global inputs
                args.append(global_inputs[input_address])
        return args

    def mutate(self):
        """Randomly change the an input address.
        """
        self.input_addresses[randrange(len(self.input_addresses))] = randint(
            0, self.index - 1)
