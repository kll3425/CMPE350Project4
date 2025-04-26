# CMPE350 Cache Simulator - Project 4

## Overview
This project simulates a cache memory system using Direct Mapping (DM) and Set Associative (SA) policies. It includes features like:
- Simulation of cache accesses
- Random, Locality, and Manual address generation
- LRU (Least Recently Used) replacement policy for Set Associative
- Hit and Miss tracking
- Graphical visualization of cache population using matplotlib

## Features
- **Random Simulation**: Random addresses from the whole address space.
- **Locality Simulation**: Addresses clustered around a base to simulate real program behavior.
- **Manual Simulation**: Enter specific word addresses by hand.
- **Direct Mapping and Set Associative**: Choose mapping policy at start.
- **LRU Replacement**: Automatically evicts the least recently used block when needed (extra credit).
- **Graphical Visualization**: Auto-generates a live bar graph showing cache population and hit rate (extra credit).

