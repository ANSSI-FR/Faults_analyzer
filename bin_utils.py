from termcolor import colored
import numpy as np

class Data:

    """Class to represent a number."""

    value: int
    dim: int

    def __init__(self, value, dim):
        """Constructor."""

        self.value = value
        self.dim = dim  # nombre de bits

    def hex(self):
        return "{0:#0{1}x}".format(self.value, self.dim / 4)

    def bin(self):
        return "{0:b0{1}b}".format(self.value, self.dim)


def to_unsigned(number: int, nb_bits: int):
    """To unsigned function.

        >>> to_unsigned(5, 32)
        5
        >>> to_unsigned(-5, 8)
        251
        >>> to_unsigned(-5, 9)
        507

        Args
        ----
            number int the number to convert
            nb_bits int The number of bits considered

        Returns
        -------
            value

    """
    if number < 0:
        return (1 << nb_bits) + number

    return number


def s2u(number: int, nb_bits: int):
    """Shorter version of to_unsigned."""
    return to_unsigned(number, nb_bits)

def to_unsigned_list(table: list, nb_bits: int):
    """Cast to unsigned every value of the table."""
    return [s2u(v, nb_bits) for v in table]
        

def a2_comp(number: int, nb_bits: int):
    """To do one complement.

        >>> a2_comp(5, 8)
        251
        >>> a2_comp(-5, 8)
        5
        >>> a2_comp(-5, 9)
        5

        Args
        ----
            number int The number to consider
            nb_bits int The number of bits considered

        Returns
        -------
            value

    """

    base = 1 << nb_bits

    return (base - number) % base


def get_bit(number, index):
    """Return the indexieme bit of number.

        >>> get_bit(5, 0)
        1
        >>> get_bit(5, 1)
        0
        >>> get_bit(5, 2)
        1

        Args
        ----
            number int The number to consider
            index int The bits to return

        Returns
        -------
            bit int 1 or 0

    """
    return (int(number) & (1 << index)) >> index


def set_bit_zero(number: int, index: int):
    return number & ~(1 << index)


def set_bit_one(number: int, index: int):
    return number | (1 << index)


def set_bit(number: int, index: int, value: int):
    if value == 1:
        return set_bit_one(number, index)

    if value == 0:
        return set_bit_zero(number, index)

    raise Exception("Error: Value can be only 1 or 0")


def comp(number, nb_bits):
    """Return the bit complementary of number."""

    if number > (1 << nb_bits):
        raise Exception("Error: the number does not fit in the number of bits")
    ret = 0
    for i in range(nb_bits):
        ret = set_bit(ret, i, 1 - get_bit(number, i))
    return ret


def bin_diff(number1, number2, nb_bits):
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
    for i in range(n):
        tab.append(val)
    return tab

def int2byte_tab(n):
    tab = []
    n_hex = hex(n)[2:]
    for i in np.arange(0, len(n_hex), 2):
        hex_s = n_hex[i:i+1]
        tab.append(int(hex_s, 16))
    return tab

def get_diff(t1, t2):
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
    for i in range(len(tab)):
        print("{:02x} ".format(tab[i]), end="")
        if i%n_cols == n_cols-1:
            print("")

def mat_diff(tab, n_cols, ref):
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
