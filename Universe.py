# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 09:53:07 2017

@author: Administrator
"""
import math
import pygame
delt=0.0001
k=10
class Vec:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self,v2):
        self.x+=v2.x
        self.y+=v2.y
    def mulc(self,c):
        return Vec(self.x*c,self.y*c)
    def show(self):
        print self.x,self.y
class Planet:
    def __init__(self,m,l,v,a):
        self.m=m
        self.l=l
        self.v=v
        self.a=a
    def distance(self,p2):
        return math.sqrt((self.l.x-p2.l.x)*(self.l.x-p2.l.x)+(self.l.y-p2.l.y)*(self.l.y-p2.l.y))
    def forth(self,p2):
        F=k*self.m*p2.m/self.distance(p2)*self.distance(p2)
        to_x=(p2.l.x-self.l.x)/self.distance(p2)
        to_y=(p2.l.y-self.l.y)/self.distance(p2)
        return Vec(F*to_x,F*to_y)
class Universe:
    def __init__(self,list_of_planets=[]):
        self.planets=list_of_planets
    def upper(self,planet):
        planet.l+planet.v.mulc(delt)
        planet.v+planet.a.mulc(delt)
        newa=Vec(0.0,0.0)
        for p in self.planets:
            if planet!=p:
                newa+planet.forth(p).mulc(1.0/planet.m*k)
        planet.a=newa
    def update(self):
        for p in self.planets:
            self.upper(p)
    def show(self):
        for p in self.planets:
            print p.l.x,p.l.y
ps=[Planet(1000,Vec(300.0,400.0),Vec(0.0,100.0),Vec(0.0,0.0))]
ps.append(Planet(1,Vec(200.0,200.0),Vec(1000.0,0.0),Vec(0.0,0.0)))
ps.append(Planet(1,Vec(350.9,450.0),Vec(1000.0,10.0),Vec(0.0,0.0)))
#ps.append(Planet(1,Vec(500.0,500.0),Vec(-100.0,0.0),Vec(0.0,0.0)))
#ps.append(Planet(1,Vec(300.0,500.0),Vec(-100.0,1000.0),Vec(0.0,0.0)))
u=Universe(ps)

ge=6
BLUE=(0,0,255)
BLACK=(0,0,0)
n=150
#def drawone(i,j,c):
#    pygame.draw.rect(dissurf,(0,int(c.a[i][j].b),int(c.a[i][j].a)),(i*ge,j*ge,ge-5,ge-5))
def drawone(i,c):
    x=c.planets[i].l.x
    y=c.planets[i].l.y           
    pygame.draw.rect(dissurf,BLUE,(x,y,ge-5,ge-5))
pygame.init()
dissurf=pygame.display.set_mode((n*ge,n*ge))
dissurf.fill(BLACK)
while True:
    for event in  pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    u.update()
    u.planets[0].l=Vec(300,400)
    for i in range(len(u.planets)):
        drawone(i,u)
    pygame.display.update()

                
                
                