import numpy as np
import pygame
import pygame.sprite as spriteclass

class BgImage(spriteclass.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.bg_image = pygame.image.load("manhattan.jpg").convert_alpha()
        scaleX = 1.45
        scaleY = 1.45
        self.bg_image = pygame.transform.scale(self.bg_image, (int(1280*scaleX), int(720*scaleY)))
        self.rect = self.bg_image.get_rect()

        # return (self.bg_image)

    def ret_bg(self):
        return (self.rect)

class Wall(spriteclass.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("wall_block.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def retLoc(self):
        return self.rect.x, self.rect.y

    def retSize(self):
        return self.image.get_size()


class Fighter(spriteclass.Sprite):
    def __init__(self, pos):
        # initialize Sprite class
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load("wall_block.png").convert_alpha()
        self.image = pygame.image.load("redfighter0006.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 16))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    # this returns the coordinates of the upper left corner of the fighter
    def retLoc(self):
        return self.rect.x, self.rect.y

    # this returns the coordinates of the
    def retLocCenter(self):
        return self.rect.topleft

    # dims of the sprite
    def retSize(self):
        return self.image.get_size()

    # center the sprite
    def NewPos(self, pos):
        self.rect.center = pos

    # get the route and move the spaceship
    def moveFighter(self, dir, step):
        if dir == 'right':
            self.rect.x += step
        elif dir == 'left':
            self.rect.x -= step
        elif dir == "up":
            self.rect.y -= step
        elif dir == "down":
            self.rect.y += step


class Target(spriteclass.Sprite):
    def __init__(self, loc):
        spriteclass.Sprite.__init__(self)
        self.image = pygame.image.load("target.png")
        self.image = pygame.transform.scale(self.image, (15, 16))
        self.rect = self.image.get_rect()
        self.rect.topleft = loc

    def NewPos(self, pos):
        self.rect.x = pos[0] - self.image.get_size()[0] / 2
        self.rect.y = pos[1] - self.image.get_size()[1] / 2

    def retLoc(self):
        return self.rect.x, self.rect.y

    def retLocCenter(self):
        return self.rect.center

    def retSize(self):
        return self.image.get_size()


class Grid(object):
    def __init__(self, screensize):
        self.image = pygame.image.load("wall_block.png").convert_alpha()
        self.grid = self.image.get_size()
        self.screensize = screensize

    # construct the grid along x axis
    def getXGrid(self):
        self.xrange = []
        t = 0
        while (t * self.grid[0] < self.screensize[0]):
            xval = t * self.grid[0]
            self.xrange.append(xval)
            t += 1

        self.xrange = np.asarray(self.xrange)
        return self.xrange

    # construct the grid along y axis
    def getYGrid(self):
        self.yrange = []
        s = 0
        while (s * self.grid[1] < self.screensize[1]):
            yval = s * self.grid[1]
            self.yrange.append(yval)
            s += 1

        self.yrange = np.asarray(self.yrange)
        return self.yrange

    # get the coordinates of the wall on the screen
    def getWallLoc(self, wallpos):
        self.true_xval = max(self.xrange[wallpos[0] > self.xrange])
        self.true_yval = max(self.yrange[wallpos[1] > self.yrange])
        return (self.true_xval, self.true_yval)

    # get the address of the wall in the matrix
    def retGridLoc(self, bingrid):
        self.binlocx = np.where(self.xrange == self.true_xval)
        self.binlocy = np.where(self.yrange == self.true_yval)
        return (self.binlocx, self.binlocy)

class Candid(spriteclass.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("cand_block.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def retLoc(self):
        return self.rect.x, self.rect.y

    def retSize(self):
        return self.image.get_size()

