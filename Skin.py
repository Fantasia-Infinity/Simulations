# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 15:24:43 2017
@author: Fantasia
"""
import classroom
import random
import pygame
import time
def showstate(p):
    return p.a,p.b
class Cell:
    def __init__(self,x,y,pheromoneA,pheromoneB):
        self.a=pheromoneA
        self.b=pheromoneB
        self.x=x
        self.y=y
class Skin(classroom.Classroom):
    def setbeing(self):
        for i in range(self.n):
            for j in range(self.n):
                self.a[i][j]=Cell(i,j,0.1,0.1)
    def upper(self,cell):
        rate=0.9999
        delta=0
        deltb=0
        for f in self.l:
            delta+=(f(self,cell).a)*rate/8
        delta-=cell.a*rate
        for f in self.l:
            deltb+=(f(self,cell).b)*rate/8
        deltb-=cell.b*rate
        return (cell.a+delta,cell.b+deltb)
    def update(self):
        newskin=Skin(self.n)
        newskin.setbeing()
        for i in range(self.n):
            for j in range(self.n):
                newskin.a[i][j]=Cell(i,j,self.upper(self.a[i][j])[0],self.upper(self.a[i][j])[1])
        self.a=newskin.a
    def show(self):
        for i in self.a:
            print(map(showstate,i))
        return
n=40
c=Skin(n)
c.setbeing()
ge=15
BLUE=(0,0,255)
BLACK=(0,0,0)
def drawone(i,j,c):
    pygame.draw.rect(dissurf,(0,int(c.a[i][j].b),int(c.a[i][j].a)),(i*ge,j*ge,ge-5,ge-5))
pygame.init()
dissurf=pygame.display.set_mode((n*ge,n*ge))
dissurf.fill(BLACK)
while True:
    for event in  pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    c.update()
    c.a[20][20].a=255
    c.a[10][10].b=255
    for i in range(n):
        for j in range(n):
            drawone(i,j,c)
    pygame.display.update()


    
        
        