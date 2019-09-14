from finder import *
from costumes import *
import ctypes

__author__ = 'Alex'
__customization__ = 'Itzik and Sasha'

import numpy as np
import pygame
import os, sys, time
from pygame.constants import QUIT, K_ESCAPE, KEYDOWN, \
    MOUSEBUTTONDOWN, MOUSEBUTTONUP, K_SPACE, K_s, K_g
import pygame.sprite as spriteclass
import pickle
from classes import *

SCREEN_SIZE = (1200, 768)
os.environ['SDL_VIDEO_CENTERED'] = '1'

def printGraph(maingrid, screen):
    r = 0
    steps = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
    for r in range(0,47):

        for c in range(0, 79):
            if(maingrid[(c, r)] == 0):
                pygame.draw.circle(screen, (0, 0, 0), (int(c*15 + 7.5), int(r*16 + 8)), 2)
            for step in steps:
                cand = (c + step[0], r + step[1])
                if cand[0] < 0 or cand[1] < 0 or cand[0] > 79 or cand[1] > 47:
                    pass
                else:
                    if(maingrid[(c, r)] == 0 and maingrid[cand] == 0):
                        pygame.draw.aaline(screen, (0, 0, 0), (int(cand[0]*15 + 7.5), int(cand[1]*16 + 8)), (int(c*15 + 7.5), int(r*16 + 8)), 1)


def main():
    clock = pygame.time.Clock()
    pygame.init()
    pygame.font.init()

    main_title = "Pizza Delivery By Itzik and Sasha!"
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(main_title)
    bgimage = BgImage()

    wallsprite = pygame.sprite.RenderUpdates()
    targetGroup = pygame.sprite.RenderUpdates()

    pointer_target = False
    done_pointer = False
    done_locating = False
    distset = False
    input_on = False
    job_succeed=False
    show_graph = False

    #sounds
    fail_sound = pygame.mixer.Sound('171493__fins__alarm.wav')
    fail_sound.set_volume(0.1)
    win_sound = pygame.mixer.Sound('249524__limetoe__badass-victory.wav')
    win_sound.set_volume(0.1)

    fighter_for_mouse = Fighter(pygame.mouse.get_pos())
    fighterGroup = pygame.sprite.RenderUpdates()
    fighterGroup.add(fighter_for_mouse)

    pizerias_loc = []
    pizerias_loc.append((60,8))
    pizerias_loc.append((59,39))
    pizerias_loc.append((9,25))
    full_route = []
    grid = Grid(SCREEN_SIZE)
    xgrid = grid.getXGrid()
    ygrid = grid.getYGrid()
    #grid to save unreachable positions
    maingrid = np.zeros([len(xgrid), len(ygrid)])
    #grid to save walls
    wallgrid = []
    #grids to save position of the fighter and target
    fightergrid = np.zeros([len(xgrid), len(ygrid)])
    targetgrid = np.zeros([len(xgrid), len(ygrid)])

    FPS = 60
    pygame.time.Clock()
    start = True
    # launch

    #start sequence
    maingrid = loadBuildings(wallsprite, wallgrid, "buildings.dat")
    addPizerias(fightergrid, maingrid, fighterGroup, targetGroup, screen, pizerias_loc)
    pointer_fighter = True

    ctypes.windll.user32.MessageBoxW(0, "!!ATTENTION!!\n To Simulate, set the target and press ENTER.\n To Show or hide Graph press G.", "!!ATTENTION!!", 1)

    while (start):
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == QUIT:
                #start = False
                #time.sleep(0)
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                #exit program
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)

                #show or hide graph
                elif (event.key == K_g):
                    show_graph = not show_graph
                #to save new buildings structure to the file
                elif(event.key == K_s and not pointer_fighter and not done_locating):
                    #function to save buildings array into dat file
                    #pickle.dump(maingrid, open("buildings.dat", "wb"))
                    pass

                #after target is located need to press space
                elif (event.key == K_SPACE and not done_locating):
                    pointer_fighter = True
                    done_locating = True
                #finish locating, run A* pathfinder
                elif (event.key == K_SPACE and done_locating and distset):
                    input_on = True
                    distset = False

                    aRoute = getPathR(fightergrid, maingrid, targetgrid, screen, wallsprite, grid, pizerias_loc[0])
                    bRoute = getPathR(fightergrid, maingrid, targetgrid, screen, wallsprite, grid, pizerias_loc[1])
                    cRoute = getPathR(fightergrid, maingrid, targetgrid, screen, wallsprite, grid, pizerias_loc[2])

                    print("% d route length is: % d" % (0, len(aRoute)))
                    print("% d route length is: % d" % (1, len(bRoute)))
                    print("% d route length is: % d" % (2, len(cRoute)))

                    full_route.extend([aRoute, bRoute, cRoute])
                    printRoutes(full_route, screen, fighterGroup)
                    job_succeed=True

            #set walls
            elif (event.type == MOUSEBUTTONDOWN and event.button == 1
                  and not pointer_fighter and not done_locating):
                pos = pygame.mouse.get_pos()
                wallpos = grid.getWallLoc(pos)
                this_grid_loc = grid.retGridLoc(maingrid)

                #if the grid is available for the wall
                if not maingrid[this_grid_loc]:
                    maingrid[this_grid_loc] = 1
                    wall = Wall(wallpos)
                    wallsprite.add(wall)
                    #store the location of the vertex
                    #to remove it if necessary
                    wallgrid.append(wallpos)
                else:
                    maingrid[this_grid_loc] = 0
                    j = 0
                    for j in range(len(wallgrid)):
                        if wallgrid[j] == wallpos:
                            wallgrid.remove(wallpos)
                            break

                    for walls in wallsprite:

                        posThis = walls.retLoc()
                        if (posThis[0] == wallpos[0] and posThis[1] == wallpos[1]):
                            wallsprite.remove(walls)
                            break

            #delete all wallblocks
            elif (event.type == MOUSEBUTTONDOWN and event.button == 3
                  and not pointer_fighter and not done_locating):
                if wallsprite:
                    wallsprite.empty()
                    maingrid = np.zeros([len(xgrid), len(ygrid)])
                    wallgrid = []

            #put the target(after I've moved it around as a mousepointer
            elif event.type == MOUSEBUTTONDOWN and event.button \
                    and done_locating and pointer_target:
                pos = pygame.mouse.get_pos()
                targetpos = grid.getWallLoc(pos)
                target_grid_loc = grid.retGridLoc(targetpos)

                canFinish = True
                for walls in wallsprite:
                    if pygame.sprite.spritecollide(walls, targetGroup, False):
                        #print('You can"t place the target here!')
                        fail_sound.play()
                        canFinish = False
                        break

                for fighters in fighterGroup:
                    if pygame.sprite.spritecollide(fighters, targetGroup, False):
                        fail_sound.play()
                        #print('You can"t place the target here!')
                        canFinish = False
                        break

                #valid location
                if canFinish:
                    pointer_target = False
                    targetgrid[target_grid_loc] = 1
                    target = Target(targetpos)
                    targetGroup.remove(target_mouse)
                    targetGroup.add(target)
                    distset = True
                    pygame.mouse.set_visible(1)


        #this runs all the time
        screen.blit(bgimage.bg_image, (0, 0))

        if pointer_fighter:
            fighterGroup.remove(fighter_for_mouse)
            done_locating = True
            pointer_fighter = False
            pointer_target = True
            target_mouse = Target(pygame.mouse.get_pos())
            targetGroup.add(target_mouse)

        if done_locating:
            fighterGroup.update()
            fighterGroup.draw(screen)

        if show_graph:
            printGraph(maingrid,screen)

        if pointer_target:
            target_mouse.NewPos(pygame.mouse.get_pos())
            targetGroup.update()
            targetGroup.draw(screen)

        if done_pointer:
            targetGroup.update()
            targetGroup.draw(screen)

        if input_on or distset:
            targetGroup.update()
            targetGroup.draw(screen)

            fighterGroup.update()
            fighterGroup.draw(screen)


        if job_succeed:
            printRoutes(full_route, screen, fighterGroup)
            #print("job_succeed!")

        wallsprite.update()
        wallsprite.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()

