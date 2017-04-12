# Monte Carlo Method
Monte Carlo Method is a broad class of computationl algorithm that relies on random sampling to obtained numerical results. Often use to compute physical and mathematical problems.
This is method is often used in three problem classes:
* optimization
* numerical integration
* generating draws from a probability distribution
Monte Carlo Localization (MCL) is used in robotics to determine the position of the robot.

## Method
Monte Carlo generally follows the pattern below (though in some cases it may differ):
1. Define domain of possible inputs
2. Generate input randomly from a probability distribution over the domain (more inputs mean high accuracy)
3. Perform deterministic computation on the input
4. Aggregate the result
Generally it gives the ratio
```
ratio = (no. chosen input)/(no. of total input)
```

## Example
The following example tries to find the area of a circle with radius of one (obviously its 3.141).
1. cut the circle into 4
2. in box of area 1, we have quater of a circle inscribe to it
3. the function of the ark would be x^2+y^2
4. we give random n coordinate but only consider the coordinate within the function in 3.
We get the ratio,  then multiple that by 4 (since its only a quater of a circle) to get the area of the circle
