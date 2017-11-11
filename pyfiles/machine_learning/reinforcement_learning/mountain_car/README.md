# Mountain Car problem

## Training
```
python <filename>.py train
```

## Test
```
python <filename>.py test <modelname>.json <weightname>.hdf5
```

## Environment
### Observation
Type: Continuous

Num | Observation  | Min  | Max
----|--------------|------|----
0   | position     | -1.2 | 0.6
1   | velocity     | -0.07| 0.07

## Actions
Type: Discrete

Num | Action 
----|-------------
0   | push left 
1   | no push
2   | push right

