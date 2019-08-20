import pickle, math
import pygame, os 

class GameInfo:
    def __init__(self, nodes, connections):
        self.nodes = nodes
        self.connections = connections
    
class Node: 
    radius = 20

    def __init__(self, pos):
        self.ID = globalID(Node).__next__()
        self.pos = pos
        self.colour = RED
        self.connections = []
        self.distance = math.inf

    def addConnection(self, connection):
        self.connections.append(connection)
        print(self.ID)
    
    def display(self):
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)
        centre(str(self.ID), text, WHITE, self.pos)
        if self.distance != math.inf:
            centre(str(self.distance), text, BLACK, [self.pos[0], self.pos[1] - self.radius - 10])
    
    def selected(self, mousePos):
        if (mousePos[0] - self.pos[0])**2 + (mousePos[1] - self.pos[1])**2 < self.radius**2:
            return True
        else: return False
    
    def setColour(self, colour):
        self.colour = colour

    def getDistance(self):
        return self.distance

    def setDistance(self, distance):
        self.distance = distance


class Connection:
    def __init__(self, nodes):
        self.ID = globalID(Connection).__next__()
        self.nodes = nodes
        pos1 = nodes[0].pos
        pos2 = nodes[1].pos
        self.weightPos = [(max(pos1[0],pos2[0]) - min(pos1[0],pos2[0])) /2 + min(pos1[0],pos2[0]), (max(pos1[1],pos2[1]) - min(pos1[1],pos2[1])) / 2 + min(pos1[1],pos2[1])]
        self.colour = BLACK
        self.weight = -1
        self.width = 3

    def setWeight(self, weight):
        self.weight = weight

    def display(self):
        pygame.draw.line(screen, self.colour, self.nodes[0].pos, self.nodes[1].pos, self.width)
        if self.weight != -1:
            centre(str(self.weight), text, RED, self.weightPos)

dictionary = {}
def globalID(identifier):
  global dictionary
  while True:
    if(identifier in dictionary):
      dictionary[identifier] += 1
    else:
      dictionary[identifier] = 0
    yield dictionary[identifier]

BLACK = 0,0,0
WHITE = 255,255,255
RED   = 255,0,0
GREEN = 0,255,0
BLUE  = 0,0,255
GREY  = 100,100,100
YELLOW= 255,255,0

mode = 0
modeTitles = ["Place Nodes", "Add Connections", "Set Weight", "Name Network Save"]
weight = ""
size = width, height = 800,800
nodes = []
connections = []
selectedNodes = []
frameRate = 30
fileName = ""
fileType = "lvl"
fileNameExists = False
displayMessage = ""

#main is called once
def main():
    global screen, size, text, titleFont, subtitleFont, clock
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Network Creator")

    clock = pygame.time.Clock()
    #1ms delay, and then another event will be sent every 50ms
    pygame.key.set_repeat(1,500)

    text = pygame.font.Font(None, 24)
    titleFont = pygame.font.Font(None, 40)
    subtitleFont = pygame.font.Font(None, 30)


def mainLoop():
    while True:
        clock.tick(frameRate)
        for event in pygame.event.get(): 
            eventManager(event)
        
        screen.fill(WHITE)
        centre("Mode: " + modeTitles[mode], titleFont, BLACK, [width/2, 15])

        for connection in connections:
            connection.display()
        
        for node in nodes:
            node.display()

        if len(connections) != 0 and len(weight) != 0:
            centre(weight, text, RED, connections[len(connections) - 1].weightPos)
        
        if len(displayMessage) != 0:
            centre(displayMessage, text, RED, [(width / 2), 65])

        if mode == 3:
           centre("Filename: " + fileName, subtitleFont, BLACK, [width / 2, 40])

        pygame.display.flip()

def centre(string, font, colour, pos):
    textSize = font.size(string)
    screen.blit(font.render(string, True, colour), pygame.Rect(pos[0] - textSize[0] / 2, pos[1] - textSize[1] / 2, textSize[0], textSize[1]))

def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def keyPressed(event):
    global mode, weight, fileName, fileNameExists, displayMessage
    key = pygame.key.name(event.key)
    #print(key)
    if key == "=": 
        increaseMode(True)
    elif mode == 2 and isNumber(key):
        weight += key
    elif key == "backspace":
        if mode == 2 and len(weight) != 0:
            weight = weight[:-1]
        elif mode == 3 and len(fileName) != 0:
            fileName = fileName[:-1]
    elif key == "return":
        if mode == 2 and len(weight) != 0:
            saveWeight()
        elif mode == 0 or mode == 1:
            increaseMode(3)
        elif mode == 3 and len(fileName) != 0:
            if not os.path.isfile(fileName + "." + fileType):
                saveLevel()
                displayMessage = "Level Saved"
                print("LevelSaved")
            else:
                fileNameExists = True
                displayMessage = "That Filename Already Exists!"
    elif key == "escape":
        quit()
    elif mode == 3 and len(key) == 1:
        fileName += key
        if fileNameExists: 
            filefileNameExists = False
            displayMessage = ""

def saveLevel():
    global nodes, connections, fileName, fileType
    for node in nodes:
        print(len(node.connections))
    gameInfo = GameInfo(nodes, connections)
    with open(fileName + "." + fileType,"wb") as file:
        pickle.dump(gameInfo, file)
    
def saveWeight():
    global weight
    increaseMode(1)
    connections[len(connections) - 1].setWeight(int(weight))
    weight = ""

def mouseButtonDown(event):
    global selectedNodes  
    mousePressed = pygame.mouse.get_pressed()
    if mode == 0 and mousePressed[0]:
        nodes.append(Node(pygame.mouse.get_pos()))
        print("added")
    elif mode == 1 and mousePressed[0]:
        for node in nodes:
            if node.selected(pygame.mouse.get_pos()):
                selectedNodes.append(node)
                if len(selectedNodes) == 2:
                    setNodeConnections(selectedNodes)
                    selectedNodes = []
                    break
    elif mode == 1 and mousePressed[2]:
        selectedNodes = []
    
    #When all 3 are false, scrolling with middle button:
    elif (mode == 0 or mode == 1) and not mousePressed[0] and not mousePressed[1] and not mousePressed[2]:
        increaseMode(True)

    elif mode == 2 and mousePressed[1]:
        saveWeight()

def setNodeConnections(selectedNodes):
    global connections
    print("Called")
    connection = Connection(selectedNodes)
    selectedNodes[0].addConnection(connection)
    selectedNodes[1].addConnection(connection)
    connections.append(connection)
    increaseMode(2)
    
def increaseMode(value):
    global mode, displayMessage
    displayMessage = ""
    if type(value) != int and value == True:
        mode += 1
        if mode > 1: mode = 0
    elif type(value) == int:
        mode = value;
    
def quit():
    print("exiting")
    os._exit(1)

def eventManager(event):
    if event.type == pygame.QUIT: quit()
    elif event.type == pygame.MOUSEBUTTONDOWN: mouseButtonDown(event)
    elif event.type == pygame.MOUSEBUTTONUP: return
    elif event.type == pygame.KEYDOWN: keyPressed(event)

if __name__ == "__main__":
    main()
    mainLoop()


pygame.quit()
