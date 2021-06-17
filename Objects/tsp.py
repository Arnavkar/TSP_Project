import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Objects.point import Point
from Objects.geneticAlgo import GeneticAlgo

#ordered list of Point objects
class TSP:

    def __init__(self,filename,mode,params):
        self.path = []
        self.dist = 0 #total dist
        self.file = filename
        self.mode = mode
        self.genAlgoParams = params
        self.history = None #stores progress from geneticAlgo

        #get dimensions for tsp
        with open(filename,'r') as fp:
            width ,height = [int(x) for x in next(fp).split()]
            self.width = width
            self.height = height
        fp.close()

    def noAlgo(self,point): # set up a random path
        if len(self.path) < 1:
            self.path.append(point)
        else:
            randpos = random.randint(0,len(self.path)-1) #get a random position in the list
            self.path.insert(randpos,point)

    def insertNearest(self,point): #Nearest Insertion Algorithm
        if len(self.path) < 2: #case where list size = 0 or 1
            self.path.append(point)
        else:
            min = self.path[0].getDistance(point) #starting min value
            insert_idx = 1 #insert in position right after
            for idx,item in enumerate(self.path):
                temp = item.getDistance(point)
                if temp < min: #if a new min is found...
                    min = temp
                    insert_idx = idx + 1 # insert in position right after

            if insert_idx == len(self.path): #In the case where you simply append to the end
                self.path.append(point)
            else:
                self.path.insert(insert_idx,point) #otherwise insert in the correct position in the list

    def smallestIncrease(self,point): #Smallest Insertion Algorithm
        if len(self.path) < 2: #case where list size = 0 or 1
            self.path.append(point)
        else:
            #starting min_increase value
            min_increase = abs(
            (self.path[0].getDistance(point) + point.getDistance(self.path[1])) \
            - (self.path[0].getDistance(self.path[1])))

            insert_idx = 1 #set at one - assuming we append to a list of size 1 in the early case
            for idx in range(len(self.path)):

                if idx == len(self.path)-1: #case where list is of size 2
                    temp = self.path[idx].getDistance(point)

                else:
                    original_dist = (self.path[idx].getDistance(self.path[idx+1]))
                    new_dist = (self.path[idx].getDistance(point) + point.getDistance(self.path[idx + 1]))
                    temp = abs(new_dist-original_dist)

                if temp < min_increase: #If new min found
                    min_increase = temp
                    insert_idx = idx + 1 #insert in position right after object with index idx

            if insert_idx == len(self.path):
                self.path.append(point)
            else:
                self.path.insert(insert_idx,point)

    def getPath(self,n):
        with open(self.file,'r') as fp:
            fp.readline() #skip the first line

            if self.mode == 0:
                algo = self.noAlgo
            elif self.mode == 1:
                algo = self.insertNearest
            elif self.mode == 2:
                algo = self.smallestIncrease
            elif self.mode == 3:
                algo = self.noAlgo #Genetic Algo requires a base random path

            for line in fp:
                point = Point([float(x) for x in line.split()])
                #Logic for inserting ordered path list is here
                algo(point)

            fp.close()

            if self.mode == 3: #After set up, create Genetic Algo object and run the algorithm
                gen = GeneticAlgo(self.path,self.genAlgoParams)
                self.path = gen.runGeneticAlgorithm(n)
                self.history = gen.progress

    def totalDist(self): #Calculate Total Distance
        for idx,point in enumerate(self.path):
            if idx < len(self.path)-1:
                self.dist += self.path[idx].getDistance(self.path[idx+1])
            else:
                self.dist += self.path[0].getDistance(self.path[-1])
        return self.dist
