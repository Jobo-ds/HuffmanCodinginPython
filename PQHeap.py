
## Imports


import math


## Auxiliary Methods


def Left(i):
    i = 2*i+1
    return i

def Right(i):
    i = 2*i+2
    return i

def Parent(i):
    i = math.floor((i - 1)/2)
    return i

def createEmptyPQ():
    pq = []
    return pq


## Heap Methods


def extractMin(A):
    Min = A[0]
    A[0], A[-1] = A[-1], A[0]   
    A.pop()                     
    minHeapify(A,0)
    return Min

def insert(A,e):
    A.append(e)                                     
    i = len(A)-1                                   
    while i > 0 and A[Parent(i)] > A[i]:            
        A[i], A[Parent(i)] = A[Parent(i)], A[i]     
        i = Parent(i)                               
    
def minHeapify(A,i):
    if len(A) == 0:
        return A
    l = Left(i)     
    r = Right(i)    
    if l <= len(A)-1 and A[l] < A[i]:
        smallest = l
    else:
        smallest = i
    if r <= len(A)-1 and A[r] < A[smallest]:
        smallest = r
    if A[smallest] != A[i]:
        A[i], A[smallest] = A[smallest], A[i]
        minHeapify(A, smallest)




