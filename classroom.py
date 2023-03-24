# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 18:32:12 2017

@author: Administrator
"""
import random
import pygame


class Per:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state


def showstate(p):
    return p.state


class Classroom:
    def __init__(self, n):
        self.a = []
        self.n = n
        for i in range(n):
            self.a.append([])
        for l in self.a:
            for i in range(n):
                l.append(0)

    def setbegin(self):
        for i in range(self.n):
            for j in range(self.n):
                self.a[i][j] = Per(i, j, random.randint(0, 100))

    def z(self, p):
        return self.a[p.x-1][p.y]

    def y(self, p):
        if p.x != self.n-1:
            return self.a[p.x+1][p.y]
        else:
            return self.a[0][p.y]

    def s(self, p):
        if p.y != self.n-1:
            return self.a[p.x][p.y+1]
        else:
            return self.a[p.x][0]

    def x(self, p):
        return self.a[p.x][p.y-1]

    def zs(self, p):
        return self.s(self.z(p))

    def zx(self, p):
        return self.x(self.z(p))

    def ys(self, p):
        return self.s(self.y(p))

    def yx(self, p):
        return self.x(self.y(p))
    l = [z, y, s, x, zs, zx, ys, yx]

    def rounds(self, p):
        lis = []
        for f in self.l:
            lis.append(f(self, p))
        l = [per.state for per in lis]
        a = 0
        for o in l:
            a += o
        return a

    def show(self):
        for i in self.a:
            print(map(showstate, i))
        return

    def upper(self, p):
        sound = 210
        if self.rounds(p) < sound:
            return 0
        else:
            return random.randint(0, 100)

    def update(self):
        newclass = Classroom(self.n)
        newclass.setbegin()
        for i in range(self.n):
            for j in range(self.n):
                newclass.a[i][j].state = self.upper(self.a[i][j])
        self.a = newclass.a

    def sumsound(self):
        s = 0
        for i in range(self.n):
            for j in range(self.n):
                s += self.a[i][j].state
        return s


c = Classroom(7)
c.setbegin()
if __name__ == '__main__':
    i = 0
    while c.sumsound() > 0:
        c.show()
        print(i)
        c.update()
        i += 1

    def how(n):
        s = Classroom(n)
        s.setbegin()
        i = 0
        while s.sumsound() > 0:
            s.update()
            i += 1
        return i
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    ge = 15
    n = 40
    c = Classroom(n)
    c.setbegin()

    def drawone(i, j, c):
        if c.a[i][j].state != 0:
            pygame.draw.rect(
                dissurf, (0, 0, c.a[i][j].state*2.5), (i*ge, j*ge, ge-5, ge-5))
        else:
            pygame.draw.rect(dissurf, BLACK, (i*ge, j*ge, ge-5, ge-5))
    pygame.init()
    dissurf = pygame.display.set_mode((n*ge, n*ge))
    dissurf.fill(BLACK)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        c.update()
        for i in range(n):
            for j in range(n):
                drawone(i, j, c)
        pygame.display.update()
