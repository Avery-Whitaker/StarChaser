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
import user40_vGEjZ00kyC_2 as DrawEngine

        
class WorldPlayer(DrawEngine.WorldSphere, DrawEngine.WorldAngle):
    def __init__(self,x,y,r,b,g):
        DrawEngine.WorldSphere.__init__(self, x, y, 600, r,b,g,1)
        DrawEngine.WorldAngle.__init__(self, 0)
        self.z_vel = 20
        self.radius = 30
        self.speed = 600
        
    def update(self, time_delta):
        ground_z = world_objects.grid_height(self.x,self.y)+self.radius
        
        if self.z_vel >= 0:
             self.z += self.z_vel*time_delta
        elif self.z >= ground_z and self.z + self.z_vel*time_delta < ground_z:
            self.z = ground_z
            self.z_vel = 0
        else:
            self.z += self.z_vel*time_delta
        
        self.z_vel -= 1200*time_delta
        
    def jump(self):
        ground_z = world_objects.grid_height(self.x,self.y)+self.radius
        if self.z == ground_z:
            self.z_vel += 800
       
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
        shawdow_height = world_objects.grid_height(self.x,self.y)
        r = 250
        
        if shawdow_height >= self.z-self.radius:
            return None
        
        for i in range(0,n):
            points.append(DrawEngine.WorldPoint(self.x+50*math.cos(angle),self.y+50*math.sin(angle),world_objects.grid_height(self.x,self.y)))
            angle+=(math.pi*2)/n
            
        return DrawEngine.WorldPoly(points, 20, 20, 20)


class WorldObjects():
    def __init__(self):
        self.objects = {}
        self.grid = {}
        
        self.tile_size = 400
        self.square_size = 7
        
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
        
        for x in self.x_range():
            if not self.grid.has_key(x):
                self.grid[x] = {}
                self.objects[x] = {}
                
        for x,y in self.x_y_range():
            if not self.grid[x].has_key(y):
                if random.randrange(0,3) != 1:
                    self.grid[x][y] = int(self.tile_size/0.5*int(random.randrange(0,2)*0.5*math.sqrt(x**2+y**2))/10)
                else:
                    self.grid[x][y] = -100000
                r = 170
                g = 170
                b = 170+self.grid[x][y]
                self.objects[x][y] = (DrawEngine.WorldPoly([DrawEngine.WorldPoint(self.tile_size/2+x*self.tile_size, self.tile_size/2+y*self.tile_size, self.grid[x][y]),
                                                 DrawEngine.WorldPoint(-self.tile_size/2+x*self.tile_size,                self.tile_size/2+y*self.tile_size, self.grid[x][y]),
                                                 DrawEngine.WorldPoint(-self.tile_size/2+x*self.tile_size,                -self.tile_size/2+y*self.tile_size, self.grid[x][y]), 
                                                 DrawEngine.WorldPoint(self.tile_size/2+x*self.tile_size,  -self.tile_size/2+y*self.tile_size, self.grid[x][y])], r, g, b))
                
    def grid_height(self,x,y):
        x = round(x/self.tile_size)
        y = round(y/self.tile_size)
        
        if not (x,y) in self.x_y_range():
            return -10000000.00
        return self.grid[x][y]
 
    def remove(self,object):
        self.objects.remove(object)
       
    def to_list(self):
        list = []
        for x,y in self.x_y_range():
            list.append(self.objects[x][y])
        return list
         
def render_frame(canvas):
    canvas.draw_polygon([[0, 0], [0, HEIGHT], [WIDTH, HEIGHT], [WIDTH, 0]], 1, 'White', 'Cyan')
    
    canvas.draw_text('RIP', (75, 200), 48, 'Black')
    canvas.draw_text('RIP', (WIDTH/2+100, 200), 48, 'Black')
    
    canvas.draw_text('Runner', (75, 100), 24, 'Black')
    canvas.draw_text('Seeker', (WIDTH/2+100, 100), 24, 'Black')
    
    render_objects = world_objects.to_list()
    render_objects.append(player_a)
    render_objects.append(player_b)
    render_objects.append(player_a.shadow())
    render_objects.append(player_b.shadow())
    
    if player_b.z > -2000:
        right_camera.draw(canvas,render_objects)
    if player_a.z > -2000:
        left_camera.draw(canvas,render_objects)
    #canvas.draw_line((WIDTH/2, 100), (WIDTH/2, HEIGHT), 4, 'White')
    #canvas.draw_line((0, 100), (WIDTH, 100), 4, 'White')
    canvas.draw_text('Avery Whitaker | (Split-Screen Multiplayer Prototype) V0.8', (30, 50), 48, 'Red')
    
def update_world(time_delta):
    player_a.update(time_delta)
    player_b.update(time_delta)
    
    world_objects.set_center(player_a[0], player_a[1])
    
    dx = player_b.x-player_a.x
    dy = player_b.y-player_a.y
    l = 1000
    
    L = math.sqrt( dx**2 + dy**2 )
    
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
    
    time_list.append(dt)
    if(len(time_list) > 20):
        time_list.pop(0)
    avg_time = 0
    for time_t in time_list:
        avg_time += time_t
    avg_time /= len(time_list)
    count+=1
    if count%20==0:
        print "FPS: " + str(int(10/avg_time)/10)

WIDTH = 1200
HEIGHT = 600
    
def init():
    global player_a, player_b, world_objects, left_camera, right_camera
    
    world_objects = WorldObjects()
            
    player_a = WorldPlayer(0, 0, 255, 0, 0)
    player_b = WorldPlayer(0, 0, 0, 255, 0)

    left_camera = DrawEngine.Camera(0,0,0,  0,     50,       100,      475,      HEIGHT-125)
    right_camera = DrawEngine.Camera(0,0,200,  0 ,WIDTH/2+50 , 100,     475,      HEIGHT-125)

frame = simplegui.create_frame("~", WIDTH, HEIGHT)
frame.set_draw_handler(game_loop)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

reset_button = frame.add_button('Reset All', init)

init()

frame.start()
