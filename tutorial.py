from ConstFitness import Constellation, RedConst, BlueConst
from pathlib import Path
import numpy as np

# Declare the path to the CLPSSitesRandomSats directory
rand_path = Path('./CLPSSitesRandomSats')
opt_path = Path('./AllConstellations')

# Call read_types from the Constellation class. This pulls in all of the possible site locations and orbit types from the CLPSSitesRandomSats directory
Constellation.get_root_dir(rand_dir=rand_path, opt_dir=opt_path)

# Declare what site locations will be used. The convention is the same as in the file directory, with a numbering [1-9]
site_locs = [1, 3]

# Call get_site_locs to set what the site locations are in the Constellation base class
Constellation.get_site_locs(site_locs)

# Now, declare some satellites! These must have the following form for the optimized satellites
blue_opt_sats = ["(3,3,2)", "BLUE", 1]

# Declare the blue constellation by feeding in the blue satellites. For optimized satellites, the type must be declared as "Optimized". 
blue_const = BlueConst(blue_opt_sats, type="Optimized")

# Declare the red satellites. Randomized satellites must have the following form.
red_rand_sats = [["DRO_1", "20"],
                 ["halo_1", "0"],
                 ["halo_3", "80"]]

# Declare the red constellation. This constellation is tracking the blue constellation, which is fed in as the second parameter in the constructor
red_const = RedConst(red_rand_sats, blue_const)

# These print out the generated fitness values. Each sequential set of two columns matches up to the site locations as they were declared in site_locs. 
# So, the first two columns correspond to site location 2, and the next two columns to site location 3
print(blue_const.get_blue_fitness())
print(red_const.get_red_fitness())