from Graph import *

print("\nWelcome to Graph App 1")
print("========================\n")

#Generate a Graph using a 2D Grid
nx,ny=map(int,input("Enter Total Grid Size Nx and Ny: ").split())

mygraph=Graph(nx,ny) #instantiate Graph using all weights to zero by default
mygraph.form2DGrid() # connect edges to form an (unweighted) 2D grid
mygraph.displayInfoGraph() #Display the graph info

# if Nvertex<=9, display the matrix
if mygraph.getnVertex()<=9: mygraph.displayAdjMat()


#Plot the main graph
mygraph.plot("gray")

