from Tkinter import *
import guiHelp
from guiHelp import *
import robotUtilities
from robotUtilities import *
import heapq

def solution(solutionPath, point, sol):# find the solution path
    sol.append(point)
    while (solutionPath.get(point)!=None):
        sol.append(solutionPath.get(point))
        point = solutionPath.get(point)
    return sol
    
def polygonSolver(start, end, polygons):
    alreadyVisited = [] # points have already been visited
    queue = [] # nodes waiting to be expanded
    
    solutionPath = {}
    g={} # path cost from the start node to node n
    g[start] = 0 
    f={} # estimated cost of the cheapest solution through n
    f[start] = g[start]+distance(start, end)
    
    heapq.heappush(queue, (f[start],start))
    
    while(len(queue)!=0):
        x = heapq.heappop(queue)
        current = x[1] # current point being visited
        
        if(current == end): # arrived the goal state
            sol = []
            return solution(solutionPath, end, sol)

        alreadyVisited.append(current)

        # compute the successor
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
        for pt in allPoints: # remove the vertice shared by two polygons
            if(allPoints.count(pt)>1):
                while(allPoints.count(pt)!=0): allPoints.remove(pt)
                
        for pt in allPoints:
            if(pathIntersectsAnyLines(current, pt, allLines)== False):
                successors.append(pt)
        if(pathIntersectsAnyLines(current,end,allLines)==False):
            successors.append(end)
    
        while(successors.count(current)!=0): # remove the current point from its successors
            successors.remove(current)
        for pt in successors: # the path to the successor should not be in the polygon
            for polygon in polygons:
                if (current in polygon) and (pt in polygon) and (current,pt) not in allLines and (pt,current) not in allLines:
                        if (pt!=current): successors.remove(pt)
                        
        for nextPoint in successors:
            if(alreadyVisited.count(nextPoint)!=0): continue
            gTemp = g[current]+distance(current,nextPoint)
            if( not(f.get(nextPoint)!= None and queue.count((f[nextPoint],nextPoint))!=0) or gTemp < g[nextPoint]):
                solutionPath[nextPoint] = current
                g[nextPoint] = gTemp
                f[nextPoint] = g[nextPoint]+distance(nextPoint, end)
                if(queue.count(nextPoint)==0): heapq.heappush(queue, (f[nextPoint],nextPoint))
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

    path = polygonSolver(start, end, polygons)
    if path == "failure": print "Failure"
    else:
        print "The points being visited are: "
        dist = 0
        for i in range(len(path)-1):
            print path[len(path)-1-i]
            dist = dist + distance(path[i],path[i+1])
        print path[0]
        print "The distance of the shortest path is " + str(dist) +"."
        
        for i in range(len(path)-1):
            drawLine(c, path[i], path[i+1], "red")

    mainloop()
    
