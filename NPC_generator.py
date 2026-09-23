
import os
import numpy as np 
import itertools

areas_list = ["Empire", "Bakufu", "Babaan", "Azure Coast"]
species_list = ["Dark Elf", "Desert Elf", "Dragonborn", "Dwarf", "Gnome", "Goblin", "Goliath", "Halfling", "High Elf", "Human", "Orc", "Tiefling", "Tortle", "Wood Elf"]
genders_list = ["m (he/him)", "f (she/her)", "nb (they/them)"]
# Probabilities of origin for each area (i.e. if you have a person in area X how likely is it that their origin is Y)
origins_weights = {
    "Empire":      [0.8, 0.08, 0.02, 0.1],
    "Bakufu":      [0.05, 0.89, 0.01, 0.05],
    "Babaan":      [0.0, 0.0, 1.0, 0.0],
    "Azure Coast": [0.15, 0.04, 0.01, 0.8],
}
# Probabilities of species for each area (i.e. if you have a person in area X how likely is it that their species is Y)
# Presently, this is fairly minimal (there should be a non-zero probability for each species in all areas)
# Making a species probability requires the creation of a corresponding list of names
species_weights = {
    "Empire":      [1, 0, 1, 0, 0, 0, 0, 4, 3, 4, 0, 0, 0, 4],
    "Bakufu":      [0, 0, 0, 2, 0, 0, 1, 0, 0, 2, 2, 0, 0, 0],
    "Babaan":      [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Azure Coast": [0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 2, 1, 0],
}
# Probabilities for the genders/pronouns
genders_weights = [0.45, 0.45, 0.1]
# The probability for an NPC to be Assimar
assimar_probability = 0.01


# Main function for the generation of an NPC
def generate_NPC(current_area, input_origin=None, input_species=None, input_gender=None, input_name=None):
    # Check that arguments conform to expectations 
    if current_area not in areas_list: raise Exception("Given current_area is invalid")
    if input_origin is not None and input_origin not in areas_list: raise Exception("Given origin is invalid")
    if input_species is not None and input_species not in species_list: raise Exception("Given species is invalid")
    if input_gender is not None and input_gender not in genders_list: raise Exception("Given gender is invalid")
    
    # Generate properties of NPC (use while loop to facilitate repeated generation until satisfactory)
    while True:
        origin  = generate_origin(current_area)          if input_origin  is None else input_origin
        species = generate_species(origin)               if input_species is None else input_species
        gender  = generate_gender(species)               if input_gender  is None else input_gender
        name    = generate_name(origin, species, gender) if input_name    is None else input_name
        
        # Print the result
        print(f"{"Current area: ":<25}" + current_area)
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


# Functions for generating the origin, species, gender, and name of an NPC
def generate_origin(current_area):
    return np.random.choice(areas_list, 1, p=origins_weights[current_area]/np.sum(origins_weights[current_area]))[0]


def generate_species(origin):
    # There's a chance the NPC is an Assimar (in addition to another species)
    assimar_or_blank = " (Assimar)" if np.random.rand() < assimar_probability else ""
    return np.random.choice(species_list, 1, p=species_weights[origin]/np.sum(species_weights[origin]))[0] + assimar_or_blank


def generate_gender(species):
    # Tortles always use they/them
    if species == "Tortle":
        return genders_list[2]
    else:
        return np.random.choice(genders_list, 1, p=genders_weights)[0]


def generate_name(origin, species, gender):
    # Read list of names
    filename = names_list_filename(origin, species, gender)
    with open(filename, 'r') as file:
            names_list = file.readlines()
    
    # Remove already used names
    for name in names_list:
        if name[0:3] == "USED":
            names_list.remove(name)

    # Raise exception if there are no names left, else return the name
    if len(names_list) == 0:
        raise Exception("All names have been used")
    else:
        # Add an imperial surname if the NPC has origin = Empire
        imperialSurname_or_blank = " " + generate_Imperial_surname() if origin == "Empire" else ""
        # Return name (remove the newline from the name)
        return np.random.choice(names_list, 1, p=np.ones(len(names_list))/len(names_list))[0][:-1] + imperialSurname_or_blank


# Function to put together the appropriate filename to load possible names
def names_list_filename(origin, species, gender):
    # Check successively less specific names lists
    possible_filenames = ["names_lists/" + "_".join([origin, species, gender, "names.txt"]),
                          "names_lists/" + "_".join([origin, species, "names.txt"]),
                          "names_lists/" + "_".join([origin, "names.txt"])]
    for filename in possible_filenames:
        if os.path.isfile(filename):
            return filename
    # If none of those exist raise an exception
    raise Exception(f"Could not find an approriate list of names for origin: {origin}, species: {species}, gender: {gender}")


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
    with open("names_lists/Empire_surnames.txt", 'r') as file:
        names_list = file.readlines()
    return np.random.choice(names_list, 1, p=np.ones(len(names_list))/len(names_list))[0]



# generate_NPC(origin, species, gender, name)
# gather_Empire_names_list()
# generate_Imperial_surname()



# TODO:
# Improve name lists?
#   -Dragonborn should be Germanic instead?
# Do something more clever for the assignment of Imperical surnames
