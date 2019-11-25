# Network

Python files for the creation and solving of networks.
This was split into 2 files so that I could test python's Pickling. This could be very easily combined into one program.

## Dependencies:

  Requires pygame to work. Installation instructions for pygame can be found: [here](https://www.pygame.org/wiki/GettingStarted)
  
  The "With Module" files require Network Base to be imported and initialised.
  
  **Note:** The module must be in the same directory as NetworkCreator.py and NetworkSolver.py
  
  ### Usage:
  
  ```python
  from NetworkBase import *
  import pygame
  
  ...
  
  initialiseModule(pygame.surface, pygame.font) #To be used to display the nodes and connections.
  ```
  
  ### Network Creator:
  
  Cycle between *Place Nodes* and *Add Connections* modes with *'='* key or by *scrolling* with middle mouse button.
  
  *Escape:* Quits program.
  
  ***Place Nodes Mode:***
  
  *Left Click:* Adds node where your mouse is.
  
  *Right Click:* Removes previously placed node.
  
  *Return:* Changes mode to: *Name Network Save*.
  
  ***Add Connections Mode:***
  
  *Left Click:* Selects first and second node for connection.
  
  ↳ When second node is selected, changes mode to: *Set Weight*.
  
  *Right Click:* Clears selected nodes. 
  
  *Return:* Changes mode to: *Name Network Save*.
  
  ***Set Weight Mode:***
  
  *Numbers:* Sets weight of connection.
  
  *Backspace:* Removes previous number from weight.
  
  *Return or Middle Click:* Saves weight.
  
  ↳ Changes mode back to: *Add Connection*.
  
  ***Name Network Save:*** 
  
  *Typing:* Characters typed will be added to the name of the network, which is used to save it.
  
  *Backspace:* Removes previous character from name.
  
  *Return:* Saves network as: networkname.lvl
  
  ↳ If that file already exists, you will be prompted to change the name of the network.
  
  ### Network Solver:
  
  Initially you will be prompted for a filepath for the network file (the .lvl is optional).
  
  If the file exists, the network will be opened up in *Set Start Node* mode. 
  
  Cycle between *Set Start Node* and *Set End Node* modes with *'='* key or by *scrolling* with middle mouse button.
  
  *Escape:* Quits program.
  
  ***Set Start Node:***
  
  *Left Click:* Sets start node, overriding previous start node.
  
  *Right Click or Return:* Changes the mode to: *Solve*.
  
  ↳ Only is the start node and end node has been set.
  
  ***Set End Node:***
  
  *Left Click:* Sets end node, overriding previous end node.
  
  *Right Click or Return:* Changes the mode to: *Solve*.
  
  ↳ Only is the start node and end node has been set.
  
  ***Solve:***
  
  Solves the network, from the start node to the end node.
  
## Files: 

    These could just as easily be combined into one single file, however, I specifically seperated them 
    so that I could test Python's pickling.
    
  - Network Base:
    
    >The module used within the "With Module" folder. It contains the shared functionality and classes of the two following files.
    
  - Network Creator: 
  
    >Creates the network and then saves it as a .lvl file which
    can be access by the Level Solver file.
   
  - Network Solver:
    
    >Loads a network and finds the shortest distance from a selected start node to 
    a selected end node using Dijkstra's algorithm.
    
    more info on Dijkstra's algorithm can be found on the wikipedia page: [here](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
    
    
    
    
