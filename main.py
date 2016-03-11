from tkinter import *
import random

class MapDraw:
    Colors = {
        "White"      : "#FFFFFF",
        "LightGreen" : "#9BF04D",
        "Black"      : "#000000"
    }

    fillColors = {0: "White", 1: "Black", 2: "LightGreen"}

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

#The last two variables in MapDraw determine how many squares make up a grid;
# for some reason, if they aren't equal, things break. Who cares though, right?
GFX = MapDraw(600,600,10,10)
MG = generateDungeon(10,10)
MG.createMapDraw(GFX)
GFX.DrawMap(MG.cellMap)
GFX.lock()
