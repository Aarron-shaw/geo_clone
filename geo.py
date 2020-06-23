

import pygame
import math
import random
import time
import os
pygame.init()
#Config settings



#Constants 

FS = True
SIZE_X = 600
SIZE_Y = 500
FPS = 60
clock = pygame.time.Clock()

grid = 15

#Colors 

WHITE = pygame.Color(253, 254, 254)
RED = pygame.Color(204, 15, 57,255) 
BLACK = pygame.Color(2, 2, 2)
LBLACK = pygame.Color(62, 60, 65)
BLUE = pygame.Color(15, 251, 249,255)
GREY = pygame.Color(194, 191, 204,255)
PINK = pygame.Color(195, 107, 147)
YELLOW = pygame.Color(205, 199, 100)

#Fonts config
fullname = os.path.dirname(os.path.abspath(__file__))
fullname = os.path.join(fullname,"fonts\SFAlienEncounters.ttf")
font_size = 40
font = pygame.font.Font(fullname,font_size)

if FS:
    pygame.display.init()
    info = pygame.display.Info()
    SIZE_X = info.current_w
    SIZE_Y = info.current_h
    screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
else:
    #This producers a smaller window, which is for trying new code. 

    
    screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
    
#Grid Config
edgeX = SIZE_X // grid
edgeY = SIZE_Y // grid
edge = [edgeX*1,edgeY*1,edgeX*(grid-1),edgeY*(grid-1)]


    #Our player
class dot(object):
    def __init__(self):
        self.r = 10
        self.x = SIZE_X//2
        self.y = SIZE_Y//2
        self.a = 0
        self.speed = 1
        self.bullet = 1 #Bullet type 1,2 or 3.
        
    def move(self,x,y):
        global menu 
        if self.x+x > edge[2] or self.x+x < edge[0]:
            return True
        if self.y+y > edge[3] or self.y+y < edge[1]:
            return True 
        self.x += x
        self.y += y
        
        
    
        
    def draw(self):
        points = []
        size = self.r
        target_x,target_y = pygame.mouse.get_pos()
        self.a = math.atan2(target_y - self.y, target_x - self.x)* 180 / math.pi
        self.a -= 90

        start = pygame.Vector2(self.x,self.y)
        left = pygame.Vector2(-1,-2)
        top = pygame.Vector2(0,-1)
        right = pygame.Vector2(1,-2)
        points.append(start + left.rotate(self.a) * size)
        points.append(start + top.rotate(self.a) * size)
        points.append(start + right.rotate(self.a) * size)
        points.append(start)
        pygame.draw.lines(screen,WHITE,points[0],points[0:])


class dot_ai1(object):
    def __init__(self):
        x,y = not_player_area()
        self.x = x
        self.y = y
        self.a = 0
        self.speed = 1
        self.r = 10
        self.score = 25
        self.type = 1
        
        
    def move(self):
        global menu
        self.a = math.atan2(player.y - self.y, player.x - self.x)
        self.x = self.x + math.cos(self.a) * self.speed
        self.y = self.y + math.sin(self.a) * self.speed
        if self.x > edge[2] or self.x < edge[0]:
            self.x = self.x - math.cos(self.a+1) * self.speed
        if self.y > edge[3] or self.y < edge[1]:
            self.y = self.y - math.sin(self.a+1) * self.speed
        if collide(self,player):
            print("GG")
            pygame.time.wait(1000)
            menu = -1
    def draw(self):
        points = []
        points2 = []
        points3 = []
        x = self.x
        y = self.y 
        size = 10
        target_x,target_y = player.x,player.y
        a = math.atan2(target_y - y, target_x - x)* 180 / math.pi
        a -= self.a 
        self.a += 1
        if self.a > 360:
            self.a = 0
        point = []
        start = pygame.Vector2(x,y)
        point.append(pygame.Vector2(0,1))
        point.append(pygame.Vector2(1,1))
        point.append(pygame.Vector2(1,0))
        
        
        for p in point:
            points.append(start + p.rotate(a) * size)
            points2.append(start + p.rotate(a) * (size+1))
            points3.append(start + p.rotate(a) * (size-1))
        points.append(start)
        points2.append(start)
        points3.append(start)
        myedge = pygame.draw.lines(screen,WHITE,points[0],points[0:])
        pygame.draw.lines(screen,RED,points2[0],points2[0:])
        pygame.draw.lines(screen,RED,points3[0],points3[0:])
        pygame.draw.polygon(screen,(255,255,255),points)
        self.r = myedge[2]
            

class dot_ai2(object):
    def __init__(self):
        x,y = not_player_area()
        self.x = x
        self.y = y
        self.a = 0
        self.a_detour = random.randint(-1,0)
        self.speed = 3
        self.r = 10
        self.score = 50
        self.type = 2
        
    def get_angle(self):
        x,y = pygame.mouse.get_pos()
        mouse_x_d = self.x - x
        mouse_y_d = self.y - y
    
        mdist = math.hypot(mouse_x_d, mouse_y_d)
        
        player_x_d = self.x - player.x
        player_y_d = self.y - player.y
        
        pdist = math.hypot(player_x_d, player_y_d)
        if mdist < pdist:
            self.a = math.atan2(player.y - y -  self.y , player.x - x - self.x )
        else:
            self.a = math.atan2(player.y - self.y , player.x - self.x )
        
    def move(self):
        global menu
        
        self.get_angle()
        self.a = self.a + self.a_detour
        self.x = self.x + math.cos(self.a) * self.speed
        self.y = self.y + math.sin(self.a) * self.speed
        if self.x > edge[2] or self.x < edge[0]:
            self.x = self.x - math.cos(self.a) * self.speed
        if self.y > edge[3] or self.y < edge[1]:
            self.y = self.y - math.sin(self.a) * self.speed
        if collide(self,player):
            print("GG")
            pygame.time.wait(1000)
            menu = -1
    def draw(self):
        
        points = []
        x = self.x
        y = self.y 
        size = 5
        target_x,target_y = player.x,player.y
        a = math.atan2(target_y - y, target_x - x)* 180 / math.pi
        a -= self.a 
        self.a += 1
        if self.a > 360:
            self.a = 0
        point = []
        start = pygame.Vector2(x,y)
        point.append(pygame.Vector2(-2,1))
        point.append(pygame.Vector2(-2,3))
        point.append(pygame.Vector2(0,3))
        point.append(pygame.Vector2(0,2))
        point.append(pygame.Vector2(1,2))
        for p in point:
            points.append(start + p.rotate(a) * size)
        
        points.append(start)
        
        myedge = pygame.draw.lines(screen,BLUE,points[0],points[0:])    
        self.r = myedge[2]

 
class dot_ai3(object):
    def __init__(self):
        x,y = not_player_area()
        self.x = x
        self.y = y
        self.a = 0
        self.a_detour = random.randint(-1,0)
        self.speed = 1
        self.r = 10
        self.score = 10
        self.type = 3
        
    def get_angle(self):
        x,y = pygame.mouse.get_pos()
        mouse_x_d = self.x - x
        mouse_y_d = self.y - y
    
        mdist = math.hypot(mouse_x_d, mouse_y_d)
        
        player_x_d = self.x - player.x
        player_y_d = self.y - player.y
        
        pdist = math.hypot(player_x_d, player_y_d)
        if mdist < pdist:
            self.a = math.atan2(player.y - y -  self.y , player.x - x - self.x )
        else:
            self.a = math.atan2(player.y - self.y , player.x - self.x )
        
    def move(self):
        global menu
        
        self.a = math.atan2(player.y - self.y, player.x - self.x)
        self.x = self.x + math.cos(self.a) * self.speed
        self.y = self.y + math.sin(self.a) * self.speed
        if self.x > edge[2] or self.x < edge[0]:
            self.x = self.x - math.cos(self.a) * self.speed
        if self.y > edge[3] or self.y < edge[1]:
            self.y = self.y - math.sin(self.a) * self.speed
        if collide(self,player):
            print("GG")
            pygame.time.wait(1000)
            menu = -1
    def draw(self):
        
        points = []
        points2 = []
        points3 = []
        x = self.x
        y = self.y 
        size = 10
        target_x,target_y = player.x,player.y
        a = math.atan2(target_y - y, target_x - x)* 180 / math.pi
        a -= self.a 
        self.a += 1
        if self.a > 360:
            self.a = 0
        point = []
        start = pygame.Vector2(x,y)
        point.append(pygame.Vector2(0.5,1))
        point.append(pygame.Vector2(0,2))
        point.append(pygame.Vector2(0.5,3))
        point.append(pygame.Vector2(1,3))
        
        point.append(pygame.Vector2(0.5,2))
        point.append(pygame.Vector2(1,1))
        for p in point:
            points.append(start + p.rotate(a) * size)
            points2.append(start + p.rotate(a) * (size+1))
            points3.append(start + p.rotate(a) * (size-1))
        points.append(start)
        points2.append(start)
        points3.append(start)
        
        points.append(start)
        
        myedge = pygame.draw.lines(screen,BLUE,points[0],points[0:])
        pygame.draw.lines(screen,WHITE,points2[0],points2[0:])
        pygame.draw.lines(screen,WHITE,points3[0],points3[0:])
        pygame.draw.polygon(screen,(255,255,255),points)
        self.r = myedge[2]        
        
class bullet(object):
    def __init__(self,x,y,a,t):
        if t == 1:
            self.r = 4
            self.speed = 1
        if t == 2:
            self.r = 2
            self.speed = 6
        if t == 0:
            self.r = 3
            self.speed = 4
        
        pos = pygame.mouse.get_pos()
        radians = math.atan2(pos[1] - y, pos[0] - x)
        self.a = radians + a
        self.x = x + math.cos(self.a) * self.r * 5
        self.y = y + math.sin(self.a) * self.r * 5
        self.type = t
        self.speed = 4
        
        
    def move(self):
        if self.x > edge[2] or self.x < edge[0]:
            return True
        if self.y > edge[3] or self.y < edge[1]:
            return True 
        self.x = self.x + math.cos(self.a) * self.speed
        self.y = self.y + math.sin(self.a) * self.speed
    def draw(self):
    
        pygame.draw.circle(screen,WHITE,(int(self.x),int(self.y)),self.r)

class pop(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.timer = 0
        self.speed = 1
        self.a = random.uniform(0,math.pi*2)
        #print(self.a)
    def splash(self):
    
        
        
        self.x += math.sin(self.a) * self.speed
        self.y -= math.cos(self.a) * self.speed
        
        self.timer += random.randint(1,3)
        if self.timer > 100:
            return True
    def draw(self):
        screen.set_at((int(self.x),int(self.y)),WHITE)
        

class menu_options(object):
    def __init__(self,n,string,string_size):
        self.n = n
        self.x = 200 
        self.y = SIZE_Y//grid* (self.n+1) +(font_size) 
         
        self.s = string
        self.color = GREY
        self.surface = font.render(self.s, False, self.color)
        self.tmp_surface = font.render(string_size, False, self.color)
        self.center = self.tmp_surface.get_rect()
        self.center.center = (self.x,self.y)
        
        
    def draw(self):
        if self.center.collidepoint(pygame.mouse.get_pos()):
            self.color = LBLACK
            
        else:
            self.color = GREY
        self.surface = font.render(self.s, False, self.color)
        screen.blit(self.surface,self.center)
        
    def click(self):
        pass

class player_score(object):
    def __init__(self):
        self.score = 0
        self.level = 1
        self.next_level = 1000
        
    def update_score(self,score):
        self.score += score
        print(self.score)
        while self.score > self.next_level:
            self.next_level += self.next_level +(self.next_level * 0.90)
            print("Next Level xp: ",self.next_level)
            print(self.level)
            self.level += 1
                
class barchat(object):
    def __init__(self):
        self.w = 0
        self.h = 0
        self.scale = 1
        self.reset = 0
    def update(self):
        self.scale = score.next_level
        my_scale = (SIZE_X - 200) / self.scale  
        target = score.score * my_scale
        if target > self.w:
            self.w +=1
            print("Need to upade")
        if score.level > self.reset: 
            self.w = 0
            self.reset = score.level
    
    def draw(self):
        self.scale = score.next_level
        my_scale = (SIZE_X - 200) / self.scale  
        
        height = SIZE_Y//grid - 10
        pygame.draw.rect(screen,GREY,(0,0,(SIZE_X - 200),height))
        pygame.draw.rect(screen,BLUE,(0,0,self.w,height))
        print(my_scale)
    
def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.r /2 + p2.r /2: 
        return True
        
def not_player_area():
    #This function defines an area in which 
    #our AI can not spawn. 
    allowed_values = list(range(edge[0], edge[2]))
    for x in range(player.x-200,player.x+200):
        try:
            allowed_values.remove(x)
        except:
            pass

    # can be anything in {-5, ..., 5} \ {0}:
    random_valuex = random.choice(allowed_values) 
    allowed_values = list(range(edge[1], edge[3]))
    for x in range(player.y-200,player.y+200):
        try:
            allowed_values.remove(x)
        except:
            pass

    # can be anything in {-5, ..., 5} \ {0}:
    random_valuey = random.choice(allowed_values)
    return random_valuex, random_valuey

def draw_grid_game(grid):
    
    i = SIZE_X // grid
    l = SIZE_Y // grid
    for b in range(1,grid):
            
            #Lines across
            pygame.draw.line(screen,GREY,(i,l*b),(i*(grid-1),l*b))
            pygame.draw.line(screen,BLUE,(i,l*b-1),(i*(grid-1),l*b-1))
            pygame.draw.line(screen,RED,(i,l*b+1),(i*(grid-1),l*b+1))
            #Lines down
            pygame.draw.line(screen,GREY,(i*b,l),(i*b,l*(grid-1)))
            pygame.draw.line(screen,BLUE,(i*b-1,l),(i*b-1,l*(grid-1)))
            pygame.draw.line(screen,RED,(i*b+1,l),(i*b+1,l*(grid-1)))


    #Take a mouse position and draw a cross hair using that. 
    return #currently not in use
    x,y = pygame.mouse.get_pos()
    yline1,yline2 = (x,0),(x, SIZE_Y)
    xline1,xline2 = (0,y),(SIZE_X,y)
    pygame.draw.line(screen,RED,xline1,xline2)
    pygame.draw.line(screen,RED,yline1,yline2)
        
def check_bullets():
    for p,bullet in enumerate(bullets):
        check = bullets[p].move()
        bullets[p].draw()
        for q,splish in enumerate(dots):
            if collide(bullet,splish):
                score.update_score(300)
                if dots[q].type == 3:
                    pass # spawn new ones
                del dots[q]
                check = True
        if check:
            for i in range(0,random.randint(1,10)):
                splash.append(pop(bullets[p].x,bullets[p].y))
            del bullets[p]
            
def check_splash():
    for p,splish in enumerate(splash):
        check = splash[p].splash()
        #print(splash[p].x,splash[p].y)
        splash[p].draw()
        if check:
            del splash[p]

def check_dots():
    for p,splish in enumerate(dots):
            dots[p].move()
            dots[p].draw()

def draw_game_window():
    screen.fill(BLACK)

    draw_grid_game(grid)
    xp_bar.update()
    xp_bar.draw()
    player.draw()
    
    check_bullets()
            
    check_splash()
    
    check_dots()

def draw_game_menu():

    screen.fill(BLACK)
    #draw_grid_game(grid)
    for n,temp_menu in enumerate(menu_text):
        menu_text[n].draw()

def draw_xp_bar():
    scale = score.next_level
    my_scale = (SIZE_X - 200) / scale  
    width = xp_bar * my_scale
    height = SIZE_Y//grid - 10
    pygame.draw.rect(screen,BLUE,(0,0,width,height))

    
def spawn_ai(n):
    current_ai = len(dots)
    target_dots = int(n*2)
    if target_dots < 3:
        target_dots = 3
    while current_ai < target_dots:
        dice = random.randint(1,3)
        if dice == 1:
            dots.append(dot_ai1())
        if dice == 2:
            dots.append(dot_ai2())
        if dice == 3:
            dots.append(dot_ai3())    
        current_ai = len(dots) 

def spawn_bullets():
    if score.level%2 == 0:
        for i in range(-25,26,25):
            angle = i * math.pi / 180
            bullets.append(bullet(player.x,player.y,angle,1))
    elif score.level%3 == 0:
        for i in range(-10,11,5):
            angle = i * math.pi / 180
            bullets.append(bullet(player.x,player.y,angle,2))
    else:
        bullets.append(bullet(player.x,player.y,0,0))
    
    
    
def start_game():
    #Reset all our game variables. 
    global player,bullets,splash,dots,btimer,timer,counter
    global ai_timer,hardness, score, xp_bar
    xp_bar = barchat()
    score = player_score()
    player = dot()
    bullets = []
    splash = []
    dots = []
    btimer = 0
    timer = 0
    counter = 0
    ai_timer = 10
    
    
start_game()
menu = -1
menu_text = []
str_list = ["START ","OPTIONS ","HIGH SCORES","EXIT"]

for n in range(0,len(str_list)):
    #def __init__(self,n,string):
    #print(n)
    menu_text.append(menu_options(n,str_list[n],str_list[0]))


while True:
    
    btimer += 1
    timer += 1
    
    if menu == -1:
        draw_game_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    click = pygame.mouse.get_pos()
                    for n,temp_menu in enumerate(menu_text):
                        if menu_text[n].center.collidepoint(click):
                            if menu_text[n].n == 0:
                                start_game()
                            menu = menu_text[n].n
                            
        keys = pygame.key.get_pressed()
       
    
    if menu == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
             
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_w]:
            player.move(0,-2)
        if keys[pygame.K_s]:
            player.move(0,2)
        if keys[pygame.K_a]:
            player.move(-2,0)
        if keys[pygame.K_d]:
            player.move(2,0)
        if keys[pygame.K_ESCAPE]:
            menu = -1       
        draw_game_window()
        #spawn AI
        if timer > FPS*ai_timer:
            spawn_ai(score.level)
            
            if ai_timer > 5:
                ai_timer -= 1
            timer = 0
        
        #spawn bullets area 
        if btimer > FPS/6:
            btimer = 0
            spawn_bullets()
            
    if menu == 1: #These menus are not currently functioning.
        menu = -1
    if menu == 2:
        menu = -1
    if menu == 3:
        quit()
    pygame.display.update()
    clock.tick(FPS)
    