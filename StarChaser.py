'''
Welcome to StarChaser! A 3D platformer built in a 2D game
engine. Dveloped by Avery Whitaker for COMP 140:
Introduction to Game Development in Python at Rice
University. Submitted 1st of December, 2015.

Game includes two modes. Chase mode (two player) and
Time Trial mode (single player). 

Chase mode utilizes split screen multiplayer (extremely
optimized for codeskulptor, but not enough to run
decently). Beware of keyboard ghosting with two player,
keyboard buttons can be adjusted through constants at
top of program. 

In single player mode players must try and go a set
distance as fast as possible. Game records your fastest
time and displays it on top of screen. Typically a
player is competing against themselves: I found in this
situation a separate high score page is less engaging
than a flappy bird style highscore. Unskilled players
may find it difficult to reach the required distance.
Annoying death messages are there as motivation.

I keep two player mode as a feat of technical prowess;
Single player is more fun. Two player mode can be
disabled with the below TWO_PLAYER_ENABLED constant.
I recommend, in general, disabling two player.
Maybe some day in the future codeskulptor will run fast
enough for two player mode. I look forward to that day.

Note on code: it's pretty bad. Proper object oriented
programming paradigms are not followed. Lots of global
variables do obscure things. I would not expect someone
to be able to figure out what's going on. Objects in
this final version is very specifically made for this
game. Earlier versions may better show 3D rendering
engine at its best. (Note that I did not get polygon
trimming right until very late versions) Here are links
to the project at various stages to illustrate how 3D
rendering is accomplished (there may be bugs).

Basic 3D OOP rendering:
http://www.codeskulptor.org/#user40_n76nGsSke6_20.py

Split Screen Multiplayer:
http://www.codeskulptor.org/#user40_3lQsilJfED_27.py
http://www.codeskulptor.org/#user40_3lQsilJfED_42.py

Prototype Game:
http://www.codeskulptor.org/#user40_X0HATLAfLW_12.py

For full version history see github:
https://github.com/Avery-Whitaker/Python-Game
Please forgive me on my crappy commit messages. I don't
expect anyone to need them ever anyway.

Original Pitch Sheet (Concept has since been revised)
http://www.averyw.me/RunNGunPoster.pdf

On my honor, I have neither given nor received any
unauthorized aid on this assignment.
-Avery Whitaker
'''

TWO_PLAYER_ENABLED = True

#Print FPS and number of tiles rendered
FPS_PRINT = False

#Set volumes between 0.0 and 1.0
MUSIC_VOLUME = 0.2
SOUND_VOLUME = 1

#Set a default highscore or leave at 10000000 for no initial highscore
highscore = 10000000

FONT = "monospace"

import simplegui
#Key Bindings
BUTTON_PLAYER_A_UP = simplegui.KEY_MAP["w"]
BUTTON_PLAYER_A_DOWN = simplegui.KEY_MAP["s"]
BUTTON_PLAYER_A_LEFT = simplegui.KEY_MAP["a"]
BUTTON_PLAYER_A_RIGHT = simplegui.KEY_MAP["d"]
BUTTON_PLAYER_A_JUMP = simplegui.KEY_MAP["space"]
BUTTON_PLAYER_B_UP = simplegui.KEY_MAP["up"]
BUTTON_PLAYER_B_DOWN = simplegui.KEY_MAP["down"]
BUTTON_PLAYER_B_LEFT = simplegui.KEY_MAP["left"]
BUTTON_PLAYER_B_RIGHT = simplegui.KEY_MAP["right"]
BUTTON_PLAYER_B_JUMP = 16
BUTTON_ESCAPE = 27

'''
please direct any questions to
averywhitaker@gmail.edu

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

#Sorry, game does not handle resizing
WIDTH = 1200
HEIGHT = 600

import math
import random
import time
loading_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/loading_back.png")
loading_animation = []
for i in range(1,13):
    loading_animation.append(simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/loading_"+str(i)+".png"))
menu_music = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/menu.ogg")
menu_music.play()
background_image = []
for i in range(1,300):
    s = str(i)
    while(len(s) < 3):
        s = '0'+s
    background_image.append(simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/background/background%20"+s+".png"))
logo_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/logo.png")
background_menu_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/background_round.png")
subtitle_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/subtitle.png")
how_to_play_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/how_to_play.png")
chase_mode_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/chase_mode.png")
time_trial_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/time_trial.png")
how_to_play_image_down = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/how_to_play_pressed.png")
chase_mode_image_down = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/chase_mode_pressed.png")
time_trial_image_down = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/time_trial_pressed.png")
if TWO_PLAYER_ENABLED:
    how_to_play_menu_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/How%20to%20play.png")
else:
    how_to_play_menu_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/How%20to%20play_one_player.png")
player_image_a = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/player_sprite_a.png")
player_image_b = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/player_sprite_b.png")
player_image_a_speedup = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/player_sprite_a_speed.png")
player_image_b_speedup = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/player_sprite_b_speed.png")
bounce_blue_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/bounce_blue.mp3")
beep_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/beep_sound.mp3")
falling_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/falling_sound.mp3")
platform_death_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/platform_death_sound.mp3")
victory_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/victory_fanfare.mp3")
speed_up_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/speed_up.mp3")
speed_down_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/speed_down.mp3")
game_music = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/game_music_loop.ogg")
game_music_intro = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/game_intro.ogg")
menu_music.set_volume(MUSIC_VOLUME)
game_music.set_volume(MUSIC_VOLUME)
game_music_intro.set_volume(MUSIC_VOLUME)
speed_down_sound.set_volume(SOUND_VOLUME)
speed_up_sound.set_volume(SOUND_VOLUME)
victory_sound.set_volume(SOUND_VOLUME)
platform_death_sound.set_volume(SOUND_VOLUME)
falling_sound.set_volume(SOUND_VOLUME)
beep_sound.set_volume(SOUND_VOLUME)
bounce_blue_sound.set_volume(SOUND_VOLUME)
background_image_counter = 0
player_rotate = 0
keys_down = {}
for i in range(1,300):
    keys_down[i] = False
blinker_counter = 0
loading_time = time.time()
next_runner = None
time_list = []
count = 0
prev_time = time.time()
num_players = 2
left_score = 0
right_score = 0
background_rotation = 0   
frame = simplegui.create_frame("StarChaser", WIDTH, HEIGHT)

def trim_zero(points, axis, axis_n):
        #Below function from: https://paolocrosetto.wordpress.com/python-code/
        #I claim no rights to the below function "check_convexity"
        def check_convexity(p):
            def sign(x):
                if x >= 0: 
                    return 1
                else: 
                    return 0
            def triads(p):
                return zip(p, p[1:]+[p[0]], p[2:]+[p[0]]+[p[1]])
            i = 0
            for ((x0, y0), (x1, y1), (x2,y2)) in triads(p):
                if i==0: fsign = sign(x2*(y1-y0)-y2*(x1-x0)+(x1-x0)*y0-(y1-y0)*x0)
                else:
                    newsign = sign(x2*(y1-y0)-y2*(x1-x0)+(x1-x0)*y0-(y1-y0)*x0)
                    if newsign != fsign: return False
                i +=1
            return True
        def intersection(point_a, point_b, axis, axis_n):
            new_point = []
            for i in range(0,axis_n):
                new_point.append(0)
            if axis_n == 3:       
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
def trim_axis(points, n_min, n_max, axis, trim_min, trim_max):
    if trim_min:
        if min != 0:
            for point in points:
                point[axis] -= n_min
        trim_zero(points, axis, 2)
        if min != 0:
            for point in points:
                point[axis] += n_min  
    if trim_max:
        for point in points:
            point[axis] = -(point[axis] - n_max)
        trim_zero(points, axis, 2)
        for point in points:
            point[axis] = -point[axis] + n_max
def poly_trim(points, x_min, x_max, y_min, y_max, crop_left, crop_right, crop_top, crop_bot):        
    trim_axis(points, x_min, x_max, 0, crop_left, crop_right)
    trim_axis(points, y_min, y_max, 1, crop_top, crop_bot)
    
class WorldAngle:
    def __init__(self, angle_xy):
        self.angle_xy = angle_xy
        
    def set_angle_xy(self, angle_xy):
        self.angle_xy = angle_xy
        
    def turn_angle_xy(self, turn_amount):
        self.angle_xy += turn_amount
    
    def angleBetweenWorldPoints(point_a, point_b):
        return math.atan2(point_b[1] - point_a[1], point_b[0] - point_a[0])
    
class Color:
    def rgba(self):
        return "rgba("+str(self.color_r)+","+str(self.color_g)+","+str(self.color_b)+","+str(self.color_a)+")"
    
    def __init__(self,r,g,b,a):
        self.color_r = r
        self.color_g = g
        self.color_b = b
        self.color_a = a
    
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
        return ScreenPoint(camera.vanishingPointX + x * abs(scale), camera.vanishingPointY + y * abs(scale), self.z, -scale)
    
class WorldSphere(WorldPoint, Color):
    def __init__(self, x, y, z, radius, r, g, b, a):
        WorldPoint.__init__(self, x, y, z)
        Color.__init__(self, r, g, b, a)
        self.radius = radius
        
    def transform(self,camera):
        s = WorldPoint.transform(self,camera)
        return ScreenCircle(s[0],s[1],self.z,s.scale,self.radius,self.color_r,self.color_g,self.color_b,self.color_a)

class Camera(WorldAngle, WorldPoint):
    
    def draw(self, canvas, world_objects):
        global background_image, background_image_counter
        background_image_counter+= 1+int(math.sqrt(self.x**2 + self.y**2))/20000
        self.background_index = background_image_counter 
        self.background_index += 2
        while self.background_index <= 0:
            self.background_index += 298
        while self.background_index >= 299:
            self.background_index -= 298
        canvas.draw_image(background_image[self.background_index], (1280/2,720/2), (1280,720), (self.screen_x+self.screen_width/2, self.screen_y+self.screen_height/2), (self.screen_width,self.screen_height))
        canvas.draw_polygon([[self.screen_x, self.screen_y], [self.screen_x+self.screen_width, self.screen_y], [self.screen_x+self.screen_width, self.screen_y+self.screen_height], [self.screen_x, self.screen_y+self.screen_height]], 1, 'Black', "rgba(0,0,0,0.6)")
        list = []
        for a in world_objects:
            if a is not None:
                b = a.transform(self)
                if b is not None:
                    list.append(b)
        list.sort()
        for twoDPoly in list:
            twoDPoly.draw(canvas, self)
        canvas.draw_polygon([[self.screen_x, self.screen_y], [self.screen_x+self.screen_width, self.screen_y], [self.screen_x+self.screen_width, self.screen_y+self.screen_height], [self.screen_x, self.screen_y+self.screen_height]], 2, 'Black')
           
    def __init__(self, x, y, z, yAngle, screen_x, screen_y, screen_width, screen_height, crop_left, crop_right, crop_top, crop_bot):
        WorldPoint.__init__(self, x, y, z)
        WorldAngle.__init__(self, yAngle)
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.focalLength = 300.0
        self.vanishingPointX, self.vanishingPointY = screen_width/2.0, screen_height/2.5
        self.crop_left = crop_left
        self.crop_right = crop_right
        self.crop_top = crop_top
        self.crop_bot = crop_bot
        self.background_index = 1
    
class WorldPoly(Color):
    def __init__(self,points, r = random.randrange(70,100), g = random.randrange(200,255), b = random.randrange(70,100), a = 1, border_a = 1):
        self.points = points
        Color.__init__(self,r,g,b,a)
        self.border_a = border_a
        
    def __getitem__(self,key):
        return self.points[key]
    
    def __len__(self):
        return len(self.points)
    
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
                    trim_zero(points, 2, 3)
                return ScreenPoly(points, self.points[0].z, self.color_r, self.color_g, self.color_b, self.color_a,self.border_a )
            return None
        
class ScreenPoint:
    def __init__(self,x,y,world_z,scale):
        self.x = x
        self.y = y
        self.world_z = world_z
        self.scale = scale
        
    def __getitem__(self,key):
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.scale
        if key < 0:
            return self[key+2]
            
    def __cmp__(self, other):
        if self.world_z < other.world_z:
            return -1
        elif self.world_z == other.world_z:
            return 0
        return 1
    
class ScreenCircle(ScreenPoint, Color):
    def __init__(self,x,y,world_z,scale,radius, r,g,b,a):
        ScreenPoint.__init__(self,x,y,world_z,scale)
        Color.__init__(self,r,g,b,a)
        self.radius = radius
        self.world_z = world_z
        
    def __cmp__(self, other):
        if self.world_z < other.world_z:
            return -1
        elif self.world_z == other.world_z:
            return 0
        return 1
            
    def draw(self, canvas, camera):
        global player_rotate
        if self.scale > 0 and self.x > 0 and self.y > 0 and self.x < camera.screen_width and self.y < camera.screen_height :
            if self.color_b == 255:
                if self.color_g != 255:
                    canvas.draw_image(player_image_a_speedup, (100/ 2, 100/2), (100, 100), (self.x+camera.screen_x, self.y+camera.screen_y),(self.radius * self.scale*5, self.radius * self.scale * 5), player_rotate)
                else:
                    canvas.draw_image(player_image_a, (100/ 2, 100/2), (100, 100), (self.x+camera.screen_x, self.y+camera.screen_y),(self.radius * self.scale*5, self.radius * self.scale * 5), player_rotate)
            else:
                player_rotate += 0.05
                if self.color_g != 255:
                    canvas.draw_image(player_image_b, (100/ 2, 100/2), (100, 100), (self.x+camera.screen_x, self.y+camera.screen_y),(self.radius * self.scale*5, self.radius * self.scale * 5), player_rotate)
                else:
                    canvas.draw_image(player_image_b_speedup, (100/ 2, 100/2), (100, 100), (self.x+camera.screen_x, self.y+camera.screen_y),(self.radius * self.scale*5, self.radius * self.scale * 5), player_rotate)
                    
class ScreenPoly:
    def __init__(self, points, world_z, color_r, color_g, color_b, color_a, border_a = 1):
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
        self.color_a = color_a
        self.points = points
        self.world_z = world_z
        self.border_a = border_a
        
    def __getitem__(self,key):
        return list[key]
        
    def __cmp__(self, other):
        if self.world_z < other.world_z:
            return -1
        elif self.world_z == other.world_z:
            return 0
        return 1
            
    def draw(self, canvas, camera):
        new = []
        for point in self.points:
            new.append([point[0]+camera.screen_x, point[1]+camera.screen_y])
        minX = 10000000000
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
            poly_trim(new, camera.screen_x, camera.screen_x+camera.screen_width, camera.screen_y, camera.screen_y+camera.screen_height,camera.crop_left,camera.crop_right,camera.crop_top,camera.crop_bot)
            canvas.draw_polygon(new, 1, "rgba("+str(self.color_r)+","+str(self.color_g)+","+str(self.color_b)+","+str(self.border_a)+")","rgba("+str(self.color_r)+","+str(self.color_g)+","+str(self.color_b)+","+str(self.color_a)+")")

class WorldPlayer(WorldSphere, WorldAngle):
    def __init__(self,x,y,r,b,g):
        WorldSphere.__init__(self, x, y, 600, 30, r,g,b,1)
        WorldAngle.__init__(self, 0)
        self.z_vel = 20
        self.radius = 30
        self.speed = 800
        self.speed_mod = 1
        self.prev_loc = []
        
    def get_prev_loc(self):
        i = 0
        while i < len(self.prev_loc)-1 and self.prev_loc[i][3] < 0.3:
            i+=1
        return self.prev_loc[i]
        
    def update(self, time_delta):
        global grid, time_end, num_players
        if self.z < -400:
            game_music.rewind()
            game_music_intro.rewind()
            if num_players == 1 and time_end is None:
                time_end = time.time()
            falling_sound.play()
        for item in self.prev_loc:
            item[3] += time_delta
        self.prev_loc.append([self.x, self.y, self.z, time_delta])
        while len(self.prev_loc) > 0 and self.prev_loc[0][3] > 0.3:
            self.prev_loc.pop(0)
        ground_z = grid.grid_height(self.x,self.y)+self.radius
        moving_ground_z = grid.grid_prev_height(self.x,self.y)+self.radius
        if self.z_vel >= 0:
             self.z += self.z_vel*time_delta
        elif self.z == ground_z or self.z == moving_ground_z:
            self.z = ground_z
            grid.get_item(self.x,self.y).stand_damage(time_delta)
            if self.speed_mod < grid.get_item(self.x,self.y).speed_mod:
                speed_up_sound.rewind()
                speed_up_sound.play()
            if self.speed_mod > grid.get_item(self.x,self.y).speed_mod:
                speed_down_sound.rewind()
                speed_down_sound.play()
            self.speed_mod = grid.get_item(self.x,self.y).speed_mod
            self.z_vel = 0
        elif self.z >= ground_z and self.z + self.z_vel*time_delta < ground_z:
            self.z = ground_z
            if grid.get_item(self.x,self.y).is_bouncy():
                if self.speed_mod < grid.get_item(self.x,self.y).speed_mod:
                    speed_up_sound.rewind()
                    speed_up_sound.play()
                if self.speed_mod > grid.get_item(self.x,self.y).speed_mod:
                    speed_down_sound.rewind()
                    speed_down_sound.play()
                self.speed_mod = grid.get_item(self.x,self.y).speed_mod
                bounce_blue_sound.rewind()
                bounce_blue_sound.play()
                self.z_vel = 1200
            else:
                self.z_vel = 0
        elif self.z < ground_z and self.z + self.radius*3 > ground_z:
            self.z = ground_z
            grid.get_item(self.x,self.y).stand_damage(time_delta)
            if self.speed_mod < grid.get_item(self.x,self.y).speed_mod:
                speed_up_sound.rewind()
                speed_up_sound.play()
            if self.speed_mod > grid.get_item(self.x,self.y).speed_mod:
                speed_down_sound.rewind()
                speed_down_sound.play()
            self.speed_mod = grid.get_item(self.x,self.y).speed_mod
            self.z_vel = 0
        else:
            self.z += self.z_vel*time_delta
        self.z_vel -= 1200*time_delta
        if self.speed_mod > 1.2:
            self.color_g = 255
        else:
            self.color_g = 0
        
    def jump(self):
        if len(self.prev_loc) != 0:
            prev_x, prev_y, prev_z = self.get_prev_loc()
        else:
            prev_x, prev_y, prev_z = 0,0,0
        ground_z = grid.grid_height(self.x,self.y)+self.radius
        prev_ground_z = grid.grid_height(prev_x,prev_y)+self.radius
        moving_ground_z = grid.grid_prev_height(self.x,self.y)+self.radius
        if self.z == ground_z or self.z == moving_ground_z or (prev_z >= prev_ground_z and prev_z < self.radius/2+prev_ground_z) and grid.get_item(self.x,self.y) is not None:
            grid.get_item(self.x,self.y).jump_damage()
            if self.speed_mod < grid.get_item(self.x,self.y).speed_mod:
                speed_up_sound.rewind()
                speed_up_sound.play()
            if self.speed_mod > grid.get_item(self.x,self.y).speed_mod:
                speed_down_sound.rewind()
                speed_down_sound.play()
            self.speed_mod = grid.get_item(self.x,self.y).speed_mod
            self.prev_loc = []
            if grid.get_item(self.x,self.y).is_bouncy():
                bounce_blue_sound.rewind()
                bounce_blue_sound.play()
                self.z_vel = 1200
            else:  
                beep_sound.rewind()
                beep_sound.play()
                self.z_vel = 800
       
    def forward(self, dt):
        if self.z > -100:
            self.y += self.speed * dt * math.cos(self.angle_xy) * self.speed_mod
            self.x += self.speed * dt * math.sin(self.angle_xy) * self.speed_mod
        
    def left(self, dt):
        if self.z > -100:
            self.x -= self.speed * dt * math.cos(self.angle_xy) * self.speed_mod
            self.y += self.speed * dt * math.sin(self.angle_xy) * self.speed_mod
        
    def right(self, dt):
        if self.z > -100:
            self.x += self.speed * dt * math.cos(self.angle_xy) * self.speed_mod
            self.y -= self.speed * dt * math.sin(self.angle_xy) * self.speed_mod
       
    def back(self, dt):
        if self.z > -100:
            self.y -= self.speed * dt * math.cos(self.angle_xy) * self.speed_mod
            self.x -= self.speed * dt * math.sin(self.angle_xy) * self.speed_mod
        
    def shadow(self, r):
        points = []
        n = 10
        angle = 0
        shawdow_height = grid.grid_height(self.x,self.y)
        if shawdow_height >= self.z-self.radius*2:
            return None
        for i in range(0,n):
            points.append(WorldPoint(self.x+r*math.cos(angle),self.y+r*math.sin(angle),grid.grid_height(self.x,self.y)))
            angle+=(math.pi*2)/n
        return WorldPoly(points, 0, 0, 0, 0.12,0)

class GridSquare:
    def __init__(self, height, x, y, world_poly = None, level = 0):
        self.world_poly = world_poly
        self.level = level
        self.height = height
        self.prev_height = -10000
        self.sound_played = False
        self.x = x
        self.y = y
        type = 0
        if random.random() > 0.75 and math.sqrt(x**2+y**2) > 20: #if special
            type = random.randrange(1,5)
        self.bouncy = False
        if type == 1:
            self.bouncy = True
        self.direction = 0
        self.min_height = self.height-200
        self.max_height = self.height+200
        if type == 2:
            self.direction = (random.randrange(0,2)*2)-1
        self.health = None
        if type == 3:
            self.health = 100
        self.speed_mod = 1
        if type == 4:
            self.speed_mod = 1.5
        if self.world_poly is not None:
            self.world_poly.color_a = 0
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
            elif type == 4:
                self.world_poly.color_r = int(0*(0.75+self.level/4.0))
                self.world_poly.color_g = int(200*(0.75+self.level/4.0))
                self.world_poly.color_b = int(0*(0.75+self.level/4.0))
    
    def update(self, time_delta):   
        if self.world_poly is not None:  
            self.world_poly.color_a += time_delta*0.9
            if self.world_poly.color_a > 1:
                self.world_poly.color_a = 1
        if self.height <= -400:
            self.height = -1000000
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
            self.world_poly.color_r = int((255*self.health*0.01)*(0.75+self.level/4.0))
            self.world_poly.color_g = int((42*self.health*0.01)*(0.75+self.level/4.0))
            self.world_poly.color_b = int((42*self.health*0.01)*(0.75+self.level/4.0))
        if self.health <= 0:
            if not self.sound_played:
                platform_death_sound.rewind()
                platform_death_sound.play()
            self.sound_played = True
            self.direction = -5
            self.min_height = -100000
        
    def jump_damage(self):
        if self.health is not None:
            self.health -= 100
            self.health_update()
        
    def stand_damage(self, delta_time):
        if self.health is not None:
            self.health -= delta_time*300
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
                spawn = math.sqrt(x**2+y**2) < 15
                if math.sqrt(x**2+y**2) > 5 and (random.random() > 0.2 + math.sqrt(x**2+y**2)/200 or spawn):
                    if spawn:
                        level = 0
                    else:
                        level = random.randrange(0,2)
                    height = self.tile_size/4*level
                    self.objects[x][y]=GridSquare(height, x, y, WorldPoly([WorldPoint(self.tile_size/2+x*self.tile_size, self.tile_size/2+y*self.tile_size, height),
                                                 WorldPoint(-self.tile_size/2+x*self.tile_size,                self.tile_size/2+y*self.tile_size, height),
                                                 WorldPoint(-self.tile_size/2+x*self.tile_size,                -self.tile_size/2+y*self.tile_size, height), 
                                                 WorldPoint(self.tile_size/2+x*self.tile_size,  -self.tile_size/2+y*self.tile_size, height)]), level)
                else:
                    self.objects[x][y]=GridSquare(-100000, x, y)
            
    def update(self,time_delta):
        for x,y in self.x_y_range():
            self.objects[x][y].update(time_delta)
                
    def grid_height(self,x,y):
        x = round(x/self.tile_size)
        y = round(y/self.tile_size)
        if not (x,y) in self.x_y_range():
            return -10000000.00
        return self.objects[x][y].height
    
    def grid_prev_height(self,x,y):
        x = round(x/self.tile_size)
        y = round(y/self.tile_size)
        if not (x,y) in self.x_y_range():
            return -10000000.00
        return self.objects[x][y].prev_height
            
    def get_item(self,x,y):
        x = round(x/self.tile_size)
        y = round(y/self.tile_size)
        if (x,y) in self.x_y_range():
            return self.objects[x][y]
       
    def to_list(self):
        list = []
        for x,y in self.x_y_range():
            list.append(self.objects[x][y])
        return list

def render_frame(canvas):
    global game_over, left_score, right_score, random_victory_text_id, match_start_countdown,running_player
    render_objects = grid.to_list()
    render_objects.append(player_a)
    if num_players == 2:
        render_objects.append(player_b)
    render_objects.append(player_a.shadow(10))
    render_objects.append(player_a.shadow(25))
    render_objects.append(player_a.shadow(50))
    render_objects.append(player_a.shadow(75))
    if num_players == 2:
        render_objects.append(player_b.shadow(10))
        render_objects.append(player_b.shadow(25))
        render_objects.append(player_b.shadow(50))
        render_objects.append(player_b.shadow(75))
    if num_players == 2:
        right_camera.draw(canvas,render_objects)
    left_camera.draw(canvas,render_objects)
    if green_right:
        canvas.draw_polygon([[WIDTH/2, 0], [WIDTH, 0], [WIDTH, HEIGHT], [WIDTH/2, HEIGHT]], 1, "rgba(0,0,0,0)", "rgba(0,255,0,0.65)")
    if green_left:
        canvas.draw_polygon([[0, 0], [WIDTH/2, 0], [WIDTH/2, HEIGHT], [0, HEIGHT]], 1, "rgba(0,0,0,0)", "rgba(0,255,0,0.65)")
    if red_right:
        canvas.draw_polygon([[WIDTH/2, 0], [WIDTH, 0], [WIDTH, HEIGHT], [WIDTH/2, HEIGHT]], 1, "rgba(0,0,0,0)", "rgba(255,0,0,0.5)")
    if red_left:
        canvas.draw_polygon([[0, 0], [WIDTH/2, 0], [WIDTH/2, HEIGHT], [0, HEIGHT]], 1, "rgba(0,0,0,0)", "rgba(255,0,0,0.5)")
    if green_right or green_left or red_right or red_left:
        x_left = WIDTH/2-frame.get_canvas_textwidth("Click to Restart", 24, FONT)/2-12
        x_right = WIDTH/2+frame.get_canvas_textwidth("Click to Restart", 24, FONT)/2+12
        y_top = HEIGHT - 48-36
        y_bot = HEIGHT
        canvas.draw_polygon([[x_left, y_bot], [x_right, y_bot], [x_right, y_top], [x_left, y_top]], 1, "rgba(0,0,0,0)", "rgba(0,0,0,0.5)")
        canvas.draw_text("Click to Restart", (x_left+12, HEIGHT - 36), 24, 'White', FONT)
    if red_left and red_right:
        if distance_to_go() > 1000:
            text = "...Wrong way...."
        elif distance_to_go() > 666.666:
            if random_victory_text_id == 0:
                text = "Go back to candy crush"
            elif random_victory_text_id == 1:
                text = "Better luck next time"
            elif random_victory_text_id == 2:
                text = "First game?"
            elif random_victory_text_id == 3:
                text = "Winning isn't everything"
            elif random_victory_text_id == 4:
                text = "You tried"
            elif random_victory_text_id == 5:
                text = "awwww"
            elif random_victory_text_id == 6:
                text = "Mistakes were made"
            elif random_victory_text_id == 7:
                text = "No comment"
            elif random_victory_text_id == 8:
                text = "wah wah wahhh"
            else:
                text = "Die trying"
        elif distance_to_go() > 333.333:
            if random_victory_text_id == 0:
                text = "Too complicated for you?"
            elif random_victory_text_id == 1:
                text = "Nope"
            elif random_victory_text_id == 2:
                text = "Here lies skill"
            elif random_victory_text_id == 3:
                text = "Oops"
            elif random_victory_text_id == 4:
                text = "Lame"
            elif random_victory_text_id == 5:
                text = "Loser"
            elif random_victory_text_id == 6:
                text = "wow"
            elif random_victory_text_id == 7:
                text = "You're garbage"
            elif random_victory_text_id == 8:
                text = "!$%@"
            else:
                text = "Must be a glitch"
        else:
            if random_victory_text_id == 0:
                text = "Not even close"
            elif random_victory_text_id == 1:
                text = "Just give up"
            elif random_victory_text_id == 2:
                text = "You blew it"
            elif random_victory_text_id == 3:
                text = "You suck"
            elif random_victory_text_id == 4:
                text = "Nice one"
            elif random_victory_text_id == 5:
                text = "Pro top: don't fall"
            elif random_victory_text_id == 6:
                text = "Why bother trying?"
            elif random_victory_text_id == 7:
                text = "Try pressing space next time"
            elif random_victory_text_id == 8:
                text = "Amuture"
            else:
                text = "..."
        canvas.draw_text(text, (WIDTH/2-frame.get_canvas_textwidth(text, 50,FONT)/2, 150), 50,'White',FONT)
    if num_players == 2:
        current_time = time.time()
        if match_start_countdown > current_time:
            text = str(int(match_start_countdown-current_time))
            canvas.draw_text(text, (WIDTH/2-frame.get_canvas_textwidth(text, 120, FONT)/2, HEIGHT/2), 120, 'Yellow',FONT)
            if running_player == 0:
                text_left = "Runner"
                text_right = "Tagger"
            if running_player == 1:
                text_left = "Tagger"
                text_right = "Runner"
            canvas.draw_text(text_left, (WIDTH/4-frame.get_canvas_textwidth(text_left, 40, FONT)/2, HEIGHT/8), 40, 'White',FONT)
            canvas.draw_text(text_right, (3*WIDTH/4-frame.get_canvas_textwidth(text_right, 40, FONT)/2, HEIGHT/8), 40, 'White',FONT)
        canvas.draw_text(str(left_score), (30, 30), 24, 'White', FONT)
        canvas.draw_text(str(right_score), (WIDTH-30, 30), 24, 'White', FONT)
    else:
        if time_end is not None:
            time_str = str(int((time_end-time_start)*10)/10.0)
        else:
            time_str = str(int((time.time()-time_start)*10)/10.0)  
        if distance_to_go() > 0:
            canvas.draw_text("Distance", (0, 25), 24, 'White',FONT)
            canvas.draw_text(str(distance_to_go()), (0, 53), 36, 'White',FONT)
            if highscore != 10000000:
                canvas.draw_text("Best Time", (WIDTH/2-frame.get_canvas_textwidth("Best Time", 12, FONT)/2, 14), 12, 'White',FONT)
                canvas.draw_text(str(int(highscore*10)/10.0), (WIDTH/2-frame.get_canvas_textwidth(str(int(highscore*10)/10.0), 24, FONT)/2, 38), 24, 'White',FONT)
            canvas.draw_text("Time", (1140, 25), 24, 'White',FONT)
            canvas.draw_text(time_str, (1200-frame.get_canvas_textwidth(time_str, 36, FONT), 53), 36, 'White',FONT)
        else:
            if highscore == time_end-time_start:
                text = "New Record!"
            else:
                if random_victory_text_id == 0:
                    text = "You made it!"
                elif random_victory_text_id == 1:
                    text = "Not quite record worthy!"
                elif random_victory_text_id == 2:
                    text = "You didn't die!"
                elif random_victory_text_id == 3:
                    text = "Pretty good considering!"
                elif random_victory_text_id == 4:
                    text = "Better late then never!"
                elif random_victory_text_id == 5:
                    text = "Close enough!"
                elif random_victory_text_id == 6:
                    text = "A little on the slow side"
                elif random_victory_text_id == 7:
                    text = "New Record! Not."
                elif random_victory_text_id == 8:
                    text = "Adequate!"
                else:
                    text = "Ok!"
                canvas.draw_text("Best Time", (WIDTH/2-frame.get_canvas_textwidth("Best Time", 12, FONT)/2, HEIGHT/2+100), 12, 'White',FONT)
                canvas.draw_text(str(int(highscore*10)/10.0), (WIDTH/2-frame.get_canvas_textwidth(str(int(highscore*10)/10.0), 24, FONT)/2, HEIGHT/2+126), 24, 'White',FONT)
            canvas.draw_text(text, (WIDTH/2-frame.get_canvas_textwidth(text, 72, FONT)/2, 100), 72, 'White',FONT)
            canvas.draw_text("Time:", (WIDTH/2-frame.get_canvas_textwidth("Time:", 30, FONT)/2, HEIGHT/2-90), 30, 'White',FONT)
            canvas.draw_text(time_str, (WIDTH/2-frame.get_canvas_textwidth(time_str, 84, FONT)/2, HEIGHT/2), 84, 'White',FONT)
             
def distance_to_go():    
    return int(1000-(math.sqrt( player_a.x**2 + player_a.y**2)-math.sqrt(2)*2500 )/50)-20
      
def update_world_always(time_delta):
    global pause, match_start_countdown
    if num_players == 2:
        if pause and match_start_countdown is not None and match_start_countdown < time.time():
            pause = False
            match_start_countdown = None
        dx = player_b.x-player_a.x
        dy = player_b.y-player_a.y
        dz = player_b.z-player_a.z
        L = math.sqrt( dx**2 + dy**2 + dz**2 )
        if running_player == 0:
            grid.set_center(player_a[0], player_a[1])
        else:
            grid.set_center(player_b[0], player_b[1])
    else:
        angle_temp = WorldAngle.angleBetweenWorldPoints(player_a, WorldPoint(0,0,0))+math.pi
        grid.set_center(player_a[0]+math.cos(angle_temp)*600, player_a[1]+math.sin(angle_temp)*600)
        
def update_world(time_delta):
    global left_score,right_score,running_player,pause,match_start_countdown,pause
    grid.update(time_delta)
    player_a.update(time_delta)
    if num_players == 2:
        player_b.update(time_delta)
    if num_players == 2:
        dx = player_b.x-player_a.x
        dy = player_b.y-player_a.y
        dz = player_b.z-player_a.z
        L = math.sqrt( dx**2 + dy**2 + dz**2 )
        l = 1000
        if player_b.z < -12000:
            left_score += 1
            end_multi(1,0)
            return
        if player_a.z < -12000:
            right_score += 1
            end_multi(0,1)
            return
        if  L < 100:
            if running_player == 0:
                right_score += 1
                end_multi(0,1)
            else:
                left_score += 1
                end_multi(1,0)
            return
        angle_a = WorldAngle.angleBetweenWorldPoints(player_a, WorldPoint(0,0,0))+math.pi
        angle_b = WorldAngle.angleBetweenWorldPoints(player_b, WorldPoint(0,0,0))+math.pi
        player_a.set_angle_xy(math.pi/2-angle_a)
        player_b.set_angle_xy(math.pi/2-angle_b)
        left_camera.set_angle_xy(player_a.angle_xy)
        right_camera.set_angle_xy(player_b.angle_xy)
        left_camera.set_pos(player_a.x - math.cos(angle_a)*l, player_a.y - math.sin(angle_a)*l - l/4, 500+player_a.z)
        right_camera.set_pos(player_b.x - math.cos(angle_b)*l, player_b.y - math.sin(angle_b)*l - l/4, 500+player_b.z)
    else:
        if player_a.z < -12000 or distance_to_go() <= 0:
            end_single()
            return
        angle_a = WorldAngle.angleBetweenWorldPoints(player_a, WorldPoint(0,0,0))+math.pi
        player_a.set_angle_xy(math.pi/2-angle_a)
        left_camera.set_angle_xy(player_a.angle_xy)
        l = 1000
        left_camera.set_pos(player_a.x - math.cos(angle_a)*l, player_a.y - math.sin(angle_a)*l - l/4, 500+player_a.z)
        
def keydown(k):
    global keys_down
    keys_down[k] = True
    if not pause and k == BUTTON_PLAYER_A_JUMP:
        player_a.jump()
    if k == BUTTON_ESCAPE: #escape
        init_menu()
    if not pause and keys_down[45] or keys_down[16] and num_players == 2:
        player_b.jump()

def keyup(k):
    global keys_down
    keys_down[k] = False
            
def key_action(dt):    
    if keys_down[45]:
        if num_players == 2:
            player_b.jump()
        else:
            player_a.jump()
    if keys_down[BUTTON_PLAYER_A_JUMP]:
        player_a.jump()
    if keys_down[BUTTON_PLAYER_B_UP] and num_players == 2:
        player_b.forward(dt)
    if keys_down[BUTTON_PLAYER_B_DOWN] and num_players == 2:
        player_b.back(dt)
    if keys_down[BUTTON_PLAYER_B_LEFT] and num_players == 2:
        player_b.left(dt)
    if keys_down[BUTTON_PLAYER_B_RIGHT] and num_players == 2:
        player_b.right(dt)
    if keys_down[BUTTON_PLAYER_A_DOWN]:
        player_a.back(dt)
    if keys_down[BUTTON_PLAYER_A_LEFT]:
        player_a.left(dt)
    if keys_down[BUTTON_PLAYER_A_RIGHT]:
        player_a.right(dt)
    if keys_down[BUTTON_PLAYER_A_UP]:
         player_a.forward(dt)

def game_loop(canvas):
    global count, prev_time,music_restart_time, pause
    dt = time.time() - prev_time
    prev_time = time.time()
    if not pause and prev_time > music_restart_time:
        game_music_intro.rewind()
        game_music.rewind()
        game_music.play()
        music_restart_time = prev_time + 42.6634
    update_world_always(dt)
    if not pause:
        update_world(dt)
    render_frame(canvas)
    if not pause:
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
        fps= 1/avg_time
        if FPS_PRINT:
            print "FPS: " + str(int(10/avg_time)/10)
            print "GRID SIZE: " + str(grid.square_size**2)
        if fps > 20:
            grid.square_size += 1
        elif fps < 15:
            if grid.square_size > 6:
                grid.square_size -= 1
            else:
                print "Warning: This computer is too slow!"
    
def init():
    global player_a, player_b, grid, left_camera, right_camera, music_restart_time, green_right, green_left, red_right, red_left
    green_right = False
    green_left = False
    red_right = False
    red_left = False
    victory_sound.rewind()
    menu_music.rewind()
    game_music_intro.rewind()
    game_music.rewind()
    game_music_intro.play()
    music_restart_time = time.time() + 125.478
    frame.set_draw_handler(game_loop)
    frame.set_keydown_handler(keydown)
    frame.set_keyup_handler(keyup)
    frame.set_mouseclick_handler(pass_function)
    frame.set_mousedrag_handler(pass_function)
    grid = Grid()
    if num_players == 2:
        player_a = WorldPlayer(3000, 3000, 255, 0, 0)
        player_b = WorldPlayer(2500, 2500, 0, 255, 0)
        if running_player == 1:
            temp = player_b
            player_b = player_a
            player_a = temp
    else:
        random_angle = random.random()*2*math.pi
        player_a = WorldPlayer(2500.0*math.cos(random_angle), 2500.0*math.sin(random_angle), 255, 0, 0)
    if num_players == 2:
        left_camera = Camera(0,0,0,  0,     0,       0,      WIDTH/2,      HEIGHT, False, True, False, False)
        right_camera = Camera(0,0,0,  0 , WIDTH/2 , 0,     WIDTH/2,      HEIGHT, True, False, False, False)
    elif num_players == 1:
        left_camera = Camera(0,0,0,  0,     0,       0,      WIDTH,      HEIGHT, False, False, False, False)
        
def init_single():
    global num_players,time_start,random_victory_text_id,time_end,pause
    pause = False
    time_start = time.time()
    time_end = None
    random_victory_text_id = random.randrange(0,10)
    num_players = 1
    init()

def init_multi():
    global num_players, running_player,pause,match_start_countdown,next_runner
    pause = False
    if next_runner == None:
        running_player = random.randrange(0,2)
    else:
        running_player = next_runner
        next_runner = None
    num_players = 2
    init()
    update_world(0)
    pause = True
    match_start_countdown = time.time()+4

def pass_function(x=None):
    pass

def menu_mouseclick(pos):
    global how_to_play_pressed, chase_mode_pressed, time_trial_pressed, TWO_PLAYER_ENABLED
    how_to_play_pressed = False
    chase_mode_pressed = False
    time_trial_pressed = False
    if pos[0] > 2*WIDTH/7-100-150 and pos[0] < 2*WIDTH/7-100+150 and pos[1] > HEIGHT-100-75 and pos[1] < HEIGHT-100+75:
        init_help() 
    if TWO_PLAYER_ENABLED and pos[0] > 4*WIDTH/7-100-150 and pos[0] < 4*WIDTH/7-100+150 and pos[1] > HEIGHT-100-75 and pos[1] < HEIGHT-100+75:
        init_multi()
    if pos[0] > 6*WIDTH/7-100-150 and pos[0] < 6*WIDTH/7-100+150 and pos[1] > HEIGHT-100-75 and pos[1] < HEIGHT-100+75:
        init_single()

def menu_mousedrag(pos):
    global how_to_play_pressed, chase_mode_pressed, time_trial_pressed
    how_to_play_pressed = False
    chase_mode_pressed = False
    time_trial_pressed = False
    if pos[0] > 2*WIDTH/7-100-150 and pos[0] < 2*WIDTH/7-100+150 and pos[1] > HEIGHT-100-75 and pos[1] < HEIGHT-100+75:
        how_to_play_pressed = True
    if pos[0] > 4*WIDTH/7-100-150 and pos[0] < 4*WIDTH/7-100+150 and pos[1] > HEIGHT-100-75 and pos[1] < HEIGHT-100+75:
        chase_mode_pressed = True
    if pos[0] > 6*WIDTH/7-100-150 and pos[0] < 6*WIDTH/7-100+150 and pos[1] > HEIGHT-100-75 and pos[1] < HEIGHT-100+75:
        time_trial_pressed = True
    
def help_draw(canvas):
    canvas.draw_image(how_to_play_menu_image, (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT), (WIDTH/2, HEIGHT/2), (WIDTH, HEIGHT))
    
def init_help():
    frame.set_draw_handler(help_draw)
    frame.set_keydown_handler(init_menu)
    frame.set_keyup_handler(init_menu)
    frame.set_mouseclick_handler(init_menu)
    frame.set_mousedrag_handler(init_menu)
    
def init_menu(dummy = None):
    global how_to_play_pressed, chase_mode_pressed, time_trial_pressed, left_score, right_score
    left_score = 0
    right_score = 0
    how_to_play_pressed = False
    chase_mode_pressed = False
    time_trial_pressed = False
    frame.set_keydown_handler(pass_function)
    frame.set_keyup_handler(pass_function)
    frame.set_draw_handler(menu_handler)
    frame.set_mouseclick_handler(menu_mouseclick)
    frame.set_mousedrag_handler(menu_mousedrag)
    bounce_blue_sound.rewind()
    beep_sound.rewind()
    falling_sound.rewind()
    platform_death_sound.rewind()
    menu_music.play()
    game_music.rewind()
    game_music_intro.rewind()
    
def end_multi(player_a_score, player_b_score):
    global pause, green_right, green_left, red_right, red_left, next_runner
    if player_a_score == 1:
        next_runner = 1
    else:
        next_runner = 0
    if player_a_score == 1:
        green_left = True
    else:
        red_left = True
    if player_b_score == 1:
        green_right = True
    else:
        red_right = True
    pause = True
    frame.set_mouseclick_handler(click_multi_reset)

def end_single():
    global pause, green_right, green_left, red_right, red_left,time_end, highscore
    game_music.rewind()
    game_music_intro.rewind()
    if time_end is None:
        time_end = time.time()
    if distance_to_go() <= 0:
        victory_sound.play()
        if time_end-time_start < highscore:
            highscore = time_end-time_start  
        green_left = True
        green_right = True
    else:
        red_left = True
        red_right = True
    pause = True
    frame.set_mouseclick_handler(click_single_reset)

def click_multi_reset(pos):
    init_multi()
    
def click_single_reset(pos):
    init_single()
    
def menu_handler(canvas):
    global background_menu_image, background_rotation, how_to_play_pressed, chase_mode_pressed, time_trial_pressed, TWO_PLAYER_ENABLED
    background_rotation += 0.001
    canvas.draw_image(background_menu_image, ( 705/2, 718/2), ( 705, 718), (WIDTH/2, HEIGHT/2), (HEIGHT*2.5,2.5*HEIGHT), background_rotation)
    canvas.draw_polygon([[150, 25], [WIDTH-150, 25], [WIDTH-150, HEIGHT-425], [150, HEIGHT-425]], 12, "rgba(255,0,0,0)", "rgba(0,0,0,0.5)")
    canvas.draw_polygon([[150, HEIGHT-425], [WIDTH-150, HEIGHT-425], [WIDTH-150, HEIGHT-375], [150, HEIGHT-375]], 12, "rgba(255,0,0,0)", "rgba(255,255,255,0.5)")
    canvas.draw_image(logo_image, ( 1634/2, 266/2), ( 1634, 266), (WIDTH/2, HEIGHT/6), (1634/2,266/2))
    canvas.draw_image(subtitle_image, ( 1733/2, 80/2), ( 1733, 80), (WIDTH/2, HEIGHT/3), (1733/2,80/2))
    if not how_to_play_pressed:
        canvas.draw_image(how_to_play_image, ( 695/2, 168/2), ( 695, 168), (2*WIDTH/7-100,HEIGHT-100), (300,150))
    else:
        canvas.draw_image(how_to_play_image_down, ( 695/2, 168/2), ( 695, 168), (2*WIDTH/7-100,HEIGHT-100), (300,150))
    if TWO_PLAYER_ENABLED:
        if not chase_mode_pressed:    
            canvas.draw_image(chase_mode_image, ( 655/2, 168/2), ( 655, 168), (4*WIDTH/7-100,HEIGHT-100), (300,150))
        else:
            canvas.draw_image(chase_mode_image_down, ( 655/2, 168/2), ( 655, 168), (4*WIDTH/7-100,HEIGHT-100), (300,150))
    if not time_trial_pressed:
        canvas.draw_image(time_trial_image, ( 593/2, 168/2), ( 593, 168), (6*WIDTH/7-100,HEIGHT-100), (300,150))
    else:
        canvas.draw_image(time_trial_image_down, ( 593/2, 168/2), ( 593, 168), (6*WIDTH/7-100,HEIGHT-100), (300,150))

def loading_handler(canvas):
    global blinker_counter
    blinker_counter+=1
    if blinker_counter == 12*5:
        blinker_counter = 0
    if time.time()-loading_time > 2 or time_trial_image_down.get_height() != 0:
        canvas.draw_image(loading_image, ( 600/2, 400/2), ( 600, 400), (WIDTH/2,HEIGHT/2), (WIDTH,HEIGHT))
        canvas.draw_image(loading_animation[10-blinker_counter/5], ( 400/2, 300/2), ( 400, 300), (WIDTH/2,HEIGHT/2), (400,300))
        canvas.draw_image(loading_animation[10-blinker_counter/5-1], ( 400/2, 300/2), ( 400, 300), (WIDTH/2,HEIGHT/2), (400,300))
        canvas.draw_image(loading_animation[10-blinker_counter/5-2], ( 400/2, 300/2), ( 400, 300), (WIDTH/2,HEIGHT/2), (400,300))
    loading_text = ""
    if time.time()-loading_time < 5:
        loading_text = "Loading..."
    elif time.time()-loading_time > 10 and time.time()-loading_time < 15:
        loading_text = "Still loading..."
    elif time.time()-loading_time > 20 and time.time()-loading_time < 25:
        loading_text = "Making everything perfect..."
    elif time.time()-loading_time > 30 and time.time()-loading_time < 35:
        loading_text = "Clipping polygons..."
    elif time.time()-loading_time > 40 and time.time()-loading_time < 45:
        loading_text = "Raising the volume..."
    elif time.time()-loading_time > 50 and time.time()-loading_time < 55:
        loading_text = "Thinking about how you will die..."
    elif time.time()-loading_time > 60 and time.time()-loading_time < 65:
        loading_text = "The wait will be worth it..."
    elif time.time()-loading_time > 70 and time.time()-loading_time < 75:
        loading_text = "Browsers arn't very fast..."
    elif time.time()-loading_time > 80 and time.time()-loading_time < 85:
        loading_text = "Almost there..."
    elif time.time()-loading_time > 90:
        loading_text = "Sorry, this is taking awhile..."
    canvas.draw_text(loading_text, (WIDTH/2-frame.get_canvas_textwidth(loading_text, 30,FONT)/2, HEIGHT-150), 30,'White',FONT)
    if time.time()-loading_time > 2 and time_trial_image_down.get_height() != 0:
        init_menu()
        
frame.set_draw_handler(loading_handler)
frame.start()
