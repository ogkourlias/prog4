#!/usr/bin/env python3

"""
    A simulation of photosynthesis using object-oriented Python.
    Run with:
        python3 assignment2.py
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "Production"
__version__ = "1.0"

# IMPORTS
import sys


# CLASSES
class Atom:
    """
    Represents a chemical atom with a symbol, number of protons (atomic number), and number of neutrons.
    """

    def __init__(self, symbol, atom_nr, neutrons):
        """
        Initialize an Atom instance.

        Args:
            symbol (str): Chemical symbol (e.g., 'H', 'O').
            atom_nr (int): Number of protons (atomic number).
            neutrons (int): Number of neutrons.
        """
        self.symbol = symbol
        self.atom_nr = atom_nr
        self.neutrons = neutrons

    def __lt__(self, other):
        """
        Compare atoms by mass number. Raises if atoms are not isotopes.
        """
        if self.atom_nr != other.atom_nr:
            raise Exception("Not isotopes of the same element")
        return self.mass_number() < other.mass_number()

    def __le__(self, other):
        """
        Compare atoms by atomic number.
        """
        return self.atom_nr <= other.atom_nr

    def proton_number(self):
        """
        Return the number of protons.
        """
        return self.atom_nr

    def mass_number(self):
        """
        Return the mass number (protons + neutrons).
        """
        return self.atom_nr + self.neutrons

    def isotope(self, new_nr):
        """
        Change the number of neutrons (create a new isotope).

        Args:
            new_nr (int): New number of neutrons.
        """
        self.neutrons = new_nr


class Molecule:
    """
    Represents a molecule composed of atoms and their respective counts.
    """

    def __init__(self, atoms):
        """
        Initialize a Molecule.

        Args:
            atoms (list of tuple): List of (Atom, count) tuples.
        """
        self.atoms = atoms
        # Generate a chemical formula, omitting the count if it's 1
        self.symbol = (
            ("")
            .join([f"{tpl[0].symbol}{tpl[1]}" for tpl in self.atoms])
            .replace("1", "")
        )

    def __add__(self, other):
        """
        Combine two molecules into a new chemical formula string.
        """
        return self.symbol + other.symbol

    def __str__(self):
        """
        Return the molecule's chemical formula as a string.
        """
        return self.symbol


class Chloroplast:
    """
    Simulates a chloroplast capable of performing photosynthesis using H2O and CO2.
    """

    def __init__(self):
        """
        Initialize with zero molecules of water, CO2, sugar, and O2.
        """
        self.water = 0
        self.co2 = 0
        self.sugar = 0
        self.o2 = 0

    def add_molecule(self, molecule):
        """
        Add a molecule (H2O or CO2) to the chloroplast and trigger photosynthesis if possible.

        Args:
            molecule (Molecule): Molecule to be added.

        Returns:
            list: A list containing newly formed sugar and oxygen molecules (if photosynthesis occurs),
                  or an empty list otherwise.
        """
        # Identify molecule and increment the appropriate counter
        if str(molecule) == "H2O":
            self.water += 1
        elif str(molecule) == "CO2":
            self.co2 += 1
        else:
            raise ValueError("Not H2O or CO2")

        # Check if enough reactants are present for photosynthesis
        if self.water >= 12 and self.co2 >= 6:
            self.water -= 12
            self.co2 -= 6

            # Define product atoms
            hydrogen = Atom("H", 1, 0)
            carbon = Atom("C", 6, 6)
            oxygen = Atom("O", 8, 8)

            # Create sugar (C6H12O6) and oxygen (O2) molecules
            sugar = Molecule([(carbon, 6), (hydrogen, 12), (oxygen, 6)])
            o2 = Molecule([(oxygen, 2)])

            self.sugar += 1
            self.o2 += 6

            return [(str(sugar), self.sugar), (str(o2), self.o2)]

        return []

    def __str__(self):
        """
        Return a string representation of current molecule counts.
        """
        return f"H2O: {self.water} \n CO2: {self.co2}"


# MAIN
def main(args):
    """
    Main function to simulate user-driven molecule input and photosynthesis reactions.
    """
    # Create atoms
    hydrogen = Atom("H", 1, 0)
    carbon = Atom("C", 6, 6)
    oxygen = Atom("O", 8, 8)

    # Create basic molecules
    water = Molecule([(hydrogen, 2), (oxygen, 1)])
    co2 = Molecule([(carbon, 1), (oxygen, 2)])

    # Instantiate chloroplast simulation
    demo = Chloroplast()
    els = [water, co2]

    # Interactive loop
    while True:
        print("\nWhat molecule would you like to add?")
        print("[1] Water")
        print("[2] carbon dioxide")
        print("Please enter your choice: ", end="")

        try:
            choice = int(input())
            res = demo.add_molecule(els[choice - 1])
            if len(res) == 0:
                print(demo)
            else:
                print("\n=== Photosynthesis!")
                print(res)
                print(demo)

        except Exception:
            print("\n=== That is not a valid choice.")


# Entry point
if __name__ == "__main__":
    sys.exit(main(sys.argv))
