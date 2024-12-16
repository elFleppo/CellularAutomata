import numpy as np

def euclidian_distance(cellAgent, cellTarget):
    x1, y1 = cellAgent
    x2, y2 = cellTarget
    sum = (y1-x1)^2+(y2-x2)^2
    if sum >= 0:
        result = np.sqrt(sum)
        return result
    else:
        return print("Error - negative value under square root")
