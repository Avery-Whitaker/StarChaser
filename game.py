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

#in: list of points
##########################################################################################
def trimZero(points, axis, axis_n):
    
        #stolen from internet https://paolocrosetto.wordpress.com/python-code/
        #works like magic
        #I claim no rights to this function
        def check_convexity(p):
            #this checks the sign of a number
            def sign(x):
                if x >= 0: 
                    return 1
                else: 
                    return 0
            #this defines triples of subsequent vertexes on any polygon
            def triads(p):
                return zip(p, p[1:]+[p[0]], p[2:]+[p[0]]+[p[1]])
            #this uss Bastian's three-vertex function to check convexity
            i = 0
            for ((x0, y0), (x1, y1), (x2,y2)) in triads(p):
                if i==0: fsign = sign(x2*(y1-y0)-y2*(x1-x0)+(x1-x0)*y0-(y1-y0)*x0)
                else:
                    newsign = sign(x2*(y1-y0)-y2*(x1-x0)+(x1-x0)*y0-(y1-y0)*x0)
                    if newsign != fsign: return False
                i +=1
            return True
            
        #point on line from point_a to point_b where axis = 0
        def intersection(point_a, point_b, axis, axis_n):
            new_point = []
            for i in range(0,axis_n):
                new_point.append(0)
            if axis_n == 3:       
                #new_point[axis-2] = (max(point_a[axis-2],point_b[axis-2])-min(point_b[axis-2],point_a[axis-2]))*max(point_b[axis],point_a[axis]) / ( abs(point_b[axis])+abs(point_a[axis])) + min(point_b[axis-2],point_a[axis-2])
                #new_point[axis-1] = (max(point_a[axis-1],point_b[axis-1])-min(point_b[axis-1],point_a[axis-1]))*(max(point_b[axis],point_a[axis])/( abs(point_b[axis])+abs(point_a[axis])))+min(point_b[axis-1],point_a[axis-1])
                new_point[axis-2] = (-(point_b[axis-2]-point_a[axis-2])/(point_b[axis]-point_a[axis]))*point_a[axis]  + point_a[axis-2]
                new_point[axis-1] = (-(point_b[axis-1]-point_a[axis-1])/(point_b[axis]-point_a[axis]))*point_a[axis]  + point_a[axis-1]
                new_point[axis] = 0
                return [new_point[0],new_point[1],new_point[2]]
            if axis_n == 2:
                new_point[axis] = 0
                new_point[axis-1] = (-(point_b[axis-1]-point_a[axis-1])/(point_b[axis]-point_a[axis]))*point_a[axis]  + point_a[axis-1]
                return [new_point[0],new_point[1]]
        
        min_num = 1000000000000
        max_num = -1000000000000
        for point in points:
            if point[axis] < min_num:
                min_num = point[axis]
            if point[axis] > max_num:
                max_num = point[axis]
                
        if min_num < 0 and max_num > 0:
            i = 0
            while points[i][axis] < 0:
                i = (i+1)%len(points)
            while points[i][axis] > 0:
                i = (i+1)%len(points)

            point_a = intersection(points[i],points[i-1],axis,axis_n)

            cut_start = i
            while points[i][axis] <= 0:
                i = (i+1)%len(points)
            point_b = intersection(points[i],points[i-1],axis,axis_n)
            cut_end = i
            if cut_start > cut_end:
                for  i in range(cut_start,len(points)):
                    points.pop(cut_start)
                for  i in range(0,cut_end):
                    points.pop(0)
            else:
                for i in range(cut_start,cut_end):
                    points.pop(cut_start)
            
            points.insert(cut_start,point_b)
            points.insert(cut_start,point_a)
            
            if not check_convexity(points):
                points.remove(point_a)
                points.remove(point_b)
                points.insert(cut_start,point_a)
                points.insert(cut_start,point_b)
                
##########################################################################################

#mutates points_list
#trims polygon to be in rectangle defined by xMin, xMax yMin, yMax
def polyTrim(points_list, xMin, xMax, yMin, yMax):
    #can optimize by not running for edges of screen
    def trimAxis(points, min, max, axis, axis_n):
        if min != 0:
            for point in points:
                point[axis] -= min
        trimZero(points, axis, axis_n)
        for point in points:
            point[axis] = -(point[axis] + min - max)
        trimZero(points, axis, axis_n)
        for point in points:
            point[axis] = -point[axis] + max
            
    trimAxis(points_list, xMin, xMax, 0, 2)
    trimAxis(points_list, yMin, yMax, 1, 2)


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
        y = -self.z + camera.z
        z = -self.y + camera.y
        cos_xy = math.cos(-camera.angle_xy)
        sin_xy = math.sin(-camera.angle_xy)
        old_x = x
        x = x * cos_xy - (z+camera.focalLength)*sin_xy
        z = (z+camera.focalLength) * cos_xy + old_x * sin_xy - camera.focalLength
        if camera.focalLength + z == 0:
            scale = 1000000000000
        else:
            scale = camera.focalLength/(camera.focalLength + z)
        return ScreenPoint(
            camera.vanishingPointX + x * abs(scale), 
            camera.vanishingPointY + y * abs(scale), -scale)
    
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
        self.focalLength = 250.0
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
                    trimZero(points, 2, 3)
                return ScreenPoly(points, self.color_r, self.color_g, self.color_b)
            return None
        
    #prototope temp
    def min_x(self):
        min_x = 10000000000
        for point in self.points:
            if point[0] < min_x:
                min_x = point[0]
        return min_x
    def max_x(self):
        max_x = -1000000000
        for point in self.points:
            if point[0] > max_x:
                max_x = point[0]
        return max_x
    
    def min_y(self):
        min_y = 10000000000
        for point in self.points:
            if point[1] < min_y:
                min_y = point[1]
        return min_y
    
    def max_y(self):
        max_y = -1000000000
        for point in self.points:
            if point[1] > max_y:
                max_y = point[1]
        return max_y
       
    
class WorldPlayer(WorldPoint, WorldAngle):
    def __init__(self,x,y):
        WorldPoint.__init__(self, x, y, 75)
        WorldAngle.__init__(self, 0)
        self.z_vel = 1
        
    def update(self):
        if self.z_vel >= 0:
             self.z += self.z_vel
        elif self.z >= 75 and self.z + self.z_vel < 75:
         
            collide = False
            for item in world_objects:
                if item != player_a and item != player_b:
                    if self.x >= item.min_x()-50 and self.x <= item.max_x()+50  and self.y >= item.min_y()-50  and self.y <= item.max_y()+50 :
                        collide = True
                        break
            if not collide:
                self.z += self.z_vel
            else:
                self.z = 75
                self.z_vel = 0
        else:
            self.z += self.z_vel
        
        self.z_vel -= 3
       
    def jump(self):
        if self.z == 75:
            collide = False
            for item in world_objects:
                if item != player_a and item != player_b:
                    if self.x >= item.min_x()-50 and self.x <= item.max_x()+50  and self.y >= item.min_y()-50  and self.y <= item.max_y()+50 :
                        collide = True
                        break
            #cases: in air above, on platform, below platform
            if collide: 
                self.z_vel += 40
       
    def forward(self):
        self.y += 20 * math.cos(self.angle_xy)
        self.x += 20 * math.sin(self.angle_xy)
        
    def left(self):
        self.x -= 20 * math.cos(self.angle_xy)
        self.y += 20 * math.sin(self.angle_xy)
        
    def right(self):
        self.x += 20 * math.cos(self.angle_xy)
        self.y -= 20 * math.sin(self.angle_xy)
       
    def back(self):
        self.y -= 20 * math.cos(self.angle_xy)
        self.x -= 20 * math.sin(self.angle_xy)
        
#class ScreenImage:
#    def __init__(self,x,y,image)
#    	pass
             
    #    def draw(self, canvas, camera):
    #         pass
            #crop so entirly whiten camera
                     
    #       canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest, rotation)
        
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
        line_width = 5
        radius = 30
        if self.scale > 0 and self.x > 0 and self.y > 0 and self.x < camera.screen_width and self.y < camera.screen_height :
            canvas.draw_circle((self.x+camera.screen_x, self.y+camera.screen_y), radius * self.scale, line_width, 'Red','Red')

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
            polyTrim(new, camera.screen_x, camera.screen_x+camera.screen_width, camera.screen_y, camera.screen_y+camera.screen_height)
            canvas.draw_polygon(new, 1, 'rgb(0,0,255)',"rgb("+str(self.color_r)+","+str(self.color_g)+","+str(self.color_b)+")")

world_objects = []
n = 5
l = 300 

for y in range(0,n):
    for x in range(0,n):
        if random.random() > 0.2:
            world_objects.append(WorldPoly([WorldPoint(l+x*l, l+y*l, 0),
                                                      WorldPoint(0+x*l, l+y*l, 0),
                                                      WorldPoint(0+x*l, y*l, 0), 
                                                      WorldPoint(l+x*l, y*l, 0)]))

player_a = WorldPlayer(world_objects[0][0][0]-l/2, world_objects[0][0][1]-l/2)
player_b = WorldPlayer(world_objects[5][0][0]-l/2, world_objects[5][0][1]-l/2)

world_objects.append(player_a)
world_objects.append(player_b)

WIDTH = 1200
HEIGHT = 600

left_camera = Camera(0,0,0,  0,     50,       100,      475,      HEIGHT-125)
right_camera = Camera(0,0,200,  0 ,WIDTH/2+50 , 100,     475,      HEIGHT-125)
         
def render_frame(canvas):
    canvas.draw_polygon([[0, 0], [0, HEIGHT], [WIDTH, HEIGHT], [WIDTH, 0]], 1, 'White', 'Cyan')
    
    canvas.draw_text('RIP', (75, 200), 48, 'Black')
    canvas.draw_text('RIP', (WIDTH/2+100, 200), 48, 'Black')
    
    if player_b.z > -2000:
        right_camera.draw(canvas,world_objects)
    if player_a.z > -2000:
        left_camera.draw(canvas,world_objects)
    #canvas.draw_line((WIDTH/2, 100), (WIDTH/2, HEIGHT), 4, 'White')
    #canvas.draw_line((0, 100), (WIDTH, 100), 4, 'White')
    canvas.draw_text('Avery Whitaker | (Split-Screen Multiplayer Prototype) V0.8', (30, 50), 48, 'Red')
    
def update_world():
    
    player_a.update()
    player_b.update()
    
    
    #lenAB = math.sqrt( (p2x-p1x)**2 + (p2y-p1y)**2 )
    
    
    #left_camera.set_pos(math.cos(angle_b)*300+player_a.x,  math.sin(angle_b)*300+player_a.y, 300+player_a.z)
    #right_camera.set_pos(math.cos(angle_a)*300+player_b.x,  math.sin(angle_a)*300+player_b.y,300+player_b.z)
    
    
    # right_camera.set_pos(-p1x - (p1x-p2x) / lenAB * 300,200-player_a.y, -p1y - (p2y-p1y) / lenAB * 300)
    #left_camera.set_pos(-p2x + (p1x-p2x) / lenAB * 300,200-player_b.y, -p2y + (p1y-p2y) / lenAB * 300)
    
    #left_camera.set_pos(-math.sin(angle_a)*100-player_a.x, 200-player_a.y, -math.cos(angle_a)*100-player_a.z)
    #right_camera.set_pos(-player_a.x-math.cos(angle_a)*600, 200-player_a.y, -player_a.z-math.sin(angle_a)*600)
    #right_camera.set_pos(-player_b.x, 200-player_b.y, 100-player_b.z)
    #print angle_a
    #left_camera.set_pos(-math.cos(-angle_a)*800-player_a.x, 200-player_a.y, -math.sin(-angle_a)*800-player_a.z)
    #right_camera.set_pos(-math.cos(-angle_b)*800-player_b.x, 200-player_b.y, -math.sin(-angle_b)*800-player_b.z)
    
    #left_camera.set_pos(math.cos(temp_angle)*500+player_a.x, math.sin(temp_angle)*500+player_a.y, 300+player_a.z)
    
    #player_a.z = 75
    #player_b.z = 75
    
    dx = player_b.x-player_a.x
    dy = player_b.y-player_a.y
    l = 600
    L = math.sqrt( dx**2 + dy**2 )
    angle_a = WorldAngle.angleBetweenWorldPoints(player_a, player_b)
    angle_b = WorldAngle.angleBetweenWorldPoints(player_b, player_a)
    
    left_camera.set_angle_xy(math.pi/2-WorldAngle.angleBetweenWorldPoints(player_a, player_b))
    right_camera.set_angle_xy(math.pi/2-WorldAngle.angleBetweenWorldPoints(player_b, player_a))
    
    left_camera.set_pos(player_a.x - math.cos(angle_a)*l, player_a.y - math.sin(angle_a)*l - l/2, 300+player_a.z)
    right_camera.set_pos(player_b.x - math.cos(angle_b)*l, player_b.y - math.sin(angle_b)*l - l/2, 300+player_b.z)
    
    #left_camera.set_pos(player_a.x, player_a.y, 300+player_a.z)
    #right_camera.set_pos(player_b.x, player_b.y, 300+player_b.z)
    
    
    player_a.set_angle_xy(math.pi/2-angle_a)
    player_b.set_angle_xy(math.pi/2-angle_b)
#    
#    random.shuffle(world_objects)
#
#    if random.random() > 0.99:
#        for item in world_objects:
#            if item != player_a and item != player_b:
#                world_objects.remove(item)
#                break
    
keys_down = {}

for i in range(1,300):
    keys_down[i] = False
    
def keydown(k):
    global keys_down
    keys_down[k] = True
    
def keyup(k):
    global keys_down
    keys_down[k] = False
            
def key_action():    
    
    if keys_down[simplegui.KEY_MAP["up"]]:
        player_b.forward()
    if keys_down[simplegui.KEY_MAP["down"]]:
        player_b.back()
    if keys_down[simplegui.KEY_MAP["left"]]:
        player_b.left()
    if keys_down[simplegui.KEY_MAP["right"]]:
        player_b.right()
        
    if keys_down[16]:
        player_b.jump()
    
    
    if keys_down[simplegui.KEY_MAP["s"]]:
        #player_a.back(math.atan2(p2y - p1y, p2x - p1x))
        player_a.back()
    if keys_down[simplegui.KEY_MAP["a"]]:
        player_a.left()
    if keys_down[simplegui.KEY_MAP["d"]]:
        player_a.right()
    if keys_down[simplegui.KEY_MAP["w"]]:
         player_a.forward()
        
    if keys_down[simplegui.KEY_MAP["space"]]:
        player_a.jump()

def game_loop(canvas):
    render_frame(canvas)
    update_world()
    key_action()

frame = simplegui.create_frame("~", WIDTH, HEIGHT)
frame.set_draw_handler(game_loop)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.start()
