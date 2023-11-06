class Graph:
    def __init__(self, graph, heuristicNodeList, startNode) -> None:
        self.graph = graph
        self.heuristicNodeList = heuristicNodeList
        self.startNode = startNode
        self.parent = {}
        self.status = {}
        self.solutionGraph = {}

    # getter and setter for status
    def getStatus(self, n):
        return self.status.get(n,0)
    def setStatus(self, n, val):
        self.status[n] = val

    # getter and setter for heuristic
    def getHeuristicNodeValue(self, n):
        return self.heuristicNodeList.get(n,0)
    def setHeuristicNodeValue(self, n, val):
        self.heuristicNodeList[n] = val

    def printSolution(self):
        print("FOR GRAPH SOLUTION, TRAVERSE THE GRAPH FROM THE START NODE:", self.startNode)
        print("------------------------------------------------------------")
        print(self.solutionGraph)
        print("------------------------------------------------------------")
    
    def startAOStar(self):
        self.aoStar(self.startNode, False)

    def getNeighbors(self, v): # gets the Neighbors of a given node
        return self.graph.get(v,'')
    
    def computeMinimumCostChildNodes(self, n):
        minCost = 0 # overall min cost across all children
        costToChildNodeListDict = {} # mapping cost to children to see what children fit the mincost bill
        costToChildNodeListDict[minCost] = []
        flag = True # are we processing first set of nodes?
        for nodeInfoTupleList in self.getNeighbors(n):
            cost = 0 # for the set
            nodeList = [] # for the set
            for node, weight in nodeInfoTupleList:
                cost = cost + self.getHeuristicNodeValue(node) + weight # add the weight and heuristic for each node throughout the set, this is a hyperarc
                nodeList.append(node) # acts as visited vector
            if flag == True:
                # if it is still the first set being visited
                minCost = cost # update min cost by default cos we need it to change
                costToChildNodeListDict[minCost] = nodeList # add to dict
                flag = False # set flag to false so it doesnt have to trigger this block anymore
            else:
                if cost < minCost:
                    minCost = cost # update minCost only when some better node is found
                    costToChildNodeListDict[minCost] = nodeList # update the nodeList accordingly (this is the hyperarc that the graph must traverse thru)
        # at the end, across all arcs and hyperarcs, return the min ones
        return minCost, costToChildNodeListDict[minCost]

    def aoStar(self, n, backTracking): # AO* algorithm for a start node and backTracking status flag
        print("HEURISTIC VALUES :", self.heuristicNodeList)
        print("SOLUTION GRAPH :", self.solutionGraph)
        print("PROCESSING NODE :", n)
        print("-----------------------------------------------------------------------------------------")

        if self.getStatus(n) >= 0:
            # only if this is true, compute min cost nodes for n
            minimumCost, childNodeList = self.computeMinimumCostChildNodes(n)
            print(minimumCost, childNodeList)
            self.setHeuristicNodeValue(n, minimumCost)
            self.setStatus(n, len(childNodeList))
            solved = True
            for childNode in childNodeList:
                # set the parent as n
                self.parent[childNode] = n
                if self.getStatus(childNode) != -1:
                    solved = solved & False
            if solved == True:
                self.setStatus(n, -1)
                self.solutionGraph[n] = childNodeList
            if n != self.startNode:
                self.aoStar(self.parent[n], True)
            if backTracking==False:
                for childNode in childNodeList:
                    self.setStatus(childNode, 0)
                    self.aoStar(childNode, False)


print ("Graph - 1")
h1 = {'A': 1, 'B': 6, 'C': 2, 'D': 12, 'E': 2, 'F': 1, 'G': 5, 'H': 7, 'I': 7, 'J': 1}
graph1 = {
    'A': [[('B', 1), ('C', 1)], [('D', 1)]],
    'B': [[('G', 1)], [('H', 1)]],
    'C': [[('J', 1)]],
    'D': [[('E', 1), ('F', 1)]],
    'G': [[('I', 1)]]
}

G1= Graph(graph1, h1, 'A')
G1.startAOStar()
G1.printSolution()