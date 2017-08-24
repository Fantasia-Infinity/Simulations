# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 16:51:51 2017

@author: Fantasia
"""
import classroom
import random
import pygame
import time
def showstate(p):
    return p.state
def showa(p):
    return p.a
class Cell:
    def __init__(self,x,y,pheromoneA,pheromoneB,state):
        self.state=state
        self.a=pheromoneA
        self.b=pheromoneB
        self.x=x
        self.y=y
class Skin(classroom.Classroom):
    def setbeing(self):
        for i in range(self.n):
            for j in range(self.n):
                self.a[i][j]=Cell(i,j,random.randint(0,10),random.randint(0,10),0.0)
    def upper(self,cell):
        rateta=0.1
        ratetb=0.1
        ratera=0.2
        raterb=0.2
        delta=0
        deltb=0
        x=0
        for f in self.l:
            delta+=(f(self,cell).a)*rateta/8
            if f(self,cell).state>x:
                delta+=f(self,cell).state*ratera
        delta-=cell.a*rateta
#        if delta>255:
#            delta=255
        for f in self.l:
            deltb+=(f(self,cell).b)*ratetb/8
            if f(self,cell).state<x:
                deltb-=f(self,cell).state*raterb
        deltb-=cell.b*ratetb
#        if deltb>255:
#            deltb=255
        delts=cell.a-cell.b
        if abs(cell.state)>255:
            delts=0
        return cell.a+delta,cell.b+deltb,cell.state+delts
    def update(self):
        newskin=Skin(self.n)
        newskin.setbeing()
        for i in range(self.n):
            for j in range(self.n):
                newskin.a[i][j]=Cell(i,j,self.upper(self.a[i][j])[0],self.upper(self.a[i][j])[1],self.upper(self.a[i][j])[2])
        self.a=newskin.a
    def show(self):
        for i in self.a:
            print map(showa,i) 
        return
n=60
c=Skin(n)
c.setbeing()
ge=5
BLUE=(0,0,255)
BLACK=(0,0,0)
#def drawone(i,j,c):
#    pygame.draw.rect(dissurf,(0,int(c.a[i][j].b),int(c.a[i][j].a)),(i*ge,j*ge,ge-5,ge-5))
def drawone(i,j,c):
    sa=c.a[i][j].state
    s=int((sa+255)/2-10)
    if s>255:
        s=255
    if s<0:
        s=0
    pygame.draw.rect(dissurf,(s,s,s),(i*ge,j*ge,ge-1,ge-1))
pygame.init()
dissurf=pygame.display.set_mode((n*ge,n*ge))
dissurf.fill(BLACK)
while True:
    for event in  pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    c.update()
    for i in range(n):
        for j in range(n):
            drawone(i,j,c)
    pygame.display.update()

#for i in range(10):
#    c.update()
#c.show()
    
        
        
