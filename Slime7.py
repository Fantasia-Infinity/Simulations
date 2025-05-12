# -*- coding: utf-8 -*-
"""
Created on Wed May 03 14:03:42 2017
@author: Fantasia
"""
import random
import pygame
import math
class Unit:
    def __init__(self,c,state,c2,c3,life):
        self.c=c#信息素浓度
        self.c2=c2
        self.c3=c3#b生长细胞的信息素
        self.s=state#状态：0-空位 1-a生长细胞 2-物体 3-捕食细胞 4-b生长细胞
        self.l=life#生命值
class Ground:
    def __init__(self,n):
        self.ground=[]
        self.n=n
        self.l=[]
        for i in range(n):
            self.ground.append([])
        for l in self.ground:
            for i in range(n):
                l.append(Unit(0,0,0,0,0))
    def show(self):
        for i in range(self.n):
            print([u.s for u in self.ground[i]])
    def randinit(self):
        for i in range(self.n):
            for j in range(self.n):
                self.ground[i][j]=Unit(random.random(),0,0,random.random(),0)
    def addslime(self,x,y):
        self.ground[x][y].s=1
        self.ground[x][y].l=50#满100
    def addslime3(self,x,y):
        self.ground[x][y].s=4
        self.ground[x][y].l=50
    def addglass(self,x,y):
        self.ground[x][y].s=2
        self.ground[x][y].l=15#护甲会降解
    def addpredator(self,x,y):
        self.ground[x][y].s=3
        self.ground[x][y].l=100
    def inrange(self,x,y):
        return (x in range(n)) and (y in range(n))
    def addc(self,x,y,n):
        sc=self.ground[x][y].c
#        if sc<10000:
        self.ground[x][y].c=sc+n
    def addc2(self,x,y,n):
        sc2=self.ground[x][y].c2
        self.ground[x][y].c2=sc2+n
    def addc3(self,x,y,n):
        sc3=self.ground[x][y].c3
        self.ground[x][y].c3=sc3+n
    def release(self,x,y):
        sc=self.ground[x][y].c###
        k=0.01
        try:
            dc=k*sc/self.abalcount(x,y)
        except:
            dc=0.0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if self.inrange(x+i,y+j):
                    if not (i==j and i==0):
                        self.addc(x+i,y+j,dc)
    def release3(self,x,y):
        sc=self.ground[x][y].c3####
        k=0.01
        try:
            dc=k*sc/self.abalcount(x,y)
        except:
            dc=0.0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if self.inrange(x+i,y+j):
                    if not (i==j and i==0):
                        self.addc3(x+i,y+j,dc)
    def nrelease(self,x,y):
        sc=self.ground[x][y].c#根据要捕食的细胞/自己的信息素浓度施放自己的信息素
        k=0.9
        try:
            dc=k*sc/self.abalcount(x,y)
        except:
            dc=0.0
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if self.inrange(x+i,y+j):
                    if not (i==j and i==0):
                        self.addc2((x+i),(y+j),dc)
    def move(self,x,y,nx,ny):
        thes=self.ground[x][y].s
        thel=self.ground[x][y].l
        self.ground[x][y].s=0
        self.ground[x][y].l=0
        x=nx
        y=ny
        self.ground[x][y].s=thes
        self.ground[x][y].l=thel
    def die(self,x,y):
        self.ground[x][y].s=0
        self.ground[x][y].l=0
    def upperslime(self,x,y):
        nx=x
        ny=y
        myc=self.ground[x][y].c
        myc2=self.ground[x][y].c2
        myc3=self.ground[x][y].c3
        k1=1.0
        k2=7.0
        k3=3.0
        totalmyc=k1*myc+k3*myc3-k2*myc2
        count=0#对周围的非空位计数
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if not (i==j and i==0):
                    if self.inrange(x+i,y+j):
                        nc=self.ground[x+i][y+j].c
                        nc2=self.ground[x+i][y+j].c2
                        nc3=self.ground[x+i][y+j].c3
                        if self.ground[x+i][y+j].s!=0:#如果不是空位且为1就计数
                            if self.ground[x+i][y+j].s==1 or self.ground[x+i][y+j].s==4:
                                count+=1
                            else:
                                pass
                        elif self.ground[x+i][y+j].s==0:#如果周围某一个是空位：
                            if self.ground[x][y].l>=100:#如果生命值满了有能力：1、分裂 2、产生护甲
                                if self.ground[x+i][y+j].c2>0.00001:#如果信息素c2浓度超过就产生护甲
                                    self.addglass(x+i,y+j)
                                elif self.ground[x+i][y+j].c3>0.0001:
                                    self.addslime(x+i,y+j)
                                    self.ground[x][y].l=50
                                elif k1*nc+k3*nc3-k2*nc2<=totalmyc:
                                    pass
                                elif k1*nc+k3*nc3-k2*nc2>totalmyc:
                                    myc=self.ground[x+i][y+j].c
                                    myc2=self.ground[x+i][y+j].c2
                                    myc3=self.ground[x+i][y+j].c3
                                    totalmyc=k1*myc+k3*myc3-k2*myc2
                                    nx=x+i
                                    ny=y+j
                            else:
                                if k1*nc+k3*nc3-k2*nc2<=totalmyc:
                                    pass
                                elif k1*nc+k3*nc3-k2*nc2>totalmyc:
                                    myc=self.ground[x+i][y+j].c
                                    myc2=self.ground[x+i][y+j].c2
                                    myc3=self.ground[x+i][y+j].c3
                                    totalmyc=k1*myc+k3*myc3-k2*myc2
                                    nx=x+i
                                    ny=y+j
#        if count==8:
#            if self.ground[x][y].l>=100:
#                for i in [-1,0,1]:
#                    for j in [-1,0,1]:
#                        if not (i==j and i==0):#如果生命值满且于内部就给周围加资源
#                            if self.ground[x+i][y+j].s==1:
#                                self.ground[x+i][y+j].l+=5#通过控制增加的资源数可以调控聚合体稳定后的大小
#                self.die(x,y)#然后死亡
        self.move(x,y,nx,ny)
        self.ground[nx][ny].l+=1.5
        if self.ground[nx][ny].l>=100:
            self.ground[nx][ny].l=100
        self.release(nx,ny)
    def upperslime3(self,x,y):
        nx=x
        ny=y
        myc=self.ground[x][y].c
        myc2=self.ground[x][y].c2
        myc3=self.ground[x][y].c3
        k2=7.0
        k1=3.0
        k3=1.0
        totalmyc=k1*myc+k3*myc3-k2*myc2
        count=0#对周围的非空位计数
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if not (i==j and i==0):
                    if self.inrange(x+i,y+j):
                        nc=self.ground[x+i][y+j].c
                        nc2=self.ground[x+i][y+j].c2
                        nc3=self.ground[x+i][y+j].c3
                        if self.ground[x+i][y+j].s!=0:#如果不是空位且为1就计数
                            if self.ground[x+i][y+j].s==4 or self.ground[x+i][y+j].s==1:
                                count+=1
                            else:
                                pass
                        elif self.ground[x+i][y+j].s==0:#如果周围某一个是空位：
                            if self.ground[x][y].l>=100:#如果生命值满了有能力：1、分裂 2、产生护甲                               
                                if self.ground[x+i][y+j].c2>0.00001:#如果信息素c2浓度超过就产生护甲
                                    self.addglass(x+i,y+j)
                                elif self.ground[x+i][y+j].c>0.0001:#并且对方信息素足够多才能分裂
                                    self.addslime3(x+i,y+j)
                                    self.ground[x][y].l=50
                                elif k1*nc+k3*nc3-k2*nc2<=totalmyc:#
                                    pass
                                elif k1*nc+k3*nc3-k2*nc2>totalmyc:
                                    myc=self.ground[x+i][y+j].c
                                    myc2=self.ground[x+i][y+j].c2
                                    myc3=self.ground[x+i][y+j].c3
                                    totalmyc=k1*myc+k3*myc3-k2*myc2
                                    nx=x+i
                                    ny=y+j
                            else:#生命值不满只有移动的选择
                                if k1*nc+k3*nc3-k2*nc2<=totalmyc:
                                    pass
                                elif k1*nc+k3*nc3-k2*nc2>totalmyc:
                                    myc=self.ground[x+i][y+j].c
                                    myc2=self.ground[x+i][y+j].c2
                                    myc3=self.ground[x+i][y+j].c3
                                    totalmyc=k1*myc+k3*myc3-k2*myc2
                                    nx=x+i
                                    ny=y+j
#        if count==8:
#            if self.ground[x][y].l>=100:
#                for i in [-1,0,1]:
#                    for j in [-1,0,1]:
#                        if not (i==j and i==0):#如果生命值满且于内部就给周围加资源
#                            if self.ground[x+i][y+j].s==1:
#                                self.ground[x+i][y+j].l+=5#通过控制增加的资源数可以调控聚合体稳定后的大小
#                self.die(x,y)#然后死亡
        self.move(x,y,nx,ny)
        self.ground[nx][ny].l+=1.5
        if self.ground[nx][ny].l>=100:
            self.ground[nx][ny].l=100
        self.release3(nx,ny)
    def upperpredator(self,x,y):
        nx=x
        ny=y
        mc=self.ground[x][y].c#按照自己/对方的信息素浓度梯度移动
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if not (i==j and i==0):
                    if self.inrange(x+i,y+j):
                        if self.ground[x+i][y+j].s==1 or self.ground[x+i][y+j].s==4:
                            self.ground[x+i][y+j].s=3
                            self.ground[x+i][y+j].l=100
                        elif self.ground[x+i][y+j].s==0:
                            if self.ground[x+i][y+j].c<=mc:#
                                pass
                            else:
                                mc=self.ground[x+i][y+j].c#
                                nx=x+i
                                ny=y+j  
        self.move(x,y,nx,ny)
        self.nrelease(nx,ny)
        self.ground[nx][ny].l-=0.5
        if self.ground[nx][ny].l<=0:
            self.die(nx,ny)
    def upperglass(self,x,y):
        if self.ground[x][y].l<=0:
            self.ground[x][y].l=0
            self.ground[x][y].s=0
        else:#护甲生命值会减少 到零死
            self.ground[x][y].l-=1
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
    def abalcount(self,x,y):
#        count=0
#        for i in [-1,0,1]:
#            for j in [-1,0,1]:
#                if self.inrange(x+i,y+j):
#                    if self.ground[x+i][y+j].s!=2:
#                        count+=1
#        return count
        return 8
    def kuosan1(self,x,y):
        rate=0.1
        deltaout=self.ground[x][y].c*rate
        deltain=0
        for f in self.fl:
            tx,ty=f(self,x,y)
            try:
                d=self.ground[tx][ty].c*rate/self.abalcount(tx,ty)
            except:
                d=0.0
            deltain+=d
        self.ground[x][y].c+=deltain
        self.ground[x][y].c-=deltaout
    def kuosan2(self,x,y):#扩散到边界会到相反的另一边
        rate=0.9
        deltaout=self.ground[x][y].c2*rate
        deltain=0
        for f in self.fl:
            tx,ty=f(self,x,y)
            try:
                d=self.ground[tx][ty].c2*rate/self.abalcount(tx,ty)
            except:
                d=0.0
            deltain+=d
        self.ground[x][y].c2+=deltain
        self.ground[x][y].c2-=deltaout
    def kuosan3(self,x,y):
        rate=0.1
        deltaout=self.ground[x][y].c3*rate
        deltain=0
        for f in self.fl:
            tx,ty=f(self,x,y)
            try:
                d=self.ground[tx][ty].c3*rate/self.abalcount(tx,ty)
            except:
                d=0.0
            deltain+=d
        self.ground[x][y].c3+=deltain
        self.ground[x][y].c3-=deltaout
    def decoposeC(self,x,y):#信息素c的降解
        c=self.ground[x][y].c
        k=0.01
        self.ground[x][y].c-=k*c
    def decomposeC2(self,x,y):#c2的降解 对护甲的解除非常关键
        c2=self.ground[x][y].c2
        k=0.1
        self.ground[x][y].c2-=k*c2
    def decomposeC3(self,x,y):
        c3=self.ground[x][y].c3
        k=0.01
        self.ground[x][y].c3-=k*c3
    def uppergroundunit(self,x,y):
        self.kuosan1(x,y)
        self.kuosan2(x,y)
        self.kuosan3(x,y)
        if self.ground[x][y].s==1:
            self.upperslime(x,y)
        elif self.ground[x][y].s==3:
            self.upperpredator(x,y)
        elif self.ground[x][y].s==2:
            self.upperglass(x,y)
        elif self.ground[x][y].s==4:
            self.upperslime3(x,y)
        self.decomposeC2(x,y)
        self.decoposeC(x,y)
        self.decomposeC3(x,y)
    def update(self):
        l1 = list(range(self.n))
        l2 = list(range(self.n))
        random.shuffle(l1)
        random.shuffle(l2)
        for i in l1:#因并不是严格的并行更新 所以打乱更新顺序防止瞬移的bug
            for j in l2:
                self.uppergroundunit(i,j)
n=50
g=Ground(n)
g.randinit()
for i in range(200):
    g.addslime(random.randint(0,g.n-1),random.randint(0,g.n-1))
for i in range(200):
    g.addslime3(random.randint(0,g.n-1),random.randint(0,g.n-1))
g.addslime(25,25)
g.addslime3(24,24)
BLUE=(0,0,255)
BLACK=(0,0,0)
YELLOW=(0,255,0)
RED=(255,0,0)
YR=(200,100,200)
ge=6
#g.addpredator(25,25)
def drawone(i,j,c):
    if c.ground[i][j].s==0:
        pygame.draw.rect(dissurf,BLACK,(i*ge,j*ge,ge-2,ge-2))
    elif c.ground[i][j].s==1:
        pygame.draw.rect(dissurf,YELLOW,(i*ge,j*ge,ge-2,ge-2))
    elif c.ground[i][j].s==2:
        pygame.draw.rect(dissurf,BLUE,(i*ge,j*ge,ge-2,ge-2))
    elif c.ground[i][j].s==3:
        pygame.draw.rect(dissurf,RED,(i*ge,j*ge,ge-2,ge-2))
    elif c.ground[i][j].s==4:
        pygame.draw.rect(dissurf,YR,(i*ge,j*ge,ge-2,ge-2))
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
    pygame.display.update()
