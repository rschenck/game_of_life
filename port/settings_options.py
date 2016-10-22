import json

settings_json = json.dumps([
    {'type': 'title',
    'title': 'Customize your cellular automata'},
    {
    'type': 'bool',
    'title': 'Wrap-around',
    'desc': 'Cells leaving one side of the screen will immediately appear on the opposite side.',
    'section': 'initiate',
    'key': 'Wrap',
    },
    {
    'type': 'scrolloptions',
    'title': 'Speed of game',
    'desc': 'Adjust the speed of the game in seconds. (Default = Fast)',
    'section': 'initiate',
    'key': 'Speed',
    'options': ['Max Speed',
    'Very Fast',
    'Faster',
    'Fast',
    'Above Average',
    'Average',
    'Slow',
    'Slower',
    'Very Slow',
    'Min Speed']
    },
    {
    'type': 'scrolloptions',
    'title': 'Death: Lonely',
    'desc': 'Adjust conditions by which a cell dies by loneliness (0 to selected value). (Default is 0-1)',
    'section': 'initiate',
    'key': 'Lonely',
    'options': ['0','1','2','3','4','5','6','7','8']
    },
    {
    'type': 'scrolloptions',
    'title': 'Death: Overcrowded',
    'desc': 'Adjust conditions by which a cell dies by overcrowdedness (selected value to 7). (Default is 4-7)',
    'section': 'initiate',
    'key': 'Crowded',
    'options': ['0','1','2','3','4','5','6','7','8']
    },
    {
    'type': 'scrolloptions',
    'title': 'Birth',
    'desc': 'Adjust conditions for a new cell to be born (Set value). (Default is 3)',
    'section': 'initiate',
    'key': 'Born',
    'options': ['0','1','2','3','4','5','6','7','8']
    },
    {
    'type': 'scrolloptions',
    'title': 'Color',
    'desc': 'Pick the color of the cells!',
    'section': 'initiate',
    'key': 'Color',
    'options': ['Random','White','Red','Blue','Green','Yellow','Orange','Pink','Purple','Cyan']
    },
    {
    'type': 'bool',
    'title': 'Music',
    'desc': '',
    'section': 'initiate',
    'key': 'Music',
    }
    # {
    # 'type': 'bool',
    # 'title': 'Sound',
    # 'desc': '',
    # 'section': 'initiate',
    # 'key': 'Sound',
    # }
    ])
