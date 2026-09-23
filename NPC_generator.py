
import os
import numpy as np 
import itertools

origins_list = ["Empire", "Bakufu", "Babaan", "Azure Coast"]
species_list = ["Assimar", "Dark Elf", "Desert Elf", "Dragonborn", "Dwarf", "Gnome", "Goblin", "Goliath", "Halfling", "High Elf", "Human", "Orc", "Tiefling", "Tortle", "Wood Elf"]
species_weights = {
    "Empire":      [0.1, 2, 1, 2, 1, 1, 1, 1, 5, 4, 5, 1, 1, 1, 4],
    "Bakufu":      [0.1, 1, 1, 5, 1, 5, 5, 1, 1, 1, 1, 1, 5, 5, 1],
    "Babaan":      [0.1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Azure Coast": [0.1, 1, 1, 4, 1, 5, 5, 1, 1, 1, 1, 1, 5, 5, 1],
}
genders_list = ["m (he/him)", "f (she/her)", "nb (they/them)"]

# Main function for the generation of an NPC
def generate_NPC(origin, input_species=None, input_gender=None, input_name=None):
    # Check that arguments conform to expectations 
    if origin not in origins_list: raise Exception("Given origin is invalid")
    if input_species is not None and input_species not in species_list: raise Exception("Given species is invalid")
    if input_gender is not None and input_gender not in genders_list: raise Exception("Given gender is invalid")
    
    # Generate properties of NPC (use while loop to facilitate repeated generation until satisfactory)
    while True:
        species = generate_species(origin)               if input_species is None else input_species
        gender  = generate_gender(species)               if input_gender  is None else input_gender
        name    = generate_name(origin, species, gender) if input_name    is None else input_name
        
        # Print the result
        print(f"{"NPC origin: ":<25}" + origin)
        print(f"{"NPC species: ":<25}" + species)
        print(f"{"NPC gender (pronouns): ":<25}" + gender)
        print(f"{"NPC name: ":<25}" + name)
        
        # Ask whether the generated NPC is accepted
        input_yes    = ["", "y", "Y", "yes"]
        input_no     = ["n", "N", "no"]
        input_cancel = ["c", "C", "cancel"]
        while True:
            inpt = input("Accept generated NPC? [Y/n/cancel]\n")
            if inpt in input_yes + input_no + input_cancel:
                print("")
                break
            else:
                print("Input not understood")

        # Depending on whether the NPC is accepted mark the name as used or re-generate
        if inpt in input_yes:
            mark_name_as_used(origin, species, gender, name)
            break
        elif inpt in input_no:
            continue
        elif inpt in input_cancel:
            return


# Functions for generating the species, gender, and name of an NPC
def generate_species(origin):
    return np.random.choice(species_list, 1, p=species_weights[origin]/np.sum(species_weights[origin]))[0]


def generate_gender(species):
    if species == "Tortle":
        return genders_list[2]
    else:
        return np.random.choice(genders_list, 1, p=[0.45, 0.45, 0.1])[0]


def generate_name(origin, species, gender):
    if species == "Tortle":
        filename = "Azure Coast_Tortle_names"
    if species == "Desert Elf":
        filename = "Babaan_Desert Elf_names"
    else:
        filename = names_list_filename(origin, species, gender)
    with open(filename, 'r') as file:
            names_list = file.readlines()
    for name in names_list:
        if name[0:3] == "USED":
            names_list.remove(name)
    if len(names_list) == 0:
        return "All names have been used"
    else:
        return np.random.choice(names_list, 1, p=np.ones(len(names_list))/len(names_list))[0]


# Function to put together the appropriate filename to load possible names
def names_list_filename(origin, species, gender):
    # Check successively less specific names lists
    possible_filenames = ["_".join([origin, species, gender, "names.txt"]),
                          "_".join([origin, species, "names.txt"]),
                          "_".join([origin, "names.txt"])]
    for filename in possible_filenames:
        if os.path.isfile(filename):
            return filename
    # If none of those exist return the general list
    return "general_names.txt"


# Function to indicate that a name has already been used (and should not be used again)
def mark_name_as_used(origin, species, gender, name):
    filename = names_list_filename(origin, species, gender)
    with open(filename, 'r') as file:
        names_list = file.readlines()
    index_of_name = names_list.index(name)
    names_list[index_of_name] = "USED " + names_list[index_of_name]
    with open(filename, 'w') as file:
        file.writelines(names_list)


# Function to get an imperial surname (since they have a special system of surnames)
def generate_Imperial_surname():
    with open("Empire_surnames", 'r') as file:
        names_list = file.readlines()
    return np.random.choice(names_list, 1, p=np.ones(len(names_list))/len(names_list))[0]
test

# # Function to put together the list of Imperial names (since they have a special system of surnames)
# def gather_Empire_names_list():
#     with open("Empire_firstnames.txt", 'r') as file:
#         Empire_firstnames_list = file.readlines()
#     with open("Empire_surnames.txt", 'r') as file:
#         Empire_surnames_list = file.readlines()
#     # Put names together, removing '\n' from the first name and adding spaces
#     Empire_names_list = [a[:-1] + " " + b for (a, b) in list(itertools.product(Empire_firstnames_list, Empire_surnames_list))]
#     with open("Empire_names.txt", 'w') as file:
#         file.writelines(Empire_names_list)



# generate_NPC(origin, species, gender, name)
# gather_Empire_names_list()
# generate_Imperial_surname()



# TODO:
# Assign names according to species rather than origin?
#   -Tortles should always have Tortle names, likewise for Desert Elves and maybe others?
# Change the distribution of species probabilities 
#   -It's weird to have many Desert Elves on the Azure Coast? Likewise for other species?
#   -Possibly just set a bunch of probabilities to zero
# Improve name lists?
#   -Dragonborn should be Germanic instead?
# Do something more clever for the assignment of Imperical surnames
