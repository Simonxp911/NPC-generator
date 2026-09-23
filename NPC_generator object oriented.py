
import numpy as np

origins_list = ["Empire", "Bakufu", "Babaan", "Azure Coast"]
species_list = ["Assimar", "Dark Elf", "Desert Elf", "Dragonborn", "Dwarf", "Gnome", "Goblin", "Goliath", "Halfling", "High Elf", "Human", "Orc", "Tiefling", "Tortle", "Wood Elf"]
species_weights = {
    "Empire":      np.ones(len(species_list)),
    "Bakufu":      np.ones(len(species_list)),
    "Babaan":      np.ones(len(species_list)),
    "Azure Coast": np.ones(len(species_list)),
}
genders_list = ["m (he/him)", "f (she/her)", "nb (they/them)"]


class NPC():
    def __init__(self, origin, species=None, gender=None, name=None):
        # Check that arguments conform to expectations 
        if origin not in origins_list: raise Exception("Given origin is invalid")
        if species is not None and species not in species_list: raise Exception("Given species is invalid")
        if gender is not None and gender not in genders_list: raise Exception("Given gender is invalid")

        # Generate properties of NPC (use while loop to facilitate repeated generation until satisfactory)
        while True:
            self.origin  = origin                                                                   #the nation or area where the NPC originated 
            self.species = species if species is not None else generate_species(origin)             #species of the NPC 
            self.gender  = generate_gender(species)                                                 #gender (pronouns) of the NPC
            self.name    = name if name is not None else generate_name(origin, species, gender)     #name of the NPC

            # Print the result 
            print(self)

            # Ask whether the generated NPC is accepted
            input_yes = ["", "y", "Y", "yes"]
            input_no  = ["n", "N", "no"]
            while True:
                inpt = input("Accept generated NPC? [Y/n]")
                if inpt in input_yes + input_no:
                    break
                else:
                    print("Input not understood")

            # Depending on whether the NPC is accepted mark the name as used or re-generate
            if inpt in ["", "y", "Y", "yes"]:
                mark_name_as_used(origin, species, gender, self.name)
                break
            elif inpt in ["n", "N", "no"]:
                continue
    
    def __str__(self):
        return ("NPC origin: " + self.origin + "\n" +
                "NPC species: " + self.species + "\n" +
                "NPC gender (pronouns): " + self.gender + "\n" +
                "NPC name: " + self.name)


# Functions to randomly generate NPC properties
def generate_species(origin):
    return species_list[0]

def generate_gender(species):
    return genders_list[0]

def generate_name(origin, species, gender):
    return "Jack"

def mark_name_as_used(origin, species, gender, name):
    pass