from termcolor import colored

import numpy as np

class Data:

    """Class to represent a number.

    """

    def __init__(self, value, dim):
        """Constructor."""

        self.value = value
        self.dim = dim  # nombre de bits

    def hex(self):
        return "{0:#0{1}x}".format(self.value, self.dim / 4)

    def bin(self):
        return "{0:b0{1}b}".format(self.value, self.dim)

def to_unsigned(number, nb_bits):
    """Compute the unsigned value of the given number according to the given number of bits used for encoding.

    >>> to_unsigned(5, 32)
    5
    >>> to_unsigned(-5, 8)
    251
    >>> to_unsigned(-5, 9)
    507

    :param int number: the number to convert.
    :param int nb_bits: the number of bits considered.

    :returns: an integer which is the unsigned value of the given number.

    """
    if number < 0:
        return (1 << nb_bits) + number

    return number

s2u = to_unsigned

def to_unsigned_list(table, nb_bits):
    """Compute the unsigned value of every values in the table according to the given number of bits used for encoding.

    :param list table: the list of values to convert.
    :param int nb_bits: the number of bits considered.

    :returns: a list containing the unsigned value of the former list.

    """
    return [s2u(v, nb_bits) for v in table]

def a2_comp(number, nb_bits):
    """Compute the A2 complement of the given number according to the given number of bits used for encoding.

    >>> a2_comp(5, 8)
    251
    >>> a2_comp(-5, 8)
    5
    >>> a2_comp(-5, 9)
    5

    :param int number: the number to compute the A2 complement from.
    :param int nb_bits: the number of bits considered.

    :returns: an integer which is the A2 complement of the given number.

    """

    base = 1 << nb_bits

    return (base - number) % base


def get_bit(number, index):
    """Return the value of the bit at the given index position in the given number.

    >>> get_bit(5, 0)
    1
    >>> get_bit(5, 1)
    0
    >>> get_bit(5, 2)
    1

    :param int number: the number to get the bit value from.
    :param int index: the index of the bit to get the value.

    :returns: an integer which value is either 0 or 1.

    """
    return (int(number) & (1 << index)) >> index


def set_bit_zero(number, index):
    """Set the bit at the given index position in the given number to 0.

    :param int number: the number the set a 0 in.
    :param int index: the index of the bit to set to 0.

    :returns: an integer which is the given number with the bit at the given index set to 0.
    """
    return number & ~(1 << index)


def set_bit_one(number, index):
    """Set the bit at the given index position in the given number to 1.

    :param int number: the number the set a 1 in.
    :param int index: the index of the bit to set to 1.

    :returns: an integer which is the given number with the bit at the given index set to 1.
    """
    return number | (1 << index)


def set_bit(number, index, value):
    """Set the bit at the given index position in the given number to the given value. This function does nothing if value is different from 0 or 1.

    :param int number: the number to set the bit in.
    :param int index: the index of the bit to set.
    :param int value: the value (0 or 1) to set the bit to.

    :returns: an integer which is the number with its bit at the index set to the value.

    :raises: Exception if value is not 0 or 1.
    """
    if value == 1:
        return set_bit_one(number, index)

    if value == 0:
        return set_bit_zero(number, index)

    raise Exception("Error: Value can be only 1 or 0")


def comp(number, nb_bits):
    """Compute the binary complementary of the given number considering the given number of bits for encoding.

    :param int number: the number to get the complementary from.
    :param int nb_bits: the number of bits considered.

    :returns: an integer which is the binary complementary of the number.

    """

    if number > (1 << nb_bits):
        raise Exception("Error: the number does not fit in the number of bits")
    ret = 0
    for i in range(nb_bits):
        ret = set_bit(ret, i, 1 - get_bit(number, i))
    return ret


def bin_diff(number1, number2, nb_bits):
    """Compute the binary difference between two numbers on a given number of bits and print the result.

    :param int number1: the first number for the comparison.
    :param int number2: the second number for the comparison.
    :param int nb_bits: the number of bits considered.

    """
    diffs = []

    for i in range(nb_bits):
        if get_bit(number1, i) != get_bit(number2, i):
            diffs.append(1)
        else:
            diffs.append(0)

    for i in reversed(range(nb_bits)):
        print(get_bit(number1, i), end="")
    print("")

    for i in reversed(range(nb_bits)):
        if diffs[i] == 1:
            to_print = colored(get_bit(number2, i), "red")
        else:
            to_print = get_bit(number2, i)
        print(to_print, end="")
    print("")

    for diff in reversed(diffs):
        if diff == 1:
            print("^", end="")
        else:
            print(" ", end="")
    print("")

def pad(tab, val, n):
    """Add a number of values at the end of a list.

    :param list tab: the list to add data in.
    :param int val: the value to add.
    :param int n: the number of values to add.

    :returns: the padded list.

    """
    for i in range(n):
        tab.append(val)
    return tab

def int2byte_tab(n):
    """Convert an integer into its byte representation.

    :param int n: the number to convert.

    :returns: a list which contains the hexadecimal coefficients of the given number.

    """
    tab = []
    n_hex = hex(n)[2:]
    for i in np.arange(0, len(n_hex), 2):
        hex_s = n_hex[i:i+2]
        tab.append(int(hex_s, 16))
    return tab

def get_diff(t1, t2):
    """Compute the difference between two lists of the same size.

    :param list t1: the first list to compare.
    :param list t2: the second list to compare.

    :returns: -1 if the list have different size, a list of False/True values in the other case, every True value corresponds to a difference in the list at the corresponding index.

    """
    if len(t1) != len(t2):
        print("Error: t1 and t2 have different size")
        return -1
    diffs = []
    for i in range(len(t1)):
        if t1[i] == t2[i]:
            diffs.append(False)
        else:
            diffs.append(True)
    return diffs

def hex_diff(number1, number2):
    """Compute the byte difference between two numbers and print the result.

    :param int number1: the first number to compare.
    :param int number2: the second number to compare.

    """
    diffs = []
    n1_hex_tab = int2byte_tab(number1)
    n2_hex_tab = int2byte_tab(number2)
    n1_l = len(n1_hex_tab)
    n2_l = len(n2_hex_tab)

    if n1_l != n2_l:
        print("Info: numbers don't have the same size in base 16, padding the shorter with 'XX'")
        if n1_l < n2_l:
            pad(n1_hex_tab, "XX", n2_l-n1_l)
            n1_l = n2_l
        elif n2_l < n1_l:
            pad(n2_hex_tab, "XX", n1_l-n2_l)
            n2_l = n1_l
        else:
            raise Exception("Error: Can't reach here")

    for i in range(n1_l):
        if n1_hex_tab[i] == "XX" or n2_hex_tab[i] == "XX":
            diffs.append(False)
        else:
            if n1_hex_tab[i] == n2_hex_tab[i]:
                diffs.append(False)
            else:
                diffs.append(True)

    for i in range(n1_l):
        print("{:02x}".format(n1_hex_tab[i]), end="")
    print("")

    for i in range(n2_l):
        if n2_hex_tab[i] == "XX":
            to_print = colored("XX", "yellow")
        else:
            if diffs[i]:
                to_print = colored("{:02x}".format(n2_hex_tab[i]), "red")
            else:
                to_print = "{:02x}".format(n2_hex_tab[i])
        print(to_print, end="")
    print("")

    for diff in diffs:
        if diff:
            print("^^", end="")
        else:
            print("  ", end="")
    print("")

def print_as_mat(tab, n_cols):
    """Print a list of integers in an hexadecimal matrix format on a certain number of columns. Useful for checking AES diagonals.

    :param list tab: the list of integers to print.
    :param int n_cols: the number of columns of the matrix.

    """
    for i in range(len(tab)):
        print("{:02x} ".format(tab[i]), end="")
        if i%n_cols == n_cols-1:
            print("")

def mat_diff(tab, n_cols, ref):
    """Print the difference between a list and a reference in an hexadecimal matrix format. Useful for AES.

    :param list tab: the list of integers to compare and print.
    :param int n_cols: the number of columns of the matrix.
    :param list ref: the list reference.

    """
    if len(tab) != len(ref):
        return -1
    diffs = get_diff(tab, ref)
    for i in range(len(tab)):
        if diffs[i]:
            to_print = colored("{:02x} ".format(tab[i]), "red")
        else:
            to_print = "{:02x} ".format(tab[i])
        print(to_print, end="")
        if i%n_cols == n_cols-1:
            print("")
