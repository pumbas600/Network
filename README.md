# Network

Python files for the creation and solving of networks.

## Dependencies:

  > Requires pygame to work. Installation instructions can be found: [here](https://www.pygame.org/wiki/GettingStarted)

## Files: 

    These could just as easily be combined into one single file, however, I specifically seperated them 
    so that I could test Python's pickling.
    
  - Level Creator: 
  
    >Creates the network and then saves it as a .lvl file which
    can be access by the Level Solver file.
   
  - Level Solver:
    
    >Loads a network and finds the shortest distance from a selected start node to 
    a selected end node using Dijkstra's algorithm.
    
    more info on Dijkstra's algorithm can be found on the wikipedia page: [here](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
    
    
