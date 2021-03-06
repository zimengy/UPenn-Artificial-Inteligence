from Tkinter import *
import guiHelp
from guiHelp import *
import robotUtilities
from robotUtilities import *
import Queue

def onLine(pt, line): # check if point pt is on the line segment
    ((a1,a2),(b1,b2)) = line
    (c1,c2) = pt
    if (b1==a1) or (b2 == a2): return False
    if (((c1-a1)/(b1-a1))-((c2-a2)/(b2-a2))==0) and ((c1-a1)/(b1-a1))<=1:
        return True
    return False

def solution(solutionPath, point, sol):# find the solution path
    sol.append(point)
    while (solutionPath.get(point)!=None):
        sol.append(solutionPath.get(point))
        point = solutionPath.get(point)
    return sol

def polygonSolverBFS(start, end, polygons):
    myqueue = Queue.Queue(maxsize = 0)
    alreadyVisited = []
    solutionPath = {}
    myqueue.put(start)
    alreadyVisited.append(start)
    while(myqueue.empty()==False):
        current = myqueue.get()
        if (current == end):
            sol = []
            return solution(solutionPath, end, sol)
        # compute successors
        allLines = []
        successors = []
        for polygon in polygons:
            for i in range(len(polygon)-1):
                allLines.append((polygon[i], polygon[i+1]))
            allLines.append((polygon[-1],polygon[0]))
        allPoints = []
        for polygon in polygons:
            for nextPt in polygon:
                allPoints.append(nextPt)
        allPointsCopy = allPoints[:]
        for pt in allPointsCopy: # remove the vertice shared by two polygons
            if(allPoints.count(pt)>1):
                while(allPoints.count(pt)!=0): allPoints.remove(pt)
             
        for pt in allPoints:    # remove the vertice that form pathes intersecting other lines  
            if(pathIntersectsAnyLines(current, pt, allLines)== False):
                successors.append(pt)
        if(pathIntersectsAnyLines(current,end,allLines)==False):
            successors.append(end)
    
        while(successors.count(current)!=0): # remove the current point from its successors
            successors.remove(current)
        for pt in successors: # vertex on a line segment
            for line in allLines:
                if(onLine(pt, line)):
                    while(successors.count(pt)!=0): successors.remove(pt)
        for pt in successors: # the path to the successor should not be in the polygon
            for polygon in polygons:
                if (current in polygon) and (pt in polygon) and (current,pt) not in allLines and (pt,current) not in allLines:
                        if (pt!=current): successors.remove(pt)
            
        for nextPoint in successors:
            if(alreadyVisited.count(nextPoint)==0):
                solutionPath[nextPoint] = current
                alreadyVisited.append(nextPoint)
                myqueue.put(nextPoint)
        
    return "failure"

if __name__ == '__main__':
    c = Canvas(height=600, width=600)

    example = 1
    if(example==1):
        drawboard(c, read('big_triangles'))
        points = read('big_triangles');
    elif(example==2):
        drawboard(c, read('square_in_the_middle'))
        points = read('square_in_the_middle');
    elif(example==3):

        drawboard(c, read('triangle_in_the_middle'))
        points = read('triangle_in_the_middle');
    elif(example==4):
        drawboard(c, read('tall_triangle_in_the_middle'))
        points = read('tall_triangle_in_the_middle');
    else:
        print "Wrong example."
    c.pack()

    start = points[0]
    end = points[1]
    polygons = points[2:][0][1:] # all the polygons (does not include the outer bound)

    
    path = polygonSolverBFS(start, end, polygons)
    
    if path == "failure": print "Failure"
    else:
        print "The points being visited are: "
        dist = 0
        for i in range(len(path)-1):
            print path[len(path)-1-i]
            dist = dist + distance(path[i],path[i+1])
        print path[0]
        print "The distance of the path is " + str(dist) +"."
        
        for i in range(len(path)-1):
            drawLine(c, path[i], path[i+1], "red")

    mainloop()
