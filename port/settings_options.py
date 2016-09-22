import json

settings_json = json.dumps([
	{'type': 'title',
	'title': 'Customize your cellular automata'},
	{
	'type': 'numeric',
	'title': 'Speed of game',
	'desc': 'Adjust the speed of the game in seconds. (Default = 0.1)',
	'section': 'initiate',
	'key': 'Speed'
	},
	{
	'type': 'numeric',
	'title': 'Death: Lonely',
	'desc': 'Adjust conditions by which a cell dies by loneliness (0 to selected value). (Default is 0-1)',
	'section': 'initiate',
	'key': 'Lonely'
	},
	{
	'type': 'numeric',
	'title': 'Death: Overcrowded',
	'desc': 'Adjust conditions by which a cell dies by overcrowdedness (selected value to 7). (Default is 4-7)',
	'section': 'initiate',
	'key': 'Crowded'
	},
	{
	'type': 'numeric',
	'title': 'Sustain Cell 1',
	'desc': 'Adjust conditions for cell to stay alive (Range from Sustain Cell 1 to Sustain Cell 2). (Default is 2-3)',
	'section': 'initiate',
	'key': 'Lives1'
	},
	{
	'type': 'numeric',
	'title': 'Sustain Cell 2',
	'desc': 'Adjust conditions for cell to stay alive (Range from Sustain Cell 1 to Sustain Cell 2). (Default is 2-3)',
	'section': 'initiate',
	'key': 'Lives2'
	},
	{
	'type': 'numeric',
	'title': 'Birth',
	'desc': 'Adjust conditions for a new cell to be born (Set value). (Default is 3)',
	'section': 'initiate',
	'key': 'Born'
	},
	{
	'type': 'options',
	'title': 'Color',
	'desc': 'Pick the color of the cells!',
	'section': 'initiate',
	'key': 'Color',
	'options': ['White','Red','Blue','Green','Random']
	},
	{
	'type': 'options',
	'title': 'Grid Color',
	'desc': 'Pick the color of the grid!',
	'section': 'initiate',
	'key': 'GridColor',
	'options': ['Grey','White','Red','Blue','Green','Random']
	},
	{
	'type': 'bool',
	'title': 'Music',
	'desc': '',
	'section': 'initiate',
	'key': 'Music',
	},
	{
	'type': 'bool',
	'title': 'Sound',
	'desc': '',
	'section': 'initiate',
	'key': 'Sound',
	}
	])
