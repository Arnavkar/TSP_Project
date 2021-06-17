import random
import numpy as np
import operator
import pandas as pd
import matplotlib.pyplot as plt


class GeneticAlgo:

    def __init__(self,basepath,params):
        self.basepath = basepath
        self.basepopulation = []
        self.popSize = params["popsize"]
        self.eliteSize = params["elitesize"]
        self.mutation = params["mutation"]
        self.generations = params["generations"]
        self.progress = []

    def createPath(self): #create a random path
        path = random.sample(self.basepath,len(self.basepath))
        return path

    def initialPopulation(self): #create n random paths
        for i in range(self.popSize):
            self.basepopulation.append(self.createPath())
        return self.basepopulation

    def getFitness(self,path): #get fitness value for one path
        dist = 0
        for idx,point in enumerate(path):
            if idx < len(path)-1:
                dist += path[idx].getDistance(path[idx+1]) #dist for all points
            else:
                dist += path[0].getDistance(path[-1]) #get dist from tail to head
        fitness = 1/dist
        return fitness

    def rankPaths(self,population): # rank all paths via fitness score, sort and return and array of tuples
        results = {}
        for idx,path in enumerate(population):
            results[idx] = self.getFitness(path)
        ranking = sorted(results.items(),key = operator.itemgetter(1),reverse = True)
        return ranking

    def selection(self, ranking): #select top performers from each generation (mating pool) TOCHECK
        selectionResults = []
        #create an dataframe listing all the fitness scores
        df = pd.DataFrame(np.array(ranking), columns=["Index","Fitness"])

        df['Cum_sum'] = df.Fitness.cumsum()
        df['Percentile'] = 100*df.Cum_sum/df.Fitness.sum()

        for i in range(0, self.eliteSize): #introduce elitism and retain n best paths, based on provided elitism value
            selectionResults.append(ranking[i][0]) #append indices of selected parents

        for i in range(0, len(ranking) - self.eliteSize): #amongst the non-elite, choose additional paths best on weighted fitness val
            pick = 100*random.random() #generate random number from 0 - 100
            for i in range(0, len(ranking)):
                if pick <= df.iat[i,3]:
                    selectionResults.append(ranking[i][0])
                    break
        return selectionResults

    def matingPool(self,population,selectionResults): #extract matingpool from population
        pool = []
        for index in selectionResults:
            pool.append(population[index])
        return pool

    def breed(self,parent1, parent2): #ordered crossover based breeding
        child = []
        p1 = []
        p2 = []

        geneA = int(random.random() * len(parent1)) #get 2 random indices from one parent
        geneB = int(random.random() * len(parent1))

        if geneA < geneB: #choose a start and end index
            end = geneB
            start = geneA
        else:
            end = geneA
            start = geneB

        for i in range(start, end):
            p1.append(parent1[i])

        p2 = [item for item in parent2 if item not in p1]

        child = p1 + p2 # splice together
        return child

    def breedPopulation(self,matingpool):
        children = []
        length = len(matingpool) - self.eliteSize
        pool = random.sample(matingpool, len(matingpool))

        for i in range(0,self.eliteSize):
            children.append(matingpool[i]) #Carry over the elite population to the next generation

        for i in range(0, length): #amongst the remainder, breed child paths
            child = self.breed(pool[i], pool[len(matingpool)-i-1])
            children.append(child)
        return children

    def mutate(self,path):
        for i in range(len(path)):
            if(random.random() < self.mutation): #chance based mutation causing a swap between two points in the list
                j = int(random.random() * len(path))

                point1 = path[i]
                point2 = path[j]

                path[i] = point1
                path[j] = point2
        return path

    def mutatePopulation(self,population): #Mutate an entire population
        mutatedPop = []
        for path  in population:
            mutatedPop.append(self.mutate(path))
        return mutatedPop

    def nextGeneration(self,generation): #Get the subsequent generation
        ranked = self.rankPaths(generation)
        selection = self.selection(ranked)
        pool = self.matingPool(generation, selection)
        offspring = self.breedPopulation(pool)
        nextGeneration = self.mutatePopulation(offspring)
        return nextGeneration

    def runGeneticAlgorithm(self,n):
        print("——————————————— Experiment {} ———————————————————".format(n))
        population = self.initialPopulation()
        print("Initial distance: " + str(1 / self.rankPaths(population)[0][1]))
        self.progress.append(1 / self.rankPaths(population)[0][1]) #Append the best Distance (distance = 1/fitness)

        for i in range(1, self.generations+1):
            population = self.nextGeneration(population)
            if (i%100)==0: #Print in steps of hundred
                print("Currently breeding Generation {} - New best distance = {}".format(i,(1 / self.rankPaths(population)[0][1])))
            self.progress.append(1 / self.rankPaths(population)[0][1])

        print("Final distance: " + str(1 / self.rankPaths(population)[0][1]))
        print()
        bestRoute = population[self.rankPaths(population)[0][0]]

        return bestRoute
