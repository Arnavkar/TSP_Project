class Point: #Point object

    def __init__(self,list):
        self.x = list[0]
        self.y = list[1]

    def getDistance(self,point):
        sq_distance = (self.x - point.x)**2 + (self.y - point.y)**2
        distance = sq_distance**(0.5)
        return distance

    def toList(self): #Mostly for debugging purposes
        ls = [self.x,self.y]
        return ls
