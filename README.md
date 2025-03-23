# Discrete Event Simulation
An Implementation of the Emergency Department Event Simulation process as described in Battu et al, 2022.

## What is a Discrete Event Simulation?

It refers to a technique to represent and study physical systems, involving varied entity interactions over time.

There are 3 specific elements of such a process - 

1. Simulation Objects : Mapping of real world objects.
2. Entities : Actors that perform specific events on specific simulation objects (depends on simulation to simulation).
3. Events : Refers to either actions that modify the status of a specific simulation object, or are responsible for scheduling future events (or actions).

## TLDR, paper summarised!

The paper describes a method by which they can linearly optimise the amount of resources required to improve patient TAT based on a 160 day simulation study conducted using SimPY and PuLP, which is then fed into a Multi-Linear Regression model. The output weights from the model are subject to a linear optimisation problem, subject to some pre-defined constraints.

## Credit : 
[1] *Battu, Anudeep, S. Venkataramanaiah, and R. Sridharan. "Patient Flow Optimization in an Emergency Department Using SimPy-Based Simulation Modeling and Analysis: A Case Study." In Applications of Computation in Mechanical Engineering: Select Proceedings of 3rd International Conference on Computing in Mechanical Engineering (ICCME 2021), pp. 271-280. Singapore: Springer Nature Singapore, 2022.*
[2] 





