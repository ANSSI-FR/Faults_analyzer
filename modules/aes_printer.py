from .bin_utils import int2byte_tab, hex_diff, mat_diff, get_diff
from .aes_analyzer import get_aes_nb_fully_faulted_diag

class AESPrinter():

    AES_BLOCK_BIT_LENGTH = 128
    """The size of an AES block in bits."""
    AES_BLOCK_BYTE_LENGTH = AES_BLOCK_BIT_LENGTH/8
    """The size of an AES block in bytes."""
    MATRIX_NB_COLUMNS = 4
    """The number of columns of an AES block matrix."""

    """A class for doing the analysis of faults on AES."""
    def __init__(self, faulted_values, expected_value):
        """The constructor of the class."""
        self.faulted_values = faulted_values
        """The faulted values to analyze."""
        self.expected_value = expected_value
        """The expected value of the ciphering."""

    def convert_faulted_values(self, faulted_values):
        """Convert a list of integers into a list where these integers are converted into a list of bytes."""
        return [int2byte_tab(fv) for fv in faulted_values]

    def print_hex_diff(self, index):
        """Print the hexadecimal difference of a faulted value with the reference.

        :param int index: the index of the faulted value to check the difference with.

        """
        hex_diff(self.expected_value, self.faulted_values[index])

    def print_list_hex_diff(self, index_list):
        """Print the hexadecimal difference of faulted values with the reference.

        :param list index_list: the indexes of the faulted value to print.

        """
        for index in index_list:
            self.print_hex_diff(index)
            print("")

    def print_all_hex_diff(self):
        """Print the hexadecimal difference of all the faulted values."""
        for i in range(len(self.faulted_values)):
            self.print_hex_diff(i)
            print("")

    def remove_bad_sized_faulted_values(self):
        """Remove the faulted value with a size different from the size of an AES block."""
        for i, fv in enumerate(self.faulted_values):
            if len(int2byte_tab(fv)) != self.AES_BLOCK_BYTE_LENGTH:
                self.faulted_values.pop(i)

    def print_mat_diff(self, index):
        """Print the matrix difference of a faulted value with the reference.

        :param int index: the index of the faulted value to check the difference with.

        """
        mat_diff(int2byte_tab(self.faulted_values[index]), self.MATRIX_NB_COLUMNS, int2byte_tab(self.expected_value))

    def print_list_mat_diff(self, index_list):
        """Print the matrix difference of faulted values with the reference."""
        for index in index_list:
            self.print_mat_diff(index)
            print("")

    def print_all_mat_diff(self):
        """Print the matrix difference of all faulted values with the reference."""
        for i in range(len(self.faulted_values)):
            self.print_mat_diff(i)
            print("")

    def get_diag_faulted_values(self, nb_faulted_diag):
        ret = []
        for fv in self.faulted_values:
            nb_f_diag = get_aes_nb_fully_faulted_diag(fv, self.expected_value)
            if nb_f_diag == nb_faulted_diag:
                ret.append(fv)
        return ret

    def get_diag_faulted_values_diff(self, nb_faulted_diag):
        faulted_values = self.get_diag_faulted_values(nb_faulted_diag)
        return [fv ^ self.expected_value for fv in faulted_values]

    def print_diag_faulted_values(self, nb_faulted_diag):
        faulted_values = self.get_diag_faulted_values(nb_faulted_diag)
        for fv in faulted_values:
            print("0x{:032x}".format(fv))

    def print_diag_faulted_values_diff(self, nb_faulted_diag):
        faulted_values = self.get_diag_faulted_values_diff(nb_faulted_diag)
        for fv in faulted_values:
            print("0x{:032x}".format(fv))

if __name__ == "__main__":
    faulted_values = [0x69c4e0d86a7b0430d864b78070b4c55a,
                      0x5dd5fa0c2f4f670d0f6634e399ad1235,
                      0x4ec17cd424f6be26c55e913b7c06d4ab,
                      0x713722d3acb5900f813c9ed3c1c0e735,
                      0x861a85617a250e561319f9985b480912,
                      0x9a2e0eb105ed0a7fb8066489da31adae,
                      0x941570c44b26d97eaf8d6e79641b740d,
                      0x9f2591bfd80327056f170ead4abac6b6,
                      0x23752829262bc571231f467e1944743f,
                      0x22cdfb1f8f41b6df33e80cb441ac6ac3,
                      0xdfc64e04f5e998b5da60da784b14701b,
                      0x2ee87aa8687dde95f6a7457a176c2d75,
                      0x4479e82eb3a2b1d1a77579adcb6d0c94,
                      0xfc9dec155c228f7d6810dd390977eac6,
                      0xd296b4ee90fb4d3b170767fac9b25ac,
                      0x845d94847d160f1c6d1f4debe77fa22c,
                      0x2eb16359ce14b250922267bad8fbfaee,
                      0x3ce5b8b3698b2340295e0f8e3037ed,
                      0xee111dd86a7b0430a60ad2e370b4c55a,
                      0x1bad0133afe0320894f18a0a9b59ee87,
                      0x17afbe436aae30790e1c940d26958f53,
                      0x434d6fab7ca271a655f531fd90745e4b,
                      0x95e2b420d82462139395f25ea357bb02,
                      0xb20568693d45cb9edb0e160a9ab4df6d,
                      0x3c531743416a5f31fe5e9c0feff2c217,
                      0xa9c4d90116b3dbdc5b475cbdc00da1c5]

    expected_value = 0x69c4e0d86a7b0430d8cdb78070b4c55a

    ap = AESPrinter(faulted_values, expected_value)
    ap.print_all_hex_diff()
    ap.print_all_mat_diff()
    print(ap.get_diag_faulted_values(1))
