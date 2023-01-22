### Your NAME: Bryan Leung
###

from tkinter import *
from Stack import *
from Queue import *
from Heap import *
import sys

class Vertex:
    def __init__(self,i,j):
        self.i=i
        self.j=j
        self.visited = False
        self.increment = 1
    """Returns Coordinate of Vertex"""
    def __str__(self):
        return "(%s,%s)"%(self.i,self.j)
class Edge:
    def __init__(self,source=0,dest=0,weight=1):
        self.s = source
        self.d = dest
        self.w= weight
    def __str__(self):
        return "(%s,%s)  %s"%(self.s,self.d,self.w)
    """Operator overloading methods __gt__ and __lt__. Returns true if comparison is correct. Otherwise, false."""
    def __gt__(self,y):
        if self.w>y:
            return True
        else:
            return False
    def __lt__(self,y):
        print(self)
        print(y)
        if self.w<y:
            return True
        else:
            return False

class Graph:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y 
        self.maxNodes = x*y # Create x by y zeros list. 
        self.nodes=[] #list of Vertex
        self.mat=[] #adj. 2D Matrix
        self.default=0
        for i in range(self.maxNodes):
            self.mat.append([0]*self.maxNodes) ### x by y list.


    def form2DGrid(self):
        help=Graph(self.x,self.y) ### Graph object
        possible=[] ## Empty list
        if len(self.nodes) >= self.x*self.y:
            print("Graph full") ### Full graph
            return
        for i in range(0,self.y):
            for j in range(0,self.x):
                self.nodes.append(Vertex(j,i)) ### Create x by y coordinates with Vertex object. 
        self.fix=self.nodes ### Used self.fix, so that BFS and DFS methods can use Vertex objects in App 2 and 3. 
        for m in range(len(self.nodes)): 
            for v in range(len(self.nodes)): ### Scan through two pairs of each Vertex coordinate.
                job1=self.nodes[m] 
                job2=self.nodes[v]
                dist=((job1.i-job2.i)**2+(job1.j-job2.j)**2)**0.5 # Check distance
                if dist == 1.0 and [job2,job1] not in help.nodes: ### addEdge for two coordinates of two vertexes if distance is 1.0.
                    self.addEdge(job1,job2,1)
                    possible+=[str(job1)+" <==> "+str(job2)+" "+str(self.mat[m][v])] ### Put print statements in possible list. 
                    help.nodes+=[[job1,job2]] ### Use help.nodes to get [[Coordinates 1 , Coordinates 2]] format. 
        self.nodes=help.nodes ### Make self.nodes the [[Coordinates 1 , Coordinates 2]] format. 

    def load2DGrid(self,input):
        self.change=[]
        ### This method helps to test if the file exist. Otherwise, use sys.exit() to leave program. 
        try:
            f1=open(input,"r")
            self.nodes=[]
        except:
            print("This file does not exist") 
            sys.exit()
        ### Similar to form2DGrid(), I create a vertex of x by y dimensions.
        for i in range(0,self.y):
            for j in range(0,self.x):
                self.nodes.append(Vertex(j,i))
        ### Use this node for BFS, DFS, and MSTW methods. 
        self.fix=self.nodes
        self.nodes=[]
        ### Read from file. Get rid of new lines and split by space between integers. 
        for answers in f1:
            self.nodes+=[answers.rstrip("\n").split(" ")]
        self.lbs=[]
        for solve in range(len(self.nodes)):
            self.lbs+=self.nodes[solve][2] ### Acquire weight
        self.dimens=self.x ### This controls how the coordinates are divided.
        for e in range(0,len(self.nodes)):
            x1=int(int(self.nodes[e][0])%(self.dimens)) ### For example, Node 5 in a 3 by 4 will be (5%3,5//3)=(2,1) 
            y1=int(int(self.nodes[e][0])//(self.dimens))
            x2=int(int(self.nodes[e][1])%(self.dimens))
            y2=int(int(self.nodes[e][1])//(self.dimens)) 
            self.nodes[e][0]=Vertex(x1,y1) ### Create [[Vertex(), Vertex()]] type. 
            self.nodes[e][1]=Vertex(x2,y2)
            self.addEdges(self.nodes[e][0],self.nodes[e][1],int(self.nodes[e][2])) ### Add edges.  
        self.change=self.nodes ### Have this display a list of Vertexes with Weights 
    """The two addEdge(s)() methods are very similar. The difference is one uses self.nodes and the other uses self.fix 
    with a format of [Vertex()]. As I scan through Vertex objects, if there is a match, between coordinates, I change 
    an index in self.mat to a value other than one."""
    def addEdge(self,c1,c2,weight):
        i1,i2=None,None
        for i in range(len(self.nodes)):
            n=self.nodes[i]
            if str(n)==str(c1):
                i1=i
            if  str(n)==str(c2): 
                i2=i
            if (i1 is not None) and (i2 is not None):
                self.mat[i1][i2] = weight
                self.mat[i2][i1] = weight

    def addEdges(self,c1,c2,weight):
        i1,i2=None,None
        for i in range(len(self.fix)):
            n=self.fix[i]
            if str(n)==str(c1):
                i1=i
            if  str(n)==str(c2): 
                i2=i
            if (i1 is not None) and (i2 is not None):
                    self.mat[i1][i2] = weight
                    self.mat[i2][i1] = weight
    """In this method, I scan through my list of vertexes. I use try/except to catch scenarios where 
    self.mat[m][v] doesn't work and set them to 1. Then, everytime self.mat[m][v] is not zero and there is
    no repeat of coordinates, I add a print statement to the possible list. I also increment self.weight by 
    save. Meanwhile, for App3, I use self.change(equals to self.node in Load2DGrid(). From self.nodes in App3, 
    I print out indexes of self.change and increment self.weight by int(self.change[i][2]). I return final weight."""
    def displayInfoGraph(self):
        print("\nList of edges + weights: ")
        possible = []
        self.weight=0
        ### Look through all the Vertex objects in self.nodes. 
        for m in range(len(self.nodes)):
            for v in range(len(self.nodes)): 
                job1=self.nodes[m] 
                job2=self.nodes[v]
                ### Find out self.mat[m][v]. If it doesn't exist, set save=1.
                try:
                    save1=job1[2]
                    save2=job2[2]
                except:
                    save1=1
                    save2=1
                ### Total incremented weight. Create a list of print statements. 
                if save1!=0 and str(job1[0])+" <==> "+str(job1[1]) not in possible:
                        possible+=[str(job1[0])+" <==> "+str(job1[1])]+[str(save1)]
                        self.weight+=int(save1) 
                if save2!=0 and str(job2[0])+" <==> "+str(job2[1]) not in possible:
                        possible+=[str(job2[0])+" <==> "+str(job2[1])]+[str(save2)]
                        self.weight+=int(save2)
        hold=self.weight
        try:
            self.weight=0                
            for i in range(0,len(self.change)):
                print(self.change[i][0],"<==>",self.change[i][1],self.change[i][2])
                self.weight+=int(self.change[i][2])
            self.nodes=[]
            for j in range(0,len(self.change)):
                self.nodes+=[[self.change[j][0],self.change[j][1],self.change[j][2]]]
        except:
            self.weight=hold
            for m in range(0,len(possible),2):
                print(possible[m],possible[m+1])
                self.nodes[m//2]+=[possible[m+1]]
        print("Total weight: "+str(self.weight))
        return self.weight

    """Here, I graph out ovals and lines. I return the color. For each dots, I use dimensions self.x and self.y. I use
    fracx and fracy to orient the ovals to be symmetric. I have self.nodes[m][2] for App3 to give out the correct weight."""
    def plot(self,c):
        root=Tk()
        w=80*self.x
        h=80*self.y
        canvas = Canvas(root, width=w,height=h,bg="white")
        fracx = self.x+1
        fracy = self.y+1
        i,j=Graph.toTkinter(0,0,-1,self.x,-1,self.y,w,h)
        for k in range(0,self.x):
            for l in range(0,self.y):
                canvas.create_oval(w/fracx+k*w/fracx-10,
                h/fracy+l*h/fracy-10,
                w/fracx+k*w/fracx+10,
                h/fracy+l*h/fracy+10,fill=c) ### Minor adjustments to display well.
        for m in range(0,len(self.nodes)):
            try:
                canvas.create_line(
                i+self.nodes[m][0].i*w/fracx,
                j-self.nodes[m][0].j*h/fracy,
                i+self.nodes[m][1].i*w/fracx,
                j-self.nodes[m][1].j*h/fracy,width=3*int(self.nodes[m][2]),fill=c) 
            except:
                canvas.create_line(
                i+self.nodes[m][0].i*w/fracx,
                j-self.nodes[m][0].j*h/fracy,
                i+self.nodes[m][1].i*w/fracx,
                j-self.nodes[m][1].j*h/fracy,width=3*1,fill=c) 
        canvas.pack()
        root.mainloop()
        return c
    """This returns how many vertexes."""
    def getnVertex(self):
        return len(self.nodes)

    def displayAdjMat(self):

        print("\nMatrix: ")
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                try:
                    print(self.mat[i][j],end=" ") ### Matrix gets printed out. Otherwise, skip.
                except:
                    pass
            print()

    @staticmethod
    def toTkinter(x,y,xmin,xmax,ymin,ymax,width,height):
        i=int(((x-xmin)*width)/(xmax-xmin))
        j=int(((ymax-y)*height)/(ymax-ymin))
        return i,j

    """I have self.fix=self.nodes for App 2 and App 3. While stack is not empty, I'll visit a unvisited node. I'll then 
    pop if there's nothing. Else, I'll push another number. Finally, I'll use [[Vertex(),Vertex()]] format to get right 
    coordinates for App 2 and App 3. help.mat[current][j] = self.mat[current][j] should help get the weight. Finally, I return
    help(Graph object). I also reset self.fix indexes to not visited. """
    def dfs(self,i):
        self.fix[i].visited=True
        mystack=Stack()
        help=Graph(self.x,self.y)
        mystack.push(i)
        for m in range(self.maxNodes):
            help.mat.append([0]*self.maxNodes)
        while not mystack.isEmpty():
            current=mystack.peek() # save current node
            j=self.getAdjUnvisitedNode(current)
            if j is None:
                mystack.pop()
            else:
                self.fix[j].visited=True
                mystack.push(j)
                help.nodes+=[[self.fix[current],self.fix[j],self.mat[current][j]]]
                help.mat[current][j]=self.mat[current][j]
                #print(self.fix[current],self.fix[j],self.mat[current][j])
        for n in self.fix:
            n.visited=False 
        return help
    """Here I see whether or not self.mat is not zero and whether the node is visited or not. If statement is True,
    I return the an integer value from 0 to len(self.fix)-1. Otherwise, I return None."""
    def getAdjUnvisitedNode(self,v):
        for i in range(len(self.fix)):
            if (self.mat[v][i]!=0) and (self.fix[i].visited==False): # if unvisited
                return i # found neighbor
        return None #no such node
    def mstw(self,i):
        start = 0
        inf=9999999
        self.fix[i].visited=True
        self.N=self.x*self.y
        help=Graph(self.x,self.y)
        if self.y>self.x:
            j=self.y
        else:
            j=self.x
        while start<self.N-1:
            min=inf
            a = 0
            b = 0
            for m in range(self.N): ### m from 0 to 4
                if self.fix[m].visited: ### IF true
                    for n in range(self.N): ### n from 0 to 4
                        if ((not self.fix[n].visited) and self.mat[m][n]):
                            # not in selected and there is an edge
                            if min >= self.mat[m][n]:
                                min = self.mat[m][n]
                                a = m
                                b = n
            help.nodes+=[[self.fix[a],self.fix[b],self.mat[a][b]]]
            help.mat[a][b]=self.mat[a][b]
                            
            self.fix[b].visited = True
            start+=1
        return help

    """In bfs method, I start out with a node. I put the node inside. Then, I dequeue the node. Then, I go to
    get an unvisited Node which becomes visited. Then I add the two nodes in pairs into help.nodes and enqueue 
    the now visited node. I also have help.mat[j][k]=self.mat[j][k]. Finally, I reset self.fix to completely not visited Nodes.
    I also return help."""
    def bfs(self,i):
        self.fix[i].visited=True
        myqueue=Queue()
        myqueue.enqueue(i)
        help=Graph(self.x,self.y)
        while not myqueue.isEmpty():
            k=myqueue.dequeue()
            while True:
                j=self.getAdjUnvisitedNode(k)
                if j is None: break
                self.fix[j].visited=True
                help.nodes+=[[self.fix[j],self.fix[k],self.mat[j][k]]]
                myqueue.enqueue(j)
                help.mat[j][k]=self.mat[j][k]
        for n in self.fix: 
            n.visited=False
        return help
   
    
