# Network

Python files for the creation and solving of networks.
This was split into 2 files so that I could test python's Pickling. This could be very easily combined into one program.

## Dependencies:

  Requires pygame to work. Installation instructions can be found: [here](https://www.pygame.org/wiki/GettingStarted)
  
  The "With Module" files require network base to be imported and initialised. This can be done by:
  
  **Note:** The module must be in the same directory as NetworkCreator.py and NetworkSolver.py
  
  ```python
  from NetworkBase import *
  
  ...
  
  initialiseModule(surface, font) #To be used to display the nodes and connections.
  ```

## Files: 

    These could just as easily be combined into one single file, however, I specifically seperated them 
    so that I could test Python's pickling.
    
  - Network Creator: 
  
    >Creates the network and then saves it as a .lvl file which
    can be access by the Level Solver file.
   
  - Network Solver:
    
    >Loads a network and finds the shortest distance from a selected start node to 
    a selected end node using Dijkstra's algorithm.
    
    more info on Dijkstra's algorithm can be found on the wikipedia page: [here](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
    
    
