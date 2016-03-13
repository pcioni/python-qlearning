try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import random

class MapDraw:
    Colors = {
        "White"      : "#FFFFFF",
        "LightGreen" : "#9BF04D",
        "Black"      : "#000000",
        "Red"        : "#FF0000"
    }

    fillColors = {0: "White", 1: "Black", 2: "LightGreen", 3: "Red"}

    def __init__(self, screenWidth, screenHeight, cellX, cellY):
        self.width = screenWidth
        self.height = screenHeight
        self.cell_x = cellX
        self.cell_y = cellY
        self.cell_width = 60
        self.cell_height = 60

        self.master = Tk()
        self.canvas = Canvas(self.master, width = self.width, height = self.height)


        self.rectangles = [ [ self.canvas.create_rectangle(self.cell_width*x, self.cell_height*y,
                                                           self.cell_height*x+self.cell_width, self.cell_width*y+self.cell_height,
                                                           fill="#000000", width=1) for x in range(cellY)] for y in range(cellX)]

        self.canvas.pack()


    def drawTile(self, tileType, x, y):
        xPos = x * self.cell_width
        yPos = y * self.cell_height
        fillColor = self.fillColors[tileType]
        self.canvas.itemconfig(self.rectangles[x][y], fill=fillColor)

    def DrawMap(self, cellMap):
        for x in range(0, self.cell_x):
            for y in range(0, self.cell_y):
                self.drawTile(cellMap[x][y], x, y)

        self.update()

    def update(self):
        self.master.update()

    def lock(self):
        self.master.mainloop()

class generateDungeon:
    def __init__(self, sizeX, sizeY):
        self.cell_x = sizeX
        self.cell_y = sizeY
        self.cellMap = [[0 for i in range(self.cell_y)] for j in range(self.cell_x)]
        #self.cellMap =  [ [0] * self.cell_y] * self.cell_x
        self.Drawupdates = False

    def createMapDraw(self, handler):
        self.GFX = handler
        self.Drawupdates = True

    def setTile(self, x, y, value):
        self.cellMap[x][y] = value

    def buildMap(self, rand, mapin):
        if (rand == True):
            for i in range(self.cell_y):
                for j in range(self.cell_x):
                    self.cellMap[i][j] = random.randint(0,1)
        else:
            for i in range(self.cell_y):
                for j in range(self.cell_x):
                    self.cellMap[i][j] = mapin[i][j]

    def tileCheck(self, x, y):
        if ( (x < 0) or (x >= self.cell_x) or (y < 0) or (y >= self.cell_y) or (self.cellMap[x][y] == 1)):
            return False
        else:
            return True

class Agent:
    Dirs = {
        "up"    : 0,
        "down"  : 1,
        "left"  : 2,
        "right" : 3
    }

    def __init__(self, startX, startY, size):
        self.xPos = startX
        self.yPos = startY
        self.Qvals = [[0 for i in range(size)] for j in range(4)]    #we have Q values for every space, even if we dont use it

    def Move(self, dir, mg):
        dx = 0
        dy = 0
        if (dir == "up"):
            dx = -1
        elif (dir == "down"):
            dx = 1
        elif (dir == "left"):
            dy = -1
        elif (dir == "right"):
            dy = 1
        else:
            print("ERROR: not a direction")

        if (mg.tileCheck(self.xPos+dx, self.yPos+dy) ):
            mg.setTile(self.xPos, self.yPos, 0);
            self.xPos += dx
            self.yPos += dy
            mg.setTile(self.xPos, self.yPos, 2);
            return True;
        else:
            return False;

map1 = [ [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0] ]

map2 = [ [0,0,0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,1,0], [0,0,0,0,0,0,0,0,0,0], [0,1,1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,1,0], [0,0,0,0,0,0,0,0,0,0], [0,1,1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,3] ]

map3 = [ [0,1,0,0,1,1,1,1,0,0], [0,0,0,0,0,1,1,1,1,0], [0,1,0,1,1,1,1,0,0,1], [0,1,0,0,0,0,0,0,0,0], [1,0,0,0,0,0,0,0,1,0], [1,1,0,1,0,1,1,1,1,0], [1,1,0,1,0,0,0,0,1,1], [1,0,0,0,0,0,0,1,1,0], [0,0,0,1,1,0,0,0,0,0], [0,0,1,1,1,1,0,0,0,3] ]

#The last two variables in MapDraw determine how many squares make up a grid;
# for some reason, if they aren't equal, things break. Who cares though, right?
GFX = MapDraw(600,600,10,10)
MG = generateDungeon(10,10)
MG.buildMap(False, map3)
Qagent = Agent(0,0, 10*10)
MG.setTile(Qagent.xPos, Qagent.yPos, 2);
MG.createMapDraw(GFX)
GFX.DrawMap(MG.cellMap)

while (True):
    while (Qagent.Move(random.choice( list(Qagent.Dirs.keys()) ), MG) == False):
        x = 0

    GFX.DrawMap(MG.cellMap)
    GFX.update()

GFX.lock()