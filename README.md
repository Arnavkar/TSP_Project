# TSP VISUALIZER

The project is a CLI program that will determine the shortest possible route for X number of points in a 2D space, with the user choosing a different algorithm to solve the problem. The best determined route will then be animated/visualized via the matplotlib library's graphing features.

3 different text files with random points are provided in the TextFiles/ directory, where the number in the file name denotes the number of points in that file

## Project Setup

```
virtualenv venv
source venv/bin/activate #For Macbook users
pip install -r requirements.txt
python main.py -h #Show info on how to use the CLI program
```
## Currently Implemented Algorithms
- Random Route
- Nearest Neighbour
- Smallest Increment/Insertion
- Genetic Algorithm

## To Implement
- Ant Colony Optimization
- Randomized Improvement - Markov Chains


## To Improve / modify
- Implementation of genetic algorithm can be varied, especially the "gene crossover"

Let me know if you think this might be cool as a web app! 
