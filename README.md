# Traffic-Lights-Simulation

Simulating a T-Junction traffic lights as seen below. The two roads
will lead to a one-way flow of vehicles.

![Image](images/T-junction.png?raw=true "T-Junction")

## Prerequisites

The inter-arrival time between cars will follow a exponential distribution
with λ = 2 with a lower and upper bound of 1 and 10 respectively. The duty cycles
for both traffic lights are the same and the cycle changes every 30 seconds.
Only 1 traffic light can be green at a time. A car can pass when the traffic light is
green and there are no other cars in front of it and will have
a service time of 2 seconds. There will be 2 simulations, one at morning and one at evening.
Both follow Gaussian distributions and the parameters are as follows:

* Morning, road A: μ = 8:30 am and σ = 1 hour.
* Morning, road B: μ = 9:00 am and σ = 0.95 hour.
* Evening, road A: μ = 6:00 pm and σ = 0.95 hour.
* Evening, road B: μ = 5:30 pm and σ = 1 hour.

The exponentially distributed inter-arrival time therefore has to be modulated (divided) by the
Gaussian probability density function depending on the time of day.

## Design