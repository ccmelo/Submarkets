# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[str(k)]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]

# Paste your code for both WeightedEdge and WeightedDigraph in this box.
# You may assume the grader has provided implementations for Node, Edge, and Digraph.
class WeightedEdge(Edge):
    def __init__(self,src,dest,dist,out):
        Edge.__init__(self,src,dest)
        self.distance=dist
        self.outdoors=out
    def getTotalDistance(self):
        return self.distance 
    def getOutdoorDistance(self):
        return self.outdoors
    def __str__(self):
        return '{0}->{1} ({2},{3})'.format(self.src, self.dest, self.distance,self.outdoors)
    

class WeightedDigraph(Digraph):
    def __init__(self):
        Digraph.__init__(self)
    def addEdge(self,edge):
        src = edge.getSource()
        dest = edge.getDestination()
        weight=(float(edge.getTotalDistance()),float(edge.getOutdoorDistance()))
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[Node(src)].append([Node(dest),weight])
    def childrenOf(self,node):
        children=[]
        for c in self.edges[node]:
            children.append(c[0])
        return children
    def __str__(self):
        res = ''
        # go through each source node in graph; k=a node 
        for k in self.edges:
            #for each source node go through each child 
            for c in self.edges[k]:
                res = '{0}{1}->{2} {3}\n'.format(res, k, c[0],c[1])
        return res[:-1]