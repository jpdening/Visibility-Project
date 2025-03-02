from pathlib import Path
import pandas as pd
import numpy as np

class Constellation():

    ## Class attributes
    # Default variables
    T_f = 192.0
    dt = 30.0
    alpha = 30

    # Variables to be filled with read_types
    root_path = 0
    site_dict = {}
    orbit_types = []

    # Variables to be filled with get_site_locs
    site_locs = []
    
    # The constructor must take in a list of tuples
    def __init__(self, in_sats):

        # Check that in_sats is of the proper shape. It should be a list of lists
        proper_len = True
        for ii in range(len(in_sats)):
            if len(in_sats[ii]) != 2:
                proper_len = False
                break
        
        if not proper_len:
            raise Exception("Please ensure that all satellites are composed of orbit_type and phasing string pairs")

        if len(Constellation.site_dict) == 0:
            raise Exception("Please call Constellation.read_types first")

        # Add all of the satellites
        self.add_satellites(in_sats)

    # This method overwrites all of the satellites present in the constellation, and then computes the data associated with them
    def add_satellites(self, in_sats):
        self.sats = in_sats
        self.sat_data = []
        for s in range(len(self.sats)):
            self.sat_data.append(Constellation.get_visibility_data(self.sats[s]))

    # The class method must return the visibility data associated with a given satellite
    @classmethod
    def get_visibility_data(cls, in_sat):

        # in_sat is expected to be a list of the form ["orbit_type, "phasing"]

        # We need the visibility arrays for all of the site locations for the given satellite. 
        # These visibility arrays will be stored in tuples

        # Throw an error if there are no site locations listed
        if len(cls.site_locs) == 0:
            raise Exception("Please use get_site_locs to enter at least one site location before calling this")
        
        # Throw an error if the path is not declared yet
        if cls.root_path == 0:
            raise Exception("Please use read_types to enter the root path")

        # Check that the orbit type is valid
        if in_sat[0] not in cls.orbit_types:
            raise Exception("Please use one of the correct orbit types. Refer to the CLPSSitesRandomSats directory for valid types")

        # Read in the phasing. Correct to 0.1 if it is 0 to agree with pandas renaming convention
        phasing = in_sat[1]
        if phasing == "0":
            phasing = "0.1"

        vis_store = []
        for s in cls.site_locs:
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

    # The class method must take in the site locations used
    @classmethod
    def get_site_locs(cls, in_site_locs):

        if len(cls.site_dict) == 0:
            raise Exception("Please call Constellation.read_types first")

        if max(in_site_locs) > len(cls.site_dict) or min(in_site_locs) < 1:
            raise Exception("Invalid index for a site location. Please choose again")

        cls.site_locs = in_site_locs

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


# Make a derived class "BlueConst"

class BlueConst(Constellation):

    def __init__(self, in_sats):
        super().__init__(in_sats)

    # This will output a 
    def get_blue_fitness(self):

        n_sat = len(self.sats) # The number of satellites
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

    def __init__(self, in_sats, in_blue_const:BlueConst):
        super().__init__(in_sats)
        self.blue_const = in_blue_const

    def get_red_fitness(self):
        n_blue = len(self.blue_const.sats)
        n_red = len(self.sats) # The number of satellites
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
                















    







