import pygame, math, os

class GameInfo:
    def __init__(self, nodes, connections):
        self.nodes = nodes
        self.connections = connections
    
class Node: 
    radius = 20

    def __init__(self, pos, id):
        self.ID = id
        self.pos = pos
        self.colour = RED
        self.connections = []
        self.distance = math.inf

    def addConnection(self, connection):
        self.connections.append(connection)
        print(self.ID)
    
    def display(self):
        global moduleFont, moduleScreen
        pygame.draw.circle(moduleScreen, self.colour, self.pos, self.radius)
        centre(str(self.ID), moduleFont, WHITE, self.pos)
        if self.distance != math.inf:
            centre(str(self.distance), moduleFont, BLACK, [self.pos[0], self.pos[1] - self.radius - 10])
    
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
    """A representation of a connection between 2 nodes.

    :param nodes: A node, the nodes connected by this connection.
    :param id: An int, the id of this node.
    """
    def __init__(self, nodes, id):
        self.ID = id
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
        global moduleFont, moduleScreen
        pygame.draw.line(moduleScreen, self.colour, self.nodes[0].pos, self.nodes[1].pos, self.width)
        if self.weight != -1:
            centre(str(self.weight), moduleFont, RED, self.weightPos)

    def setColour(self, colour):
        self.colour = colour

    def setWidth(self, width):
        self.width = width

def initialiseModule(screen, font):
    global moduleScreen, moduleFont
    moduleScreen = screen
    moduleFont = font

moduleScreen = None
moduleFont = None
BLACK = 0,0,0
WHITE = 255,255,255
RED   = 255,0,0
GREEN = 0,255,0
BLUE  = 0,0,255
GREY  = 100,100,100
YELLOW= 255,255,0
   
def quit():
    print("exiting")
    os._exit(1)

def initialiseText():

    text = pygame.font.Font(None, 24)
    titleFont = pygame.font.Font(None, 40)
    subtitleFont = pygame.font.Font(None, 30)

    return text, titleFont, subtitleFont

def centre(string, font, colour, pos):
    global moduleScreen
    textSize = font.size(string)
    moduleScreen.blit(font.render(string, True, colour), pygame.Rect(pos[0] - textSize[0] / 2, pos[1] - textSize[1] / 2, textSize[0], textSize[1]))

