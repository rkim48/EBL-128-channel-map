# EBL-128-channel-map

## About
This repository contains scripts to visualize the channel mapping of a Single shank 128-channel EBL device from Xie-Luan labs through various hardware stages including the flex cable, ZIF connectors, Samtec connectors, and Ripple micro front ends, via a custom 128-channel adapter board. Each hardware stage section plots three figures: a plot with positional ids, a plot with previous stage ids, and a plot with electrode ids. 
The source files directory contains initial files which were used to construct the mapping.  

## Example
<img src="./example%20images/probe.png" width="40%" /> <img src="./example%20images/ripple_FE.png" width="40%" />

## Usage
1. Clone this repository and navigate to its directory.
2. Execute main.py to generate the plots for each hardware stage.

## Probe Interface Visualization
The script also contains a section for generating a probeinterface visualization and .json file for future use with spikeinterface package. Ensure probeinterface library is installed. 
