from ConstFitness import Constellation, RedConst, BlueConst
from pathlib import Path
import numpy as np

# Declare the path to the CLPSSitesRandomSats directory
root_path = Path('./CLPSSitesRandomSats')

# Call read_types from the Constellation class. This pulls in all of the possible site locations and orbit types from the CLPSSitesRandomSats directory
Constellation.read_types(root_path)

# Declare what site locations will be used. The convention is the same as in the file directory, with a numbering [1-9]
site_locs = [2, 3]

# Call get_site_locs to set what the site locations are in the Constellation base class
Constellation.get_site_locs(site_locs)

# Now, declare some satellites! These must have the following form. This is an nx2 array, with n satellites. Each satellite is specified by the name of the orbit and the phasing
blue_sats = [["DRO_1", "20"],
           ["halo_1", "0"],
           ["halo_3", "80"]]

# Declare the blue constellation by feeding in the blue satellites
blue_const = BlueConst(blue_sats)

# Declare the red satellites
red_sats = [["DRO_1", "20"],
            ["halo_1", "0"],
            ["halo_3", "80"]]

# Declare the red constellation. This constellation is tracking the blue constellation, which is fed in as the second parameter in the constructor
red_const = RedConst(red_sats, blue_const)

# These print out the generated fitness values. Each sequential set of two columns matches up to the site locations as they were declared in site_locs. 
# So, the first two columns correspond to site location 2, and the next two columns to site location 3
print(blue_const.get_blue_fitness())
print(red_const.get_red_fitness())