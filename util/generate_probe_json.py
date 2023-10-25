import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from probeinterface import Probe
from probeinterface.plotting import plot_probe
from probeinterface import generate_multi_columns_probe
from probeinterface import write_probeinterface

channel_map_df = pd.read_csv('channel_map.csv')
df = channel_map_df.drop(65)
n = 128
positions = np.zeros((n,2))
for i in range(n):
    x = df['X, um'].iloc[i]
    y = df['Y, um'].iloc[i]
    positions[i] = x, y
    
    
probe = Probe(ndim=2, si_units='um')
probe.set_contacts(positions=positions, shapes='circle', shape_params={'radius': 10})


height = 2050
left = -50
right = 50
mid_x = 0
depth = -10
max_depth = -60

polygon = [(left, depth), (mid_x, max_depth), (right, depth), (right, height), (left, height)]
probe.set_planar_contour(polygon)
fig, ax = plt.subplots(figsize=(5, 8))

electrode_ids = np.concatenate((np.arange(1,66), np.arange(67,130)))
ripple_ids = list(electrode_to_ripple.values())
probe.set_contact_ids(electrode_ids) # contact ids
probe.set_device_channel_indices(ripple_ids) # device channel ids
write_probeinterface('NET-EBL-1-128.json', probe)

plot_probe(probe, ax, with_contact_id=True, with_device_index=False)
plot_probe(probe, ax, with_channel_index=True)
probe2 = probe
probe2.move([300, 0])
plot_probe(probe2, ax, with_contact_id=False, with_device_index=True)
ax.set_xlim(-150, 500)
ax.set_ylim(-150, 2100)

plt.tight_layout()

probe.annotate(name='NET-EBL-1-128', manufacturer='xieluanlabs', first_index=1)

df = probe.to_dataframe()
df

