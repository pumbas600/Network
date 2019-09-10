import pickle, os
import pygame, math 
from NetworkBase import *

dictionary = {}
def globalID(identifier):
  global dictionary
  while True:
    if(identifier in dictionary):
      dictionary[identifier] += 1
    else:
      dictionary[identifier] = 0
    yield dictionary[identifier]

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

#==================================================================================================
#main is called once
def main():
    global screen, size, clock, text, titleFont, subtitleFont
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Network Creator")

    clock = pygame.time.Clock()
    #1ms delay, and then another event will be sent every 50ms
    pygame.key.set_repeat(1,500)
    text, titleFont, subtitleFont = initialiseText()
    initialiseModule(screen, text)


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

#=========================================================================================================

def increaseMode(value):
    global mode, displayMessage
    displayMessage = ""
    if type(value) != int and value == True:
        mode += 1
        if mode > 1: mode = 0
    elif type(value) == int:
        mode = value;
 

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
    global nodes, connections, fileName, fileType, screen, text

    gameInfo = GameInfo(nodes, connections)

    with open(fileName + "." + fileType,"wb") as file:
        pickle.dump(gameInfo, file)
    
    
def saveWeight():
    global weight
    increaseMode(1)
    connections[len(connections) - 1].setWeight(int(weight))
    weight = ""

def mouseButtonDown(event):
    global selectedNodes, mode  
    mousePressed = pygame.mouse.get_pressed()
    if mode == 0 and mousePressed[0]:
        nodes.append(Node(pygame.mouse.get_pos(), globalID(Node).__next__()))
        print("added")
    elif mode == 1 and mousePressed[0]:
        for node in nodes:
            if node.selected(pygame.mouse.get_pos()):
                selectedNodes.append(node)
                if len(selectedNodes) == 2:
                    setNodeConnections(selectedNodes)
                    selectedNodes = []
                    break
    elif mode == 1 or mode == 2 and mousePressed[2]:
        selectedNodes = []
        mode = 1
    elif mode == 0 and mousePressed[2] and len(nodes) != 0:
        nodes.pop(len(nodes) - 1)
        dictionary[Node] -= 1

    #When all 3 are false, scrolling with middle button:
    elif (mode == 0 or mode == 1) and not mousePressed[0] and not mousePressed[1] and not mousePressed[2]:
        increaseMode(True)

    elif mode == 2 and mousePressed[1]:
        saveWeight()

def setNodeConnections(selectedNodes):
    global connections, screen, text
    print("Called")
    connection = Connection(selectedNodes, globalID(Connection).__next__())
    selectedNodes[0].addConnection(connection)
    selectedNodes[1].addConnection(connection)
    connections.append(connection)
    increaseMode(2)
    
def eventManager(event):
    if event.type == pygame.QUIT: quit()
    elif event.type == pygame.MOUSEBUTTONDOWN: mouseButtonDown(event)
    elif event.type == pygame.MOUSEBUTTONUP: return
    elif event.type == pygame.KEYDOWN: keyPressed(event)

if __name__ == "__main__":
    main()
    mainLoop()


pygame.quit()
