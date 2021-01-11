"""Node module. *(heh)*

Contains the class `Node` used as a container for a function and where it
should take inputs from. Output nodes are impelemnted as nodes of size 1 and
inner function of None.
"""
from random import choice, randint, random, randrange
from inspect import signature


class Node:
    # TODO: contructor that take in a gene string
    """The class `Node` is used as a container for a function and where it
    should take inputs from.

    Attributes:
        parent (Specimen) : the specimen to which the node belongs.
        size (int) : amount of inputs this node accepts.
    """

    def __init__(self, parent, index, size):
        self.parent = parent
        # TODO: make a standalone OutputNode class
        self.inner_function = choice(parent.function_table)
        self.index = index
        # Inputs can only be in front of the current node
        self.input_addresses = [randint(0, index - 1)
                                for _ in range(size)]

    def calculate(self):
        """Take input from `input_addresses` in 'parent.genotype'and return the
        output of `inner_function`.

        The args needed for `inner_function` are gathered recursively.

        Returns:
            Output of `inner_function`.
        """
        args = list()
        # Only take as many args as the function needs
        needed = len(signature(self.inner_function).parameters)
        for input_address in self.input_addresses[:needed]:
            # Recursively get the arguments
            args.append(
                self.parent.genotype[input_address].calculate())

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
    def __init__(self, index, parent):
        """The class `OutputNode` is used as a container for the final output.

        Attributes:
            parent (Specimen) : the specimen to which the node belongs.
        """
        super().__init__(parent, index, 1)

    def calculate(self):
        """Take input from `input_addresses` in 'parent.genotype'and return them.

        Returns:
            Output of 'input_addresses'.
        """
        args = list()
        needed = len(self.input_addresses)
        for input_address in self.input_addresses[:needed]:
            # Recursively get the arguments
            args.append(
                self.parent.genotype[input_address].calculate())
        return args

    def mutate(self):
        """Randomly change the an input address.
        """
        self.input_addresses[randrange(len(self.input_addresses))] = randint(
            0, self.index - 1)


class InputNode(Node):
    def __init__(self, parent, index, input_index):
        """The class `InputNode` is used as a container for the initial program input.

        Attributes:
            parent (Specimen) : the specimen to which the node belongs.
            input_index (int) : index of the program input.
        """
        super().__init__(parent, index, 0)
        self.input_index = input_index

    def calculate(self):
        return self.parent.inputs[self.input_index]

    def mutate(self):
        pass
