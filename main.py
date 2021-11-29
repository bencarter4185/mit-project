"""
Initial basic Python code for modelling the Biot-Savart law for a loop of wire

At first I'm going to use external code as 'inspiration' before moving on to write my own implementation if appropriate.

As it stands now this repository is simply a testbed for the Biot-Savart code found at https://github.com/vuthalab/biot-savart, with all rights going to Mingde Yin and Ryan Zazo
"""

"""
This is the `Helmholtz Coils` example as shown in https://github.com/vuthalab/biot-savart#helmholtz-coils
"""

import biot_savart_v4_3 as bs

bs.helmholtz_coils("helm1.txt", "helm2.txt", 50, 5, 2, 1)
# makes a pair of helmholtz coils
# 50 segments each, with radius of 5 cm
# spaced out by 2 cm, located at z = +/- 1 respectively
# 1 amp of current

bs.plot_coil("helm1.txt", "helm2.txt")

bs.write_target_volume("helm1.txt", "targetvol1", (10, 10, 10), (-5, -5, -5), 0.5, 0.5)
bs.write_target_volume("helm2.txt", "targetvol2", (10, 10, 10), (-5, -5, -5), 0.5, 0.5)
# use a target volume of size 10, centred about origin

h1 = bs.read_target_volume("targetvol1")
h2 = bs.read_target_volume("targetvol2")
# produce the target volumes we want

# use linear superposition of magnetic fields, to get the combined effects of multiple coils
h_total = h1 + h2

bs.plot_fields(h_total, (10, 10, 10), (-5, -5, -5), 0.5, which_plane='z', level=0, num_contours=50)