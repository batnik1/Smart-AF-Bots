# Smart-AF-Bots
# Warehouse Simulation Project

## Introduction

The main goal of this project is to simulate autonomous warehouse robots, to improve the delivery times of a wide array of items. This is accomplished by simulating tasks such as efficient order retrieval, sorting, and stacking of stocks, alongside the transport of parcels within the warehouse, with proper collision avoidance and congestion control.

The project offers significant cost-saving and efficiency benefits, with a fully automated warehouse predicted to hold 50% more stock, deliver three times faster, and reduce overall fulfillment cost by 40%.

The challenges faced in this project include optimal allocation of worker bots, collision avoidance, congestion management and scalability.

## Applications of Warehouse Simulation

The warehouse simulation software offers various benefits:

- Reduction of overall fulfilment costs
- Faster service delivery
- Less error-prone systems 
- Modeling for improvement of real-life efficiency

## Warehouse Simulator

This project includes a scalable simulator that allows users to generate random orders, decide the frequency of new items being delivered to the warehouse, simulate the actions of warehouse bots, and stop the simulation at any time for debugging. It is compatible with any OS that can run Python3 and MongoDB.

## Objectives

- Fair allocation of orders to robots.
- Prevention of collisions between bots.
- Avoiding deadlocks and livelocks.
- Proper congestion management.

## Phases of Simulation

There are three main phases to the simulation: the stacking phase, the rack to human counter phase, and the sorting phase. Each phase has a designated type of bot to manage different tasks.

## Intersection Management

Intersection Management was implemented to handle the intersection of bots in the warehouse. This was done by moving from a discrete system to a continuous one, introducing a "booking" mechanism for intersections, and designing different schemes for intersection management.

## Future Work

To improve the warehouse simulation, the project plans to introduce order pickup schemes, improve intersection management, and make the simulator more robust overall. 

## Running the Simulation
Clone this repo and after installing pygame and mongodb on your system run the comand "python window.py"


The paper was submitted at IEEE CASE'2022 held at Mexico.
