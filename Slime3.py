
# -*- coding: utf-8 -*-
"""
Created on Wed May 03 14:03:42 2017
@author: Fantasia
"""
import random
import pygame
import math


class Unit:
    def __init__(self, c, s, c2):
        self.c = c  # 信息素浓度
        self.c2 = 0
        self.s = 0  # 状态：0-空位 1-普通细胞 2-物体 3-捕食细胞


class Ground:
    def __init__(self, n):
        self.ground = []
        self.n = n
        self.l = []
        for i in range(n):
            self.ground.append([])
        for l in self.ground:
            for i in range(n):
                l.append(Unit(0, 0, 0))

    def show(self):
        for i in range(self.n):
            print([u.s for u in self.ground[i]])

    def randinit(self):
        for i in range(self.n):
            for j in range(self.n):
                self.ground[i][j] = Unit(random.random(), 0, 0)

    def addslime(self, x, y):
        self.ground[x][y].s = 1

    def addglass(self, x, y):
        self.ground[x][y].s = 2

    def addpredator(self, x, y):
        self.ground[x][y].s = 3

    def inrange(self, x, y):
        return (x in range(n)) and (y in range(n))

    def addc(self, x, y, n):
        sc = self.ground[x][y].c
#        if sc<10000:
        self.ground[x][y].c = sc+n

    def addc2(self, x, y, n):
        sc2 = self.ground[x][y].c2
        self.ground[x][y].c2 = sc2+n

    def release(self, x, y):
        sc = self.ground[x][y].c
        k = 0.01
        try:
            dc = k*sc/self.abalcount(x, y)
        except:
            dc = 0.0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if self.inrange(x+i, y+j):
                    if not (i == j and i == 0):
                        self.addc(x+i, y+j, dc)

    def nrelease(self, x, y):
        sc = self.ground[x][y].c  # 根据要捕食的细胞/自己的信息素浓度施放自己的信息素
        k = 0.9
        try:
            dc = k*sc/self.abalcount(x, y)
        except:
            dc = 0.0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if self.inrange(x+i, y+j):
                    if not (i == j and i == 0):
                        self.addc2((x+i), (y+j), dc)

    def upperslime(self, x, y):
        nx = x
        ny = y
        myc = self.ground[x][y].c
        myc2 = self.ground[x][y].c2
        k2 = 8
        totalmyc = myc-k2*myc2
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not (i == j and i == 0):
                    if self.inrange(x+i, y+j):
                        nc = self.ground[x+i][y+j].c
                        nc2 = self.ground[x+i][y+j].c2
                        if nc-k2*nc2 <= totalmyc:
                            pass
                        elif self.ground[x+i][y+j].s != 0:
                            pass
                        else:
                            myc = self.ground[x+i][y+j].c
                            myc2 = self.ground[x+i][y+j].c2
                            totalmyc = myc-k2*myc2
                            nx = x+i
                            ny = y+j
        self.ground[x][y].s = 0
        x = nx
        y = ny
        self.ground[x][y].s = 1
        self.release(x, y)

    def upperpredator(self, x, y):
        nx = x
        ny = y
        mc = self.ground[x][y].c  # 按照自己/对方的信息素浓度梯度移动
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not (i == j and i == 0):
                    if self.inrange(x+i, y+j):
                        if self.ground[x+i][y+j].s == 1:
                            self.ground[x+i][y+j].s = 3
                        elif self.ground[x+i][y+j].s == 0:
                            if self.ground[x+i][y+j].c <= mc:
                                pass
                            else:
                                mc = self.ground[x+i][y+j].c
                                nx = x+i
                                ny = y+j
        self.ground[x][y].s = 0
        x = nx
        y = ny
        self.ground[x][y].s = 3
        self.nrelease(x, y)

    def z(self, x, y):
        return x, y-1

    def y(self, x, y):
        if y != self.n-1:
            return x, y+1
        else:
            return x, 0

    def s(self, x, y):
        return x-1, y

    def x(self, x, y):
        if x != self.n-1:
            return x+1, y
        else:
            return 0, y

    def zs(self, x, y):
        return self.s(*self.z(x, y))

    def zx(self, x, y):
        return self.x(*self.z(x, y))

    def ys(self, x, y):
        return self.s(*self.y(x, y))

    def yx(self, x, y):
        return self.x(*self.y(x, y))
    fl = [z, y, s, x, zs, zx, ys, yx]

    def abalcount(self, x, y):
        #        count=0
        #        for i in [-1,0,1]:
        #            for j in [-1,0,1]:
        #                if self.inrange(x+i,y+j):
        #                    if self.ground[x+i][y+j].s!=2:
        #                        count+=1
        #        return count
        return 8

    def kuosan1(self, x, y):
        rate = 0.9
        deltaout = self.ground[x][y].c*rate
        deltain = 0
        for f in self.fl:
            tx, ty = f(self, x, y)
            try:
                d = self.ground[tx][ty].c*rate/self.abalcount(tx, ty)
            except:
                d = 0.0
            deltain += d
        self.ground[x][y].c += deltain
        self.ground[x][y].c -= deltaout

    def kuosan2(self, x, y):
        rate = 0.9
        deltaout = self.ground[x][y].c2*rate
        deltain = 0
        for f in self.fl:
            tx, ty = f(self, x, y)
            try:
                d = self.ground[tx][ty].c2*rate/self.abalcount(tx, ty)
            except:
                d = 0.0
            deltain += d
        self.ground[x][y].c2 += deltain
        self.ground[x][y].c2 -= deltaout

    def uppergroundunit(self, x, y):
        self.kuosan1(x, y)
        self.kuosan2(x, y)
        if self.ground[x][y].s == 1:
            self.upperslime(x, y)
        if self.ground[x][y].s == 3:
            self.upperpredator(x, y)

    def update(self):
        for i in range(self.n):
            for j in range(self.n):
                self.uppergroundunit(i, j)


n = 50
g = Ground(n)
g.randinit()
for i in range(500):
    g.addslime(random.randint(0, g.n-1), random.randint(0, g.n-1))
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (0, 255, 0)
RED = (255, 0, 0)
ge = 6
g.addpredator(20, 20)


def drawone(i, j, c):
    if c.ground[i][j].s == 0:
        pygame.draw.rect(dissurf, BLACK, (i*ge, j*ge, ge-2, ge-2))
    elif c.ground[i][j].s == 1:
        pygame.draw.rect(dissurf, YELLOW, (i*ge, j*ge, ge-2, ge-2))
    elif c.ground[i][j].s == 2:
        pygame.draw.rect(dissurf, BLUE, (i*ge, j*ge, ge-2, ge-2))
    elif c.ground[i][j].s == 3:
        pygame.draw.rect(dissurf, RED, (i*ge, j*ge, ge-2, ge-2))


pygame.init()
dissurf = pygame.display.set_mode((n*ge, n*ge))
dissurf.fill(BLACK)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    g.update()
    for i in range(n):
        for j in range(n):
            drawone(i, j, g)
    pygame.display.update()
