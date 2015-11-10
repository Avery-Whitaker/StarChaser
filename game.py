import simplegui
import math
import random

#in: list of points

##########################################################################################
def trimZero(points, axis, axis_n):
        #stolen from internet https://paolocrosetto.wordpress.com/python-code/
        #works like magic
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
                new_point[axis-2] = max(point_a[axis-2],point_b[axis-2])-min(point_b[axis-2],point_a[axis-2])*max(point_b[axis],point_a[axis]) / ( abs(point_b[axis])+abs(point_a[axis])) + min(point_b[axis-2],point_a[axis-2])
                new_point[axis-1] = (max(point_a[axis-1],point_b[axis-1])-min(point_b[axis-1],point_a[axis-1]))*(max(point_b[axis],point_a[axis])/( abs(point_b[axis])+abs(point_a[axis])))+min(point_b[axis-1],point_a[axis-1])
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
            while points[i][axis] >= 0:
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

        
    

class DrawEngine:
    class Camera:
        def draw(self, canvas):
            
            canvas.draw_polygon([[self.screen_x, self.screen_y], [self.screen_x+self.screen_width, self.screen_y], [self.screen_x+self.screen_width, self.screen_y+self.screen_height], [self.screen_x, self.screen_y+self.screen_height]], 3, 'White','Black')
             
            list = []
            for a in world_objects:
                b = a.transform(self)
                if b is not None:
                    list.append(b)
            list.sort()
            for twoDPoly in list:
                twoDPoly.draw(canvas, self)
            
            canvas.draw_polygon([[self.screen_x, self.screen_y], [self.screen_x+self.screen_width, self.screen_y], [self.screen_x+self.screen_width, self.screen_y+self.screen_height], [self.screen_x, self.screen_y+self.screen_height]], 3, 'Black')
               
               
        def __init__(self, x, y, z, yAngle, world_objects, screen_x, screen_y, screen_width, screen_height):
            self.x = x
            self.y = y
            self.z = z
            self.y_rotate = yAngle
            self.world_objects = world_objects
            self.screen_x = screen_x
            self.screen_y = screen_y
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.focalLength = 250.0
            self.vanishingPointX, self.vanishingPointY = screen_width/2.0, screen_height/2.0
            
        def move(self, x_change, y_change, z_change):                                                                                                        #WHY????
            self.x += x_change
            self.y += y_change
            self.z += z_change
            
        def set_pos(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
            
        def turn(self, y_change):
            self.y_rotate += y_change
    
    
    class WorldPoint:
        def __init__(self,x,y,z):
            self.x = x
            self.y = y
            self.z = z
            
        def move(self,a,b,c):
            self.x += a
            self.y += b
            self.z += c
            
        def __getitem__(self,key):
            if key == 0:
                return self.x
            if key == 1:
                return self.y
            if key == 2:
                return self.z

        def transform(self,camera):
            x = self.x + camera.x
            y = self.y + camera.y 
            z = self.z + camera.z
            cos_y = math.cos(camera.y_rotate)
            sin_y = math.sin(camera.y_rotate)
            old_x = x
            x = x * cos_y - (z+camera.focalLength)*sin_y
            z = (z+camera.focalLength) * cos_y + old_x * sin_y - camera.focalLength
            if camera.focalLength + z == 0:
                scale = 1000000000000
            else:
                scale = camera.focalLength/(camera.focalLength + z)
            return DrawEngine.ScreenPoint(
                camera.vanishingPointX + x * abs(scale), 
                camera.vanishingPointY + y * abs(scale), scale)
        
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
            maxZ = -1000000000
            minZ = 10000000000
            for point in self.points:
                points.append( point.transform(camera) )
                if points[len(points)-1][2] > maxZ:
                    maxZ = points[len(points)-1][2]
                if points[len(points)-1][2] < maxZ:
                    minZ = points[len(points)-1][2]
            if maxZ > 0:
                if minZ < 0:
                    trimZero(points, 2, 3)
                return DrawEngine.ScreenPoly(points, self.color_r, self.color_g, self.color_b)
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
        
        def min_z(self):
            min_z = 10000000000
            for point in self.points:
                if point[2] < min_z:
                    min_z = point[2]
            return min_z
        
        def max_z(self):
            max_z = -1000000000
            for point in self.points:
                if point[2] > max_z:
                    max_z = point[2]
            return max_z
           
        
    class WorldPlayer(WorldPoint):
        def __init__(self,x,y,z):
            DrawEngine.WorldPoint.__init__(self, x,y,z)
            self.y_vel = 0
            
        def update(self):
            
            collide = False
            
            for item in world_objects:
                if item != player_a and item != player_b:
                    if self.x > item.min_x() and self.x < item.max_x() and self.z > item.min_z() and self.z < item.max_z():
                        collide = True
                        break
            
            
            self.y += self.y_vel
            
            if self.y_vel > 0 and not collide:
                self.y = -75
            
            # if collide:
            #     self.y = 100
            # else:
            #     self.y = 500
            
                
            self.y_vel += 1
            
        def jump(self):
            
            collide = False
            
            for item in world_objects:
                if item != player_a and item != player_b:
                    if self.x > item.min_x() and self.x < item.max_x() and self.z > item.min_z() and self.z < item.max_z():
                        collide = True
                        break
            if collide:   
                if self.y >= -75:
                    self.y_vel -= 5
                self.y_vel -= 0.1
            
        def forward(self):
            self.z += 10
            
        def left(self):
            self.x -= 10
            
        def right(self):
            self.x += 10
            
        def back(self):
            self.z -= 10
            
         
        
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
            
        def __cmp__(self, other):
            if self.priority < other.priority:
                return -1
            elif self.priority == other.priority:
                return 0
            return 1
            
        def draw(self, canvas, camera):
            line_width = 5
            radius = 15
            if self.scale > 0 and self.x > 0 and self.y > 0 and self.x < camera.screen_width and self.y < camera.screen_height :
                canvas.draw_circle((self.x+camera.screen_x, self.y+camera.screen_y), radius * self.scale, line_width, 'White','Grey')
    
            
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
n = 8
l = 300 

for y in range(0,n):
    for x in range(0,n):
        if random.random() > 0.4:
            world_objects.append(DrawEngine.WorldPoly([DrawEngine.WorldPoint(l+x*l, 0, l+y*l),
                                                      DrawEngine.WorldPoint(0+x*l, 0, l+y*l),
                                                      DrawEngine.WorldPoint(0+x*l, 0, 0+y*l), 
                                                      DrawEngine.WorldPoint(l+x*l, 0, 0+y*l)]))

player_a = DrawEngine.WorldPlayer(world_objects[0][0][0]-l/2, -75, world_objects[0][0][2]-l/2)
player_b = DrawEngine.WorldPlayer(world_objects[5][0][0]-l/2, -75, world_objects[5][0][2]-l/2)

world_objects.append(player_a)
world_objects.append(player_b)

            
WIDTH = 1200
HEIGHT = 600
#                            (self, x, y, z, yAngle, world_objects, screen_x, screen_y, screen_width, screen_height)
left_camera = DrawEngine.Camera(-200,200,-200,  0, world_objects,     50,       100,      475,      HEIGHT-125)
right_camera = DrawEngine.Camera(-200,200,-200,  0, world_objects ,WIDTH/2+50 , 100,     475,      HEIGHT-125)
  
                
def render_field(canvas):
    canvas.draw_polygon([[0, 0], [0, HEIGHT], [WIDTH, HEIGHT], [WIDTH, 0]], 1, 'White', 'Cyan')
    right_camera.draw(canvas)
    left_camera.draw(canvas)
    #canvas.draw_line((WIDTH/2, 100), (WIDTH/2, HEIGHT), 4, 'White')
    #canvas.draw_line((0, 100), (WIDTH, 100), 4, 'White')
    canvas.draw_text('Avery Whitaker | Split-Screen Multiplayer Prototype V0.2', (30, 50), 48, 'Red')
    
    
    player_a.update()
    player_b.update()
    left_camera.set_pos(-player_a.x, 200-player_a.y, 100-player_a.z)
    right_camera.set_pos(-player_b.x, 200-player_b.y, 100-player_b.z)
    
    
    random.shuffle(world_objects)

    if random.random() > 0.99:
        for item in world_objects:
            if item != player_a and item != player_b:
                world_objects.remove(item)
                break
    
    
        
#####################################################################
#### Key handler stuff for testing
    
keys_down = {
    simplegui.KEY_MAP['a']: False,
    simplegui.KEY_MAP['b']: False,
    simplegui.KEY_MAP['c']: False,
    simplegui.KEY_MAP['d']: False,
    simplegui.KEY_MAP['e']: False,
    simplegui.KEY_MAP['f']: False,
    simplegui.KEY_MAP['g']: False,
    simplegui.KEY_MAP['h']: False,
    simplegui.KEY_MAP['i']: False,
    simplegui.KEY_MAP['j']: False,
    simplegui.KEY_MAP['k']: False,
    simplegui.KEY_MAP['l']: False,
    simplegui.KEY_MAP['m']: False,
    simplegui.KEY_MAP['n']: False,
    simplegui.KEY_MAP['o']: False,
    simplegui.KEY_MAP['p']: False,
    simplegui.KEY_MAP['q']: False,
    simplegui.KEY_MAP['r']: False,
    simplegui.KEY_MAP['s']: False,
    simplegui.KEY_MAP['t']: False,
    simplegui.KEY_MAP['u']: False, #MAKE THIS A LOOP IDIOT
    simplegui.KEY_MAP['v']: False,
    simplegui.KEY_MAP['w']: False,
    simplegui.KEY_MAP['x']: False,
    simplegui.KEY_MAP['y']: False,
    simplegui.KEY_MAP['z']: False,
    simplegui.KEY_MAP['up']: False,
    simplegui.KEY_MAP['down']: False,
    16: False,
    simplegui.KEY_MAP['space']: False,
    simplegui.KEY_MAP['left']: False,
    simplegui.KEY_MAP['right']: False
}
    
def set_keydown_handler(k):
    global keys_down
    keys_down[k] = True
    
def set_keyup_handler(k):
    global keys_down
    keys_down[k] = False
            
def key_action():
    global draw_engine,keys_down
 
#    if keys_down[simplegui.KEY_MAP["up"]]:
#        right_camera.move(0,0,-10)
#    if keys_down[simplegui.KEY_MAP["down"]]:
#        right_camera.move(0,0,10)
#    if keys_down[simplegui.KEY_MAP["left"]]:
#        right_camera.move(-10,0,0)
#    if keys_down[simplegui.KEY_MAP["right"]]:
#        right_camera.move(10,0,0)
#    if keys_down[simplegui.KEY_MAP["o"]]:
#        right_camera.move(0,-10,0)
#    if keys_down[simplegui.KEY_MAP["p"]]:
#        right_camera.move(0,10,0)
#    if keys_down[simplegui.KEY_MAP["z"]]:
#        left_camera.turn(-.05)
#    if keys_down[simplegui.KEY_MAP["x"]]:
#        left_camera.turn(0.05)
#    if keys_down[simplegui.KEY_MAP["k"]]:
#        right_camera.turn(-0.05)
#    if keys_down[simplegui.KEY_MAP["l"]]:
#        right_camera.turn(0.05)
#    if keys_down[simplegui.KEY_MAP["w"]]:
#        left_camera.move(0,0,-10)
#    if keys_down[simplegui.KEY_MAP["a"]]:
#        left_camera.move(-10,0,0)
#    if keys_down[simplegui.KEY_MAP["s"]]:
#        left_camera.move(0,0,10)
#    if keys_down[simplegui.KEY_MAP["d"]]:
#        left_camera.move(10,0,0)
#    if keys_down[simplegui.KEY_MAP["q"]]:
#        left_camera.move(0,-10,0)
#    if keys_down[simplegui.KEY_MAP["e"]]:
#        left_camera.move(0,10,0)

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
    render_field(canvas)
    key_action()



frame = simplegui.create_frame("", WIDTH, HEIGHT)
frame.set_draw_handler(game_loop)
frame.set_keydown_handler(set_keydown_handler)
frame.set_keyup_handler(set_keyup_handler)

frame.start()
