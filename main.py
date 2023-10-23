from probeinterface.plotting import plot_probe, plot_probe_group
from probeinterface import read_probeinterface
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from map_utils import *

# %% Plot probe with electrode ids
# Electrode 66 isn't used
plot_probe_with_electrode_ids()

# %% Plot flex cable with ids
plot_flex_cable_ids()
electrode_to_flex, electrode_to_sg_chs = map_electrode_ids_to_flex_cable_ids()
sorted_flex_ids = sort_electrode_ids_by_flex_cable_pos(electrode_to_flex)
plot_flex_cable_ids(label_ids=sorted_flex_ids,
                    title="Flex Cable with Electrode IDs")

# %% Plot ZIF connectors with ids
''' 
Each hardware stage section plots three figures: 
    1. Plot with positional ids (ids based on position)
    2. Plot with previous stage ids
    3. Plot with electrode ids
'''
# 1
plot_ZIF_ids()

# 2
sorted_flex_ids_by_ZIF = sort_flex_ids_by_ZIF_pos()
plot_ZIF_ids(label_ids=sorted_flex_ids_by_ZIF,
             title="ZIF Connectors with Flex Cable IDs")

# 3 (construct dictionary that maps electrode ID to this hardware stage ids)
_, _, flex_to_ZIF = map_flex_cable_to_ZIF()
electrode_to_ZIF = {
    key: flex_to_ZIF[electrode_to_flex[key]] for key in electrode_to_flex}
sorted_electrode_ids_by_ZIF = sort_electrode_ids_by_ZIF_pos(
    electrode_to_ZIF)
plot_ZIF_ids(label_ids=sorted_electrode_ids_by_ZIF,
             title="ZIF Connectors with Electrode IDs")


# %% Plot samtec connectors with ids

# L corresponds to left ZIF or zif1
# R corresponds to right ZIF or zif2
plot_samtec_ids()

ZIF_to_samtec = map_ZIF_to_samtec()
sorted_ZIF_ids_by_samtec = sort_ZIF_ids_by_samtec_pos(ZIF_to_samtec)
plot_samtec_ids(label_ids=sorted_ZIF_ids_by_samtec,
                title="Samtec Connectors with ZIF IDs")

electrode_to_samtec = {
    key: ZIF_to_samtec[flex_to_ZIF[electrode_to_flex[key]]] for key in electrode_to_flex}
sorted_electrode_ids_by_samtec = sort_electrode_ids_by_samtec_pos(
    electrode_to_samtec)
plot_samtec_ids(label_ids=sorted_electrode_ids_by_samtec,
                title="Samtec Connectors with Electrode IDs")

# %% Plot Ripple front ends with ids

# Ripple FE ids 1-4 from left to right
# ST3 on design file corresponds to FE1 and ST2 to FE4
plot_ripple_ids(title='Ripple FE Positional and Channel IDs')

samtec_to_ripple = map_samtec_to_ripple()
sorted_samtec_ids_by_ripple = sort_samtec_ids_by_ripple_pos(samtec_to_ripple)
plot_ripple_ids(label_ids=sorted_samtec_ids_by_ripple,
                title="Ripple Front Ends with Samtec IDs")

electrode_to_ripple = {
    key: samtec_to_ripple[ZIF_to_samtec[flex_to_ZIF[electrode_to_flex[key]]]] for key in electrode_to_flex}
sorted_electrode_ids_by_ripple = sort_electrode_ids_by_ripple_pos(
    electrode_to_ripple)
plot_ripple_ids(label_ids=sorted_electrode_ids_by_ripple,
                title="Ripple Front Ends with Electrode IDs")

# %% Plot probe with Ripple channels

dict_vals = list(electrode_to_ripple.values())
dict_vals.insert(65, 'nan')
plot_probe_with_electrode_ids(dict_vals)

# %% Map functions
ripple_to_electrode = {value: key for key,
                       value in electrode_to_ripple.items()}


def map_electrode_to_ripple(elec_id):
    return electrode_to_ripple[elec_id]


def map_ripple_to_electrode(ripple_id):
    return ripple_to_electrode[ripple_id]


print(f'Electrode ID 1 maps to Ripple channel {map_electrode_to_ripple(1)}')
print(f'Ripple channel 1 maps to electrode ID {map_ripple_to_electrode(1)}')

# %% Plot probeinterface figures (later used in spikeinterface)

# left has electrode IDs
# right has Ripple channels

fig, ax = plt.subplots(figsize=(5, 8))
pi = read_probeinterface('NET-EBL-1-128.json')  # load from json file
probe = pi.probes[0]
plot_probe(probe, ax, with_contact_id=True, with_device_index=False)
probe2 = probe
probe2.move([300, 0])
plot_probe(probe2, ax, with_contact_id=False, with_device_index=True)
ax.set_xlim(-150, 500)
ax.set_ylim(-150, 2100)

plt.tight_layout()
plt.show()
