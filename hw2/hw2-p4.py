## The 8-Puzzle

# Zimeng Yang

class Problem:    
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal
    def goalTest(self, current):
        if(current == self.goal): return True
        else: return False
    def actions(self, node):
        blankIndex = node.state.index(0)
        act = {
            0: ["right","down"],
            1:["left","right","down"],
            2:["left","down"],
            3:["up","right","down"],
            4:["up","down","left","right"],
            5:["up","left","down"],
            6:["right","up"],
            7:["left","right","up"],
            8:["left","up"] 
            }
        return act.get(blankIndex)
    
class Node:
    def __init__(self, state, child, parent, depth):
        self.state = state
        self.child = child
        self.parent = parent
        self.depth = depth
    
def childNode(node, action):
    currentState = node.state
    newstate = currentState[:]
    blankIndex = currentState.index(0)
    if (action == "left"): # the blank could only be in the second or third row
        newstate[blankIndex] = newstate[blankIndex-1]
        newstate[blankIndex-1] = 0
    elif (action == "right"):
        newstate[blankIndex] = newstate[blankIndex+1]
        newstate[blankIndex+1] = 0
    elif (action == "up"):
        newstate[blankIndex] = newstate[blankIndex-3]
        newstate[blankIndex-3] = 0
    else: #down
        newstate[blankIndex] = newstate[blankIndex+3]
        newstate[blankIndex+3] = 0
    childNode = Node(newstate, None, node, node.depth+1)
    return childNode
            
def solution(node, sol, num):
    num = num + 1
    sol.append(node.state)
    if(node.parent != None):
        solution(node.parent, sol, num)
    else:
        sol.append(num-1)
        return sol

def RecursiveDLS(node, problem, limit):
    sol = []
    if (problem.goalTest(node.state) == True):
        num = 0
        solution(node, sol, num)
        return sol
    elif(limit==0): return "cutoff"
    else:
        cutoffOccurred = False
        actionslist = problem.actions(node)
        actionslistReduced = actionslist[:]
        cache=[]
        cache.append(node.state)##
        for action in actionslist:
            node.child = childNode(node, action)
            if(cache.count(node.child.state)!=0): actionslistReduced.remove(action)         
        for action in actionslistReduced:
            node.child = childNode(node, action)
            result = RecursiveDLS(node.child, problem, limit-1)
            if(result=="cutoff"): cutoffOccurred = True
            elif(result!="failure"): return result
        if(cutoffOccurred == True): return "cutoff"
        else: return "failure"
        
def depthLimitedSearch(problem, limit):
    state = problem.initial # the root node
    node = Node(state, None, None, 0)
    return RecursiveDLS(node, problem, limit)

def eightPuzzleDemo(problem):
    depth = 0
    while(True):
        result = depthLimitedSearch(problem, depth)
        if(result=="cutoff"):
            depth = depth + 1
        else:
            return result

if __name__ == '__main__':
    #initial = [1,0,5,3,2,4,6,7,8] #5steps
    #initial = [1,4,2,3,7,5,0,6,8] #4steps
    initial = [1,5,4,3,2,8,6,7,0] #8steps    
    goal =    [0,1,2,3,4,5,6,7,8]
    
    newproblem = Problem(initial, goal)
    solution = eightPuzzleDemo(newproblem)
    solution.reverse()
    print "The initial state is"
    print str(solution[1][0:3])+'\n'+str(solution[1][3:6])+'\n'+str(solution[1][6:9])+'\n'
    print "To reach the goal state, there are " + str(solution[0])+ " steps."+'\n'+"The transitions and the goal state are:"
    for i in range(2, len(solution)):
        print str(solution[i][0:3])+'\n'+str(solution[i][3:6])+'\n'+str(solution[i][6:9])+'\n'
