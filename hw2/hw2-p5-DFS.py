from Tkinter import *
import guiHelp
from guiHelp import *
import robotUtilities
from robotUtilities import *

def onLine(pt, line):   # check if point pt is on the line segment
    ((a1,a2),(b1,b2)) = line
    (c1,c2) = pt
    if (b1==a1) or (b2 == a2): return False
    if (((c1-a1)/(b1-a1))-((c2-a2)/(b2-a2))<EPSILON) and ((c1-a1)/(b1-a1))<=1:
        return True
    return False

def solution(solutionPath, point, sol):# find the solution path
    sol.append(point)
    while (solutionPath.get(point)!=None):
        sol.append(solutionPath.get(point))
        point = solutionPath.get(point)
    return sol

def polygonSolverDFS(start, end, polygons, alreadyVisited, solutionPath, allLines):    
    alreadyVisited.append(start)
    current = start
    if (current == end):
        sol = []
        return solution(solutionPath, end, sol)

    # compute successors
    successors = []
    allPoints = []
    for polygon in polygons:
        for nextPt in polygon:
            allPoints.append(nextPt)
    allPointsCopy = allPoints[:]
    
    # remove the vertice shared by two polygons
    for pt in allPointsCopy: 
        if(allPoints.count(pt)>1):
            while(allPoints.count(pt)!=0): allPoints.remove(pt)

    # remove the vertice that form pathes intersecting other lines
    for pt in allPoints:      
        if(pathIntersectsAnyLines(current, pt, allLines)== False):
            successors.append(pt)
    if(pathIntersectsAnyLines(current,end,allLines)==False):
        successors.append(end)

    # remove the current point from its successors
    while(successors.count(current)!=0): 
        successors.remove(current)
    for pt in successors:
        for line in allLines:
            if(onLine(pt, line)):
                while(successors.count(pt)!=0): successors.remove(pt)

    # the path to the successor should not be in the polygon
    for pt in successors: 
        for polygon in polygons:
            if (current in polygon) and (pt in polygon) and (current,pt) not in allLines and (pt,current) not in allLines:
                if (pt!=current): successors.remove(pt)

    cutoffOccurred = False
    for nextPoint in successors:
        if(alreadyVisited.count(nextPoint)==0):
            solutionPath[nextPoint] = current
            alreadyVisited.append(nextPoint)
            #allLines.append((current, nextPoint))
            result = polygonSolverDFS(nextPoint, end, polygons, alreadyVisited, solutionPath, allLines)
            if(result == "cutoff"): cutoffOccurred = True
            elif(result!="failure"): return result
    if(cutoffOccurred == True): return "cufoff"
    else: return "failure"

if __name__ == '__main__':
    c = Canvas(height=600, width=600)

    example = 4
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

    alreadyVisited = []
    solutionPath = {}
    allLines = [] 
    for polygon in polygons:
        for i in range(len(polygon)-1):
            allLines.append((polygon[i], polygon[i+1]))
        allLines.append((polygon[-1],polygon[0]))
    path = polygonSolverDFS(start, end, polygons, alreadyVisited, solutionPath, allLines)
    
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
