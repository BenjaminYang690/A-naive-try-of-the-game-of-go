import turtle as tt
import tkinter as tk
import time
import math
import random
'''
sgf文件读取部分
'''
def anls(sgfname):# 简易sgf文件读取，按部就班
    f = open(sgfname, 'rb')
    bdata = f.readlines()[0]
    data = str(bdata, encoding='gbk')
    dtlst = data.split(';')[1:-1]
    def anls_info(info):
        infolst = info.split(']')[:-1]
        infodic = {}
        for c in infolst:
            infodic[c[:2]] = c[3:]
        return infodic
    infodic=anls_info(dtlst[0])
    go = dtlst[1:]
    f.close()
    return (infodic, go)


'''
围棋逻辑部分
'''
charset='abcdefghijklmnopqrstuvwxyz'

class gogame:
    
    def __init__(self,info):
        self.info=info# sgf文件中包含的棋谱信息头
        self.SZ=int(info['SZ'])# Size
        self.elems=[[0 for i in range(self.SZ)] for j in range(self.SZ)]# 棋盘二维数组
        self.record=[]# 着手栈

    def init_draw(self):# 画出棋盘

        tt.clear()
        tt.color('black')
        d=33
        r=33*2/5
        a=(self.SZ-1)//2
        tt.screensize(800,800,'burlywood')
        tt.title(self.info['PB']+' VS '+self.info['PW'])
        tt.speed(1000)
        tt.ht()
        tt.up()
        tt.goto(-a*d,-a*d)
        tt.down()
        tt.goto(a*d,-a*d)
        tt.goto(a*d,a*d)
        tt.goto(-a*d,a*d)
        tt.goto(-a*d,-a*d)
        for j in range(-a,a+1):
            tt.up()
            tt.goto(-a*d,j*d)
            tt.down()
            tt.goto(a*d,j*d)
        for i in range(-a,a+1):
            tt.up()
            tt.goto(i*d,-a*d)
            tt.down()
            tt.goto(i*d,a*d)
        # 下面是天元与星位的标记
        def Point(x,y):
            tt.up()
            tt.goto(x,y-3)
            tt.down()
            tt.begin_fill()
            tt.circle(3)
            tt.end_fill()
            tt.up()
            tt.goto(0,0)
            tt.down()
        Point(0,0)
        if self.SZ==19:
            Point(6*d,6*d)
            Point(6*d,-6*d)
            Point(-6*d,6*d)
            Point(-6*d,-6*d)
        elif self.SZ==13:
            Point(3*d,3*d)
            Point(3*d,-3*d)
            Point(-3*d,3*d)
            Point(-3*d,-3*d)
        # 下面是坐标的标记
        def Write(x,y,s):
            tt.up()
            tt.goto(x,y)
            tt.down()
            tt.write(s,font=('Arial',14,'normal'))
            tt.up()
            tt.home()
            tt.down()
        for j in range(self.SZ):
            Write(-(a-j)*d-2,a*d+21,charset[j])
            Write(-(a-j)*d-2,-a*d-35,charset[j])
        for j in range(self.SZ):
            Write(a*d+21,(a-j)*d-7,str(j))
            if j<10:
                Write(-(a)*d-28,(a-j)*d-7,str(j))
            else:
                Write(-(a)*d-35,(a-j)*d-7,str(j))

    def push(self,dt):# 放置棋子的元操作，逻辑意义

        self.record.append(dt)
        if dt=='W[]':
            print('白方虚着')
            return dt
        if dt=='B[]':
            print('黑方虚着')
            return dt
        i=charset.index(dt[-2])# 第i行第j列
        j=charset.index(dt[-3])

        if dt[0]=='W':
            self.elems[i][j]=-1
        elif dt[0]=='B':
            self.elems[i][j]=1
        else:
            self.elems[i][j]=0

    def push_draw(self,dt):# 放置棋子的元操作，同时画出图像
        
        self.push(dt)
        
        if dt[-2:]=='[]':
            return
        
        i=charset.index(dt[-2])# 第i行第j列
        j=charset.index(dt[-3])
        a=(self.SZ-1)//2
        d=33
        r=33*2/5
        x,y=(-a+j)*d,(a-i)*d
        tt.ht()
        
        if dt[0]=='W':
            tt.up()
            tt.goto(x,y-r)
            tt.down()
            tt.begin_fill()
            tt.color('white')
            tt.circle(r)
            tt.end_fill()
            tt.up()
            tt.home()
            tt.color('black')
            tt.down()
        elif dt[0]=='B':
            tt.up()
            tt.goto(x,y-r)
            tt.down()
            tt.begin_fill()
            tt.color('black')
            tt.circle(r)
            tt.end_fill()
            tt.up()
            tt.home()
            tt.down()
        else:
            tt.up()
            tt.goto(x,y-r-3)
            tt.down()
            tt.begin_fill()
            tt.color('burlywood')
            tt.circle(r+3)
            tt.end_fill()
            tt.color('black')
            if i-1>=0:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x,y+r+3)
            if i+1<=self.SZ-1:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x,y-r-3)
            if j-1>=0:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x-r-3,y)
            if j+1<=self.SZ-1:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x+r+3,y)
            tt.up()
            tt.home()
            tt.down()

    def pop(self):# 撤销上次元操作，逻辑意义
        dt=self.record.pop()
        if dt=='W[]':
            return dt
        if dt=='B[]':
            return dt
        i=charset.index(dt[-2])# 第i行第j列
        j=charset.index(dt[-3])

        if dt[0]=='d':
            if dt[1]=='W':
                self.elems[i][j]=-1
            else:
                self.elems[i][j]=1
        else:
            self.elems[i][j]=0

        return dt

    def pop_draw(self):# 撤销上次元操作，同时画出图像

        dt=self.pop()
        if dt=='W[]':
            return
        if dt=='B[]':
            return
        
        i=charset.index(dt[-2])# 第i行第j列
        j=charset.index(dt[-3])
        a=(self.SZ-1)//2
        d=33
        r=33*2/5
        x,y=(-a+j)*d,(a-i)*d
        tt.ht()
        if dt[0]=='d':
            if dt[1]=='W':
                tt.up()
                tt.goto(x,y-r)
                tt.down()
                tt.begin_fill()
                tt.color('white')
                tt.circle(r)
                tt.end_fill()
                tt.up()
                tt.home()
                tt.color('black')
                tt.down()
            else:
                tt.up()
                tt.goto(x,y-r)
                tt.down()
                tt.begin_fill()
                tt.color('black')
                tt.circle(r)
                tt.end_fill()
                tt.up()
                tt.home()
                tt.down()   
        else:
            tt.up()
            tt.goto(x,y-r-3)
            tt.down()
            tt.begin_fill()
            tt.color('burlywood')
            tt.circle(r+3)
            tt.end_fill()
            tt.color('black')
            if i-1>=0:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x,y+r+3)
            if i+1<=self.SZ-1:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x,y-r-3)
            if j-1>=0:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x-r-3,y)
            if j+1<=self.SZ-1:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x+r+3,y)
            tt.up()
            tt.home()
            tt.down()
        
    def components(self):# 得到棋子的连通分支
        com=[[i*self.SZ+j+1 for j in range(self.SZ)] for i in range(self.SZ)]
        for i in range(self.SZ):
            for j in range(self.SZ):
                if j+1<self.SZ:
                    if self.elems[i][j]==self.elems[i][j+1]:
                        for u in range(self.SZ):
                            for v in range(self.SZ):
                                if u==i and v==j+1:
                                    continue
                                if com[u][v]==com[i][j+1]:
                                    com[u][v]=com[i][j]
                        com[i][j+1]=com[i][j]
                if i+1<self.SZ:
                    if self.elems[i][j]==self.elems[i+1][j]:
                        for u in range(self.SZ):
                            for v in range(self.SZ):
                                if u==i+1 and v==j:
                                    continue
                                if com[u][v]==com[i+1][j]:
                                    com[u][v]=com[i][j]
                        com[i+1][j]=com[i][j]
        vset=set()
        for line in com:
            vset.update(set(line))
        comdic={}
        for i in range(self.SZ):
            for j in range(self.SZ):
                comdic.setdefault(com[i][j],[]).append([i,j])
        return list(comdic.values())
    
    def check(self):# 提子，逻辑意义
        dt=self.record[-1]
        if dt=='W[]':
            return
        if dt=='B[]':
            return
        i,j=charset.index(dt[3]),charset.index(dt[2])
        
        def neighbor(poslst):
            neighborlst=[]
            for pos in poslst:
                i,j=pos
                if i+1<self.SZ and [i+1,j] not in poslst:
                    neighborlst.append([i+1,j])
                if i-1>=0 and [i-1,j] not in poslst:
                    neighborlst.append([i-1,j])
                if j+1<self.SZ and [i,j+1] not in poslst:
                    neighborlst.append([i,j+1])
                if j-1>=0 and [i,j-1] not in poslst:
                    neighborlst.append([i,j-1])
            return neighborlst
        def is_live(poslst):
            for nb in neighbor(poslst):
                if self.elems[nb[0]][nb[1]]==0:
                    return True
            return False
        def get_died():
            diedblocks=[]
            for poslst in self.components():
                if self.elems[poslst[0][0]][poslst[0][1]]!=0 and (not is_live(poslst)):
                    diedblocks.append(poslst)
            return diedblocks
        def remove(poslst):
            for pos in poslst:
                x,y=pos
                u,v=charset[y],charset[x]
                if self.elems[x][y]==1:
                    dt='dB['+u+v+']'
                else:
                    dt='dW['+u+v+']'
                self.push(dt)

        Diedblocks=get_died()
        if len(Diedblocks)==0:
            return
        elif len(Diedblocks)==1:
            remove(Diedblocks[0])
        else:
            for poslst in Diedblocks:
                if [i,j] in poslst:
                    continue
                remove(poslst)

    def check_draw(self):# 提子，同时画出图像
        dt=self.record[-1]
        if dt=='W[]':
            return
        if dt=='B[]':
            return
        i,j=charset.index(dt[3]),charset.index(dt[2])
        
        def neighbor(poslst):
            neighborlst=[]
            for pos in poslst:
                i,j=pos
                if i+1<self.SZ and [i+1,j] not in poslst:
                    neighborlst.append([i+1,j])
                if i-1>=0 and [i-1,j] not in poslst:
                    neighborlst.append([i-1,j])
                if j+1<self.SZ and [i,j+1] not in poslst:
                    neighborlst.append([i,j+1])
                if j-1>=0 and [i,j-1] not in poslst:
                    neighborlst.append([i,j-1])
            return neighborlst
        def is_live(poslst):
            for nb in neighbor(poslst):
                if self.elems[nb[0]][nb[1]]==0:
                    return True
            return False
        def get_died():
            diedblocks=[]
            for poslst in self.components():
                if self.elems[poslst[0][0]][poslst[0][1]]!=0 and (not is_live(poslst)):
                    diedblocks.append(poslst)
            return diedblocks
        def remove(poslst):
            for pos in poslst:
                x,y=pos
                u,v=charset[y],charset[x]
                if self.elems[x][y]==1:
                    dt='dB['+u+v+']'
                else:
                    dt='dW['+u+v+']'
                self.push_draw(dt)

        Diedblocks=get_died()
        if len(Diedblocks)==0:
            return
        elif len(Diedblocks)==1:
            remove(Diedblocks[0])
        else:
            for poslst in Diedblocks:
                if [i,j] in poslst:
                    continue
                remove(poslst)

    def show_latest(self):# 在图像上显示最近一步着手

        if len(self.record)==1 and self.record[0][-2:]=='[]':
            return
        
        idx=-1
        while self.record[idx][0]=='d' or self.record[idx][-2:]=='[]':
            idx-=1
        dt=self.record[idx]
        i=charset.index(dt[-2])# 第i行第j列
        j=charset.index(dt[-3])
        
        a=(self.SZ-1)//2
        d=33
        r=33*2/5
        x,y=(-a+j)*d,(a-i)*d
        tt.up()
        tt.shape('circle')
        tt.shapesize(0.5)
        tt.color('red')
        tt.goto(x,y)
        tt.st()
        tt.down()
        
    def nxt(self,dt):# 一手棋，逻辑意义
        self.push(dt)
        self.check()

    def nxt_draw(self,dt):# 一手棋，同时画出图像
        self.push_draw(dt)
        self.check_draw()
        self.show_latest()

    def last(self):# 撤回一手棋，逻辑意义
        if self.record[-1]=='W[]' or self.record[-1]=='B[]':
            self.pop()
        while self.record[-1][0]=='d':
            self.pop()
        self.pop()

    def last_draw(self):# 撤回一手棋，同时画出图像
        if self.record[-1]=='W[]' or self.record[-1]=='B[]':
            self.pop_draw()
        while self.record[-1][0]=='d':
            self.pop_draw()
        self.pop_draw()
        self.show_latest()

    def run(self,go):# 运行若干手棋，逻辑意义
        for dt in go:
            self.nxt(dt)

    def run_draw(self,go,sleep=1):# 运行若干手棋，同时画出图像
        for dt in go:
            self.nxt_draw(dt)
            time.sleep(sleep)

    def value(self):# 粗略计算当前势力，逻辑

        def neighbor(poslst):
            neighborlst=[]
            for pos in poslst:
                i,j=pos
                if i+1<self.SZ and [i+1,j] not in poslst:
                    neighborlst.append([i+1,j])
                if i-1>=0 and [i-1,j] not in poslst:
                    neighborlst.append([i-1,j])
                if j+1<self.SZ and [i,j+1] not in poslst:
                    neighborlst.append([i,j+1])
                if j-1>=0 and [i,j-1] not in poslst:
                    neighborlst.append([i,j-1])
            return neighborlst

        def judge(distance):
            assert type(distance)==int and distance>=1
            if distance>=5:
                return 0
            return 16//(2**distance)

        valuemtx=[[0 for _ in range(self.SZ)] for _ in range(self.SZ)]
        com=self.components()
        Bnum,Wnum=0,0
        for block in com:
            if self.elems[block[0][0]][block[0][1]]==1:
                Bnum+=len(block)
            elif self.elems[block[0][0]][block[0][1]]==-1:
                Wnum+=len(block)
            else:
                neibor=neighbor(block)
                for empty in block:
                    i,j=empty
                    for pos in neibor:
                        x,y=pos
                        valuemtx[i][j]+=self.elems[x][y]*judge(abs(x-i)+y+j)
                        valuemtx[i][j]+=self.elems[x][y]*judge(abs(x-i)+2*self.SZ-y-j)
                        valuemtx[i][j]+=self.elems[x][y]*judge(abs(y-j)+x+i)
                        valuemtx[i][j]+=self.elems[x][y]*judge(abs(y-j)+2*self.SZ-x-i)
                        valuemtx[i][j]+=self.elems[x][y]*judge(abs(x-i)+abs(y-j))
        for i in range(self.SZ):
            for j in range(self.SZ):
                if valuemtx[i][j]>0:
                    Bnum+=1
                elif valuemtx[i][j]<0:
                    Wnum+=1
                else:
                    pass
        return Bnum,Wnum,valuemtx

    def value_draw(self):# 显示当前势力
        valuemtx=self.value()[2]
        for i in range(self.SZ):
            for j in range(self.SZ):
                if valuemtx[i][j]>0:
                    a=(self.SZ-1)//2
                    d=33
                    r=33*2/5
                    x,y=(-a+j)*d,(a-i)*d
                    tt.up()
                    tt.goto(x,y-2)
                    tt.color('black')
                    tt.down()
                    tt.begin_fill()
                    tt.circle(2)
                    tt.end_fill()
                    tt.up()
                elif valuemtx[i][j]<0:
                    a=(self.SZ-1)//2
                    d=33
                    r=33*2/5
                    x,y=(-a+j)*d,(a-i)*d
                    tt.up()
                    tt.goto(x,y-2)
                    tt.color('white')
                    tt.down()
                    tt.begin_fill()
                    tt.circle(2)
                    tt.end_fill()
                    tt.color('black')
                    tt.up()    
                else:
                    pass
        self.show_latest()

    def strategy(self):# 推荐着手
        
        if self.record!=[]:
            idx=-1
            while self.record[idx][0]=='d':
                idx-=1
            latest=self.record[idx]
        else:
            latest='W'
        
        if latest[0]=='W':
            maxvalue=-math.inf
            maxposlst=[]
            for i in range(self.SZ):
                for j in range(self.SZ):
                    if self.elems[i][j]!=0:
                        continue
                    dt='B['+charset[j]+charset[i]+']'
                    self.nxt(dt)
                    vl=self.value()[0]-self.value()[1]
                    if vl>=maxvalue:
                        maxvalue=vl
                        maxposlst.append([i,j,vl])
                    self.last()
            if maxvalue<-self.SZ**2//4:
                return 'B[]'
            maxlst=[]
            for c in maxposlst:
                if c[2]==maxposlst[-1][2]:
                    maxlst.append(c[:2])
            x,y=maxlst[random.randint(0,len(maxlst)-1)]
            Nxtdt='B['+charset[y]+charset[x]+']'
        else:
            maxvalue=-math.inf
            maxposlst=[]
            for i in range(self.SZ):
                for j in range(self.SZ):
                    if self.elems[i][j]!=0:
                        continue
                    dt='W['+charset[j]+charset[i]+']'
                    self.nxt(dt)
                    vl=self.value()[1]-self.value()[0]
                    if vl>=maxvalue:
                        maxvalue=vl
                        maxposlst.append([i,j,vl])
                    self.last()
            if maxvalue<-self.SZ**2//4:
                return 'W[]'
            maxlst=[]
            for c in maxposlst:
                if c[2]==maxposlst[-1][2]:
                    maxlst.append(c[:2])
            x,y=maxlst[random.randint(0,len(maxlst)-1)]
            Nxtdt='W['+charset[y]+charset[x]+']'

        return Nxtdt

'''
程序交互部分
'''

def PVP(SZ=19):

    def input_pos():
        numstr=[str(_) for _ in range(SZ)]
        while True:
            i,j=input('Input the position. \'-1 -1\' to exit.').split()
            if i=='-1' and j=='-1':
                break
            if i in charset[:SZ] and j in numstr:
                if g.elems[int(j)][charset.index(i)]==0:
                    break
            if j in charset[:SZ] and i in numstr:
                if g.elems[int(i)][charset.index(j)]==0:
                    break
        if i=='-1':
            return ''
        if i in charset:
            pos=i+charset[int(j)]
        else:
            pos=j+charset[int(i)]
        return pos
    
    info={'SZ':SZ,'PB':'棋手','PW':'棋手'}
    g=gogame(info)
    g.init_draw()
    counter=0
    while True:
        pos=input_pos()
        if counter%2==0:
            dt='B['+pos+']'
        else:
            dt='W['+pos+']'
        g.nxt_draw(dt)
        print(dt)
        counter+=1
        if pos=='':
            return

def PVC(SZ=19):

    def input_pos():
        numstr=[str(_) for _ in range(SZ)]
        while True:
            i,j=input('Input the position. \'-1 -1\' to exit.').split()
            if i=='-1' and j=='-1':
                break
            if i in charset[:SZ] and j in numstr:
                if g.elems[int(j)][charset.index(i)]==0:
                    break
            if j in charset[:SZ] and i in numstr:
                if g.elems[int(i)][charset.index(j)]==0:
                    break
        if i=='-1':
            return ''
        if i in charset:
            pos=i+charset[int(j)]
        else:
            pos=j+charset[int(i)]
        return pos
    
    mode=int(input('Input 1 to go first. Otherwise -1. '))
    if mode==1:
        info={'SZ':SZ,'PB':'棋手','PW':'电脑'}
    else:
        info={'SZ':SZ,'PW':'棋手','PB':'电脑'}
    g=gogame(info)
    g.init_draw()
    counter=0
    if mode==1:
        while True:
            if counter%2==0:
                pos=input_pos()
                dt='B['+pos+']'
            else:
                dt=g.strategy()
            g.nxt_draw(dt)
            print(dt)
            counter+=1
            if dt[-2:]=='[]':
                return g
    else:
        while True:
            if counter%2==1:
                pos=input_pos()
                dt='B['+pos+']'
            else:
                dt=g.strategy()
            g.nxt_draw(dt)
            print(dt)
            counter+=1
            if dt[-2:]=='[]':
                return g

def CVC(SZ=19):
    info={'SZ':SZ,'PB':'电脑','PW':'电脑'}
    g=gogame(info)
    g.init_draw()
    counter=0
    while True:
        dt=g.strategy()
        pos=dt[2:-1]
        g.nxt_draw(dt)
        print(dt)
        counter+=1
        if pos=='':
            return g

def demo():
    Mode=int(input('Input 0 to PVP, 1 to PVC, 2 to CVC: '))
    SZ=int(input('Input the size of the board: '))
    if Mode==0:
        PVP(SZ)
    elif Mode==1:
        PVC(SZ)
    else:
        CVC(SZ)
    

fname='/Users/yangpeng/Downloads/自己写的一些程序/黑胜5.75子.sgf'
info,go=anls(fname)
g=gogame(info)
g.init_draw()
g.run_draw(go[0:25],0)
