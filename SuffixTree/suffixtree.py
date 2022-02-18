from itertools import chain


class SuffixTree(object):

    class Node(object):
        def __init__(self, label):
            self.label = label
            self.out = {}    

        def __iter__(self):
            return chain((self.label,), *map(iter, self.out))
                

    s = ""
    
    def __init__(self,s):
        s += '$'
        self.s = s
        self.root = self.Node(None)
        self.root.out[s[0]] = self.Node(s) #Adding longest suffix
        for i in range(1, len(s)): #adding all suffixes - Longest -> shortest
            cur = self.root
            j = i
            while j < len(s):
                if s[j] in cur.out:
                    print("s[j] " + s[j])
                    child = cur.out[s[j]]
                    print("child " + str(child.label))
                    label = child.label
                    k = j+1
                    while k-j < len(label) and s[k] == label[k-j]: #Checking if mismatched suffix or made it to the end of the edge
                        k += 1
                    if k-j == len(label): #made it to the end of the edge
                        cur = child
                        j = k
                    else:
                        #split an edge (uv edge -> u edge and v edge)
                        cExist, cNew = label[k-j], s[k]
                        newNode = self.Node(label[:k-j]) # :k-j represents first item to k-j
                        newNode.out[cNew] = self.Node(s[k:])
                        newNode.out[cExist] = child #Assigns original child to the new node
                        child.label = label[k-j:] #Updates child label
                        cur.out[s[j]] = newNode #Assigns newNode as new child of parent node
                else:
                    cur.out[s[j]] = self.Node(s[j:]) #Exited at node, making new edge from node

    def printTree(self, Node):
        if Node == None:
            cur = self.root
        while cur.out is not None:
            for s in cur.out:
               if s in cur.out:
                   print(s)
                   cur = cur.out[s]
    
    def followPath(self, s):
        cur = self.root
        i = 0
        while i < len(s):
            c = s[i]
            if c not in cur.out:
                return (None, None)
            child = cur.out[s[i]]
            label = child.label
            j = i+1
            while j-i < len(label) and j < len(s) and s[j] == label[j-i]:
                j +=1
            if j-i == len(label):
                cur = child
                i = j
            elif j == len(s):
                return (child, j-i)
            else:
                return (None, None)
        return (cur, None)

    def hasSubstring(self,s):
        #Returns true if s appears as a substring
        node, off = self.followPath(s)
        return node is not None

    def hasSuffix(self,s):
        #Return true if s is a suffix
        node, off = self.followPath(s)
        if node is None:
            return False
        else:
            return node.label[off] == '$'

        

            
    

