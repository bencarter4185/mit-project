# mit_project
Repository for code related to our 4th year project in Magnetic Induction Tomography, modelling the forward and inverse problems. Currently working on a Biot-Savart solver in lieu of tackling the forward problem.

## Table of Contents
- [mit_project](#mit_project)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
    - [Modules](#modules)
  - [To Do](#to-do)

## Requirements
Python 3.10 or higher

### Modules
numpy, matplotlib, scipy

## To Do
- [x] Ascertain whether discretizing/chunking the wires is strictly necessary for square loops.
  - **Done.** Wire discretization unnecessary for circular current loops, but necessary for square loops.
- [x] Compare the accuracy of the Biot-Savart solver in a test vs. a known analytical solution. (Circular loop as analytical solutions for square loops can be hard to come by)
  - **Done.** Completed for both square and circular loops. Code can be found in:
```
mit_project
|
└───modules
    |
    └───tests
        |
        └───validation tests
            |    circular_loop_validation.py
            |    square_loop_validation.py
```
- [x] Implement a smarter discretization than taking the midpoints of each discretized segment. (Simpson's Rule?)
  - **Not implemented.** Currently not seen as necessary given the sufficient accuracy of the solver using the midpoint rule. 
- [x] Write a configparser to parse a "parameters.txt" or "config.txt" file. Code should then accept some parameters for square/circular loops etc. and create the requisite Wire objects; performing Biot-Savart calculations for a given set of points. 
  - **Done.** Implemented config in JSON files, parsing them to dictionaries. Documentation/lab book stuff to follow.
- [ ] Implement a Biot-Savart solver for multiple coils/wires at once.
- [ ] Improve documentation on how the code works/update lab book as necessary.
- [ ] Write some more unit tests:
  - [ ] Test for Wire object creation
  - [ ] Test for Biot-Savart calculations
- [ ] Write an end-to-end simulation which makes a ring of circular coils (maybe 8 at first) all surrounding the origin in the x-y plane. Write some logic to plot a 2d colourmap/surface plot to show areas of high and low magnetic field, B. 