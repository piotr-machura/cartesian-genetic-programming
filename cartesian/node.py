"""Node module. *(heh)*

Contains the class `Node` and its subsidiaries used in a `Specimen`s genotype.
`OutputNode`s are used to begin the recursive proces of gathering data and
executing the algorithm encoded in the nodes. `InputNode`s are simply pointing
that process to the data temporarily stored in `Specimen._input_data`.
"""
from random import randint, random, randrange
from inspect import signature


class Node:
    """The class `Node` is used as a container for a function and where it
    should take inputs from.

    Attributes:
        parent (Specimen) : the specimen to which the node belongs.
        size (int) : amount of inputs this node accepts.
    """
    def __init__(self, parent, index, size):
        self.parent = parent
        self.inner_function_index = randint(0, len(parent.function_table) - 1)
        self.inner_function = parent.function_table[self.inner_function_index]
        self.index = index
        # Inputs can only be in front of the current node
        self.input_addresses = [
            randint(0, self.index - 1) for _ in range(size)
        ]
        self._cached_data = None    # We will store calculated data here

    def calculate(self):
        """Take input from `input_addresses` in 'parent.genotype'and return the
        output of `inner_function`.

        The args needed for `inner_function` are gathered recursively.

        Returns:
            Output of `inner_function`.
        """
        if self._cached_data is not None:
            # We have already made the calculations
            return self._cached_data
        args = list()
        # Only take as many args as the inner function needs
        needed = len(signature(self.inner_function).parameters)
        for input_address in self.input_addresses[:needed]:
            # Recursively get the arguments
            args.append(self.parent.genotype[input_address].calculate())

        self._cached_data = self.inner_function(*args)
        return self._cached_data

    def mutate(self):
        """Randomly change the an input address or `innner_function`."""
        if random() <= 1 / (len(self.input_addresses) + 1):
            last_function_index = self.inner_function_index
            while self.inner_function_index == last_function_index:
                # Generate new index
                self.inner_function_index = randint(
                    0,
                    len(self.parent.function_table) - 1)
            self.inner_function = self.parent.function_table[
                self.inner_function_index]
        else:
            self.input_addresses[randrange(len(
                self.input_addresses))] = randint(0, self.index - 1)

    def to_raw(self):
        """Encode into a list of integers for usage with `Specimen`'s
        encoding method `to_raw()`.

        Returns:
            list of integers encoded as follows:
            [0] -> index of inner_function in the lookup table
            [...] -> contents of input_adresses
        """
        raw = list()
        raw.append(self.inner_function_index)
        raw += self.input_addresses
        return raw


class OutputNode(Node):
    """The class `OutputNode` is used as a container for the final output.

    Attributes:
        parent (Specimen) : the specimen to which the node belongs.
    """
    def __init__(self, parent, index):
        super().__init__(parent, index, size=1)

    def calculate(self):
        """Take input from `input_addresses` in 'parent.genotype'and return
        them.

        Returns:
            Output of 'input_addresses'.
        """
        adress = self.input_addresses[0]    # There is only one input adress
        return self.parent.genotype[adress].calculate()

    def mutate(self):
        """Randomly change the input address.
        """
        self.input_addresses[randrange(len(self.input_addresses))] = randint(
            0, self.index - 1)

    def to_raw(self):
        """Encode into a list of integers for usage with `Specimen`'s
        encoding method `to_raw()`.

        Returns:
            self.input_addresses (since there is no inner_function to encode)
        """
        return self.input_addresses


class InputNode(Node):
    """The class `InputNode` is used as a container for the initial program
    input.

    Attributes:
        parent (Specimen) : the specimen to which the node belongs.
        input_index (int) : index of the program input.
    """
    def __init__(self, parent, index, input_index):
        super().__init__(parent, index, 0)
        self.input_index = input_index

    def calculate(self):
        """Take input from parent and pass them down."""
        return self.parent._input_data[self.input_index]    #pylint: disable=protected-access

    def mutate(self):
        pass

    def to_raw(self):
        """Return an empty list since this type of node should not be included
        in the tuple produced by `Specimen.to_raw()`.
        """
        return list()
