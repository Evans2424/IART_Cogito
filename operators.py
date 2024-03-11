# TODO: define operations for each level. They are currently all the same

operations = [
    {                       # Level 1
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 2
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 3
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 4
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 5
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 6
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 7
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 8
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 9
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 10
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 11
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    },
    {                       # Level 12
        "ownDir": 1,
        "perpDir": 0,
        "delta": 0
    }
]


def getOperation(level):
    return operations[level%12]