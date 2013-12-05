#!/usr/local/bin/python

# Obviously path dependent. Also, uses the /usr/share/dict/words webster's
# dictionary, which may or may not work on other file systems.

# If it's the first time creating the graph for an n-letter word, it will
# create the graph and then pickle a copy for later use. This was a much bigger
# deal when the CreateGraph() was dumb (big-Oh of stupid amounts of time, i.e.
# O(n^2). It now works in O(n) time, which is honestly good enough for a pretty
# complete entire English dictionary

import sys
from timeit import default_timer as clock
import copy
import heapq
import pickle

def IsOffByOneLetter(wordA, wordB):
  lA = [ord(x) for x in wordA]
  lB = [ord(x) for x in wordB]
  lD = sorted([(x - y)**2 for x,y in zip(lA,lB)])
  if lD[0:len(lA)-1] == (len(lA)-1)*[0]:
    if lD[-1] != 0:
      return True
  return False

def GetMaimedWords(word):
  altWords = []
  for i in range(len(word)):
    altWords.append(word[0:i] + '_' + word[i+1:len(word)])
  return altWords

def CreateGraph(textFile, nLetters):
  pickleFileName = 'wordList'+str(nLetters)+'.pkl'
  try:
    wordList = pickle.load(open(pickleFileName,'r'))
    return wordList
  except:
    start = clock()
    inFile = open(textFile, 'r')
    wordList = {}
    for word in inFile:
      word = word.rstrip().lower()
      if len(word) == nLetters:
        wordList[word] = [] #good, ignores duplicates
    maimed = {}
    for word in wordList:
      for altWord in GetMaimedWords(word):
        if altWord not in maimed:
          maimed[altWord] = []
        maimed[altWord].append(word)
    print 'Time taken = %.5f' %(clock()-start)
    for word in wordList:
      for maimWord in GetMaimedWords(word):
        for altWord in maimed[maimWord]:
          if altWord not in wordList[word] and altWord != word:
            wordList[word].append(altWord)
    print 'Created pre-processed graph in %.5f seconds' % (clock()-start)
    pickle.dump(wordList, open(pickleFileName, 'w'))
    return wordList

def dijkstra(graph, head, tail):
  if head not in graph:
    print 'Couldn\'t find', head, 'in dictionary!'
    return -1, 'poop'
  if tail not in graph:
    print 'Couldn\'t find', tail, 'in dictionary!'
    return -1, 'poop'

  visited = {}
  notVisited = {}
  for key in graph.keys():
    notVisited[key] = graph[key]

  heap = []
  heapq.heappush(heap, [1, head, head ])
  while heap:
    s, thisVtxKey, path = heapq.heappop(heap)
    if thisVtxKey not in visited:
      visited[thisVtxKey] = notVisited.pop(thisVtxKey)
      for vtx in graph[thisVtxKey]:
        if vtx not in visited:
          sum1 = s +1
          heapq.heappush(heap, [sum1,vtx,path+'-'+vtx])
          if vtx == tail:
            return sum1, path+'-'+vtx

  print 'Guess we couldn\'t find a path from', head, 'to', tail
  return -1, 'poop'


def main(head = 'head', tail = 'tail'):
  head = head.lower()
  tail = tail.lower()
  wordList = CreateGraph('/usr/share/dict/words', len(head))
  start = clock()
  
  theSum, path = dijkstra(wordList, head,tail)
  print 'The path is', path
  print 'with length', len(path.split('-'))-1
  print 'Time taken = %.5f' %(clock()-start)


if __name__ == '__main__':
  if len(sys.argv) == 3:
    main(sys.argv[1], sys.argv[2])
  if len(sys.argv) == 1:
    main()
  else:
    print 'Seriously. You have to give me something to work with.'
    print 'Like a beginning word and then a tail word.' 
    print 'So I\'ll just assume you want to get from the HEAD to the TAIL'
    main()
