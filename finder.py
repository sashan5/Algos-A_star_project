from heapq import *
import heapq
import numpy as np
from costumes import addCand

# takes a dictionary as input
def recurrentPath(final_path, raw_path, dest, origin):
    a = raw_path[tuple(dest[0]), tuple(dest[1])]
    final_path.append(a)
    if (a != origin):
        recurrentPath(final_path, raw_path, a, origin)
    else:
        return final_path

def CalcHValue(target, best_pos_now):
    ##euclide distance
    #dist = ((abs(target[0] - best_pos_now[0])**2) + (abs(target[1] - best_pos_now[1])**2))**0.5

    #manhattan distance
    dist = abs(target[0] - best_pos_now[0]) + abs(target[1] - best_pos_now[1])

    return dist



def getPathR(fightergrid, maingrid, targetgrid, screen, wallsprite, grid, fighterpos):
    # array to store path locations
    direct_graph = {}
    # target location, returns a tuple
    target = np.where(targetgrid)
    # end location, returns locations
    fightergrid = np.zeros(targetgrid.shape)
    fightergrid[(fighterpos[0], fighterpos[1])] = 1;
    start = np.where(fightergrid)

    #start = (tuple(fighterpos[0]), tuple(fighterpos[1]))

    # array of cost to travel so far
    total_g_cost = 0
    #array for heuristic cost
    #h_cost_array = np.zeros(fightergrid.shape)
    #need to use a loop unfortunately...
    t = 0
    #possible steps
    steps = ((-1, 0), (+1, 0), (0, -1), (0, +1))
    count = 0
    #total cost =  f + g


    g_cost_array = np.full(fightergrid.shape,100)
    g_cost_array[start] = 0

    f_cost_array = np.full(fightergrid.shape,100)
    f_cost_array[start] = CalcHValue(target, start)

    #closed and open sets
    open_set = []
    heappush(open_set, (0, start))
    closed = np.zeros(fightergrid.shape)
    opened = np.zeros(fightergrid.shape)
    #actual path
    path = []

    path.append([tuple(target[0]), tuple(target[1])])
    solution_found = False
    while (open_set):

        node = heapq.nsmallest(1, open_set, key=lambda x: x[0])[0]
        best_pos_now = node[1]
        open_set.remove(node)
        closed[best_pos_now] = 1


        #if the destination is reached, finish!
        if (tuple(best_pos_now) == target):
            solution_found = True
            print("solution found")
            break
        else:

            for step in steps:
                cand = (best_pos_now[0] + step[0], best_pos_now[1] + step[1])
                # need an else clause here to weed out the off-screen locations
                newg = g_cost_array[best_pos_now] + 1
                #check if there's a wall or beyond the screen
                if cand[0] < 0 or cand[1] < 0 or cand[0] > 79 or cand[1] > 47:
                   #out of screen
                    pass
                elif maingrid[cand] or closed[cand]:
                    #wall or f calculated
                    pass
                elif newg < g_cost_array[cand]:
                    #update nodes
                    g_cost_array[cand] = newg
                    f_cost_array[cand] = newg + CalcHValue(target, cand)
                    #graph
                    direct_graph[tuple(cand[0]), tuple(cand[1])] = (tuple(best_pos_now[0]), tuple(best_pos_now[1]))

                    addCand(wallsprite, maingrid, grid, cand)
                    if not opened[cand]:
                        heappush(open_set, (f_cost_array[cand], cand))
                        opened[cand] = 1



    if not solution_found:
        return None
    else:
        recurrentPath(path, direct_graph, target, start)

        return path


