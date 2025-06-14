﻿# Grocery Store Shelf Optimization Using Genetic Algorithms

## Overview
This project implements a genetic algorithm (GA) to solve the problem of optimizing product placement on grocery store shelves. The algorithm considers multiple constraints such as shelf capacity, refrigeration for perishable goods, hazardous zones, heavy item placement for restocking efficiency, and high-demand/promotional item visibility. The optimized shelf allocation is exported to an Excel file for visualization and further analysis.

## Features
- **Constraint Handling:**
  - Shelf capacity limits
  - Refrigeration requirements for perishable products
  - Hazardous product segregation
  - Restocking efficiency for heavy items
  - High-demand, discounted, and promotional product placement in high-visibility zones
  - Complementary product grouping and category segmentation
- **Genetic Algorithm:**
  - Random population initialization
  - Tournament selection, single-point crossover, and mutation operators
  - Fitness function that penalizes constraint violations
- **Output:**
  - Optimized shelf allocation with details (shelf ID, shelf name, assigned product IDs/names, and total weight per shelf)
  - Excel file export for further analysis

## Requirements
- Python 3.x
- [pandas](https://pandas.pydata.org/)
