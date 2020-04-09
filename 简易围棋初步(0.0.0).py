import turtle as tt
import tkinter as tk
import time
'''
sgf文件读取部分
'''
def anls(sgfname):
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
        self.info=info
        self.SZ=int(info['SZ'])
        self.elems=[[0 for i in range(self.SZ)] for j in range(self.SZ)]# 棋盘二维数组
        self.record=[]# 着手栈
        self.avlb=[(i,j) for i in range(self.SZ) for j in range(self.SZ)]# 空位置

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

    def push(self,dt):# 放置棋子的元操作

        self.record.append(dt)
        if dt=='W[]':
            print('白方虚着')
            return
        if dt=='B[]':
            print('黑方虚着')
            return
        i=charset.index(dt[-2])# 第i行第j列
        j=charset.index(dt[-3])
        
        a=(self.SZ-1)//2
        d=33
        r=33*2/5
        x,y=(-a+j)*d,(a-i)*d
        tt.ht()
        
        if dt[0]=='W':
            self.elems[i][j]=-1

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
            self.elems[i][j]=1

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
            self.elems[i][j]=0

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
            if i+1<=19:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x,y-r-3)
            if j-1>=0:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x-r-3,y)
            if j+1<=19:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x+r+3,y)
            tt.up()
            tt.home()
            tt.down()

    def pop(self):
        dt=self.record.pop()
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
                self.elems[i][j]=-1

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
                self.elems[i][j]=1

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
            self.elems[i][j]=0

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
            if i+1<=19:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x,y-r-3)
            if j-1>=0:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x-r-3,y)
            if j+1<=19:
                tt.up()
                tt.goto(x,y)
                tt.down()
                tt.goto(x+r+3,y)
            tt.up()
            tt.home()
            tt.down()
        
    def components(self):
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
    
    def check(self):
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

        for poslst in self.components():
            if self.elems[poslst[0][0]][poslst[0][1]]!=0 and (not is_live(poslst)):
                if [i,j] in poslst:
                    continue
                for pos in poslst:
                    x,y=pos
                    u,v=charset[y],charset[x]
                    if self.elems[x][y]==1:
                        dt='dB['+u+v+']'
                    else:
                        dt='dW['+u+v+']'
                    self.push(dt)

    def show_latest(self):
        idx=-1
        while self.record[idx][0]=='d':
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
        
    def nxt(self,dt):
        self.push(dt)
        self.check()
        self.show_latest()

    def last(self):
        if self.record[-1]=='W[]' or self.record[-1]=='B[]':
            self.pop()
        while self.record[-1][0]=='d':
            self.pop()
        self.pop()
        self.show_latest()

    def run(self,go,sleep=1):
        for dt in go:
            self.nxt(dt)
            time.sleep(sleep)

'''
程序交互部分
'''

    

fname='/Users/yangpeng/Downloads/自己写的一些程序/黑中盘胜.sgf'
info,go=anls(fname)
g=gogame(info)
