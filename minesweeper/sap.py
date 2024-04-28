import pyxel
from sys import setrecursionlimit
class Game():
    def __init__(self,width,height):
        self.width=width
        self.height=height
        pyxel.init(width*16,height*16+10,title='minesweeper',fps=60,display_scale=2)
        self.mines=[[[-1 if pyxel.rndi(0,15)<2 else 0,1,0,0] for x in range(width)] for y in range(height)]
        self.generate()
        pyxel.camera(0,-10)
        setrecursionlimit(100000)
        self.lose=False
        self.win=False
        self.showmines=True
        pyxel.run(self.update,self.draw)

    def generate(self):
        for x in range(1,self.width-1):
            if self.mines[0][x][0]!=-1:
                l=[self.mines[0][x-1][0],
                self.mines[1][x-1][0],
                self.mines[1][x][0],
                self.mines[1][x+1][0],
                self.mines[0][x+1][0]]
                self.mines[0][x][0]=l.count(-1)
                del l
            
            if self.mines[self.height-1][x][0]!=-1:
                l=[self.mines[self.height-1][x-1][0],
                self.mines[self.height-2][x-1][0],
                self.mines[self.height-2][x][0],
                self.mines[self.height-2][x+1][0],
                self.mines[self.height-1][x+1][0]]
                self.mines[self.height-1][x][0]=l.count(-1)
                del l
            

            for y in range(1,self.height-1):
                if self.mines[y][x][0]==-1:
                    
                    continue
                else:
                    l=[self.mines[y+1][x][0],
                       self.mines[y-1][x][0],
                       self.mines[y][x+1][0],
                       self.mines[y][x-1][0],
                       self.mines[y+1][x+1][0],
                       self.mines[y-1][x+1][0],
                       self.mines[y+1][x-1][0],
                       self.mines[y-1][x-1][0]]                    
                    self.mines[y][x][0]=l.count(-1)
                    del l
        if self.mines[0][0][0]!=-1:

            l=[self.mines[0][1][0],
               self.mines[1][0][0],
               self.mines[1][1][0]]
            self.mines[0][0][0]=l.count(-1)
            del l
        

        if self.mines[0][self.width-1][0]!=-1:

            l=[self.mines[0][self.width-2][0],
               self.mines[1][self.width-1][0],
               self.mines[1][self.width-2][0]]
            self.mines[0][self.width-1][0]=l.count(-1)
            del l
        

        if self.mines[self.height-1][0][0]!=-1:

            l=[self.mines[self.height-2][0][0],
               self.mines[self.height-1][1][0],
               self.mines[self.height-2][1][0]]
            self.mines[self.height-1][0][0]=l.count(-1)
            del l
        

        if self.mines[self.height-1][self.width-1][0]!=-1:

            l=[self.mines[self.height-2][self.width-1][0],
               self.mines[self.height-1][self.width-2][0],
               self.mines[self.height-2][self.width-2][0]]
            self.mines[self.height-1][self.width-1][0]=l.count(-1)
            del l
        

        for y in range(1,self.height-1):
            if self.mines[y][0][0]!=-1:
                l=[self.mines[y][1][0],
                self.mines[y-1][0][0],
                self.mines[y-1][1][0],
                self.mines[y+1][0][0],
                self.mines[y+1][1][0]]
                self.mines[y][0][0]=l.count(-1)
                del l
            
            if self.mines[y][self.width-1][0]!=-1:
                l=[self.mines[y][self.width-2][0],
                self.mines[y-1][self.width-1][0],
                self.mines[y-1][self.width-2][0],
                self.mines[y+1][self.width-1][0],
                self.mines[y+1][self.width-2][0]]
                self.mines[y][self.width-1][0]=l.count(-1)  
                del l

    def check_mines_count(self,x,y):
        if x==0 and y==0:
            l=[self.mines[0][1][2],self.mines[1][0][2],self.mines[1][1][2]]  
            d=[[1,0],[0,1],[1,1]]          
        elif x==0 and y==self.height-1:
            l=[self.mines[self.height-2][0][2],self.mines[self.height-1][1][2],self.mines[self.height-2][1][2]]
            d=[[0,self.height-2],[1,self.height-1],[1,self.height-2]]
        elif x==self.width-1 and y==0:
            l=[self.mines[0][self.width-2][2],self.mines[1][self.width-1][2],self.mines[1][self.width-2][2]]
            d=[[self.width-2,0],[self.width-1,1],[self.width-2,1]]
        elif x==self.width-1 and y==self.height-1:
            l=[self.mines[self.height-2][self.width-1][2],self.mines[self.height-1][self.width-2][2],self.mines[self.height-2][self.width-2][2]]
            d=[[self.width-1,self.height-2],[self.width-2,self.height-1],[self.width-2,self.height-2]]
        elif x==0:
            l=[self.mines[y][1][2],
               self.mines[y-1][0][2],
               self.mines[y-1][1][2],
               self.mines[y+1][0][2],
               self.mines[y+1][1][2]]
            d=[[1,y],[0,y-1],[1,y-1],[0,y+1],[1,y+1]]
        elif x==self.width-1:
            l=[self.mines[y][self.width-2][2],
               self.mines[y-1][self.width-1][2],
               self.mines[y-1][self.width-2][2],
               self.mines[y+1][self.width-1][2],
               self.mines[y+1][self.width-2][2]]
            d=[[self.width-2,y],[self.width-1,y-1],[self.width-2,y-1],[self.width-1,y+1],[self.width-2,y+1]]
        elif y==0:
            l=[self.mines[0][x-1][2],
               self.mines[1][x-1][2],
               self.mines[1][x][2],
               self.mines[1][x+1][2],
               self.mines[0][x+1][2]]
            d=[[x-1,0],[x+1,0],[x-1,1],[x+1,1],[x,1]]
        elif y==self.height-1:
            l=[self.mines[self.height-1][x-1][2],
               self.mines[self.height-2][x-1][2],
               self.mines[self.height-2][x][2],
               self.mines[self.height-2][x+1][2],
               self.mines[self.height-1][x+1][2]]
            d=[[x-1,self.height-1],[x+1,self.height-2],[x-1,self.height-2],[x+1,self.height-1],[x,self.height-2]]
        else:
            l=[self.mines[y+1][x][2],
                self.mines[y-1][x][2],
                self.mines[y][x+1][2],
                self.mines[y][x-1][2],
                self.mines[y+1][x+1][2],
                self.mines[y-1][x+1][2],
                self.mines[y+1][x-1][2],
                self.mines[y-1][x-1][2]]
            d=[[x+1,y],[x-1,y],[x,y+1],[x,y-1],[x+1,y+1],[x-1,y+1],[x+1,y-1],[x-1,y-1]]
        c=l.count(1)
        del l
        return self.mines[y][x][0]==c,d

    def openc(self,x,y):
        if not self.lose and not self.win:
            print(x,y)
            if self.mines[y][x][2]==0:
                if self.mines[y][x][1]==1:
                    if self.mines[y][x][0]==-1:
                        self.lose=True
                        print('LOSE')
                    else:
                        self.mines[y][x][1]=0
                        if self.mines[y][x][0]==0:
                            t,d=self.check_mines_count(x,y)
                            if t and self.mines[y][x][3]==0:
                                self.mines[y][x][3]=1
                                for i in d:
                                    self.openc(i[0],i[1])
                elif self.mines[y][x][1]==0 and self.mines[y][x][0]!=0:
                    t,d=self.check_mines_count(x,y)
                    if t and self.mines[y][x][3]==0:
                        self.mines[y][x][3]=1
                        for i in d:
                            if self.mines[i[1]][i[0]][0]>0:
                                self.mines[i[1]][i[0]][1]=0
                            else:
                                self.openc(i[0],i[1])

    def wincheck(self):
        points=0
        for x in range(self.width):
            for y in range(self.height):
                if (self.mines[y][x][0]==-1 and self.mines[y][x][2]==1) or (self.mines[y][x][0]!=-1 and self.mines[y][x][1]==0):
                    points+=1
        return points==self.width*self.height

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT,hold=60,repeat=120):
            if not self.lose and not self.win:
                self.openc(pyxel.mouse_x//16,pyxel.mouse_y//16)
                self.win=self.wincheck()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT,hold=60,repeat=120):
            if not self.lose and not self.win and self.mines[pyxel.mouse_y//16][pyxel.mouse_x//16][1]==1:
                self.mines[pyxel.mouse_y//16][pyxel.mouse_x//16][2]=(self.mines[pyxel.mouse_y//16][pyxel.mouse_x//16][2]+1)%2

    def draw(self):
        pyxel.cls(0)
        for x in range(self.width):
            for y in range(self.height):
                if self.mines[y][x][1]==0:
                    pyxel.rectb(x*16,y*16,16,16,pyxel.COLOR_ORANGE)
                    pyxel.text(x*16+7,y*16+7,str(self.mines[y][x][0]),(self.mines[y][x][0])%16)
                else:
                    pyxel.rectb(x*16,y*16,16,16,pyxel.COLOR_ORANGE)
                    if self.mines[y][x][2]==0:
                        pyxel.rect(x*16+2,y*16+2,12,12,pyxel.COLOR_ORANGE)
                    else:
                        pyxel.rect(x*16+2,y*16+2,12,12,pyxel.COLOR_RED)
        pyxel.pset(pyxel.mouse_x,pyxel.mouse_y,pyxel.COLOR_WHITE)
        if -1<pyxel.mouse_x<self.width*16 and -1<pyxel.mouse_y<self.height*16:
            pyxel.text(0,-5,' '.join(map(str,self.mines[pyxel.mouse_y//16][pyxel.mouse_x//16])),pyxel.COLOR_ORANGE)
       
        pyxel.text(40,-5,str(self.win),pyxel.COLOR_ORANGE)

Game(20,20)

    