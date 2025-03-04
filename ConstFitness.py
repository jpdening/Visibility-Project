from pathlib import Path
import pandas as pd
import numpy as np

class Constellation():

    ## Class attributes
    # Default variables
    T_f = 192.0
    dt = 30.0
    alpha = 30
    valid_site_locs = [x for x in range(1, 10)]

    # Variables to be filled with get_site_locs
    site_locs = []
    
    # The constructor must take in a list of tuples
    def __init__(self, in_sats, type="Random"):

        # Check that the type is correct
        if type not in ["Random", "Optimized"]:
            raise Exception("Please use a valid type. Use either Random or Optimized")

        # Check that in_sats is of the proper shape. It should be a list of lists
        proper_len = True

        if type == "Random":
            for ii in range(len(in_sats)):
                if len(in_sats[ii]) != 2:
                    proper_len = False
                    break
        else:
            if len(in_sats) != 3:
                proper_len = False

        if not proper_len:
            if type == "Random":
                raise Exception("Please ensure that all satellites are composed of orbit_type and phasing string pairs")
            if type == "Optimized":
                raise Exception("Please ensure that the optimized constellation is represented by a 3-tuple string, RED/BLUE type, and constellation number strings")

        # Add all of the satellites
        self.add_satellites(in_sats, type)

    # This method overwrites all of the satellites present in the constellation, and then computes the data associated with them
    def add_satellites(self, in_sats, type):
        self.sat_data = []

        if type == "Random":
            self.sat_data = RandConst.all_vis_data(in_sats)
        else:
            self.sat_data = OptConst.all_vis_data(in_sats)

    # The class method must take in the site locations used
    @classmethod
    def get_site_locs(cls, in_site_locs):

        if max(in_site_locs) > cls.valid_site_locs[-1] or min(in_site_locs) < 1:
            raise Exception("Invalid index for a site location. Please choose again")

        cls.site_locs = in_site_locs

    @staticmethod
    def get_root_dir(rand_dir=0, opt_dir=0):

        if rand_dir != 0:
            if not rand_dir.exists():
                raise Exception("Invalid path to random directory")
            else:
                RandConst.read_types(rand_dir)
        
        if opt_dir != 0:
            if not opt_dir.exists():
                raise Exception("Invalid path to optimized directory")
        
        RandConst.rand_path = rand_dir
        OptConst.opt_path = opt_dir


# Do NOT call this class from outside
class RandConst(Constellation):

    ## Class attributes
    # Default variables
    site_dict = {}
    orbit_types = []
    rand_path = 0

    # The class method must take in the location of CLPSSitesRandomSats and instantiate the applicable orbits and site locations
    @classmethod
    def read_types(cls, in_path:Path):

        if in_path.exists():
            cls.root_path = in_path
        else:
            raise Exception("Path to repository does not exist. Please check spelling")

        # Define the file format to look for
        my_format = f"T_fin_{cls.T_f}_dt_{cls.dt}_site_*"
        site_gen = in_path.glob(my_format)

        site_dirs = [site for site in site_gen]
            
        for ii in range(1, len(site_dirs)+1):
            cls.site_dict[ii] = site_dirs[ii-1]
        
        # In one of the subfolders, find all file names that have number(s) terminating the name
        orbit_format = f"*_[0-9]*"
        file_gen = Path(site_dirs[0]).glob(orbit_format)
        cls.orbit_types = [file.name for file in file_gen]
    
    # The class method must return the visibility data associated with a given satellite
    @classmethod
    def get_visibility_data(cls, in_sat):

        # in_sat is expected to be a list of the form ["orbit_type, "phasing"]

        # We need the visibility arrays for all of the site locations for the given satellite. 
        # These visibility arrays will be stored in tuples

        # Throw an error if there are no site locations defined yet
        if len(Constellation.site_locs) == 0:
            raise Exception("Please declare some site locations using Constellation.get_site_locs")
        
        # Throw an error if the path is not declared yet
        if cls.rand_path == 0:
            raise Exception("Please use Constellation.get_root_dir to enter the root path")

        # Check that the orbit type is valid
        if in_sat[0] not in cls.orbit_types:
            raise Exception("Please use one of the correct orbit types. Refer to the CLPSSitesRandomSats directory for valid types")

        # Read in the phasing. Correct to 0.1 if it is 0 to agree with pandas renaming convention
        phasing = in_sat[1]
        if phasing == "0":
            phasing = "0.1"

        vis_store = []
        for s in Constellation.site_locs:
            my_path = cls.site_dict[s] / f"{in_sat[0]}/site_detection.csv"

            # Read the data
            my_df = pd.read_csv(my_path)

            # Check that the phasing is valid
            all_columns = my_df.columns.values
            all_columns = all_columns[1:].tolist()

            if phasing not in all_columns:
                raise Exception("Please use one of the correct phasing types. Refer to a data file in the CLPSSitesRandomSats directory for valid types")

            vis_dat = my_df[phasing].values
            vis_store.append(vis_dat)
        
        return vis_store
    
    @classmethod
    def all_vis_data(cls, in_sats):
        all_data = []
        for s in range(len(in_sats)):
            all_data.append(RandConst.get_visibility_data(in_sats[s]))
        return all_data


class OptConst(Constellation):

    ## Class attributes
    # Default variables
    opt_path = 0

    @classmethod
    def all_vis_data(cls, in_sats):

        # Form the path to the data
        site_loc_string = "("
        for s in cls.site_locs[:-1]:
            site_loc_string = site_loc_string + f"({s},{cls.alpha}),"
        site_loc_string = site_loc_string + f"({cls.site_locs[-1]},{cls.alpha}))"

        base_path = cls.opt_path / in_sats[0] / f"T_fin_{cls.T_f}_dt_{cls.dt}_site_locs_{site_loc_string}"

        if not base_path.exists():
            raise Exception("Cannot find optimized data. Check the 3-tuple OR the site locations for correctness")
        
        my_path = base_path / in_sats[1]

        # See how many constellations are in this directory
        my_format = "const_*"
        all_const_iter = my_path.glob(my_format)

        num_const = 0

        for _ in all_const_iter:
            num_const += 1

        if in_sats[2] > num_const:
            raise Exception(f"Invalid constellation number. Exceeds the number of constellations present. Choose a constellation between 1 and {num_const}")
        
        # Get the path to my constellation
        my_const = my_path / f"const_{in_sats[2]}"

        # Determine the number of satellites
        all_sats_iter = my_const.glob("sat_*")
        num_sats = 0

        for _ in all_sats_iter:
            num_sats += 1

        # Now, extract the data. Note that visibility data is defined in layers. The outer layer is for satellites, layer 2 is for sites, layer 3 is the actual data
        all_data = []

        for sat in range(1, num_sats+1):
            data_path = my_const / f"sat_{sat}/site_detection.csv"

            my_df = pd.read_csv(data_path)

            sat_data = []
            for site in range(1, len(cls.site_locs)+1):
                col_num = f"0.{site}"
                temp_data = my_df[col_num].values
                temp_data = np.concatenate((np.array([0]), temp_data))

                sat_data.append(temp_data)
            
            all_data.append(sat_data)
        return all_data


# Make a derived class "BlueConst"
class BlueConst(Constellation):

    def __init__(self, in_sats, type="Random"):
        super().__init__(in_sats, type)
        
    # This will output a 
    def get_blue_fitness(self):

        n_sat = len(self.sat_data) # The number of satellites
        n_sites = len(Constellation.site_locs)
        # For each site location, we will compute the coverage and the maximum visible satellites
        blue_fit = np.zeros((1, 2 * n_sites))

        for s in range(n_sites):

            coverage_vec = self.sat_data[0][s]
            num_sat_vec = self.sat_data[0][s]
            for q in range(1, n_sat):
                coverage_vec = np.maximum(coverage_vec, self.sat_data[q][s])
                num_sat_vec = num_sat_vec + self.sat_data[q][s]

            tot_coverage = np.sum(coverage_vec) / len(coverage_vec)

            vis_times = np.sum(num_sat_vec != 0)

            if vis_times != 0:
                avg_num_vis = np.sum(num_sat_vec) / (n_sat * vis_times)
            else:
                avg_num_vis = 0

            blue_fit[0, (2*s):(2*s+2)] = np.array([tot_coverage, avg_num_vis])

        return(blue_fit)

class RedConst(Constellation):

    def __init__(self, in_sats, in_blue_const:BlueConst, type="Random"):
        super().__init__(in_sats, type)
        self.blue_const = in_blue_const

    def get_red_fitness(self):
        n_blue = len(self.blue_const.sat_data)
        n_red = len(self.sat_data) # The number of satellites
        n_sites = len(Constellation.site_locs)

        red_fit = np.zeros((1, 2 * n_sites))
        for s in range(n_sites):
            
            coverage_vec = self.sat_data[0][s]
            num_sat_vec = self.sat_data[0][s]

            # Get the blue constellation coverage vector, a vector of boolean values
            blue_coverage = self.blue_const.sat_data[0][s]
            for q in range(1, n_blue):
                blue_coverage = np.maximum(blue_coverage, self.blue_const.sat_data[q][s])

            for q in range(1, n_red):
                coverage_vec = np.maximum(coverage_vec, self.sat_data[q][s])
                num_sat_vec = num_sat_vec + self.sat_data[q][s]
            
            coverage_vec[np.logical_not(blue_coverage.astype(bool))] = 0
            num_sat_vec[np.logical_not(blue_coverage.astype(bool))] = 0

            vis_times = np.sum(num_sat_vec != 0)

            tot_coverage = np.sum(coverage_vec) / np.sum(blue_coverage)

            if vis_times != 0:
                avg_num_vis = np.sum(num_sat_vec) / (n_red * vis_times)
            else:
                avg_num_vis = 0

            red_fit[0, (2*s):(2*s+2)] = np.array([tot_coverage, avg_num_vis])
        
        return red_fit
                















    







