# Cartpole problem

## Training
```
python pdnddqn.py train
```

## Test
```
python pdnddqn.py test <modelname>.json <weightname>.hdf5
```

## Environment
### Observation
Type: Continuous 

Num | Observation | Min | Max
---|---|---|---
0 | Cart Position | -2.4 | 2.4
1 | Cart Velocity | -Inf | Inf
2 | Pole Angle | ~ -41.8&deg; | ~ 41.8&deg;
3 | Pole Velocity At Tip | -Inf | Inf

### Actions
Type: Discrete

Num | Action
--- | ---
0 | Push cart to the left
1 | Push cart to the right

