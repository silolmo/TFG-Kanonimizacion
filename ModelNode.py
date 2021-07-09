import BD

class Node:
    def __init__(self, value):
        self.value = value
        self.dimension = len(value)
        self.mark = False
        self.frequencySet = {}
        self.fathers = []
    
        nodes = BD.bd_nodes.exist(self.dimension)
        edges = BD.bd_edges.exist(self.dimension)
        if(self.dimension==0 or nodes==False):
            self.root = False
            self.id = 0
        else:
            self.id = BD.bd_nodes.getId(value)
            if(edges==False):
                self.root = False
            else:
                self.root = BD.bd_nodes.isRoot(value)

    def getId(self):
        return self.id

    def getValue(self):
        return self.value

    def getDimension(self):
        return self.dimension

    def getMark(self):
        return self.mark

    def getRoot(self):
        return self.root

    def getFrequencySet(self):
        return self.frequencySet

    def getFathers(self):
        return self.fathers
    
    def setFather(self, father):
        self.fathers.append(father)

    def setMark(self, mark):
        self.mark = bool(mark)

    def setFrequencySet(self, frequencySet):
        self.frequencySet = frequencySet

    @staticmethod
    def getFrequencySetByDimension(quasiidentifiers,dimension):
        attributes = []
        for i in range(dimension):
            attributes.append(quasiidentifiers[i])
        frequencySet = {}
        data = list(BD.bd_data.getDataByAttributes(attributes))

        while len(data)!=0:
            item = data.pop()
            frequencySet[item] = data.count(item)+1
            for i in range(data.count(item)):
                data.remove(item)  

        return frequencySet    

    @staticmethod
    def getFrequencySetByFather(quasiidentifiers,frequencyFather, node):
        frequencySet = {}
        for key, value in frequencyFather.items():
            aux = []
            for i in range(len(node.getValue())):
                attribute = quasiidentifiers[i]
                level = BD.bd_hierarchy.getLevel(attribute, key[i])
                aux.append(BD.bd_hierarchy.getGeneralization(attribute, level, node.getValue()[i], key[i]))
            if(tuple(aux) in frequencySet.keys()):
                frequencySet[tuple(aux)] = frequencySet[tuple(aux)] + value
            else:
                frequencySet[tuple(aux)] = value
        
        node.setFrequencySet(frequencySet)

        return frequencySet