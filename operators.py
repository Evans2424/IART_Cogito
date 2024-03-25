# TODO: define operations for each level. They are currently all the same
# delta represents the type of move
operations = [
    {                       # Level 1
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0,
        "ignoreButtons": []
    },
    {                       # Level 2
        "ownDir": 2,
        "perpDir": 0,
        "delta": 0,
        "ignoreButtons": []
    },
    {                       # Level 3
        "ownDir": 0,
        "perpDir": 1,
        "delta": 0,
        "ignoreButtons": []
    },
    {                       # Level 4
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0,
        "ignoreButtons": [(3,1),(3,2),(1,1),(1,2),(3,6),(1,6),(2,2),(2,6),(0,6),(0,2)]
    },
    {                       # Level 5
        "ownDir": -1,
        "perpDir": 0,
        "delta": 0,
        "ignoreButtons": []
    },
    {                       # Level 6
        "ownDir": -1,
        "perpDir": 0,
        "delta": 1,
        "ignoreButtons": []
    },
    {                       # Level 7
        "ownDir": 1,
        "perpDir": 0,
        "delta": 2,
        "ignoreButtons": []
    },
    {                       # Level 8
        "ownDir": 1,
        "perpDir": 1,
        "delta": 3,
        "ignoreButtons": []
    },
    {                       # Level 9
        "ownDir": 1,
        "perpDir": 0,
        "delta": 4,
        "ignoreButtons": []
    },
    {                       # Level 10 
        "ownDir": 1,
        "perpDir": 1,
        "delta": 3,
        "ignoreButtons": [(3,1),(3,2),(1,1),(1,2),(3,6),(1,6),(2,2),(2,6),(0,6),(0,2)]
    },
    {                       # Level 11
        "ownDir": 1,
        "perpDir": 0,
        "delta": 5,
        "ignoreButtons": []
    },
    {                       # Level 12
        "ownDir": 1,
        "perpDir": 0,
        "delta": 6,
        "ignoreButtons": []
    }
]


def getOperation(level):
    return operations[level%12]