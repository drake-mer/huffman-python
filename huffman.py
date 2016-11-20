import sys
import pprint

class Node:
    
    def __init__(self, content):
        self.content = content
        self.left = None
        self.right = None



    def __repr__(self):
        return ("'{}'-----'{}'\n      |"
        "        \n").format(self.content,self.left.content)



    def getLeftNode(self):
        return self.left
    
    
    def getRightNode(self):
        return self.right



class Tree:
    def __init__(self, rootNode = None):
        self.rootNode=Node('')
        self.curNode=self.rootNode



    def __repr__(self):
       curNode = self.rootNode
       output = ''
       while curNode.left is not None and curNode.right is not None:
            output+=str(curNode)
            curNode = curNode.right
       return output


    def buildNode(self, key):
        if self.curNode.left is None:
                self.curNode.left = Node( key )
        elif self.curNode.right is None:
                self.curNode.right = Node( key )
        else:
            self.curNode = self.curNode.right
            assert isinstance(self.curNode, Node)
            assert self.curNode.left is None
            assert self.curNode.right is None
            self.buildNode(key)



    def makeTree(self, sortedTupleList):
        for byte, count in sortedTupleList:
            self.buildNode((byte,count))  



def lazyReader(fname):
    f=open(fname)
    x = f.read(1)
    while x:
        yield x
        x = f.read(1)
    f.close()

def count( byteGenerator ):
    hashMap = {}
    for byte in byteGenerator: 
        if byte in hashMap:
            hashMap[byte] += 1
        else:
            hashMap[byte]=1
    return hashMap

def tree( hashMap ):
    my = sorted([(x,y) for x,y in hashMap.items()], key=lambda x: (x[1],x[0]), reverse=True)
    myTree = Tree()  
    myTree.makeTree(my)
    return myTree


def main():
    hashMap = count(lazyReader(sys.argv[1]))
    print(tree(hashMap))
    with open(sys.argv[1]+'.dict','w') as f:
        f.write(pprint.pformat(hashMap))
    
        

if __name__=='__main__':
    main()
