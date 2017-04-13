# Utility Based System
Unlike the other AI, this AI architecture closely resembles human emotions. In concept, instead of switching states(action or task) based on environment triggers, the agent assesses the available states in their current environmnent and asssign a utility (benefits) for each states on a continous scale. The agent then execute the state with the the greatest utility.

## Utility Function
When assigning utility to different action, it is helpful to graph the function.
There are several type of function
* Step Function
* Linear Function
* Exponential Increase
* Logarithm Increase
* Exponential Decay
* Sigmoid Curve

## Multiple Variable
Most of the time, the utility of an action depends on two or more variables. In this case for utilities U1 and U2, combine them as follows: 
```
Utility = U1 - U2
```

## Example
For example we have a three action Attack, Heal, Reload with variable HP, Health and Bullet. Say for each action we have linear, sigmoid and exponential decay for utility function. 
```
enemy HP = 6 -> utility of attack = 40
health = 70 -> utility of healing = 10.9
bullet = 30 -> utility of reload = 9.48
the greatest utility is attack so agent will attack
therefore:
enemy HP = 6 -> utility of attack = 40
health = 70 -> utility of healing = 14
bullet = 10 -> utility of reload = 53.78
this time the greatest utility is reload so agent will reload
```
