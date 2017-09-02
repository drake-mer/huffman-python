import sys
import pprint
import random
import string

class Node:
    """ A Node is is a data structure made of 
    - a character (the data)
    - two pointers to another Node (left and right)
    """
    def __init__(self, content):
        self.content = content
        self.left = None
        self.right = None

    def __repr__(self):
        return str(
            # returns a string representation of a 3-uplet containing the data in the Node
            (
                self.content,  # the node content
                self.right.content if self.right else None,  # right node content
                self.left.content if self.left else None,    # left node content
            )
        )
    
    def getCode(self, codeMap, codeList=[]):
        """
        """
        if self.content[1] != '':
            codeMap[self.content[1]] = codeList
        else:
            if self.left is not None:
                self.left.getCode(codeMap, codeList=[x for x in codeList]+[0])
            if self.right is not None:
                self.right.getCode(codeMap, codeList=[x for x in codeList]+[1])
            

        

def makeTree(nodeList):
    nodeList.sort(key=lambda x: x.content, reverse=True)

    if len(nodeList)==1:
        """ extra special case when the encoded buffer contains always the same byte.
        Notice that it doesn't make sense for huffman coding"""
        node = nodeList.pop()
        newNode = Node( (node.content[0],'') )
        newNode.right = node
        return newNode
        
    while len(nodeList) > 1 :
        a = nodeList.pop()
        b = nodeList.pop()
        newNode = Node( (a.content[0]+b.content[0],'') )
        newNode.left, newNode.right = (a,b) if a.content>b.content else (b,a)
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


def encode( byteGenerator, hashmap ):
    myCode={}
    output = []
    tree(hashmap).getCode(myCode)
    
    for x in byteGenerator:
        output = output + myCode[x]
        
    return output

def decode(codeTree, boolList):
    """ the convention is 0: to the left, 1: to the right """
    output = []
    workTree = codeTree
    for boolean in boolList:
        workTree = workTree.right if boolean else workTree.left
        
        if workTree.content[1]!='':
            output.append(workTree.content[1])
            workTree=codeTree
            
    return output

def main():
    byteStrings = [ "a"*random.randint(10,100),
                    "aaaaaaaaaabc",
                    "bbbbbbbbbba",
                    "aaaaaaaabbbbbbbbbbbccccccccc",
                    string.ascii_letters,
                    string.ascii_letters+"aabb",
                    ''.join(random.sample(string.ascii_letters,9)) ]
    for testString in byteStrings:
        test(testString)
        
def test(testString):
    codec = {}
    hashmap = count(testString)
    print("source : "+testString)
    myTree = tree(hashmap)
    assert myTree.content[0] == len(testString)
    myTree.getCode(codec)
    encodedBytes=encode(testString, hashmap)
    decodedBytes=decode(myTree, encodedBytes)
    print("decoded: "+''.join(decodedBytes))
            
    assert testString==''.join(decodedBytes)
        
if __name__=='__main__':
    main()
