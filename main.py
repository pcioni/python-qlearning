try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import random
import qlearn

class MapDraw:
    Colors = {
        "White"      : "#FFFFFF",
        "Black" : "#9BF04D",
        "LightGreen"      : "#000000",
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
        self.endgoal = (0, 0)
        self.MAX_steps = 0

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
                    if (self.cellMap[i][j] != 1):
                        self.MAX_steps += 1
            self.cellMap[0][0] = 0
            self.cellMap[self.cell_y][self.cell_x] = 3
            self.endgoal = (self.cell_y, self.cell_x)
        else:
            for i in range(self.cell_y):
                for j in range(self.cell_x):
                    self.cellMap[i][j] = mapin[i][j]
                    if (self.cellMap[i][j] == 3):
                        self.endgoal = (i, j)
                        self.MAX_steps += 1
                    elif (self.cellMap[i][j] != 1):
                        self.MAX_steps += 1

    def tileCheck(self, x, y):
        if ( (x < 0) or (x >= self.cell_x) or (y < 0) or (y >= self.cell_y) or (self.cellMap[x][y] == 1)):
            return False
        else:
            return True

class Agent:
    actions = {
        0 : "up",
        1 : "down",
        2 : "left",
        3 : "right"
    }

    def __init__(self, startX, startY, size, epsilon = 0.1, alpha = 0.2, gamma = 0.9):
        self.xPos = startX
        self.yPos = startY
        self.Qvals = [[0 for i in range(size)] for j in range(size)]    #we have Q values for every space, even if we dont use it

        self.endGoal = [0,0]

        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def getState(self, ):
        def cellvalue(cell):
            if  self.xPos == self.endGoal[0] and self.ypos == self.endGoal[1]:
                return 1
            else:
                return 0

    def setEndGoal(self, end):
        self.endGoal = [end[0], end[1]]

    #QVal ( (x,y), a) ==> Qvals[(x*10) + y][action]
    #             y----->
    # Qvals = [ x 0,0,0,0,  <= This is how the board looks when displayed
    #           | 0,0,0,0,
    #           | 0,0,0,0,
    #           v 0,0,0,0]
    
    def setQval(self):
        if self.xPos != self.endGoal[0] or self.yPos != self.endGoal[1]:
            self.Qvals[self.xPos][self.yPos] -= 1 * self.alpha

    def Move(self, dir, mg):
        dx = 0
        dy = 0
        if dir == "up":
            dx = -1
        elif dir == "down":
            dx = 1
        elif dir == "left":
            dy = -1
        elif dir == "right":
            dy = 1
        else:
            print("ERROR: not a direction")

        if mg.tileCheck(self.xPos+dx, self.yPos+dy):
            mg.setTile(self.xPos, self.yPos, 0);
            self.xPos += dx
            self.yPos += dy
            mg.setTile(self.xPos, self.yPos, 2);
            return True;
        else:
            return False;
    
    def isFinished(self, endgoal):
        if (endgoal[0] == self.xPos and endgoal[1] == self.yPos):
            return True
        else:
            return False

############################################

    def getQ(self, x, y):
        v = []
        if x > 0:
            v.append( self.Qvals[x-1][y])
        if x < 9:
            v.append( self.Qvals[x+1][y])
        if y > 0:
            v.append( self.Qvals[x][y-1])
        if y < 9:
            v.append( self.Qvals[x][y+1])
        return v

    def learnQ(self, state, action, reward, value):
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

    def chooseAction(self, state):
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            q = self.getQ(self.xPos, self.yPos)
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(q)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)
            action = self.actions[i]
            #print (q, maxQ, i, action) ######################MASTER DEBUG
        return action

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)

#########################################################

map1 = [ [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,3] ]

map2 = [ [0,0,0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,1,0], [0,0,0,0,0,0,0,0,0,0], [0,1,1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,1,0], [0,0,0,0,0,0,0,0,0,0], [0,1,1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,3] ]

map3 = [ [0,1,0,0,1,1,1,1,0,0], [0,0,0,0,0,1,1,1,1,0], [0,1,0,1,1,1,1,0,0,1], [0,1,0,0,0,0,0,0,0,0], [1,0,0,0,0,0,0,0,1,0], [1,1,0,1,0,1,1,1,1,0], [1,1,0,1,0,0,0,0,1,1], [1,0,0,0,0,0,0,1,1,0], [0,0,0,1,1,0,0,0,0,0], [0,0,1,1,1,1,0,0,0,3] ]

#10 walls
map4 = [ [0,0,0,0,0,0,0,0,0,0], [0,0,0,1,1,0,0,0,0,0], [0,0,0,0,0,0,1,0,0,1], [0,0,0,1,1,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,1,1,0,0,0], [0,0,0,0,0,0,0,1,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,1,0,0,0], [0,0,0,0,0,0,0,0,0,3] ]


#The last two variables in MapDraw determine how many squares make up a grid;
# for some reason, if they aren't equal, things break. Who cares though, right?
GFX = MapDraw(600,600,10,10)
MG = generateDungeon(10,10)

MG.buildMap(False, map1)       #set to false, give it a map above

# Set up agent
Qagent = Agent(0,0, 10)
MG.setTile(Qagent.xPos, Qagent.yPos, 2);

MG.createMapDraw(GFX)
GFX.DrawMap(MG.cellMap)

print(MG.MAX_steps)

for i in range(5):
    Qagent.xPos = 0
    Qagent.yPos = 0
    finished = False
    moves = 0

    MG.setTile(Qagent.xPos, Qagent.yPos, 2);
    MG.setTile(MG.endgoal[0], MG.endgoal[1], 3)
    Qagent.setEndGoal(MG.endgoal)

    while (not finished):

        Qagent.Move( Qagent.chooseAction( Qagent.getState() ), MG)
        Qagent.setQval()

        moves+=1
        finished = Qagent.isFinished(MG.endgoal);

        GFX.DrawMap(MG.cellMap)
        GFX.update()
    print("endgoal reached in %d moves\n" % moves)

GFX.lock()