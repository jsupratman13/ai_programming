# LunarLander Continuous problem

## Training
```
python ddpg.py train
```

## Testing
```
python ddpg.py test <modelname>.json <weightname>.hdf5
```

## Environment
### Observation
Type: Continuous

Num | Observation | Min | Max
----|-------------|-----|----
0   | x position  | inf | -inf
1   | y position  | inf | -inf
2   | x velocity  | inf | -inf
3   | y velocity  | inf | -inf
4   | angle       | inf | -inf
5   | rotation    | inf | -inf
6   | left leg    | inf | -inf
7   | right leg   | inf | -inf

### Actions
Type: Continuous

Num | Observation | Min | Max
----|-------------|-----|----
0   | left engine | 1.0 | -1.0
1   | right engine| 1.0 | -1.0

