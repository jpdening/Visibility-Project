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

