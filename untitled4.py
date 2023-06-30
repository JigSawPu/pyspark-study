import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from PIL import Image
import pandas as pd


class dfNode:
    def __init__(self, subset, q):
        self.subset = subset
        self.q = q
        self.cost = self.distCalc(self.subset, self.q).sum()
        self.weight = self.subset.shape[0]

        self.leftChild = None
        self.rightChild = None
        self.parent = None

    def distCalc(self, miniset, x):
        distances = (miniset.subtract(x.values)**2).sum(axis=1)
        return distances

    def subsetFinder(self):
        dist = self.distCalc(self.subset, self.q)
        # max_dist_index = np.unravel_index(np.argmax(dist, axis=None),
        #                                   dist.shape)[1]
        max_dist_index = dist.idxmax()  # change3
        q2 = self.subset.loc[max_dist_index]
        q2 = q2.to_frame().transpose()
        q2dist = self.distCalc(self.subset, q2)
        group_dist = pd.concat([dist, q2dist], axis=1)
        nearest_indices = group_dist.idxmin(axis=1)
        subset1 = self.subset[nearest_indices == 0]
        subset2 = self.subset[nearest_indices == 1]
        return (subset1, self.q), (subset2, q2)


class CoreSetTree:
    def __init__(self, X, m):
        self.wholeSet = X
        self.m = m
        self.coreset = pd.DataFrame([])

    def fit(self):
        q1 = self.wholeSet.sample()
        self.coreset = pd.concat([self.coreset, q1])
        self.Root = dfNode(self.wholeSet, q1)

        for i in range(self.m):
            self.maxnode = None
            self.maxcost = 0
            # self.visit(self.Root)
            # self.addChild(self.Root)
            self.propagateUp(self.Root)

    def addChild(self, node):
        stack = []
        stack.append(node)
        while stack:
            curr = stack.pop()
            if type(curr.leftChild) is type(None) and type(curr.rightChild) is type(None):
                if curr.cost == self.MaxNodeCost:
                    childs = self.MaxNode.subsetFinder()
                    self.coreset = pd.concat([self.coreset, childs[1][1]])
                    curr.leftChild = dfNode(childs[0][0],
                                            childs[0][1])
                    curr.rightChild = dfNode(childs[1][0],
                                             childs[1][1])
                    curr.rightChild.parent = curr
                    curr.leftChild.parent = curr
            if curr.rightChild:
                stack.append(curr.rightChild)
            if curr.leftChild:
                stack.append(curr.leftChild)

    def visit(self, node):
        stack = []
        stack.append(node)
        while stack:
            curr = stack.pop()
            if type(curr.leftChild) is type(None) and type(curr.rightChild) is type(None):
                if curr.cost >= self.MaxNodeCost:
                    self.MaxNode = curr
                    self.MaxNodeCost = curr.cost
            if curr.rightChild:
                stack.append(curr.rightChild)
            if curr.leftChild:
                stack.append(curr.leftChild)

    def propagateUp(self, root):
        q = deque()
        q.append(root)
        ans = deque()
        while q:
            node = q.popleft()
            if node is None:
                continue
            ans.appendleft(node)
            if node.rightChild:
                q.append(node.rightChild)
            if node.leftChild:
                q.append(node.leftChild)
        for node in ans:
            if type(node.leftChild) is type(None) and type(node.rightChild) is type(None):
                if node.cost >= self.maxcost:
                    self.maxcost = node.cost
                    self.maxnode = node
        childs = self.maxnode.subsetFinder()
        self.coreset = pd.concat([self.coreset, childs[1][1]])
        for node in ans:
            if node == self.maxnode:
                node.leftChild = dfNode(childs[0][0],
                                        childs[0][1])
                node.rightChild = dfNode(childs[1][0],
                                         childs[1][1])
                node.rightChild.parent = node
                node.leftChild.parent = node
        ans.appendleft(node.rightChild)
        ans.appendleft(node.leftChild)
        ans.pop()
        while ans:
            left = ans.popleft()
            right = ans.popleft()
            left.parent.cost = left.cost + right.cost


mandril = Image.open('/home/aryakumar/Downloads/mandril.jpg')
mandril
mandril_rgb = np.array(mandril.getdata())
dfmandril = pd.DataFrame(mandril_rgb)
dfmandril.drop_duplicates(inplace=True)
tt = CoreSetTree(dfmandril, 1000)
tt.fit()
