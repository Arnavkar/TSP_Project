
import time
from Objects.tsp import TSP
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Visualizer:
    def __init__(self,filename,mode,runs,params,enable_graph): # init visualizer , run algorithm
        self.file = filename
        self.mode = mode
        self.runs = runs
        self.genAlgoParams = params
        self.history = []
        self.tsp = TSP(filename,mode,params)
        self.enable_graph = enable_graph

    def runExperiment(self):

        totalTime = 0
        totalDist = 0

        for i in range(1, self.runs+1):

            self.tsp = TSP(self.file,self.mode,self.genAlgoParams) #New TSP object

            start = time.time() #Used to time the runtime of getPath
            self.tsp.getPath(i)
            end = time.time()

            runtime = end - start
            distance = self.tsp.totalDist()

            totalTime = totalTime + runtime
            totalDist = totalDist + distance

            if i == 1:
                self.bestDistance = distance
                self.bestTSP = self.tsp
            elif distance < self.bestDistance:
                self.bestDistance = distance
                self.bestTSP = self.tsp

            if i%10 == 0 and i >= 10:
                self.history.append((i,totalTime/i,totalDist/i))

        self.avgDist = totalDist/self.runs
        self.avgRuntime = totalTime/self.runs

        print("Run  |Avg Runtime  |Avg Distance")
        for item in self.history:
            print("{} |{:.10f} |{:.3f}".format(item[0],item[1],item[2]))
        print()
        print("Avg Runtime = {:.10f}, Avg Distance = {:.3f}, Best Dist. = {:.3f}".format(self.avgRuntime,self.avgDist,self.bestDistance))

    def configurePlot(self):

        plt.style.use("ggplot")

        if self.mode == 3: #Accounting for 2 graphs when using the genetic algo
            self.fig,self.axes = plt.subplots(1,2,figsize = (12,8))
        else:
            self.fig,self.ax = plt.subplots(figsize = (8,8))

        if self.mode == 3:
            self.axes[0].set(xlim = (0,self.tsp.width),ylim = (0,self.tsp.height))
            self.axes[0].set_xlabel("Tour")
            self.axes[1].set(xlim = (0,len(self.tsp.history)),ylim = (0,max(self.tsp.history)+200))
        else:
            self.ax.set(xlim = (0,self.tsp.width),ylim = (0,self.tsp.height))
            self.ax.set_xlabel("Tour")

    def plotPoints(self):
        self.x = []
        self.y = []
        for point in self.bestTSP.path:
            self.x.append(point.x)
            self.y.append(point.y)
        if self.mode == 3:
            self.axes[0].plot(self.x,self.y,'co',markersize = 3)
        else:
            self.ax.plot(self.x,self.y,'co',markersize = 3)

    def connectGraph(self):#Connect the end of the tour to the start
        if self.mode == 3:
            self.axes[0].arrow(self.x[-1], self.y[-1], (self.x[0] - self.x[-1]), (self.y[0] - self.y[-1]), head_width = 5,
                color = 'g', length_includes_head = True)
        else:
            plt.arrow(self.x[-1], self.y[-1], (self.x[0] - self.x[-1]), (self.y[0] - self.y[-1]), head_width = 5,
                color = 'g', length_includes_head = True)

    def animate(self,i):
        if self.mode == 3:
            if i < len(self.x)-1: #prevent index out of bounds error
                self.axes[0].arrow(self.x[i], self.y[i], (self.x[i+1] - self.x[i]), (self.y[i+1] - self.y[i]), head_width = 5,
                    color = 'g', length_includes_head = True)
        else:
            if i < len(self.x)-1: #prevent index out of bounds error
                plt.arrow(self.x[i], self.y[i], (self.x[i+1] - self.x[i]), (self.y[i+1] - self.y[i]), head_width = 5,
                    color = 'g', length_includes_head = True)

    def animateTour(self):
        self.anim = FuncAnimation(plt.gcf(),self.animate,interval = 1) #Animation to draw the tour (Not realtime)

    def plotProgress(self): #Used to Plot improvement over generations with the genetic algorithm
        self.axes[1].plot(self.bestTSP.history,'b')
        self.axes[1].set_xlabel("Generations")
        self.axes[1].set_ylabel("Distance")

    def visualize(self): #Overarching function call to visualize everything
        if self.enable_graph == 0:
            self.runExperiment()
        else:
            self.runExperiment()
            self.configurePlot()
            self.plotPoints()
            #self.connectGraph() #Draw the line connecting the head and tail of the tour
            if self.mode == 3:
                self.plotProgress()

            self.animateTour()

            plt.draw()
            plt.suptitle("Average Distance = {:.3f} units \n Average Runtime = {:.10f} s \n No. of runs = {} \n Best Distance = {:.3f} ".format(self.avgDist,self.avgRuntime,self.runs,self.bestDistance))
            plt.show()
