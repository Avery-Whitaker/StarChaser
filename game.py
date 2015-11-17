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
import user40_hIgQ2QMFUJ_1 as trim

class WorldAngle:
    def __init__(self, angle_xy):
        self.angle_xy = angle_xy
        
    def set_angle_xy(self, angle_xy):
        self.angle_xy = angle_xy
        
    def turn_angle_xy(self, turn_amount):
        self.angle_xy += turn_amount
    
    def angleBetweenWorldPoints(point_a, point_b):
        return math.atan2(point_b[1] - point_a[1], point_b[0] - point_a[0])
    
class WorldPoint:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
    def move(self,a,b,c):
        self.x += a
        self.y += b
        self.z += c
                
    def set_pos(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __getitem__(self,key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z
        if key < 0:
            return self[key+3]
        
    def transform(self,camera):
        x = self.x - camera.x
        old_x = x
        y = -self.z + camera.z 
        z = -self.y + camera.y + camera.focalLength
        cos_xy = math.cos(camera.angle_xy)
        sin_xy = -math.sin(camera.angle_xy)
        x = x * cos_xy - z * sin_xy
        z = z * cos_xy + old_x * sin_xy - camera.focalLength
        if z == 0:
            scale = 1000000000000.0
        else:
            scale = camera.focalLength/z
        return ScreenPoint(camera.vanishingPointX + x * abs(scale), camera.vanishingPointY + y * abs(scale), -scale)
    
class Camera(WorldAngle, WorldPoint):
    def draw(self, canvas, world_objects):
        canvas.draw_polygon([[self.screen_x, self.screen_y], [self.screen_x+self.screen_width, self.screen_y], [self.screen_x+self.screen_width, self.screen_y+self.screen_height], [self.screen_x, self.screen_y+self.screen_height]], 1, 'White','Grey')
            
        list = []
        for a in world_objects:
            b = a.transform(self)
            if b is not None:
                list.append(b)
        list.sort()
        for twoDPoly in list:
            twoDPoly.draw(canvas, self)
        
        canvas.draw_polygon([[self.screen_x, self.screen_y], [self.screen_x+self.screen_width, self.screen_y], [self.screen_x+self.screen_width, self.screen_y+self.screen_height], [self.screen_x, self.screen_y+self.screen_height]], 2, 'White')
           
    def __init__(self, x, y, z, yAngle, screen_x, screen_y, screen_width, screen_height):
        WorldPoint.__init__(self, x,y,z)
        WorldAngle.__init__(self, yAngle)
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.focalLength = 300.0
        self.vanishingPointX, self.vanishingPointY = screen_width/2.0, screen_height/2.0
    
class WorldPoly:
    def __init__(self,points, color_r = random.randrange(70,100), color_g = random.randrange(200,255),color_b = random.randrange(70,100)):
        self.points = points
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
        
    def __getitem__(self,key):
        return self.points[key]
    
    def transform(self, camera):
            line_thinkness = 1
            points = []
            maxScale = -1000000000
            minScale = 10000000000
            for point in self.points:
                points.append( point.transform(camera) )
                if points[len(points)-1][2] > maxScale:
                    maxScale = points[len(points)-1][2]
                if points[len(points)-1][2] < maxScale:
                    minScale = points[len(points)-1][2]
            if maxScale > 0:
                if minScale < 0:
                    trim.trimZero(points, 2, 3)
                return ScreenPoly(points, self.color_r, self.color_g, self.color_b )
            return None
        
class WorldPlayer(WorldPoint, WorldAngle):
    def __init__(self,x,y):
        WorldPoint.__init__(self, x, y, 600)
        WorldAngle.__init__(self, 0)
        self.z_vel = 20
        self.radius = 30
        
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
        self.y += 500 * dt * math.cos(self.angle_xy)
        self.x += 500 * dt * math.sin(self.angle_xy)
        
    def left(self, dt):
        self.x -= 500 * dt * math.cos(self.angle_xy)
        self.y += 500 * dt * math.sin(self.angle_xy)
        
    def right(self, dt):
        self.x += 500 * dt * math.cos(self.angle_xy)
        self.y -= 500 * dt * math.sin(self.angle_xy)
       
    def back(self, dt):
        self.y -= 500 * dt * math.cos(self.angle_xy)
        self.x -= 500 * dt * math.sin(self.angle_xy)

class ScreenPoint:
    def __init__(self,x,y,scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.priority = scale
        
    def __getitem__(self,key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.scale
        if key < 0:
            return self[key+3]
            
    def __cmp__(self, other):
        if self.priority < other.priority:
            return -1
        elif self.priority == other.priority:
            return 0
        return 1
            
    def draw(self, canvas, camera):
        if self.scale > 0 and self.x > 0 and self.y > 0 and self.x < camera.screen_width and self.y < camera.screen_height :
            canvas.draw_circle((self.x+camera.screen_x, self.y+camera.screen_y), 30 * self.scale, 1, 'Black', 'Black')

class ScreenPoly:
    def __init__(self, points, color_r, color_g, color_b):
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
        
        self.points = points
        self.priority = 0
        for point in self.points:
            self.priority += point[2]
        self.priority /= len(self.points)
        
    def __getitem__(self,key):
        return list[key]
        
    def __cmp__(self, other):
        if self.priority < other.priority:
            return -1
        elif self.priority == other.priority:
            return 0
        return 1
            
    def draw(self, canvas, camera):
        new = []
        for point in self.points:
            new.append([point[0]+camera.screen_x, point[1]+camera.screen_y])
        minX =  10000000000
        maxX = -10000000000
        minY = 1000000000
        maxY = -10000000000
        for point in new:
            if point[0] < minX:
                minX = point[0]
            if point[1] < minY:
                minY = point[1]
            if point[0] > maxX:
                maxX = point[0]
            if point[1] > maxY:
                maxY = point[1]
        if maxX > camera.screen_x and minX < camera.screen_x+camera.screen_width and maxY > camera.screen_y and minY < camera.screen_y+camera.screen_height:
            trim.polyTrim(new, camera.screen_x, camera.screen_x+camera.screen_width, camera.screen_y, camera.screen_y+camera.screen_height)
            canvas.draw_polygon(new, 1, 'rgba(0,0,0,0)',"rgba("+str(self.color_r)+","+str(self.color_g)+","+str(self.color_b)+","+str(0.8)+")")
            
class WorldObjects():
    def __init__(self):
        self.objects = {}
        self.grid = {}
        
        self.center_tile_x = 1000000 #add big number so never negative
        self.center_tile_y = 1000000
        
        self.tile_size = 300
        self.tiles_width = 6
        self.tiles_height = 6
        
        self.set_center(0,0)
        
    def x_range(self):
        return range(self.center_tile_x-int(self.tiles_width/2),self.center_tile_y+int(self.tiles_width/2))
        
    def y_range(self):
        return range(self.center_tile_y-int(self.tiles_height/2),self.center_tile_y+int(self.tiles_height/2))
        
    def set_center(self,x,y):
        x = int(x/self.tile_size)
        y = int(y/self.tile_size)
        
        self.center_tile_x = x + 1000000 #add big number so never negative
        self.center_tile_y = y + 1000000 
        
        for x in self.x_range():
            
            if not self.grid.has_key(x):
                self.grid[x] = {}
                self.objects[x] = {}
                
            for y in self.y_range():
                if not self.grid[x].has_key(y):
                    self.grid[x][y] = int(self.tile_size/0.000002*random.randrange(0,2))
                    self.objects[x][y] = {}
                    
                x1 = x - 1000000
                y1 = y - 1000000
                r = 170
                g = 170
                b = 170
                self.objects[x][y] = (WorldPoly([WorldPoint(self.tile_size+x1*self.tile_size, self.tile_size+y1*self.tile_size, self.grid[x][y]),
                                       WorldPoint(x1*self.tile_size, self.tile_size+y1*self.tile_size, self.grid[x][y]),
                                       WorldPoint(x1*self.tile_size, y1*self.tile_size, self.grid[x][y]), 
                                       WorldPoint(self.tile_size+x1*self.tile_size, y1*self.tile_size, self.grid[x][y])], r, g, b))
                
    def grid_height(self,x,y):
        
        x = int(x/self.tile_size)
        y = int(y/self.tile_size)
        
        x += 1000000
        y += 1000000
        
        
        if not x in self.x_range() or not y in self.y_range(): # x < self.center_tile_x-int(self.tiles_width/2) or y < self.center_tile_y-int(self.tiles_height/2) or x > (self.center_tile_y+int(self.tiles_width/2)) or y > self.center_tile_y+int(self.tiles_height/2):
            return -10000000.00
        return self.grid[int(x)][int(y)]
                    
    def __iter__(self):
        return self.objects.__iter__()
        
    def remove(self,object):
        self.objects.remove(object)
       
    def to_list(self):
        list = []        
        for x in self.x_range():
            for y in self.y_range():
                list.append(self.objects[x][y])
        return list
            
    def sort(self):
        self.objects.sort()
            
world_objects = WorldObjects()
            
player_a = WorldPlayer(0, 0)
player_b = WorldPlayer(0, 0)

print world_objects.grid_height(0,0)

WIDTH = 1200
HEIGHT = 600

left_camera = Camera(0,0,0,  0,     50,       100,      475,      HEIGHT-125)
right_camera = Camera(0,0,200,  0 ,WIDTH/2+50 , 100,     475,      HEIGHT-125)
         
def render_frame(canvas):
    canvas.draw_polygon([[0, 0], [0, HEIGHT], [WIDTH, HEIGHT], [WIDTH, 0]], 1, 'White', 'Cyan')
    
    canvas.draw_text('RIP', (75, 200), 48, 'Black')
    canvas.draw_text('RIP', (WIDTH/2+100, 200), 48, 'Black')
    
    render_objects = world_objects.to_list()
    render_objects.append(player_a)
    render_objects.append(player_b)
    
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
    angle_a = WorldAngle.angleBetweenWorldPoints(player_a, player_b)
    angle_b = WorldAngle.angleBetweenWorldPoints(player_b, player_a)
    
    if L < 100:
        keys_down[simplegui.KEY_MAP["up"]] = False
        keys_down[simplegui.KEY_MAP["w"]] = False
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

frame = simplegui.create_frame("~", WIDTH, HEIGHT)
frame.set_draw_handler(game_loop)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.start()
