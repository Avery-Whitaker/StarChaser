''' 
Looking for a new name for this project. If you have any ideas plese put in evaluation!

Pitch Sheet: http://www.averyw.me/RunNGunPoster.pdf

Description:
2 Player game. (split-screen mulitplayer) Goal is to survive 
longer then other player. Death currently can only occur by 
falling off platforms. Platforms can be destroyed (currently 
just randomly disapear).

Controls: 
Left palyer: WASD to move, space to jump
         Right Player: Arrow Keys to move, shift to jump
Currently Camera fixes static angle. have it working that
camera can face other player, but dont have offset working.
Ultimatly plan is camera alway facec other player except
when players are close.

Author Contact:

please direct any questions to
averywhitaker@rice.edu

Liscensed under BSD:

Copyright (c) 2015 Avery Whitaker.
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by Avery Whitaker. The name of Avery Whitaker may not be used to 
endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
'''

import simplegui
import math
import random
import time
import user40_vGEjZ00kyC_7 as DrawEngine
        
class WorldPlayer(DrawEngine.WorldSphere, DrawEngine.WorldAngle):
    def __init__(self,x,y,r,b,g):
        DrawEngine.WorldSphere.__init__(self, x, y, 600, 30, r,b,g,1)
        DrawEngine.WorldAngle.__init__(self, 0)
        self.z_vel = 20
        self.radius = 30
        self.speed = 800
        
    def update(self, time_delta):
        global grid
        ground_z = grid.grid_height(self.x,self.y)+self.radius
        
        moving_ground_z = grid.get_item(self.x,self.y).prev_height+self.radius
        
        if self.z_vel >= 0: #if going up
             self.z += self.z_vel*time_delta
        elif self.z == ground_z or self.z == moving_ground_z: #if sitting on ground
            self.z = ground_z
            grid.get_item(self.x,self.y).stand_damage(time_delta)
            self.z_vel = 0
        elif self.z >= ground_z and self.z + self.z_vel*time_delta < ground_z: #if falling into ground
            self.z = ground_z
            if grid.get_item(self.x,self.y).is_bouncy():
                self.z_vel = 1200
            else:
                self.z_vel = 0
        else:#else falling into space
            self.z += self.z_vel*time_delta
        
        self.z_vel -= 1200*time_delta
        
    def jump(self):
        ground_z = grid.grid_height(self.x,self.y)+self.radius
        moving_ground_z = grid.get_item(self.x,self.y).prev_height+self.radius
        if self.z == ground_z or self.z == moving_ground_z:
            grid.get_item(self.x,self.y).jump_damage()
                
            if grid.get_item(self.x,self.y).is_bouncy():
                self.z_vel = 1200
            else:  
                self.z_vel = 800
       
    def forward(self, dt):
        self.y += self.speed * dt * math.cos(self.angle_xy)
        self.x += self.speed * dt * math.sin(self.angle_xy)
        
    def left(self, dt):
        self.x -= self.speed * dt * math.cos(self.angle_xy)
        self.y += self.speed * dt * math.sin(self.angle_xy)
        
    def right(self, dt):
        self.x += self.speed * dt * math.cos(self.angle_xy)
        self.y -= self.speed * dt * math.sin(self.angle_xy)
       
    def back(self, dt):
        self.y -= self.speed * dt * math.cos(self.angle_xy)
        self.x -= self.speed * dt * math.sin(self.angle_xy)
        
    def shadow(self):
        points = []
        n = 10
        angle = 0
        shawdow_height = grid.grid_height(self.x,self.y)
        r = 250
        
        if shawdow_height >= self.z-self.radius*2:
            return None
        
        for i in range(0,n):
            points.append(DrawEngine.WorldPoint(self.x+50*math.cos(angle),self.y+50*math.sin(angle),grid.grid_height(self.x,self.y)))
            angle+=(math.pi*2)/n
            
        return DrawEngine.WorldPoly(points, 20, 20, 20)

class GridSquare:
    def __init__(self, height, world_poly = None, level = 0):
        self.world_poly = world_poly
        
        self.level = level
        
        self.height = height
        self.prev_height = -10000
        
        #types of squares:
        #0 - normal
        #1 - bouncy
        #2 - up/down
        #3 - disapear
        
        type = 0
        if random.random() > 0.85: #if special
            type = random.randrange(1,4)
        
        self.bouncy = False
        if type == 1:
            self.bouncy = True
         
        self.direction = 0
        self.min_height = self.height-100
        self.max_height = self.height+100
        if type == 2:
            self.direction = (random.randrange(0,2)*2)-1 #-1 or 1
        
        self.health = None
        if type == 3:
            self.health = 100
        
        if self.world_poly is not None:
            if type == 0:
                self.world_poly.color_r = int(255*(0.75+self.level/4.0))
                self.world_poly.color_g = int(255*(0.75+self.level/4.0))
                self.world_poly.color_b = int(255*(0.75+self.level/4.0))
            elif type == 1:
                self.world_poly.color_r = int(0*(0.75+self.level/4.0))
                self.world_poly.color_g = int(0*(0.75+self.level/4.0))
                self.world_poly.color_b = int(200*(0.75+self.level/4.0))
            elif type == 2:
                self.world_poly.color_r = int(255*(0.75+self.level/4.0))
                self.world_poly.color_g = int(127*(0.75+self.level/4.0))
                self.world_poly.color_b = int(80*(0.75+self.level/4.0))
            elif type == 3:
                self.health_update()
    
    def update(self, time_delta):    
        if self.direction != 0:
            self.prev_height = self.height
            
            if self.height < self.min_height:
                self.direction = 1
                
            if self.height > self.max_height:
                self.direction = -1

            self.height += 100*time_delta*self.direction

            if self.world_poly is not None:
                for i in range(0,len(self.world_poly)):
                    self.world_poly[i].z = self.height
        
    def health_update(self):
        if self.world_poly is not None:
            self.world_poly.color_r = int((165*self.health*0.01)*(0.75+self.level/4.0))
            self.world_poly.color_g = int((42*self.health*0.01)*(0.75+self.level/4.0))
            self.world_poly.color_b = int((42*self.health*0.01)*(0.75+self.level/4.0))
        
        if self.health <= 0:
            self.direction = -5
            self.min_height = -100000
        
    def jump_damage(self):
        if self.health is not None:
            self.health -= 100
            self.health_update()
        
    def stand_damage(self, delta_time):
        if self.health is not None:
            self.health -= delta_time*150
            self.health_update()
        
    def transform(self,camera):
        if self.world_poly is None:
            return None
        return self.world_poly.transform(camera)
    
    def is_bouncy(self):
        return self.bouncy
    
class Grid:
    def __init__(self):
        self.objects = {}
        self.tile_size = 400
        self.square_size = 9
        self.set_center(0,0)
        
    def x_range(self):
        return range(self.center_tile_x-int(self.square_size/2), self.center_tile_x+int(self.square_size/2))
        
    def y_range(self):
        return range(self.center_tile_y-int(self.square_size/2), self.center_tile_y+int(self.square_size/2))
        
    def x_y_range(self):
        return [(x,y) for x in self.x_range() for y in self.y_range()]
        
    def set_center(self,x,y):
        self.center_tile_x = int(x/self.tile_size)
        self.center_tile_y = int(y/self.tile_size)
                
        for x,y in self.x_y_range():
            if not self.objects.has_key(x):
                self.objects[x] = {}
            if not self.objects[x].has_key(y):
                spawn = (x > -5 and y > -5 and x < 5 and y < 5)
                if random.random() > 0.2 + math.sqrt(x**2+y**2)/150 or spawn:
                    if spawn:
                        level = 0
                    else:
                        level = random.randrange(0,2)
                    height = self.tile_size/4*level
                    self.objects[x][y]=GridSquare(height, DrawEngine.WorldPoly([DrawEngine.WorldPoint(self.tile_size/2+x*self.tile_size, self.tile_size/2+y*self.tile_size, height),
                                                 DrawEngine.WorldPoint(-self.tile_size/2+x*self.tile_size,                self.tile_size/2+y*self.tile_size, height),
                                                 DrawEngine.WorldPoint(-self.tile_size/2+x*self.tile_size,                -self.tile_size/2+y*self.tile_size, height), 
                                                 DrawEngine.WorldPoint(self.tile_size/2+x*self.tile_size,  -self.tile_size/2+y*self.tile_size, height)]), level)
                else:
                    self.objects[x][y]=GridSquare(-100000)
                
    def update(self,time_delta):
        for x,y in self.x_y_range():
            self.objects[x][y].update(time_delta)
                
    def grid_height(self,x,y):
        x = round(x/self.tile_size)
        y = round(y/self.tile_size)
        if not (x,y) in self.x_y_range():
            return -10000000.00
        return self.objects[x][y].height
            
    def get_item(self,x,y):
        return self.objects[round(x/self.tile_size)][round(y/self.tile_size)]
       
    def to_list(self):
        list = []
        for x,y in self.x_y_range():
            list.append(self.objects[x][y])
        return list

def render_frame(canvas):
    global game_over
    
    canvas.draw_polygon([[0, 0], [0, HEIGHT], [WIDTH, HEIGHT], [WIDTH, 0]], 1, 'White', 'Green')
    
    canvas.draw_text(text_left, (75, 200), 48, 'Black')
    canvas.draw_text(text_right, (WIDTH/2+100, 200), 48, 'Black')
    
    canvas.draw_text('Runner - WASD, Space', (75, 100), 24, 'Black')
    canvas.draw_text('Seeker - Arrow Keys, Shift', (WIDTH/2+100, 100), 24, 'Black')
    
    render_objects = grid.to_list()
    render_objects.append(player_a)
    render_objects.append(player_b)
    render_objects.append(player_a.shadow())
    render_objects.append(player_b.shadow())
    
    if not game_over:
        right_camera.draw(canvas,render_objects)
        left_camera.draw(canvas,render_objects)
    canvas.draw_text('Avery Whitaker | This game still needs a name', (30, 50), 48, 'Red')
    

    
def update_world(time_delta):
    global game_over,text_left,text_right
    
    player_a.update(time_delta)
    player_b.update(time_delta)
    
    grid.set_center(player_a[0], player_a[1])
    grid.update(time_delta)
    
    dx = player_b.x-player_a.x
    dy = player_b.y-player_a.y
    l = 1000
    
    L = math.sqrt( dx**2 + dy**2 )
    
    if not game_over and player_b.z < -2000:
        text_left = "You Win"
        game_over = True
        
    if not game_over and player_a.z < -2000:
        text_right = "You Win"
        game_over = True
    
    if not game_over and L < 100:
        text_right = "You Win"
        game_over = True
    
    angle_a = DrawEngine.WorldAngle.angleBetweenWorldPoints(player_a, player_b)+math.pi
    angle_b = DrawEngine.WorldAngle.angleBetweenWorldPoints(player_b, player_a)
    
    player_a.set_angle_xy(math.pi/2-angle_a)
    player_b.set_angle_xy(math.pi/2-angle_b)

    left_camera.set_angle_xy(player_a.angle_xy)
    right_camera.set_angle_xy(player_b.angle_xy)

    left_camera.set_pos(player_a.x - math.cos(angle_a)*l, player_a.y - math.sin(angle_a)*l - l/2, 500+player_a.z)
    right_camera.set_pos(player_b.x - math.cos(angle_b)*l, player_b.y - math.sin(angle_b)*l - l/2, 500+player_b.z)

keys_down = {}
for i in range(1,300):
    keys_down[i] = False
    
def keydown(k):
    global keys_down
    keys_down[k] = True
    
    if k == simplegui.KEY_MAP["space"]:
        player_a.jump()
    if keys_down[16]:
        player_b.jump()

def keyup(k):
    global keys_down
    keys_down[k] = False
            
def key_action(dt):    
    
    if keys_down[simplegui.KEY_MAP["up"]]:
        player_b.forward(dt)
    if keys_down[simplegui.KEY_MAP["down"]]:
        player_b.back(dt)
    if keys_down[simplegui.KEY_MAP["left"]]:
        player_b.left(dt)
    if keys_down[simplegui.KEY_MAP["right"]]:
        player_b.right(dt)
        
    if keys_down[16]:
        player_b.jump()
    
    if keys_down[simplegui.KEY_MAP["s"]]:
        player_a.back(dt)
    if keys_down[simplegui.KEY_MAP["a"]]:
        player_a.left(dt)
    if keys_down[simplegui.KEY_MAP["d"]]:
        player_a.right(dt)
    if keys_down[simplegui.KEY_MAP["w"]]:
         player_a.forward(dt)

    if keys_down[simplegui.KEY_MAP["space"]]:
        player_a.jump()
        
time_list = []
count = 0
prev_time = time.time()
    
def game_loop(canvas):
    global count, prev_time
    dt = time.time() - prev_time
    prev_time = time.time()
    
    ##main Stuff
    update_world(dt)
    render_frame(canvas)
    key_action(dt)
    
    #FPS Stuff
    time_list.append(dt)
    if(len(time_list) > 20):
        time_list.pop(0)
    avg_time = 0
    for time_t in time_list:
        avg_time += time_t
    avg_time /= len(time_list)
    count+=1
    if count%20==0:
        fps= 1/avg_time
        #print "FPS: " + str(int(10/avg_time)/10)
        #print "GRID SIZE: " + str(grid.square_size**2)
        if fps > 15:
            grid.square_size += 1
        elif fps < 10:
            if grid.square_size > 8:
                grid.square_size -= 1
            else:
                print "Warning: This computer is too slow!"

WIDTH = 1200
HEIGHT = 600
    
def init():
    global player_a, player_b, grid, left_camera, right_camera, game_over, text_left, text_right
    
    grid = Grid()
            
    player_a = WorldPlayer(300, 0, 255, 0, 0)
    player_b = WorldPlayer(-300, 0, 0, 255, 0)

    left_camera = DrawEngine.Camera(0,0,0,  0,     50,       100,      475,      HEIGHT-125)
    right_camera = DrawEngine.Camera(0,0,200,  0 , WIDTH/2+50 , 100,     475,      HEIGHT-125)
    
    game_over = False
    text_left = "You Lose!"
    text_right = "You Lose!"

frame = simplegui.create_frame("~", WIDTH, HEIGHT)
frame.set_draw_handler(game_loop)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

reset_button = frame.add_button('Reset All', init)

init()

frame.start()

'''
Game State:
0 - main menu
1 - single player
2 - two player


'''
