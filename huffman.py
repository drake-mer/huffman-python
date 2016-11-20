import sys
import pprint
import copy

class Node:
    
    def __init__(self, content):
        self.content = content
        self.left = None
        self.right = None


    def __repr__(self):
        return ("'{}'-----'{}'\n      |"
        "        \n").format(self.content,self.left.content)


    def getCode(self, codeMap, codeList=[]):
        if self.content[1] == '':
            assert self.right is not None
            assert self.left is not None
            self.left.getCode(  codeMap, codeList=[x for x in codeList]+[0] )
            self.right.getCode( codeMap, codeList=[x for x in codeList]+[1] )
        else:
            codeMap[self.content[1]] = codeList


def makeTree(nodeList):
    nodeList.sort(key=lambda x: x.content, reverse=True)
    while len(nodeList) > 1 :
        a = nodeList.pop()
        b = nodeList.pop()
        newNode = Node( (a.content[0]+b.content[0],'') )
        newNode.left = min( a, b, key=lambda x: x.content )
        newNode.right = max( a, b, key=lambda x: x.content ) 
        nodeList.append(newNode)
        nodeList.sort(key=lambda x: x.content, reverse=True)
    return nodeList.pop()

    



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
    nodeList=[]
    for (key, value) in hashMap.items():
        nodeList.append( Node((value, key)) )
    myTree = makeTree( nodeList )
    return myTree

def code( byteGenerator ):
    hashMap = count(byteGenerator)
    myTree = Tree()
    myCode = myTree.getCode()
    print(myCode)

def encode( byteGenerator ):
    hashMap=count(byteGenerator)
    myTree=tree(hashMap)


def main():
    myByteGenerator = "aaaaaabbbbbbbbbbbbbbbbbbbbbccccccccccccccccccccccddddddddddddddeejjhffqq"
    hashMap = count(myByteGenerator)
    myTree = tree(hashMap)
    my = {}
    myTree.getCode(codeMap=my)
    x=sorted([ (k,v) for k,v in my.items() ], key=lambda x : len(x[1]))
    print(pprint.pformat(x))
        

if __name__=='__main__':
    main()
