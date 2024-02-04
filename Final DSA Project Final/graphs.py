# Description: This file contains the classes for the graph and edge objects.
class Edge:
    def __init__(self, src=-1, dest=0, weight=0):
        self.src = src
        self.dest = dest
        self.weight = weight
