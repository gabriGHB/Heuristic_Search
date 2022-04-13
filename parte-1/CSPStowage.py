"""MODULE USED TO SOLVE THE CSPStowage Problem"""

#IMPORTS ----------------------------------------------------------------------------------------------
import os
import sys
from constraint import *


#FUNCTIONS --------------------------------------------------------------------------------------------
def readArguments():
    """Function that will be used to read the arguments from cmd"""
    # First, we read the arguments
    path = sys.argv[1]
    mapFile = sys.argv[2]
    containersFile = sys.argv[3]
    # Now, create the full path of each file
    mapPath = f"{path}{os.sep}{mapFile}"
    containersPpath = f"{path}{os.sep}{containersFile}"
    return mapPath, containersPpath


def openAndCreateMaps(mapPath, containersPath):
    """Function that will be used to open the files and create the map"""
    #First, we open the map and read the contents
    with open(mapPath, "r", newline="", encoding="utf-8") as mapFile:
        mapData = mapFile.read()
    mapFile.close()
    #now, we open the containers file and read the data
    with open(containersPath, "r", newline="", encoding="utf-8") as containersFile:
        containersData = containersFile.read()
    containersFile.close()
    # Now, we create the two matrices 
    mapMatrix = [i.split(" ") for i in mapData.split("\r\n")]
    containersMatrix = [i.split(" ") for i in containersData.split("\r\n")]
    return mapMatrix, containersMatrix


def createDomainsContainers(containersMatrix):
    """Function used to assign the domains to the containers, S and R"""
    #iterate though the containersMatrix, checking if the container is either S or R, and adding them
    # to the corresponding list
    scContainers,rContainers = [], []
    for container in containersMatrix:
        if container[1] == "S":
            scContainers.append(container)
        if container[1] == "R":
            rContainers.append(container)
    return scContainers, rContainers


def createDomainsMap(mapMatrix):
    """Function used to assign the domains to the cells, N and E"""
    #first, we iterate through the map and add all the coordinates of the cells (standard can go to both
    # normal and energetic cells, and regrigerated only to energetic cells)
    sDomain, rDomain = [], []
    for i, row in enumerate(mapMatrix):
        for j, col in enumerate(row):
            if col.upper() == "N":
                sDomain.append((i, j))
            if col.upper() == "E":
                sDomain.append((i, j))
                rDomain.append((i, j))
    return sDomain, rDomain
    

def gravity(mapMatrix, *args):
    """gravitational constraint, which ensures that every container is positioned above an X cell, or
    above another container"""
    for container in args:
        # check that the container is not positioned above an "X" cell
        if mapMatrix[container[0] + 1][container[1]] != "X":
            # check if there's any other container below, that is, the same column but one row below:
            found = any(container != container2 and container2[1] == container[1]
                        and container2[0] == container[0] + 1 for container2 in args)
            # if we dont find any container balow, this asignment cannot be performed (as the
            # container will be floating in space), so we return false
            if not found:
                return False
    #otherwise, either we found an X below or another container, therefore
    # we can return True as the assignment can be performed
    return True


def portsOrder(allContainers, *args):
    """constraint that ensures a container going to port 2 will be always placed below a container going to 
    port 1 (as the ship will go first to port1)"""
    for i, container in enumerate(args):
        for j, container2 in enumerate(args):
            # check if both containers are on the same column and if container is going to port
            # 1 and container2 to port 2. If that happens, the assignment cannot be done
            if (container != container2 and container[1] == container2[1]
                    and allContainers[j][2] > allContainers[i][2]):
                cond = False
                # check if container is above container2. If that happens, the assignment can be done
                if container2[0] > container[0]:
                    cond = True
                # if container is below container2, this assignment is illegal
                if not cond:
                    return False
    return True


def outputSolutions(solutions):
    """Function that is used to write the solution to the output file"""
    #get the arguments
    path = sys.argv[1]
    mapFile = sys.argv[2]
    containersFile = sys.argv[3]
    #get only the name, without the extension
    mapFile = mapFile[:mapFile.index(".")]
    containersFile = containersFile[:containersFile.index(".")]
    #define the name of the output file
    outputFile = f"{path}{os.sep}{mapFile}-{containersFile}.output"
    #open and write the file
    with open(outputFile, "w", newline="", encoding="utf-8") as outputFile:
        outputFile.write(f"Number of solutions: {len(solutions)}")
        for solution in solutions:
            outputFile.write(f"\n{solution}")
    #close the file        
    outputFile.close()


# -------------------------------------- MAIN --------------------------------------------------------------
if __name__ == "__main__":

    #obtain the arguments and create the matrices
    mapPath, containersPath = readArguments()
    mapMatrix, containersMatrix = openAndCreateMaps(mapPath, containersPath)
    #lists of cells
    sDomain, rDomain,  = createDomainsMap(mapMatrix)
    #lists of containers
    sContainers, rContainers = createDomainsContainers(containersMatrix)
    allContainers = sContainers + rContainers
    # get the ID for each container
    sContainersID = [i[0] for i in sContainers]
    rContainersID = [i[0] for i in rContainers]
    #create the problem and assign variables
    problem = Problem()
    problem.addVariables(sContainersID, sDomain)
    problem.addVariables(rContainersID, rDomain)
    #create constraints
    allContainersID= sContainersID + rContainersID
    #to ensure that all containers are located in different cells (that is, get all the
    # possible solutions) it just suffices to ensure that they all take different values
    problem.addConstraint(AllDifferentConstraint())
    #add the gravitational constraint
    problem.addConstraint(lambda *args: gravity(mapMatrix, *args), allContainersID)
    #add the ports order constraint
    problem.addConstraint(lambda *args: portsOrder(allContainers, *args), allContainersID)
    # compute solutions
    solutions = problem.getSolutions()
    #write them into the output file
    outputSolutions(solutions)
