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

class Chroloplast:
    def __init__(self):
        self.water = 0
        self.co2 = 0
        self.sugar = 0
        self.o2 = 0
    
    def add_molecule(self, molecule):
        if str(molecule) == "H2O":
            self.water += 1
        elif str(molecule) == "CO2":
            self.co2 += 1
        else:
            raise ValueError("Not H2O or CO2")
        if self.water >= 12 and self.co2 >= 6:
            self.water -= 12
            self.co2 -= 6
            hydrogen = Atom("H", 1, 0)
            carbon = Atom("C", 6, 6)
            oxygen = Atom("O", 8, 8)
            sugar = Molecule( [ (carbon, 6), (hydrogen, 12), (oxygen, 6) ] )
            o2 = Molecule([(oxygen, 2)])
            self.sugar += 1
            self.o2 += 6
            return [(str(sugar), self.sugar), (str(o2), self.o2)]
        return []

    def __str__(self):
        return f"H2O: {self.water} \n CO2: {self.co2}"

# MAIN
def main(args):
    """ Main function """
    hydrogen = Atom('H', 1, 0)
    carbon = Atom('C', 6, 6)
    oxygen = Atom('O', 8, 8)
    water = Molecule( [ (hydrogen, 2), (oxygen, 1) ] )
    co2 = Molecule( [ (carbon, 1), (oxygen, 2) ])
    demo = Chroloplast()
    els = [water, co2]
    while (True):
        print ('\nWhat molecule would you like to add?')
        print ('[1] Water')
        print ('[2] carbondioxyde')
        print ('Please enter your choice: ', end='')
        try:
            choice = int(input())
            res = demo.add_molecule(els[choice-1])
            if (len(res)==0):
                print (demo)
            else:
                print ('\n=== Photosynthesis!')
                print (res)
                print (demo)

        except Exception:
            print ('\n=== That is not a valid choice.')
    # FINISH
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
