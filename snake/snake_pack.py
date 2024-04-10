import pyxel

class Game:
    def __init__(self,width,height,scale,fps):
        self.width=width
        self.fps=fps
        self.height=height        
        self.lvl=0        
        self.levels=[
                [[0,-1,-1]],
                [[0,1,1],[0,2,2],[0,3,3],[0,4,4],[0,5,5],[0,6,6],[0,7,7]],
                [[1,1,1],[1,2,2],[1,3,3],[1,4,4],[1,5,5],[1,6,6],[1,7,7]],
                [[0,4,3],[0,5,3],[0,6,3],[0,7,3],[0,8,3],[0,4,13],[0,5,13],
                 [0,6,13],[0,7,13],[0,8,13],[0,25,3],[0,24,3],[0,23,3],[0,22,3],
                 [0,21,3],[0,21,13],[0,22,13],[0,23,13],[0,24,13],[0,25,13]],
                [[1,17,10],[1,12,10],[1,12,6],[1,17,6],[1,17,7],[1,17,8],
                 [1,17,9],[1,16,10],[1,13,10],[1,15,10],[1,14,10],[1,12,9],
                 [1,12,8],[1,12,7],[1,13,6],[1,15,6],[1,14,6],[1,16,6]],
                [[0,4,14],[0,3,14],[0,2,14],[0,2,13],[0,2,12],[0,2,3], 
                 [0,2,4],[0,3,2],[0,4,2],[0,26,2],[0,25,2],[0,27,3],[0,27,4],
                 [1,14,7],[1,14,8],[1,15,8],[1,13,8],[1,14,9],[1,2,2],[1,27,2],
                 [1,27,14],[0,27,12],[0,27, 13],[0,26,14],[0,25,14]],
            ]
        self.scores=[15,15,15,15,15,15]
        self.boost_allowed=[0,0,1,0,1,1]
        self.levels_count=len(self.levels)
        self.boost=False
        self.level=self.new_level()     
        self.endgame=False
        self.notgame=True
        self.start_menu=True  
        self.cd=240
        self.latest_eat=0      
        self.start_menu_select=['START',"CHEATS","EXIT"]
        self.pause_select=['CONTINUE','BACK TO MENU']
        self.pointer=0
        self.debug=False
        self.debr=0        
        self.debcomb=[pyxel.KEY_0,pyxel.KEY_1,pyxel.KEY_2,pyxel.KEY_3]
        self.debuppr=False
        self.editor=False
        self.yb=False
        self.edit_level=[]
        pyxel.init(width*16,(height+1)*16,title='snake',fps=fps,display_scale=3,quit_key=pyxel.KEY_Q)
        self.apple=[pyxel.rndi(0,width-1),pyxel.rndi(0,height-1)]
        pyxel.camera(0,-16)
        pyxel.load('snake1.pyxres')
        pyxel.run(self.update,self.draw)

    def restart(self):
        self.lose=False
        self.direction=0
        self.snake=[[0,self.height//2,-1,0],[0,self.height//2+1,-1,0],[0,self.height//2+2,-1,0]]
        self.score=3
        self.speed=15

    def global_restart(self):
        self.lvl=0
        self.level=self.new_level()
        self.endgame=False

    def new_level(self):
        self.restart()
        self.lvl+=1
        if 0<self.lvl<=self.levels_count:
            self.winscore=self.scores[self.lvl-1]
            self.boost=bool(self.boost_allowed[self.lvl-1])
            return self.levels[self.lvl-1][::]
        else:
            print(1)
            self.lose=True
            self.winscore=0
            self.endgame=True
            return []
    
    def change_apple_coord(self):
        cord=[[i[0],i[1]] for i in self.snake]+list(map(lambda x:x[1:],self.level))
        while self.apple in cord:
            self.apple=[pyxel.rndi(0,self.width-1),pyxel.rndi(0,self.height-1)]

    def anim_frame_num(self):
        if self.lose:
            return 0
        if pyxel.frame_count%self.speed<self.speed//5:
            c=0
        elif self.speed//5<=pyxel.frame_count%self.speed<self.speed//5*2:
            c=1
        elif (self.speed//5)*2<=pyxel.frame_count%self.speed<self.speed//5*3:
            c=2
        elif (self.speed//5)*3<=pyxel.frame_count%self.speed<self.speed//5*4:
            c=3
        elif (self.speed//5)*4<=pyxel.frame_count%self.speed<self.speed:
            c=4
        return c
    
    def widebody(self,n):
        if n<pyxel.ceil(self.score/5):
            return 0
        elif pyxel.ceil(self.score/5)<=n<pyxel.ceil(self.score/5)*2:
            return 1
        elif pyxel.ceil(self.score/5)*2<=n<pyxel.ceil(self.score/5)*3:
            return 2
        elif pyxel.ceil(self.score/5)*3<=n<pyxel.ceil(self.score/5)*4:
            return 3
        elif pyxel.ceil(self.score/5)*4<=n<=self.score:
            return 4 
        
    def move(self): 
        for i in range(1,self.score):
            self.snake[-i][0]=self.snake[-i-1][0]
            self.snake[-i][1]=self.snake[-i-1][1]
            self.snake[-i][2]=self.snake[-i-1][2]
            self.snake[-i][3]=self.snake[-i-1][3]        
        if self.direction!=self.snake[0][3]:
            self.snake[0][3]=self.direction
            self.snake[1][3]=self.direction
            if (self.snake[2][3]==0 and self.snake[0][3]==1) or (self.snake[2][3]==3 and self.snake[0][3]==2):
                self.snake[1][2]=0

            elif (self.snake[2][3]==1 and self.snake[0][3]==2) or (self.snake[2][3]==0 and self.snake[0][3]==3):
                self.snake[1][2]=1

            elif (self.snake[2][3]==2 and self.snake[0][3]==3) or (self.snake[2][3]==1 and self.snake[0][3]==0):
                self.snake[1][2]=2

            elif (self.snake[2][3]==3 and self.snake[0][3]==0) or (self.snake[2][3]==2 and self.snake[0][3]==1):
                self.snake[1][2]=3

        if self.direction==0:
                self.snake[0][1]=self.snake[0][1]-1
        elif self.direction==1:            
                self.snake[0][0]=self.snake[0][0]+1
        elif self.direction==2:            
                self.snake[0][1]=self.snake[0][1]+1
        elif self.direction==3:            
                self.snake[0][0]=self.snake[0][0]-1
        if 0>self.snake[0][1] or self.snake[0][1]>=self.height or  0>self.snake[0][0] or self.snake[0][0]>=self.width:
            return True
        for i in range(1,self.score):
            if (self.snake[i][0]==self.snake[0][0] and self.snake[i][1]==self.snake[0][1]):
                return True
        l1=list(filter(lambda x: x[0]==0,self.level))
        l2=[[i,self.level[i]] for i in range(len(self.level)) if self.level[i][0]==1]                
        for i in l1:
            if i[1]==self.snake[0][0] and i[2]==self.snake[0][1]:
                return True
        if self.boost:
            for i in range(len(l2)):
                if l2[i][1][1]==self.snake[0][0] and l2[i][1][2]==self.snake[0][1]:
                    if not pyxel.btn(pyxel.KEY_SPACE) or (pyxel.frame_count-self.latest_eat)<self.cd:
                        return True
                    else:
                        self.level.pop(l2[i][0])
                        self.latest_eat=pyxel.frame_count
                        self.snake.append(self.snake[-1].copy())            
                        self.score+=1
                        print(self.score,self.winscore)                    
                        if self.score==self.winscore:
                            self.level=self.new_level()
                            if self.lose:
                                return True
                        break
        return False

    def update(self):
        #начальный экран
        if self.start_menu:
            if pyxel.btnp(pyxel.KEY_ESCAPE,hold=120,repeat=240):
                pyxel.quit()
            if pyxel.btnp(pyxel.KEY_UP,hold=120,repeat=240):
                self.pointer=(self.pointer-1)%len(self.start_menu_select)
            if pyxel.btnp(pyxel.KEY_DOWN,hold=120,repeat=240):
                self.pointer=(self.pointer+1)%len(self.start_menu_select)
            if pyxel.btnp(pyxel.KEY_KP_ENTER,hold=120,repeat=240):
                if self.start_menu_select[self.pointer]=="EXIT":
                    pyxel.quit()
                elif self.start_menu_select[self.pointer]=="CHEATS":
                    self.start_menu=False
                    self.debuppr=True
                    return
                elif self.start_menu_select[self.pointer]=="START":
                    self.start_menu=False
                    self.notgame=False
                    return
                elif self.start_menu_select[self.pointer]=="LEVEL EDITOR":
                    self.start_menu=False
                    self.editor=True
                    return

        if self.debuppr:
            if pyxel.btnp(self.debcomb[self.debr]):
                self.debr+=1
                print(1)
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                self.start_menu=True
                self.debuppr=False
            if self.debr==len(self.debcomb):
                self.debuppr=False
                self.debug=True
                self.debr=0
                self.start_menu=True
                self.start_menu_select.insert(2,'LEVEL EDITOR')
                return  
        #пауза
        if not self.start_menu and self.notgame and not self.debuppr and not self.editor:
            if pyxel.btnp(pyxel.KEY_ESCAPE,hold=120,repeat=240):
                self.notgame=False
                self.pointer=0
                return
            if pyxel.btnp(pyxel.KEY_UP,hold=120,repeat=240):
                self.pointer=(self.pointer+1)%len(self.pause_select)
            if pyxel.btnp(pyxel.KEY_DOWN,hold=120,repeat=240):
                self.pointer=(self.pointer-1)%len(self.pause_select)
            if pyxel.btnp(pyxel.KEY_KP_ENTER):
                if self.pause_select[self.pointer]=="BACK TO MENU":                    
                    self.start_menu=True
                    self.global_restart()
                elif self.pause_select[self.pointer]=="CONTINUE":
                    self.notgame=False
                    self.pointer=0
                    return
        #Игра
        if not self.lose and not self.notgame and not self.debuppr and not self.endgame:
            if self.debug:
                if pyxel.btn(pyxel.KEY_C) and pyxel.btn(pyxel.KEY_D) and pyxel.btnr(pyxel.KEY_KP_PLUS):
                    self.level=self.new_level()
                if pyxel.btn(pyxel.KEY_C) and pyxel.btn(pyxel.KEY_D) and pyxel.btnr(pyxel.KEY_KP_MINUS):
                    self.lvl-=2
                    self.level=self.new_level()
                if pyxel.btnr(pyxel.KEY_F):
                    print(self.apple)
                if pyxel.btn(pyxel.KEY_R) and pyxel.btn(pyxel.KEY_SHIFT):            
                    self.global_restart()
                elif pyxel.btn(pyxel.KEY_R):
                    self.restart()
            if pyxel.btnp(pyxel.KEY_ESCAPE,hold=120,repeat=240):
                self.notgame=True
                self.pointer=0
                return
            if pyxel.btn(pyxel.KEY_UP):
                if self.direction!=2:
                    self.direction=0
            if pyxel.btn(pyxel.KEY_RIGHT):
                if self.direction!=3:
                    self.direction=1
            if pyxel.btn(pyxel.KEY_DOWN):
                if self.direction!=0:                    
                    self.direction=2
            if pyxel.btn(pyxel.KEY_LEFT):
                if self.direction!=1:                    
                    self.direction=3

            if pyxel.frame_count%self.speed==0:                
                self.lose=self.move()
                #print(self.snake)
                if self.snake[0][0]==self.apple[0] and self.snake[0][1]==self.apple[1]:
                    self.change_apple_coord()
                    self.snake.append(self.snake[-1].copy())
                    self.latest_eat=pyxel.frame_count
                    self.score+=1
                    print(self.score,self.winscore)                    
                    if self.score==self.winscore:
                        self.level=self.new_level()

        if self.lose and pyxel.btn(pyxel.KEY_R) and pyxel.btn(pyxel.KEY_SHIFT) and self.debug:            
            self.global_restart()
            
        if self.editor:
            if pyxel.btnp(pyxel.KEY_ESCAPE,hold=120,repeat=240):
                self.start_menu=True
                self.editor=False
                self.global_restart()
            if pyxel.btnp(pyxel.KEY_LSHIFT,hold=120,repeat=240):
                self.yb=not self.yb
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT,hold=120,repeat=240):                
                for i in self.edit_level:
                    if pyxel.mouse_x//16==i[1] and pyxel.mouse_y//16==i[2]:                        
                        break
                else:
                    self.edit_level.append([int(self.yb),pyxel.mouse_x//16,pyxel.mouse_y//16])
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT,hold=30,repeat=60):
                for i in self.edit_level:
                    if pyxel.mouse_x//16==i[1] and pyxel.mouse_y//16==i[2]:
                        self.edit_level.remove(i)                        
                        break
            if pyxel.btnp(pyxel.KEY_SPACE,hold=30,repeat=60):
                print(self.edit_level)

    def draw(self):
        pyxel.cls(0)        
        for x in range(self.width):
            
            for y in range(self.height):

                if (x+y)%2!=0:
                    pyxel.rect(x*16,y*16,16,16,pyxel.COLOR_GREEN)

                else:
                    pyxel.rect(x*16,y*16,16,16,11)

        if self.start_menu:
            for i in range(len(self.start_menu_select)):
                pyxel.text(160,80+7*i,self.start_menu_select[i],pyxel.COLOR_ORANGE)
            pyxel.tri(150,80+7*self.pointer,150,85+7*self.pointer,158,82+7*self.pointer,pyxel.COLOR_ORANGE)
        
        if not self.lose and not self.notgame and not self.debuppr and not self.editor:
            #отрисовка яблока               
            pyxel.blt(self.apple[0]*16,self.apple[1]*16,0,48,0,16,16,pyxel.COLOR_BLACK)        
            #начало отрисовки змейки
            a=self.snake[0][0]*16
            b=self.snake[0][1]*16
            c=self.anim_frame_num()    
            if self.snake[0][3]==0:           
                b-=c*3
                pyxel.blt(a,b,0,0,0,16,16,pyxel.COLOR_BLACK)
            elif self.snake[0][3]==1:
                a+=c*3
                pyxel.blt(a,b,0,0,32,16,16,pyxel.COLOR_BLACK) 
            elif self.snake[0][3]==2:
                b+=c*3
                pyxel.blt(a,b,0,0,0,-16,-16,pyxel.COLOR_BLACK)

            elif self.snake[0][3]==3:
                a-=c*3
                pyxel.blt(a,b,0,0,32,-16,16,pyxel.COLOR_BLACK)

            for x in range(1,self.score-1):

                d=self.widebody(x)
                if self.snake[x][2]==-1 and self.snake[x-1][2]==-1:   

                    if self.snake[x][3]==0:
                        pyxel.rect(self.snake[x][0]*16+2+d,self.snake[x][1]*16-c*3,12-d*2,16,pyxel.COLOR_DARK_BLUE)

                    elif self.snake[x][3]==2:
                        pyxel.rect(self.snake[x][0]*16+2+d,self.snake[x][1]*16+c*3,12-d*2,16,pyxel.COLOR_DARK_BLUE)

                    elif self.snake[x][3]==1:
                        pyxel.rect(self.snake[x][0]*16+c*3,self.snake[x][1]*16+2+d,16,12-d*2,pyxel.COLOR_DARK_BLUE)

                    else:
                        pyxel.rect(self.snake[x][0]*16-c*3,self.snake[x][1]*16+2+d,16,12-d*2,pyxel.COLOR_DARK_BLUE)     

                elif self.snake[x][2]==-1:

                    if self.snake[x][3]==0:
                        pyxel.rect(self.snake[x][0]*16+2+d,self.snake[x][1]*16,12-d*2,16-c*3,pyxel.COLOR_DARK_BLUE)

                    elif self.snake[x][3]==2:
                        pyxel.rect(self.snake[x][0]*16+2+d,self.snake[x][1]*16+c*3,12-d*2,16-c*3,pyxel.COLOR_DARK_BLUE)

                    elif self.snake[x][3]==1:
                        pyxel.rect(self.snake[x][0]*16+c*3,self.snake[x][1]*16+2+d,16-c*3,12-d*2,pyxel.COLOR_DARK_BLUE)

                    else:
                        pyxel.rect(self.snake[x][0]*16,self.snake[x][1]*16+2+d,16-c*3,12-d*2,pyxel.COLOR_DARK_BLUE)

                else:
                    """d=self.widebody(x+1)"""
                    d=self.widebody(x)
                    if self.snake[x][2]==0:
                        pyxel.blt(self.snake[x][0]*16,self.snake[x][1]*16,0,16,16*(d+1),16,16,pyxel.COLOR_BLACK)

                    elif self.snake[x][2]==1:
                        pyxel.blt(self.snake[x][0]*16,self.snake[x][1]*16,0,16,16*(d+1),-16,16,pyxel.COLOR_BLACK)

                    elif self.snake[x][2]==2:
                        pyxel.blt(self.snake[x][0]*16,self.snake[x][1]*16,0,16,16*(d+1),-16,-16,pyxel.COLOR_BLACK)

                    elif self.snake[x][2]==3:
                        pyxel.blt(self.snake[x][0]*16,self.snake[x][1]*16,0,16,16*(d+1),16,-16,pyxel.COLOR_BLACK)

                    if self.snake[x-1][2]==-1:

                        if self.snake[x-1][3]==0:
                            pyxel.rect(self.snake[x-1][0]*16+2+d,self.snake[x][1]*16-c*3,12-d*2,c*3,pyxel.COLOR_DARK_BLUE)

                        elif self.snake[x-1][3]==2:
                            pyxel.rect(self.snake[x-1][0]*16+2+d,self.snake[x-1][1]*16,12-d*2,c*3,pyxel.COLOR_DARK_BLUE)

                        elif self.snake[x-1][3]==1:
                            pyxel.rect(self.snake[x-1][0]*16,self.snake[x-1][1]*16+2+d,c*3,12-d*2,pyxel.COLOR_DARK_BLUE)

                        else:
                            pyxel.rect(self.snake[x][0]*16-c*3,self.snake[x][1]*16+2+d,c*3,12-d*2,pyxel.COLOR_DARK_BLUE)
            
            if self.snake[-1][3]==0:
                pyxel.blt(self.snake[-1][0]*16,self.snake[-1][1]*16-c*3,0,32,0,16,16,pyxel.COLOR_BLACK)

            elif self.snake[-1][3]==1:
                pyxel.blt(self.snake[-1][0]*16+c*3,self.snake[-1][1]*16,0,32,32,16,16,pyxel.COLOR_BLACK) 

            elif self.snake[-1][3]==2:
                pyxel.blt(self.snake[-1][0]*16,self.snake[-1][1]*16+c*3,0,32,0,-16,-16,pyxel.COLOR_BLACK)

            elif self.snake[-1][3]==3:
                pyxel.blt(self.snake[-1][0]*16-c*3,self.snake[-1][1]*16,0,32,32,-16,-16,pyxel.COLOR_BLACK)
            #конец отрисовки змейки
                
            #Отрисовка стен
            for x in self.level:
                pyxel.blt(x[1]*16,x[2]*16,0,48,16+16*x[0],16,16)

        if self.lose and not self.endgame:
            pyxel.text(160,80,'YOU LOSE',pyxel.COLOR_ORANGE)

        elif self.endgame:
            pyxel.text(160,80,'YOU BEAT THIS GAME',pyxel.COLOR_ORANGE)

        if self.debuppr:
            pyxel.text(160,80,'ENTER CHEAT COMBINATION',pyxel.COLOR_ORANGE)

        if not self.start_menu and self.notgame and not self.debuppr and not self.editor:
            for i in range(len(self.pause_select)):
                pyxel.text(160,80+7*i,self.pause_select[i],pyxel.COLOR_ORANGE)
            pyxel.tri(150,80+7*self.pointer,150,85+7*self.pointer,158,82+7*self.pointer,pyxel.COLOR_ORANGE)     

        if not self.start_menu and not self.debuppr and not self.editor and not self.endgame:
            pyxel.rect(0,-16,self.width*16,16,0)
            pyxel.text(0,-16,f'LEVEL: {self.lvl}',pyxel.COLOR_ORANGE)
            pyxel.text(0,-10,f'POINT: {self.winscore-3}',pyxel.COLOR_ORANGE)
            pyxel.text(max((7+len(str(self.lvl)))*5,(7+len(str(self.winscore)))*5),-16,f'SCORE: {self.score-3}',pyxel.COLOR_ORANGE)

        if self.editor:
            pyxel.line(pyxel.mouse_x-8,pyxel.mouse_y,pyxel.mouse_x+8,pyxel.mouse_y,pyxel.COLOR_WHITE)
            pyxel.line(pyxel.mouse_x,pyxel.mouse_y-8,pyxel.mouse_x,pyxel.mouse_y+8,pyxel.COLOR_WHITE)
            pyxel.blt(self.width*16-32,-16,0,48,16+16*int(self.yb),16,16,pyxel.COLOR_BLACK)
            pyxel.text(max((7+len(str(self.lvl)))*5,(7+len(str(self.winscore)))*5)+14*5,-10,'EDITOR MODE',pyxel.COLOR_ORANGE)
            for x in self.edit_level:
                pyxel.blt(x[1]*16,x[2]*16,0,48,16+16*x[0],16,16)
        
        if self.debug:
            pyxel.text(max((7+len(str(self.lvl)))*5,(7+len(str(self.winscore)))*5),-10,'CHEATS ENABLED',pyxel.COLOR_ORANGE)

        if self.boost and not self.endgame and not self.lose:
            pyxel.rectb(max((7+len(str(self.lvl)))*5,(7+len(str(self.winscore)))*5)+14*5,-15,self.cd//5,14,pyxel.COLOR_ORANGE)            
            pyxel.rect(max((7+len(str(self.lvl)))*5,(7+len(str(self.winscore)))*5)+14*5,-15,(self.cd if self.cd<pyxel.frame_count-self.latest_eat else pyxel.frame_count-self.latest_eat)//5,14,pyxel.COLOR_ORANGE)
            pyxel.text(max((7+len(str(self.lvl)))*5,(7+len(str(self.winscore)))*5)+14*5+51,-16,"SPACE TO EAT\nYELLOW BLOCK",pyxel.COLOR_ORANGE)
            
Game(30,17,10,120)