#TODO:
'''
stars instead of balls
background
music

'''

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

loading_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/loading.png")
loading_blank_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/loading_blank.png")

import math
import random
import time
import user40_sh0DNBiS2W_88 as DrawEngine
import codeskulptor
    
    
    
class WorldPlayer(DrawEngine.WorldSphere, DrawEngine.WorldAngle):
    def __init__(self,x,y,r,b,g):
        DrawEngine.WorldSphere.__init__(self, x, y, 600, 30, r,g,b,1)
        DrawEngine.WorldAngle.__init__(self, 0)
        self.z_vel = 20
        self.radius = 30
        self.speed = 800
        
        self.prev_loc = []
        
    def get_prev_loc(self):
        i = 0
        while i < len(self.prev_loc)-1 and self.prev_loc[i][3] < 0.3:
            i+=1
        return self.prev_loc[i]
        
    def update(self, time_delta):
        global grid,time_end
        
        if self.z < -200:
            game_music.rewind()
            game_music_intro.rewind()
            if time_end is None:
                time_end = time.time()
            falling_sound.play()
        
        for item in self.prev_loc:
            item[3] += time_delta
        self.prev_loc.append([self.x, self.y, self.z, time_delta])
        while len(self.prev_loc) > 0 and self.prev_loc[0][3] > 0.3:
            self.prev_loc.pop(0)
        
        ground_z = grid.grid_height(self.x,self.y)+self.radius
        
        
        moving_ground_z = grid.grid_prev_height(self.x,self.y)+self.radius
        
        if self.z_vel >= 0: #if going up
             self.z += self.z_vel*time_delta
        elif self.z == ground_z or self.z == moving_ground_z: #if sitting on ground
            self.z = ground_z
            grid.get_item(self.x,self.y).stand_damage(time_delta)
            self.z_vel = 0
        elif self.z >= ground_z and self.z + self.z_vel*time_delta < ground_z: #if falling into ground
            self.z = ground_z
            if grid.get_item(self.x,self.y).is_bouncy():
                bounce_blue_sound.rewind()
                bounce_blue_sound.play()
                self.z_vel = 1200
            else:
                self.z_vel = 0
        elif self.z < ground_z and self.z + self.radius*3 > ground_z:
            self.z = ground_z
            grid.get_item(self.x,self.y).stand_damage(time_delta)
            self.z_vel = 0
        else:#else falling into space
            self.z += self.z_vel*time_delta
        
        self.z_vel -= 1200*time_delta
        
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
            self.y += self.speed * dt * math.cos(self.angle_xy)
            self.x += self.speed * dt * math.sin(self.angle_xy)
        
    def left(self, dt):
        if self.z > -100:
            self.x -= self.speed * dt * math.cos(self.angle_xy)
            self.y += self.speed * dt * math.sin(self.angle_xy)
        
    def right(self, dt):
        if self.z > -100:
            self.x += self.speed * dt * math.cos(self.angle_xy)
            self.y -= self.speed * dt * math.sin(self.angle_xy)
       
    def back(self, dt):
        if self.z > -100:
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
    def __init__(self, height, x, y, world_poly = None, level = 0):
        self.world_poly = world_poly
        
        self.level = level
        
        self.height = height
        self.prev_height = -10000
        
        #types of squares:
        #0 - normal
        #1 - bouncy
        #2 - up/down
        #3 - disapear
        
        self.x = x
        self.y = y
        
        
        type = 0
        if random.random() > 0.75 and math.sqrt(x**2+y**2) > 20: #if special
            type = random.randrange(1,4)
        
        self.bouncy = False
        if type == 1:
            self.bouncy = True
         
        self.direction = 0
        self.min_height = self.height-200
        self.max_height = self.height+200
        if type == 2:
            self.direction = (random.randrange(0,2)*2)-1 #-1 or 1
        
        self.health = None
        if type == 3:
            self.health = 100
        
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
    
    def update(self, time_delta):   
        
              
        if self.world_poly is not None:  
            self.world_poly.color_a += time_delta*0.9
            if self.world_poly.color_a > 1:
                self.world_poly.color_a = 1
        
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
            platform_death_sound.play()
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
                    self.objects[x][y]=GridSquare(height, x, y, DrawEngine.WorldPoly([DrawEngine.WorldPoint(self.tile_size/2+x*self.tile_size, self.tile_size/2+y*self.tile_size, height),
                                                 DrawEngine.WorldPoint(-self.tile_size/2+x*self.tile_size,                self.tile_size/2+y*self.tile_size, height),
                                                 DrawEngine.WorldPoint(-self.tile_size/2+x*self.tile_size,                -self.tile_size/2+y*self.tile_size, height), 
                                                 DrawEngine.WorldPoint(self.tile_size/2+x*self.tile_size,  -self.tile_size/2+y*self.tile_size, height)]), level)
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
    global game_over, left_score, right_score, random_victory_text_id

    render_objects = grid.to_list()
    render_objects.append(player_a)
    if num_players == 2:
        render_objects.append(player_b)
    render_objects.append(player_a.shadow())
    if num_players == 2:
        render_objects.append(player_b.shadow())
    
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
        x_left = WIDTH/2-frame.get_canvas_textwidth("Click to Restart", 24, "monospace")/2-12
        x_right = WIDTH/2+frame.get_canvas_textwidth("Click to Restart", 24, "monospace")/2+12
        y_top = HEIGHT - 48-36
        y_bot = HEIGHT
        canvas.draw_polygon([[x_left, y_bot], [x_right, y_bot], [x_right, y_top], [x_left, y_top]], 1, "rgba(0,0,0,0)", "rgba(0,0,0,0.5)")
        canvas.draw_text("Click to Restart", (x_left+12, HEIGHT - 36), 24, 'White', "monospace")
        
    if red_left and red_right:
        if distance_to_go() > 666.666:
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
        canvas.draw_text(text, (WIDTH/2-frame.get_canvas_textwidth(text, 50,"monospace")/2, 150), 50,'White',"monospace")
            
        
    if num_players == 2:
        canvas.draw_text(str(left_score), (30, 30), 24, 'White', "monospace")
        canvas.draw_text(str(right_score), (WIDTH-30, 30), 24, 'White', "monospace")
    else:
        if time_end is not None:
            time_str = str(int((time_end-time_start)*10)/10.0)
        else:
            time_str = str(int((time.time()-time_start)*10)/10.0)  
        if distance_to_go() > 0:
            canvas.draw_text("Distance", (0, 25), 24, 'White',"monospace")
            canvas.draw_text(str(distance_to_go()), (0, 53), 36, 'White',"monospace")
   
            if highscore != 10000000:
                canvas.draw_text("Best Time", (WIDTH/2-frame.get_canvas_textwidth("Best Time", 12, "monospace")/2, 14), 12, 'White',"monospace")
                canvas.draw_text(str(int(highscore*10)/10.0), (WIDTH/2-frame.get_canvas_textwidth(str(int(highscore*10)/10.0), 24, "monospace")/2, 38), 24, 'White',"monospace")

            canvas.draw_text("Time", (1140, 25), 24, 'White',"monospace")
            canvas.draw_text(time_str, (1200-frame.get_canvas_textwidth(time_str, 36, "monospace"), 53), 36, 'White',"monospace")
            
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
                    
                canvas.draw_text("Best Time", (WIDTH/2-frame.get_canvas_textwidth("Best Time", 12, "monospace")/2, HEIGHT/2+100), 12, 'White',"monospace")
                canvas.draw_text(str(int(highscore*10)/10.0), (WIDTH/2-frame.get_canvas_textwidth(str(int(highscore*10)/10.0), 24, "monospace")/2, HEIGHT/2+126), 24, 'White',"monospace")

            canvas.draw_text(text, (WIDTH/2-frame.get_canvas_textwidth(text, 72, "monospace")/2, 100), 72, 'White',"monospace")
            canvas.draw_text("Time:", (WIDTH/2-frame.get_canvas_textwidth("Time:", 30, "monospace")/2, HEIGHT/2-90), 30, 'White',"monospace")
            canvas.draw_text(time_str, (WIDTH/2-frame.get_canvas_textwidth(time_str, 84, "monospace")/2, HEIGHT/2), 84, 'White',"monospace")
           
            
def distance_to_go():    
    return int(1000-(math.sqrt( player_a.x**2 + player_a.y**2)-math.sqrt(2)*2500 )/50)-20
    #return int(10-(math.sqrt( player_a.x**2 + player_a.y**2)-math.sqrt(2)*2500 )/50)
             
def update_world(time_delta):
    global left_score,right_score,running_player
    
    if num_players == 2:
    
        dx = player_b.x-player_a.x
        dy = player_b.y-player_a.y
        dz = player_b.z-player_a.z
        L = math.sqrt( dx**2 + dy**2 + dz**2 )
        
        #angle_temp = DrawEngine.WorldAngle.angleBetweenWorldPoints(player_a, player_b)+math.pi
        #grid.set_center(player_b[0]+math.cos(angle_temp)*0.666*L, player_b[1]+math.sin(angle_temp)*0.666*L)
        
        if running_player == 0:
            grid.set_center(player_a[0], player_a[1])
        else:
            grid.set_center(player_b[0], player_b[1])
    else:
        angle_temp = DrawEngine.WorldAngle.angleBetweenWorldPoints(player_a, DrawEngine.WorldPoint(0,0,0))+math.pi
        
        
        grid.set_center(player_a[0]+math.cos(angle_temp)*600, player_a[1]+math.sin(angle_temp)*600)
        
    grid.update(time_delta)
    
    
    player_a.update(time_delta)
    if num_players == 2:
        player_b.update(time_delta)
    
    
    if num_players == 2:
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
            if running_player == 1:
                right_score += 1
                end_multi(0,1)
            else:
                left_score += 1
                end_multi(1,0)
            return
    
        angle_a = DrawEngine.WorldAngle.angleBetweenWorldPoints(player_a, DrawEngine.WorldPoint(0,0,0))+math.pi
        angle_b = DrawEngine.WorldAngle.angleBetweenWorldPoints(player_b, DrawEngine.WorldPoint(0,0,0))+math.pi

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
            
        angle_a = DrawEngine.WorldAngle.angleBetweenWorldPoints(player_a, DrawEngine.WorldPoint(0,0,0))+math.pi
        player_a.set_angle_xy(math.pi/2-angle_a)
        left_camera.set_angle_xy(player_a.angle_xy)
        l = 1000
        left_camera.set_pos(player_a.x - math.cos(angle_a)*l, player_a.y - math.sin(angle_a)*l - l/4, 500+player_a.z)
        
        
keys_down = {}
for i in range(1,300):
    keys_down[i] = False
    
def keydown(k):
    global keys_down
    keys_down[k] = True
    
    if not pause and k == simplegui.KEY_MAP["space"]:
        player_a.jump()
        
    if k == 27: #escape
        init_menu()
        
    if not pause and keys_down[45] or keys_down[16]:
        if num_players == 2:
            player_b.jump()
        else:
            player_a.jump()

def keyup(k):
    global keys_down
    keys_down[k] = False
            
def key_action(dt):    
    
    if keys_down[45] or keys_down[16] and num_players == 2:
        if num_players == 2:
            player_b.jump()
        else:
            player_a.jump()
            
    if keys_down[simplegui.KEY_MAP["space"]]:
        player_a.jump()
        
    if keys_down[simplegui.KEY_MAP["up"]] and num_players == 2:
        player_b.forward(dt)
    if keys_down[simplegui.KEY_MAP["down"]] and num_players == 2:
        player_b.back(dt)
    if keys_down[simplegui.KEY_MAP["left"]] and num_players == 2:
        player_b.left(dt)
    if keys_down[simplegui.KEY_MAP["right"]] and num_players == 2:
        player_b.right(dt)
        
    
    if keys_down[simplegui.KEY_MAP["s"]] or keys_down[simplegui.KEY_MAP["down"]] and num_players == 1:
        player_a.back(dt)
    if keys_down[simplegui.KEY_MAP["a"]] or keys_down[simplegui.KEY_MAP["left"]] and num_players == 1:
        player_a.left(dt)
    if keys_down[simplegui.KEY_MAP["d"]] or keys_down[simplegui.KEY_MAP["right"]] and num_players == 1:
        player_a.right(dt)
    if keys_down[simplegui.KEY_MAP["w"]] or keys_down[simplegui.KEY_MAP["up"]] and num_players == 1:
         player_a.forward(dt)

        
time_list = []
count = 0
prev_time = time.time()
    
def game_loop(canvas):
    global count, prev_time,music_restart_time, pause
    dt = time.time() - prev_time
    prev_time = time.time()
    
    #handle music
    if not pause and prev_time > music_restart_time:
        game_music_intro.rewind()
        game_music.rewind()
        game_music.play()
        music_restart_time = prev_time + 42.6634
        
    ##main Stuff
    if not pause:
        update_world(dt)
    render_frame(canvas)
    if not pause:
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
        if fps > 20:
            grid.square_size += 1
        elif fps < 15:
            if grid.square_size > 6:
                grid.square_size -= 1
            else:
                print "Warning: This computer is too slow!"
                

WIDTH = 1200
HEIGHT = 600

num_players = 2

highscore = 10000000 #80.7 is avery's highscore

left_score = 0
right_score = 0
    
    
def init():
    global player_a, player_b, grid, left_camera, right_camera, music_restart_time, pause, green_right, green_left, red_right, red_left

    pause = False
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
        left_camera = DrawEngine.Camera(0,0,0,  0,     0,       0,      WIDTH/2,      HEIGHT, False, True, False, False)
        right_camera = DrawEngine.Camera(0,0,0,  0 , WIDTH/2 , 0,     WIDTH/2,      HEIGHT, True, False, False, False)
    elif num_players == 1:
        left_camera = DrawEngine.Camera(0,0,0,  0,     0,       0,      WIDTH,      HEIGHT, False, False, False, False)
        
    
def init_single():
    global num_players,time_start,random_victory_text_id,time_end
    
    time_start = time.time()
    time_end = None
    random_victory_text_id = random.randrange(0,10)
    
    num_players = 1
    init()

def init_multi():
    global num_players, running_player
    
    running_player = random.randrange(0,2)
    num_players = 2
    init()
    
logo_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/logo.png")
background_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/background_round.png")
subtitle_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/subtitle.png")
 
    
how_to_play_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/how_to_play.png")
chase_mode_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/chase_mode.png")
time_trial_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/time_trial.png")

how_to_play_image_down = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/how_to_play_pressed.png")
chase_mode_image_down = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/chase_mode_pressed.png")
time_trial_image_down = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/time_trial_pressed.png")

r = 0   

def pass_function(x=None):
    pass

def menu_mouseclick(pos):
    global how_to_play_pressed, chase_mode_pressed, time_trial_pressed
    
    how_to_play_pressed = False
    chase_mode_pressed = False
    time_trial_pressed = False
    
    if pos[0] > 2*WIDTH/7-100-150 and pos[0] < 2*WIDTH/7-100+150 and pos[1] > HEIGHT-100-75 and pos[1] < HEIGHT-100+75:
        print "this feature is not yet implamented!"
        init_help() 
    if pos[0] > 4*WIDTH/7-100-150 and pos[0] < 4*WIDTH/7-100+150 and pos[1] > HEIGHT-100-75 and pos[1] < HEIGHT-100+75:
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
    
def init_menu():
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
    global pause, green_right, green_left, red_right, red_left
    
    
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
    #init_multi()


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
    pass

def click_multi_reset(pos):
    init_multi()
    
def click_single_reset(pos):
    init_single()
    
def menu_handler(canvas):
    global background_image, r, how_to_play_pressed, chase_mode_pressed, time_trial_pressed
    r += 0.001
    
   
    canvas.draw_image(background_image, ( 705/2, 718/2), ( 705, 718), (WIDTH/2, HEIGHT/2), (HEIGHT*2.5,2.5*HEIGHT), r)
    canvas.draw_polygon([[150, 25], [WIDTH-150, 25], [WIDTH-150, HEIGHT-425], [150, HEIGHT-425]], 12, "rgba(255,0,0,0)", "rgba(0,0,0,0.5)")
    canvas.draw_polygon([[150, HEIGHT-425], [WIDTH-150, HEIGHT-425], [WIDTH-150, HEIGHT-375], [150, HEIGHT-375]], 12, "rgba(255,0,0,0)", "rgba(255,255,255,0.5)")
    canvas.draw_image(logo_image, ( 1634/2, 266/2), ( 1634, 266), (WIDTH/2, HEIGHT/6), (1634/2,266/2))
    canvas.draw_image(subtitle_image, ( 1733/2, 80/2), ( 1733, 80), (WIDTH/2, HEIGHT/3), (1733/2,80/2))
     
    
    
    if not how_to_play_pressed:
        canvas.draw_image(how_to_play_image, ( 695/2, 168/2), ( 695, 168), (2*WIDTH/7-100,HEIGHT-100), (300,150))
    else:
        canvas.draw_image(how_to_play_image_down, ( 695/2, 168/2), ( 695, 168), (2*WIDTH/7-100,HEIGHT-100), (300,150))
    
    if not chase_mode_pressed:    
        canvas.draw_image(chase_mode_image, ( 655/2, 168/2), ( 655, 168), (4*WIDTH/7-100,HEIGHT-100), (300,150))
    else:
        canvas.draw_image(chase_mode_image_down, ( 655/2, 168/2), ( 655, 168), (4*WIDTH/7-100,HEIGHT-100), (300,150))
     
    if not time_trial_pressed:
        canvas.draw_image(time_trial_image, ( 593/2, 168/2), ( 593, 168), (6*WIDTH/7-100,HEIGHT-100), (300,150))
    else:
        canvas.draw_image(time_trial_image_down, ( 593/2, 168/2), ( 593, 168), (6*WIDTH/7-100,HEIGHT-100), (300,150))
    
    #booting
        
blinker_counter = 0
    
def loading_handler(canvas):
    global blinker_counter
    blinker_counter+=0.01
 
    if int(blinker_counter)%2==0:
        canvas.draw_image(loading_image, ( 600/2, 400/2), ( 600, 400), (WIDTH/2,HEIGHT/2), (WIDTH,HEIGHT))
    else:
        canvas.draw_image(loading_blank_image, ( 600/2, 400/2), ( 600, 400), (WIDTH/2,HEIGHT/2), (WIDTH,HEIGHT))

    
    if time_trial_image_down.get_height() != 0:
        init_menu()
        codeskulptor.set_timeout(2)

    
frame = simplegui.create_frame("~", WIDTH, HEIGHT)
frame.set_draw_handler(loading_handler)

#reset_button = frame.add_button('Multiplayer', init_multi)
#reset_button = frame.add_button('Single Player', init_single)
#menu_button = frame.add_button('Menu', init_menu)

frame.start()

bounce_blue_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/bounce_blue.mp3")
beep_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/beep_sound.mp3")
falling_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/falling_sound.mp3")
platform_death_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/platform_death_sound.mp3")
victory_sound = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/victory_fanfare.mp3")
    
    
menu_music = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/menu.ogg")
game_music = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/game_music_loop.ogg")
game_music_intro = simplegui.load_sound("https://github.com/Avery-Whitaker/Python-Game/raw/master/game_intro.ogg")
menu_music.set_volume(0.3)
game_music.set_volume(0.3)
game_music_intro.set_volume(0.4)



'''
Game State:
0 - main menu
1 - single player
2 - two player


'''