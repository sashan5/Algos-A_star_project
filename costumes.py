from main import *
import random


#show candidates for being part of the route
def addCand(wallsprite, maingrid, grid, wallpos):
    wallpos = (wallpos[0]*15, wallpos[1]*16)
    this_grid_loc = getNpLoc(wallpos)

    if not maingrid[this_grid_loc]:
        candid = Candid(wallpos);
        wallsprite.add(candid)


def printok():
    print("ok")

#print labels on the screen
def printNum(num, screen, wallpos):
    font_text = pygame.font.SysFont(None, 15)
    write_1 = font_text.render(num, True, (0, 0, 0))
    write_1_size = font_text.size(num)
    print(wallpos[0]*15 - (write_1_size[0] / 2))
    rect = screen.blit(write_1, (wallpos[0]*15 - (write_1_size[0] / 2), wallpos[1]*16 - (write_1_size[1]/2)))
    print(rect)

#print all posibles route (use printRoute function n times)
def printRoutes(full_route, screen, fighterGroup):

    i = 0
    for fighter in fighterGroup:
        path = full_route[i][::-1]
        path_reduce = full_route[i][::-1]
        path_reduce.pop(0)
        printRoute(path_reduce, fighter, screen)

        i += 1

#print one route
def printRoute(path_reduce, fighter, screen):
    t = 0
    next_dest = path_reduce[0]
    pygame.draw.aaline(screen, (0, 255, 0), (fighter.retLoc()[0] + 7.5, fighter.retLoc()[1] + 8),
                       (next_dest[0][0] * 15 + 7.5, next_dest[1][0] * 16 + 8), 1)
    while t < len(path_reduce) - 1:
        now_dest = path_reduce[t]
        next_dest = path_reduce[t + 1]
        pygame.draw.aaline(screen, (0, 255, 0), (now_dest[0][0] * 15 + 7.5, now_dest[1][0] * 16 + 8),
                           (next_dest[0][0] * 15 + 7.5, next_dest[1][0] * 16 + 8))
        t += 1

#load new york buildings locations
def loadBuildings(wallsprite, wallgrid, filename):
    maingrid = []
    maingrid = pickle.load(open(filename, "rb"))

    x = 0
    for rows in maingrid:
        y = 0
        for cols in rows:
            wallpos = (x*15, y*16)
            this_grid_loc = getNpLoc(wallpos)

            if (maingrid[this_grid_loc] == 1):
                wall = Wall(wallpos)
                wallsprite.add(wall)
                # store the location of the vertex
                # to remove it if necessary
                wallgrid.append(wallpos)
            y += 1
        x += 1
    return maingrid

#print frame of walls (for simulations)
def printSquare(wallsprite, wallgrid, maingrid, grid):
    for col in range(0,80*15,15):
        wallpos = (col,0)
        setSquare(wallpos, wallsprite, wallgrid, maingrid, grid)

        wallpos = (col, 48*16-16)
        setSquare(wallpos, wallsprite, wallgrid,maingrid,grid)

    for row in range(0,48*16-16,16):
        wallpos = (0,row)
        setSquare(wallpos, wallsprite, wallgrid, maingrid, grid)
        wallpos = (80*15-15, row)
        setSquare(wallpos, wallsprite, wallgrid, maingrid, grid)

#converts screen size cordinates to game grid cordiantes
def getNpLoc(wallpos):
    return(int(wallpos[0]/15), int(wallpos[1]/16))

# set ONE wall on the map
def setSquare(wallpos, wallsprite, wallgrid,maingrid,grid):
    this_grid_loc = getNpLoc(wallpos)

    # if the grid is available for the wall
    if not maingrid[this_grid_loc]:
        maingrid[this_grid_loc] = 1
        wall = Wall(wallpos)
        wallsprite.add(wall)
        # store the location of the vertex
        # to remove it if necessary
        wallgrid.append(wallpos)

# function to simulate random mazes
def randomBlocks(wallsprite, wallgrid, maingrid, grid):
    amount = 50
    for x in range(0,amount):
        x = random.randint(0, 79)*15
        y = random.randint(0, 47)*16
        wallpos = (x, y)
        setSquare(wallpos, wallsprite, wallgrid,maingrid,grid)


## add the 3 pizeria locations to the map
def addPizerias(fightergrid, maingrid, fighterGroup, targetGroup, screen, pizeriapos):
    amount = 3
    count = 0

    while(count < amount):

        fighter_grid_loc = pizeriapos[count]
        fighterpos = (fighter_grid_loc[0] * 15, fighter_grid_loc[1] * 16)

        if not fightergrid[fighter_grid_loc] and not maingrid[fighter_grid_loc]:
            pizzeria = Fighter(fighterpos)
            pointer_target = True
            done_location = True
            fightergrid[fighter_grid_loc] = 1
            maingrid[fighter_grid_loc] = 1
            fighterGroup.add(pizzeria)
            count += 1

    fighterGroup.update()
    fighterGroup.draw(screen)

