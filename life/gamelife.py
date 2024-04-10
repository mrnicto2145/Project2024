import pyxel
from copy import deepcopy

class Game:
    def __init__(self,width,height,fps,neibor_s,neibor_b,scale,debug,mode):        
        self.scale=scale
        self.fps=fps
        self.neibor_s=neibor_s
        self.neibor_b=neibor_b
        self.speed=1
        self.mode=mode
        self.debug=debug
        self.debuga=debug
        self.go=True
        if self.debug:
            self.go=False  
            #Параметры экрана:длина ширина множитель сид.
            self.screen=input().split()
        else:
            self.screen=[]
        if self.screen!=[] and len(self.screen)==4:            
            self.seed=self.screen[-1].upper()
            self.screen.pop(-1)
            self.screen=list(map(int,self.screen))  
            self.width=self.screen[0]
            self.height=self.screen[1]          
            self.seed=int(self.seed,base=36)
            pyxel.init(self.screen[0],self.screen[1],title="Life",fps=self.fps,display_scale=self.screen[2]) 
            if self.seed>-1:
                self.seed=list(map(int,list(str(bin(self.seed)))[2:]))
                self.seed=[0 for _ in range(self.width*self.height-len(self.seed))]+self.seed                
                self.pix=[self.seed[self.width*i:self.width*(i+1)] for i in range(self.height)]
                self.seed="".join(list(map(str,list(map(int,self.seed)))))
            else:
                self.pix=[[0 for _ in range(self.width)] for _ in range(self.height)]                       
        else:
            self.width=width
            self.height=height
            self.fps=fps
            pyxel.init(self.width,self.height,title="Life",fps=self.fps,display_scale=scale)
            self.pix=[[int(pyxel.rndi(1,10)<=2) for _ in range(self.width)] for _ in range(self.height)]
            if self.debug:
                self.seed=[]
                for x in self.pix:
                    self.seed+=x
                self.seed=list(map(str,list(map(int,self.seed))[self.seed.index(1):]))
                self.seed=int(''.join(self.seed),base=2)
                self.seed=base36encode(self.seed)           
                  
        self.pixn=deepcopy(self.pix)
        pyxel.run(self.update,self.draw)

    def update(self):
        if self.go:            
            for y in range(self.height):
                for x in range(self.width):
                    if self.mode==0:
                        total=self.pix[y][(x+1)%self.width]+self.pix[y][(x-1)%self.width]+self.pix[(y+1)%self.height][(x+1)%self.width]+self.pix[(y+1)%self.height][(x-1)%self.width]+self.pix[(y+1)%self.height][x]+self.pix[(y-1)%self.height][(x-1)%self.width]+self.pix[(y-1)%self.height][(x+1)%self.width]+self.pix[(y-1)%self.height][x]
                    elif self.mode==1:
                        total=self.pix[y][(x+1)%self.width]+self.pix[y][(x-1)%self.width]+self.pix[(y+1)%self.height][x]+self.pix[(y-1)%self.height][x]
                    elif self.mode==2:
                        total=self.pix[(y+1)%self.height][(x+1)%self.width]+self.pix[(y+1)%self.height][(x-1)%self.width]+self.pix[(y-1)%self.height][(x-1)%self.width]+self.pix[(y-1)%self.height][(x+1)%self.width]
                    if (total in self.neibor_s and self.pix[y][x]==1) or total in self.neibor_b:
                        self.pixn[y][x]=1       
                    else:
                        self.pixn[y][x]=0 
                    total=0
            self.pix=deepcopy(self.pixn)
            if self.debug:
                self.go=False
            if self.debuga and pyxel.btnp(pyxel.KEY_F,hold=360,repeat=1200):
                self.debug=True 
                self.seed=[]
                for x in self.pix:
                    self.seed+=x
                self.seed=list(map(str,list(map(int,self.seed))[self.seed.index(1):]))
                self.seed=int(''.join(self.seed),base=2)
                self.seed=base36encode(self.seed)          
        
        if self.debug:
            if pyxel.btnp(pyxel.KEY_SPACE,hold=20,repeat=1):
                self.go=True
                self.seed=[]
                for x in self.pix:
                    self.seed+=x
                self.seed=list(map(str,list(map(int,self.seed))[self.seed.index(1):]))
                self.seed=int(''.join(self.seed),base=2)
                self.seed=base36encode(self.seed)
            elif pyxel.btnp(pyxel.KEY_D,hold=360,repeat=1200):
                self.debug=False
                self.go=True
            elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT,hold=10,repeat=1):
                if 0<=pyxel.mouse_y<self.height and 0<=pyxel.mouse_x<self.width:
                    self.pixn[pyxel.mouse_y][pyxel.mouse_x]=1 
                    self.pix=deepcopy(self.pixn)
            elif pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT,hold=10,repeat=1):
                if 0<=pyxel.mouse_y<self.height and 0<=pyxel.mouse_x<self.width:
                    self.pixn[pyxel.mouse_y][pyxel.mouse_x]=0 
                    self.pix=deepcopy(self.pixn)

            

    def draw(self):
        pyxel.cls(0)
        for y in range(self.height):
            for x in range(self.width):
                if self.pix[y][x]==1:
                    pyxel.pset(x,y,pyxel.COLOR_WHITE)
        if self.debug and self.go:
            print(self.seed)
        if self.debug:
            pyxel.pset(pyxel.mouse_x,pyxel.mouse_y,pyxel.COLOR_ORANGE)
    
def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    base36 = ''
    sign = ''
    if 0 <= number < len(alphabet):
        return sign + alphabet[number]
    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36
    return sign + base36

Game(50,50,30,[2,3],[3],15,True,0)
