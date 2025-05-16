#!/usr/bin/env python3

"""
    usage:
        python3 assignment2.py
"""

# METADATA VARIABLES
__author__ = "Orfeas Gkourlias"
__status__ = "WIP"
__version__ = "0.1"

# IMPORTS
import sys


# CLASSES
class Atom():
    """ Desc """
    def __init__(self, symbol, atom_nr, neutrons):
        self.symbol = symbol
        self.atom_nr = atom_nr
        self.neutrons = neutrons
    
    def __lt__(self, other):
        if self.atom_nr != other.atom_nr:
            raise Exception("Not isotopes of the same element")
        return self.mass_number() < other.mass_number()


    def __le__(self, other):
        return self.atom_nr <= other.atom_nr
        
    def proton_number(self):
        return self.atom_nr
    
    def mass_number(self):
        return self.atom_nr + self.neutrons
    
    def isotope(self, new_nr):
        self.neutrons = new_nr

class Molecule():
    def __init__(self, atoms):
        self.atoms = atoms
        self.symbol = ("").join([f"{tpl[0].symbol}{tpl[1]}" for tpl in self.atoms]).replace("1", "")

    def __add__(self, other):
        return self.symbol + other.symbol

    def __str__(self):
        return self.symbol
    
# MAIN
def main(args):
    """ Main function """
    hydrogen = Atom('H', 1, 0)
    carbon = Atom('C', 6, 6)
    oxygen = Atom('O', 8, 8)

    water = Molecule( [ (hydrogen, 2), (oxygen, 1) ] )
    co2 = Molecule( [ (carbon, 1), (oxygen, 2) ])
    print (water) # H2O
    print (co2) # CO2
    print (water + co2) # H2OCO2
    # FINISH
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
