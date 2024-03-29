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

    def setPrev(self, node, connection):
        self.prevNode = node
        self.prevConnection = connection

    def getPrev(self):
        return self.prevNode, self.prevConnection


class Connection:
    def __init__(self, nodes):
        self.ID = globalID(Connection).__next__()
        self.nodes = nodes
        pos1 = nodes[0].pos
        pos2 = nodes[1].pos
        self.weightPos = [(max(pos1[0],pos2[0]) - min(pos1[0],pos2[0])) /2 + min(pos1[0],pos2[0]), (max(pos1[1],pos2[1]) - min(pos1[1],pos2[1])) / 2 + min(pos1[1],pos2[1])]
        self.colour = BLACK
        self.weight = -1
        self.width = 2

    def setWeight(self, weight):
        self.weight = weight

    def display(self):
        pygame.draw.line(screen, self.colour, self.nodes[0].pos, self.nodes[1].pos, self.width)
        if self.weight != -1:
            centre(str(self.weight), text, RED, self.weightPos)

    def setColour(self, colour):
        self.colour = colour

    def setWidth(self, width):
        self.width = width

BLACK = 0,0,0
WHITE = 255,255,255
RED   = 255,0,0
GREEN = 0,255,0
BLUE  = 0,0,255
GREY  = 100,100,100
YELLOW= 255,255,0
size = width, height = 800,800

mode = 0
modeTitles = ["Set start Node", "Set End Node", "Solve"]
fileType = "lvl"
filePath = "D:/Python/Saves/Node/LevelCreator/"
startNode = None
endNode = None
setPath = False
initiated = False
frame = 0
frameRate = 30

def main():
    global screen, size, text, subtitleFont, titleFont, gameInfo, nodes, connections, filePath, fileType, clock
    
    
    pygame.init()

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Node Level Solver")

    #1ms delay, and then another event will be sent every 50ms
    pygame.key.set_repeat(1,500)
    clock = pygame.time.Clock()

    text = pygame.font.Font(None, 24)
    subtitleFont = pygame.font.Font(None, 30)
    titleFont = pygame.font.Font(None, 40)

    while True:
        fileName = input("Enter the filename: ")
        #fileName = "networkdemo1"
        print(filePath + fileName + "." + fileType)

        if not os.path.isfile(filePath + fileName + "." + fileType):
            print("File doesn't exist! Try again")
            continue
        else:
            file = open(filePath + fileName + "." + fileType, "rb")
            gameInfo = pickle.load(file)
            nodes = gameInfo.nodes
            connections = gameInfo.connections
            print(connections[0].nodes)
            break

def mainLoop():
    global startNode, connections, nodes, bestWeight, mode, setPath, unvisitedNodes, initiated, frame, frameRate
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

        if mode == 2:
            #Dijkstra's algorithm:
            if not initiated:
                unvisitedNodes = []
                for node in nodes:
                    if node == startNode:
                        node.setDistance(0)
                    node.setPrev(None, None)
                    unvisitedNodes.append(node)
                initiated = True

            if len(unvisitedNodes) != 0 and frameRate % 15 == 0:
                node = nodeWithShortestDistance(unvisitedNodes)
                unvisitedNodes.remove(node)
                neighbours, connectionsList = nodeNeighbours(node, unvisitedNodes)
                for i in range(len(neighbours)):
                    newDistance = node.getDistance() + connectionsList[i].weight
                    connectionsList[i].setColour(RED)
                    if newDistance < neighbours[i].getDistance():
                        neighbours[i].setDistance(newDistance)
                        neighbours[i].setPrev(node, connectionsList[i])
                        
            else:
                if not setPath:
                    node = endNode
                    while True:
                        node, nextConnection = node.getPrev()
                        if node != None:
                            nextConnection.setColour(BLUE)
                            nextConnection.setWidth(4)
                        else:
                            break
                    setPath = True
                    print("Finished")
                centre("Shortest Distance found: " + str(endNode.getDistance()), subtitleFont, BLACK, [width / 2, 40])
                
        
        frame += 1
        pygame.display.flip()

def nodeWithShortestDistance(array):
    minNode = None
    minDistance = math.inf
    for node in array:
        if node.getDistance() < minDistance:
            minDistance = node.getDistance()
            minNode = node

    return minNode

def nodeNeighbours(node, array):
    neighbours = []
    connections = []
    for connection in node.connections:
        id = -1
        if connection.nodes[0] != node: id = 0
        elif connection.nodes[1] != node: id = 1
        else: print("No node found!")
        
        if id != -1 and connection.nodes[id] in array:
            neighbours.append(connection.nodes[id])
            connections.append(connection)

    return neighbours, connections


def centre(string, font, colour, pos):
    textSize = font.size(string)
    screen.blit(font.render(string, True, colour), pygame.Rect(pos[0] - textSize[0] / 2, pos[1] - textSize[1] / 2, textSize[0], textSize[1]))

def increaseMode(value):
    global mode
    if type(value) != int and value == True:
        print("bool")
        mode += 1
        if mode > 1: mode = 0
    elif type(value) == int:
        print("Int")
        mode = value;

def quit():
    print("exiting")
    os._exit(1)

def keyPressed(event):
    global mode
    key = pygame.key.name(event.key)
    if(key == "="):
        increaseMode(True)
    elif key == "return" and (mode == 0 or mode == 1) and startNode != None and endNode != None:
        increaseMode(2)
    elif key == "escape":
        quit()

def mouseButtonDown(event):
    global startNode, endNode
    #print(pygame.mouse.get_pressed())    
    mousePressed = pygame.mouse.get_pressed()

    if mode == 0 and mousePressed[0]:
        result = setNode(startNode, YELLOW, endNode)
        if result != False:
            startNode = result

    elif mode == 1 and mousePressed[0]:
        result = setNode(endNode, GREEN, startNode)
        if result != False:
            endNode = result

    elif (mode == 0 or mode == 1) and not mousePressed[0] and not mousePressed[1] and not mousePressed[2]:
        increaseMode(True)

    elif (mode == 0 or mode == 1) and startNode != None and endNode != None and mousePressed[1]:
        increaseMode(2)


def setNode(setNode, colour, otherNode):
    global nodes
    for node in nodes:
        if node.selected(pygame.mouse.get_pos()) and node != otherNode:
            if(node != setNode):
                if setNode != None:
                    setNode.setColour(RED)
                node.setColour(colour)
                return node
            else:
                node.setColour(RED)
                return None
    return False

def eventManager(event):
    if event.type == pygame.QUIT: quit()
    elif event.type == pygame.MOUSEBUTTONDOWN: mouseButtonDown(event)
    elif event.type == pygame.MOUSEBUTTONUP: return
    elif event.type == pygame.KEYDOWN: keyPressed(event)

if __name__ == "__main__":
    main()
    mainLoop()


pygame.quit()
