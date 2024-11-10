These folders contain data for several different simulation scenarios. The names of the folders denote the observation cone half-angle (alpha), the lunar latitude (phi) and the lunar longitude (lambda). Lambda is measured with respect to the dark side of the moon, so 
phi = 0
lambda = 0
corresponds to a location on the equator in the center of the dark side, and 
phi = 0
lambda = 180
corresponds to a location on the equator in the center of the near side. The observation cone is assumed to radiate perpendicularly from the surface of the moon.

Each folder contains .csv files for several different orbit/trajectory types, including LLOs, Halo orbits, Lyapunov orbits, and DROs. Each should include a .txt file called "all_data_labels.txt". This is not strictly necessary for the scheduling optimization, but it is necessary for reproducing each trajectory. 

All of the .csv files should look the same. For a given trajectory, the satellite in question can start at any angle along the trajectory between 0 and 360 degrees; this is denoted the phase angle, or true anomaly for Keplerian orbits. The phase was discretized into 20 degree increments. These different phasings were put here to mix and match with different orbits, as some phasings will undoubtedly be more interesting given this time frame. ** In the first row of each .csv, the phase is readily seen. The time in minutes is shown on the first column**. **Currently, 10 hours were simulated for all orbits. This can be lengthened in the future.** 

The data in the body of the .csv files is pretty simple. It's just binary values, with a '1' signaling that a satellite is within the observation cone, and a '0' signalling that a satellite is outside of the observation cone. 

# New Changes
The .csv files reserved for each orbit are replaced by folders. Each folder now contains two .csv files entitled "earth_detection.csv" and "site_detection.csv". In the same manner as the old files, these document the instances when an event was detected. For the site_detection files, detections are the site detecting the satellite. For the earth_detection files, detections are the satellite being able to see the earth.

In addition, two new files, "earth_visibility_percentages.csv" and "site_visibility_percentages.csv" were added. These document the percentage of the total sampled times that certain visibility conditions were met. For earth_visibility_percentages, this is the percentage of time that the earth is visible from the satellite, and for site_visibility_percentages this is the percentage of time the satellite is visible from the lunar ground site.

# New Changes, 7-30-2024
The position data was updated to account for the multiple phasings. New sub-folders (Example, Position_Data/LLO_1) were created. Each stores different files with position data sampled every 1 minute (dt = 1 minute), with these orbits propagated for one period from their initial phasing. Inside each sub-folder, a time vector is stored that is associated with all phasings in that folder. All times are in minutes.


# New Changes, 11-10-2024
A new folder named "AllConstellations" has been added. This folder has sets of matched red and blue constellations, along with their targeted ground sites.

### ./AllConstellations/(n_blue, n_red, num. sites)
The first level down in the file hierarchy has folders of the form (n_blue, n_red, num. sites), where 
n_blue is the number of blue satellites,
n_red is the number of red satellites, and 
num. sites is the number of ground sites on the moon.

Also at this level is a file called "site_locations_key.xls". This gives a list of possible ground station indices, paired with their names, and the phi-lambda pairs. The possible ground sites are a combination of CLPS ground site locations and ground sites for some international space programs targeted at the moon.

1. IM-1
2. IM-2
3. IM-3
4. Griffin Mission 1
5. Draper Series 2
6. Blue Ghost Mission 1
7. Astrobotic Peregrine Mission 1
8. Chang'e 5

### ./AllConstellations/(n_blue, n_red, num. sites)/T_fin_##_dt_##_site_locs_(##)
One hierarchy level down from this has folders of the form "T_fin_##_dt_##_site_locs_(##)". T_fin is the length of the simulation in hours, dt is the constant sampling interval in minutes, and the site_locs, are a list of 2-tuples of the form (site index, alpha), where alpha is the half angle of the observation cone.

### ./AllConstellations/(n_blue, n_red, num. sites)/T_fin_##_dt_##_site_locs_(##)/COLOR
Inside these folders will be two folders entitled "RED" and "BLUE". Each will have the same internal composition. There will be a list of folders of the form "const_#", with each folder linked to a RED or a BLUE constellation, depending which folder it is inside. **NOTE: RED/const_1 and BLUE/const_1 should be used together, as with each successive index. The red constellation was optimized to match this blue constellation, and ONLY this blue constellation.**

Aside from these "const_#" folders, there will be two .xls files in "RED" and "BLUE". These are "constellation_data.xls" and "problem_data.xls". "constellation_data.xls" has the statistics for each constellation. This includes the total visibility for each site, and the load balancing for each site. 

**Total Visibility - This is a measure of how good a constellation is at receiving signals from a ground site. For blue constellations, this is just the percentage of time that at least one member of the blue constellation is in view of that particular ground site. For red constellations, this is the percentage of time that the red constellation could intercept a signal sent from that ground station to the blue constellation**

**Load balancing - This is a measure of how much work the satellites are sharing in terms of accomplishing their goal. A very low load balancing score means that one or more satellites are performing very poorly compared to the other satellites, whereas a high load balancing score means that the satellites have similar performance**

The "problem_data.xls" file has the information on what the phi, lambda, and alpha of each ground station is. It also has the number of satellites in each constellation (for either BLUE or RED), as well as the total simulation time in hours, and the sampling rate in minutes.

### ./AllConstellations/(n_blue, n_red, num. sites)/T_fin_##_dt_##_site_locs_(##)/COLOR/const_#
Inside each "const_#" folder are folders "sat_#" for each satellite in that constellation, as well as a file entitled "satellite_data.xls". "satellite_data.xls" has information about each satellite, including their orbit type, initial condition, period, phasing, earth visibility, and the site percentages for each site.

### ./AllConstellations/(n_blue, n_red, num. sites)/T_fin_##_dt_##_site_locs_(##)/COLOR/const_#/sat_#
Inside each "sat_#" file are "earth_detection.csv", "site_detection.csv", and "position_data.csv". For "site_detection.csv", the first column is the time in minutes since the start of the simulation. The next columns have the visibility of the current satellite to each ground station. The first column after the time column corresponds to "site 1", the next to "site 2", etc.

For "earth_detection.csv", there are only two columns, with the first being the time column and the second being detections to Earth.

For "position_data.csv", these are the positions relative to the center of the Earth in a rotating synodic frame. All positions start at the chosen phasing and go for one period of the orbit. The time column has an increment of one minute. The next three columns correspond to the x, y, and z positions respectively.


