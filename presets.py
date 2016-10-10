import random

def blank(gridDict):
    for item in gridDict:
        gridDict[item].stat = 0

def rando(gridDict):
    for item in gridDict:
        val = random.randint(0,1)
        gridDict[item].stat = val

def gun(gridDict):
    # far left four squares
    gridDict[390-300,200].stat = 1
    gridDict[400-300,200].stat = 1
    gridDict[390-300,210].stat = 1
    gridDict[400-300,210].stat = 1

    # middle left
    gridDict[470-300,210].stat = 1
    gridDict[470-300,220].stat = 1
    gridDict[480-300,220].stat = 1
    gridDict[480-300,200].stat = 1
    gridDict[490-300,200].stat = 1
    gridDict[490-300,210].stat = 1

    #middle-middle
    gridDict[550-300,220].stat = 1
    gridDict[550-300,230].stat = 1
    gridDict[550-300,240].stat = 1
    gridDict[560-300,220].stat = 1
    gridDict[570-300,230].stat = 1

    #middle-top
    gridDict[610-300,210-20].stat = 1
    gridDict[610-300,220-20].stat = 1
    gridDict[620-300,220-20].stat = 1
    gridDict[620-300,200-20].stat = 1
    gridDict[630-300,200-20].stat = 1
    gridDict[630-300,210-20].stat = 1

    #middle-bottom
    gridDict[630-300,210-20+110].stat = 1
    gridDict[630-300,220-20+110].stat = 1
    gridDict[640-300,210-20+110].stat = 1
    gridDict[650-300,210-20+110].stat = 1
    gridDict[640-300,210-20+130].stat = 1

    #right bottom
    gridDict[740-300,250].stat = 1
    gridDict[740-300,250+10].stat = 1
    gridDict[740-300,250+20].stat = 1
    gridDict[750-300,250].stat = 1
    gridDict[760-300,250+10].stat = 1

    #far right four squares
    gridDict[730-300,180].stat = 1
    gridDict[740-300,180].stat = 1
    gridDict[730-300,190].stat = 1
    gridDict[740-300,190].stat = 1

def tens(gridDict):
    for i in range(0,100, 10):
        gridDict[200+i,240].stat = 1

# create a conway glider
def create_glider(gridDict, x, y):
    x = round_up_nearest_ten(x)
    y = round_up_nearest_ten(y)

    #catches when drawn pixels are off of screen
    try:
        # draw one of four orientations for glider
        direction = random.randint(0,3)
        if direction == 0:
            gridDict[x,y].stat = 1
            gridDict[x+10,y-10].stat = 1
            gridDict[x+20,y+10].stat = 1
            gridDict[x+20,y].stat = 1
            gridDict[x+20,y-10].stat = 1
        elif direction == 1:
            gridDict[x,y].stat = 1
            gridDict[x-10,y-10].stat = 1
            gridDict[x-10,y-20].stat = 1
            gridDict[x,y-20].stat = 1
            gridDict[x+10,y-20].stat = 1
        elif direction == 2:
            gridDict[x,y].stat = 1
            gridDict[x-10,y+10].stat = 1
            gridDict[x-20,y+10].stat = 1
            gridDict[x-20,y].stat = 1
            gridDict[x-20,y-10].stat = 1
        else:
            gridDict[x,y].stat = 1
            gridDict[x+10,y+10].stat = 1
            gridDict[x+10,y+20].stat = 1
            gridDict[x,y+20].stat = 1
            gridDict[x-10,y+20].stat = 1
    except KeyError:
        pass

def binary_101(gridDict):
    gridDict[180,110].stat = 1
    gridDict[190,110].stat = 1
    gridDict[200,110].stat = 1
    gridDict[90,170].stat = 1
    gridDict[100,170].stat = 1
    gridDict[100,180].stat = 1
    gridDict[90,180].stat = 1
    gridDict[90,210].stat = 1
    gridDict[100,210].stat = 1
    gridDict[100,220].stat = 1
    gridDict[90,220].stat = 1
    gridDict[120,160].stat = 1
    gridDict[120,150].stat = 1
    gridDict[130,140].stat = 1
    gridDict[140,140].stat = 1
    gridDict[140,150].stat = 1
    gridDict[140,180].stat = 1
    gridDict[140,190].stat = 1
    gridDict[140,200].stat = 1
    gridDict[140,210].stat = 1
    gridDict[120,170].stat = 1
    gridDict[120,180].stat = 1
    gridDict[120,190].stat = 1
    gridDict[120,200].stat = 1
    gridDict[120,210].stat = 1
    gridDict[120,220].stat = 1
    gridDict[120,230].stat = 1
    gridDict[120,240].stat = 1
    gridDict[130,250].stat = 1
    gridDict[140,250].stat = 1
    gridDict[140,240].stat = 1
    gridDict[160,190].stat = 1
    gridDict[160,200].stat = 1
    gridDict[170,210].stat = 1
    gridDict[180,210].stat = 1
    gridDict[170,180].stat = 1
    gridDict[180,180].stat = 1
    gridDict[190,190].stat = 1
    gridDict[190,200].stat = 1
    gridDict[210,180].stat = 1
    gridDict[210,190].stat = 1
    gridDict[210,200].stat = 1
    gridDict[210,210].stat = 1
    gridDict[210,150].stat = 1
    gridDict[210,140].stat = 1
    gridDict[220,140].stat = 1
    gridDict[230,150].stat = 1
    gridDict[230,160].stat = 1
    gridDict[230,170].stat = 1
    gridDict[230,180].stat = 1
    gridDict[230,190].stat = 1
    gridDict[230,200].stat = 1
    gridDict[230,210].stat = 1
    gridDict[230,220].stat = 1
    gridDict[230,230].stat = 1
    gridDict[230,240].stat = 1
    gridDict[220,250].stat = 1
    gridDict[210,250].stat = 1
    gridDict[210,240].stat = 1
    gridDict[250,170].stat = 1
    gridDict[260,170].stat = 1
    gridDict[260,180].stat = 1
    gridDict[250,180].stat = 1
    gridDict[250,210].stat = 1
    gridDict[260,210].stat = 1
    gridDict[260,220].stat = 1
    gridDict[250,220].stat = 1

def faces(gridDict):
    gridDict[230,370].stat = 1
    gridDict[240,370].stat = 1
    gridDict[240,360].stat = 1
    gridDict[250,360].stat = 1
    gridDict[260,360].stat = 1
    gridDict[270,360].stat = 1
    gridDict[280,360].stat = 1
    gridDict[290,360].stat = 1
    gridDict[300,360].stat = 1
    gridDict[310,360].stat = 1
    gridDict[310,370].stat = 1
    gridDict[320,370].stat = 1
    gridDict[310,380].stat = 1
    gridDict[300,380].stat = 1
    gridDict[290,380].stat = 1
    gridDict[280,380].stat = 1
    gridDict[270,380].stat = 1
    gridDict[260,380].stat = 1
    gridDict[250,380].stat = 1
    gridDict[240,380].stat = 1
    gridDict[250,390].stat = 1
    gridDict[260,390].stat = 1
    gridDict[270,390].stat = 1
    gridDict[280,390].stat = 1
    gridDict[290,390].stat = 1
    gridDict[300,390].stat = 1
    gridDict[300,350].stat = 1
    gridDict[290,350].stat = 1
    gridDict[280,350].stat = 1
    gridDict[270,350].stat = 1
    gridDict[260,350].stat = 1
    gridDict[250,350].stat = 1
    gridDict[260,340].stat = 1
    gridDict[270,340].stat = 1
    gridDict[280,340].stat = 1
    gridDict[290,340].stat = 1
    gridDict[260,400].stat = 1
    gridDict[270,400].stat = 1
    gridDict[280,400].stat = 1
    gridDict[290,400].stat = 1
    gridDict[260,310].stat = 1
    gridDict[270,310].stat = 1
    gridDict[280,300].stat = 1
    gridDict[270,290].stat = 1
    gridDict[250,300].stat = 1
    gridDict[300,300].stat = 1
    gridDict[310,300].stat = 1
    gridDict[310,310].stat = 1
    gridDict[300,310].stat = 1
    gridDict[300,260].stat = 1
    gridDict[310,250].stat = 1
    gridDict[310,240].stat = 1
    gridDict[310,230].stat = 1
    gridDict[300,220].stat = 1
    gridDict[290,220].stat = 1
    gridDict[290,260].stat = 1
    gridDict[280,250].stat = 1
    gridDict[280,240].stat = 1
    gridDict[280,230].stat = 1
    gridDict[230,230].stat = 1
    gridDict[230,240].stat = 1
    gridDict[230,250].stat = 1
    gridDict[220,220].stat = 1
    gridDict[210,220].stat = 1
    gridDict[200,230].stat = 1
    gridDict[200,240].stat = 1
    gridDict[200,250].stat = 1
    gridDict[210,260].stat = 1
    gridDict[220,260].stat = 1

def maze(gridDict):
    gridDict[210,130].stat = 1
    gridDict[210,120].stat = 1
    gridDict[220,120].stat = 1
    gridDict[230,150].stat = 1
    gridDict[240,150].stat = 1
    gridDict[240,140].stat = 1
    gridDict[190,130].stat = 1
    gridDict[180,140].stat = 1
    gridDict[190,150].stat = 1
    gridDict[210,170].stat = 1
    gridDict[220,180].stat = 1
    gridDict[230,170].stat = 1

def pulsar(gridDict):
    gridDict[150,300].stat = 1
    gridDict[160,300].stat = 1
    gridDict[170,300].stat = 1
    gridDict[180,280].stat = 1
    gridDict[180,270].stat = 1
    gridDict[180,260].stat = 1
    gridDict[170,250].stat = 1
    gridDict[160,250].stat = 1
    gridDict[150,250].stat = 1
    gridDict[130,260].stat = 1
    gridDict[130,270].stat = 1
    gridDict[130,280].stat = 1
    gridDict[200,260].stat = 1
    gridDict[200,270].stat = 1
    gridDict[200,280].stat = 1
    gridDict[210,250].stat = 1
    gridDict[220,250].stat = 1
    gridDict[230,250].stat = 1
    gridDict[250,260].stat = 1
    gridDict[250,270].stat = 1
    gridDict[250,280].stat = 1
    gridDict[210,300].stat = 1
    gridDict[220,300].stat = 1
    gridDict[230,300].stat = 1
    gridDict[230,230].stat = 1
    gridDict[220,230].stat = 1
    gridDict[210,230].stat = 1
    gridDict[200,220].stat = 1
    gridDict[200,210].stat = 1
    gridDict[200,200].stat = 1
    gridDict[250,220].stat = 1
    gridDict[250,210].stat = 1
    gridDict[250,200].stat = 1
    gridDict[210,180].stat = 1
    gridDict[220,180].stat = 1
    gridDict[230,180].stat = 1
    gridDict[180,220].stat = 1
    gridDict[180,210].stat = 1
    gridDict[180,200].stat = 1
    gridDict[170,230].stat = 1
    gridDict[160,230].stat = 1
    gridDict[150,230].stat = 1
    gridDict[130,220].stat = 1
    gridDict[130,210].stat = 1
    gridDict[130,200].stat = 1
    gridDict[170,180].stat = 1
    gridDict[160,180].stat = 1
    gridDict[150,180].stat = 1

def gliders(gridDict):
    gridDict[120,160].stat = 1
    gridDict[130,160].stat = 1
    gridDict[140,160].stat = 1
    gridDict[140,150].stat = 1
    gridDict[140,140].stat = 1
    gridDict[180,180].stat = 1
    gridDict[190,180].stat = 1
    gridDict[200,180].stat = 1
    gridDict[190,190].stat = 1
    gridDict[240,200].stat = 1
    gridDict[250,200].stat = 1
    gridDict[260,200].stat = 1
    gridDict[240,210].stat = 1
    gridDict[240,220].stat = 1











