# -*- coding: utf-8 -*-
"""
Created on Tue May 02 09:46:22 2017

@author: Administrator
"""
import classroom
import random
import pygame
import math
class Slime:
    def __init__(self,x,y):
        self.x=x
        self.y=y
class Unit:
    def __init__(self,c,s):
        self.c=c
        self.s=0
class Ground(classroom.Classroom):
    def __init__(self,n):
        self.ground=[]
        self.n=n
        self.l=[]
        for i in range(n):
            self.ground.append([])
        for l in self.ground:
            for i in range(n):
                l.append(Unit(0,0))
    def showslime(self):
        for s in self.l:
            print s.x,s.y
    def randinit(self):
        for i in range(self.n):
            for j in range(self.n):
                self.ground[i][j]=Unit(random.random(),0)
    def addslime(self,slime):
        self.l.append(slime)
        self.ground[slime.x][slime.y].s=1
    def inrange(self,x,y):
        return (x in range(n)) and (y in range(n))
    def addc(self,x,y,n):
        sc=self.ground[x][y].c
#        if sc<10000:
        self.ground[x][y].c=sc+n
    def release(self,slime):
        sx=slime.x
        sy=slime.y
        sc=self.ground[sx][sy].c
        k=0.01
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if self.inrange(sx+i,sy+j):
                    if not (i==j and i==0):
                        self.addc(sx+i,sy+j,k*sc)
#        for f in self.fl:
#            i=f(self,sx,sy)[0]
#            j=f(self,sx,sy)[1]
#            self.addc(i,j,k*sc)
    def upperslime(self,slime):
        nx=slime.x
        ny=slime.y
        mc=self.ground[slime.x][slime.y].c
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if not (i==j and i==0):
                    if self.inrange(slime.x+i,slime.y+j):
                        if self.ground[slime.x+i][slime.y+j].c<=mc:
                            pass
                        elif self.ground[slime.x+i][slime.y+j].s==1:
                            pass
                        else:
                            mc=self.ground[slime.x+i][slime.y+j].c
                            nx=slime.x+i
                            ny=slime.y+j
#        for f in self.fl:
#            if self.ground[f(self,nx,ny)[0]][f(self,nx,ny)[1]].c<=mc:
#                pass
#            elif self.ground[f(self,nx,ny)[0]][f(self,nx,ny)[1]].s==1:
#                pass
#            else:
#                mc=self.ground[f(self,nx,ny)[0]][f(self,nx,ny)[1]].c
#                nx=f(self,nx,ny)[0]
#                ny=f(self,nx,ny)[1]    
        self.ground[slime.x][slime.y].s=0
        slime.x=nx
        slime.y=ny
        self.ground[slime.x][slime.y].s=1
        self.release(slime)
    def z(self,x,y):
        return x,y-1
    def y(self,x,y):
        if y!=self.n-1:
            return x,y+1
        else:
            return x,0
    def s(self,x,y):
        return x-1,y
    def x(self,x,y):
        if x!=self.n-1:
            return x+1,y
        else:
            return 0,y
    def zs(self,x,y):
        return self.s(*self.z(x,y))
    def zx(self,x,y):
        return self.x(*self.z(x,y))
    def ys(self,x,y):
        return self.s(*self.y(x,y))
    def yx(self,x,y):
        return self.x(*self.y(x,y))
    fl=[z,y,s,x,zs,zx,ys,yx]
    def uppergroundunit(self,x,y):
        rate=0.9
        deltaout=self.ground[x][y].c*rate
        deltain=0
        for f in self.fl:
            tx,ty=f(self,x,y)
            d=self.ground[tx][ty].c*rate/8.0
            deltain+=d
        self.ground[x][y].c+=deltain
        self.ground[x][y].c-=deltaout
    def update(self):
        for slime in self.l:
            self.upperslime(slime)
        for i in range(self.n):
            for j in range(self.n):
                self.uppergroundunit(i,j)
n=50
g=Ground(n)
g.randinit()
g.addslime(Slime(5,5))
g.addslime(Slime(10,10))
for i in range(500):
    g.addslime(Slime(random.randint(0,g.n-1),random.randint(0,g.n-1)))

BLUE=(0,0,255)
BLACK=(0,0,0)
YELLOW=(0,255,0)
ge=6

def drawone(i,j,c):
    pygame.draw.rect(dissurf,BLACK,(i*ge,j*ge,ge-2,ge-2))
def drawslime(slime):
    i=slime.x
    j=slime.y
    pygame.draw.rect(dissurf,YELLOW,(i*ge,j*ge,ge-2,ge-2))
pygame.init()
dissurf=pygame.display.set_mode((n*ge,n*ge))
dissurf.fill(BLACK)
while True:
    for event in  pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    g.update()
    for i in range(n):
        for j in range(n):
            drawone(i,j,g)
    for s in g.l:
        drawslime(s)
    pygame.display.update()
        
        
