'''Pathfinder module ©️ Tigo.robotics 2022'''
#package for AStar algorithm
from math import sqrt, log
from copy import deepcopy
#toAAA
from math import sqrt, log
def toAAA(number):
    debug=1
    SYMB_RANGE=26 #this is the range of characters we want to select from
    SYMB_BEG=65 #this is the beginning number of characters from unicode
    #use following to unlock Chinese characters
    #SYMB_RANGE=0x9FFF-0x4E00
    #SYMB_BEG=0x4E00
    current = number
    if current >= SYMB_RANGE:
        num_iter=log(current) // log(SYMB_RANGE)
        num_iter=int(num_iter)
    else:
        num_iter=0
    buff=''
    while num_iter >= 0:
        offset=current//SYMB_RANGE**num_iter
        offset %= SYMB_RANGE
        buff+=str(chr(SYMB_BEG+offset))
        num_iter-=1
    return buff

#knowing 'AAA' means 000 which is just 0
#assert 'A' == toAAA(0)
#assert 'B' == toAAA(1)
#assert 'Z' == toAAA(25)
#assert 'BA' == toAAA(26)
#assert 'BAA' == toAAA(676)


class Node:
    def __init__(self,name):
        self.nodelist = []
        self.costlist = []
        self.name=name
        self.x=-1
        self.y=-1
        self.f_cost=10*10
        self.g_cost=0
        self.h_cost=0
        self.parent=None #this is for traversal
    def add_node(self,node,cost):
        if node == None:
            return
        self.nodelist.append(node)
        self.costlist.append(cost)
    def del_node(self,node):
        if node in self.nodelist:
            return self.nodelist.remove(node)
        return None
    def get_cheapest(self,bypass_list):
        smallest=10*10
        index_smallest=-1
        for i,v in enumerate(self.costlist):
            if self.nodelist[i] in bypass_list:
                continue
            if smallest > v:
                smallest=v
                index_smallest=i
        if index_smallest >= 0:
            return self.nodelist[index_smallest]
        else:
            return None
    def get_node(self,name):
        for i in self.nodelist:
            if i.name==name:
                return self
        return None
    #how the class can be known from the outside world.
    def __repr__(self):
        output=''
        for s in self.nodelist:
            output+=s.name+','
        #return self.name+':'+output
        return self.name+' '
    #heuristic function calculation: euclidean
    #however there is no obvious use of the connection weights if we only consider the direct distance.
    def calc_f_cost(self,target):
        self.h_cost=sqrt((self.x-target.x)**2 + (self.y-target.y)**2)
        self.f_cost=self.h_cost+self.g_cost
        #self.f_cost=self.h_cost
class AStar:
    def get_node_string(self, number):
        if number<=90 and number>=65:
            return str(chr(a))
        else:
            buff=''
            buff+=str(chr(number))
    def __init__(self,in_grid=None, start='A', goal='X', debug=0):
        # 1 is pathway, row is x position, coloumn is y. #2 is goal, #3 is start
        #we are going to replace every 1s to a node.
        self.allow_diagnals=0
        self.debug=debug
        self.start=start
        self.goal=goal
        if not in_grid:
            print('pdf04:WARNING:in_grid is empty, creating an example Grid')
            in_grid=[[3,1,1,0,1,1,1,1],
                     [1,1,1,1,1,0,1,1],
                     [1,1,1,1,0,1,1,2],
                     [1,1,1,0,0,0,0,0]]
        self.data=deepcopy(in_grid)
        a=0 #keep track of index
        #going through all item in this 2d array
        for y,i in enumerate(self.data):
            for x,j in enumerate(i):
                if self.data[y][x] in (0,10,11):
                    self.data[y][x]=None
                else:
                    if self.data[y][x]==2:
                        self.goal=toAAA(a)
                    if self.data[y][x]==3:
                        self.start=toAAA(a)
                    self.data[y][x]=Node(toAAA(a))
                    self.data[y][x].x=x
                    self.data[y][x].y=y
                a+=1
        #then we hook up the nodes to form a graph
        for y,i in enumerate(self.data):
            for x,j in enumerate(i):
                try:
                    if not self.data[y][x]: continue
                    if y-1>=0:self.data[y][x].add_node(self.data[y-1][x], 10)
                    if y+1<len(self.data):self.data[y][x].add_node(self.data[y+1][x], 10)
                    if x-1>=0:
                        self.data[y][x].add_node(self.data[y][x-1], 10)
                        if self.allow_diagnals:
                            if y-1>=0:self.data[y][x].add_node(self.data[y-1][x-1], 14)
                            if y+1<len(self.data):self.data[y][x].add_node(self.data[y+1][x-1], 14)
                    if x+1<len(self.data[y]):
                        self.data[y][x].add_node(self.data[y][x+1], 10)
                        if self.allow_diagnals:
                            if y+1<len(self.data):self.data[y][x].add_node(self.data[y+1][x+1], 14)
                            if y-1>=0:self.data[y][x].add_node(self.data[y-1][x+1], 14)
                except IndexError:
                    pass
        if debug:
            for row in self.data:
                for cell in row:
                    if cell: print(cell,end='')
                    else: print('#, ',end='')
                print('')
    '''
    here we have a list of nodes, the cost list of each node interconnecting is marked. However this cost is only the cost of travelling between each other.
    this costlist have importance when the maze has different obstacles like water etc.
    math.sqrt(x**2 + y**2) --> straight line distance.
    '''
    def solve(self):
        opened=[]
        closed=[]
        data=self.data
        start=self.start
        goal=self.goal
        debug=self.debug
        #so go get the starting node from the grid.
        for i in data:
            for j in i:
                if not j:continue
                if j.name==start:
                    opened.append(j)
                    start=j
                elif j.name==goal:
                    goal=j
        if goal and debug:print(opened, 'goal is set to:',goal.name)
        target_not_found=True
        while target_not_found:
            cheapest_cost=10**10#large number
            cheapest_node_in_opened=None
            for o in opened:
                if o.f_cost==10**10:
                    o.calc_f_cost(goal)
                if o.f_cost<cheapest_cost:
                    cheapest_cost=o.f_cost
                    cheapest_node_in_opened=o
            #at this point we have cheapest node in opened:
            if debug:print(cheapest_node_in_opened,end='->')
            if len(opened)>0:
                opened.remove(cheapest_node_in_opened)
            else:
                if debug:print('cannot solve!')
                break
            closed.append(cheapest_node_in_opened)
            if cheapest_node_in_opened==goal:
                target_not_found = False
                goal.parent=cheapest_node_in_opened.parent
                if debug:print('found target!',closed)
            for n in cheapest_node_in_opened.nodelist:
                if n in closed:
                    continue
                if n not in opened:
                    n.g_cost=cheapest_node_in_opened.g_cost+1
                    n.calc_f_cost(goal)
                    opened.append(n)
                n.parent=cheapest_node_in_opened
        resolved_path=[]
        checker=goal
        resolved_path.append(checker)
        while checker.parent:
            #print(checker.parent.name)
            checker=checker.parent
            resolved_path.append(checker)
        if debug:print('Ans:',resolved_path[::-1])
        return resolved_path[::-1]
if __name__=='__main__':
    print('running astar solver in demo mode.')
    asolv=AStar(debug=True)
    print(asolv.solve())