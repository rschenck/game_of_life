import json

settings_json = json.dumps([
    {'type': 'title',
    'title': 'Customize your cellular automata'},
    {
    'type': 'scrolloptions',
    'title': 'Speed of game',
    'desc': 'Adjust the speed of the game in seconds. (Default = 0.1)',
    'section': 'initiate',
    'key': 'Speed',
    'options': ['0.0','0.01','0.02','0.03','0.04','0.05','0.06','0.07','0.08','0.09','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1']
    },
    {
    'type': 'scrolloptions',
    'title': 'Death: Lonely',
    'desc': 'Adjust conditions by which a cell dies by loneliness (0 to selected value). (Default is 0-1)',
    'section': 'initiate',
    'key': 'Lonely',
    'options': ['0','1','2','3','4','5','6','7','8','9']
    },
    {
    'type': 'scrolloptions',
    'title': 'Death: Overcrowded',
    'desc': 'Adjust conditions by which a cell dies by overcrowdedness (selected value to 7). (Default is 4-7)',
    'section': 'initiate',
    'key': 'Crowded',
    'options': ['0','1','2','3','4','5','6','7','8','9']
    },
    {
    'type': 'scrolloptions',
    'title': 'Birth',
    'desc': 'Adjust conditions for a new cell to be born (Set value). (Default is 3)',
    'section': 'initiate',
    'key': 'Born',
    'options': ['0','1','2','3','4','5','6','7','8','9']
    },
    {
    'type': 'scrolloptions',
    'title': 'Color',
    'desc': 'Pick the color of the cells!',
    'section': 'initiate',
    'key': 'Color',
    'options': ['White','Red','Blue','Green','Random']
    },
    {
    'type': 'bool',
    'title': 'Music',
    'desc': '',
    'section': 'initiate',
    'key': 'Music',
    },
    # {
    # 'type': 'bool',
    # 'title': 'Sound',
    # 'desc': '',
    # 'section': 'initiate',
    # 'key': 'Sound',
    # }
    ])
