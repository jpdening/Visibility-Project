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

*******************New Changes***********************************
The .csv files reserved for each orbit are replaced by folders. Each folder now contains two .csv files entitled "earth_detection.csv" and "site_detection.csv". In the same manner as the old files, these document the instances when an event was detected. For the site_detection files, detections are the site detecting the satellite. For the earth_detection files, detections are the satellite being able to see the earth.

In addition, two new files, "earth_visibility_percentages.csv" and "site_visibility_percentages.csv" were added. These document the percentage of the total sampled times that certain visibility conditions were met. For earth_visibility_percentages, this is the percentage of time that the earth is visible from the satellite, and for site_visibility_percentages this is the percentage of time the satellite is visible from the lunar ground site.

********************************New Changes, 7-30-2024********************************
The position data was updated to account for the multiple phasings. New sub-folders (Example, Position_Data/LLO_1) were created. Each stores different files with position data sampled every 1 minute (dt = 1 minute), with these orbits propagated for one period from their initial phasing. Inside each sub-folder, a time vector is stored that is associated with all phasings in that folder.
