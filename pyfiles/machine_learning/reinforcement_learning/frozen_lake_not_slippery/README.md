# Frozen Lake Not Slippery problem
Same thing as frozen lake but no noise, all action are deterministic

## Training
```
python <filename>.py train
```

## Testing
```
python <filename>.py test <filename>.npy
```
to view simulation
```
python <filename>.py test <filename>.npy render
```

## Environment
### Observation
Type: Discrete

Num | | | ||
----|-|-|-|-
_|0|1|2|3
_|4|5|6|7
_|8|9|10|11
_|12|13|14|15

Observation | | | | |
------------|-|-|-|-
_|S|F|F|F
_|F|H|F|H
_|F|F|F|H
_|H|F|F|G

### Actions
Type: Discrete

Num | Action
----|------------
0   | move left
1   | move down
2   | move right
3   | move up

