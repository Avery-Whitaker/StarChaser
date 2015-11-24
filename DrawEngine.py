'''
New version, renders things by z value! who
cares about anything else!
'''

import math
import random
import simplegui

#in: list of points
##########################################################################################
def trim_zero(points, axis, axis_n):
    
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

    #can optimize by not running for edges of screen
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
        
#mutates points_list
#trims polygon to be in rectangle defined by xMin, xMax yMin, yMax
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

#background_image = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/background%20(11-21-2015%208-13-11%20PM)/background%20001.jpg"))

background_image_counter = 0

background_image = []
for i in range(1,300):
    s = str(i)
    while(len(s) < 3):
        s = '0'+s
    background_image.append(simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/background/background%20"+s+".png"))
    
class Camera(WorldAngle, WorldPoint):
    
    def draw(self, canvas, world_objects):
        global background_image,background_image_counter
        
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
    def __init__(self,points, r = random.randrange(70,100), g = random.randrange(200,255), b = random.randrange(70,100), a = 1):
        self.points = points
        Color.__init__(self,r,g,b,a)
        
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
                return ScreenPoly(points, self.points[0].z, self.color_r, self.color_g, self.color_b, self.color_a )
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
    
player_image_a = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/player_sprite_a.png")
player_image_b = simplegui.load_image("https://github.com/Avery-Whitaker/Python-Game/raw/master/player_sprite_b.png")
rotate = 0
    
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
        global rotate
        
        if self.scale > 0 and self.x > 0 and self.y > 0 and self.x < camera.screen_width and self.y < camera.screen_height :
            if self.color_b == 255:
                rotate += 0.05
                canvas.draw_image(player_image_a, (100/ 2, 100/2), (100, 100), (self.x+camera.screen_x, self.y+camera.screen_y),(self.radius * self.scale*5, self.radius * self.scale * 5), rotate)
            else:
                canvas.draw_image(player_image_b, (100/ 2, 100/2), (100, 100), (self.x+camera.screen_x, self.y+camera.screen_y),(self.radius * self.scale*5, self.radius * self.scale * 5), rotate)
            
            #canvas.draw_circle((self.x+camera.screen_x, self.y+camera.screen_y), self.radius * self.scale, 1, self.rgba(), self.rgba())

class ScreenPoly:
    def __init__(self, points, world_z, color_r, color_g, color_b, color_a):
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
        self.color_a = color_a
        
        self.points = points
        self.world_z = world_z
        
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
            canvas.draw_polygon(new, 1, "rgba("+str(self.color_r)+","+str(self.color_g)+","+str(self.color_b)+","+str(1)+")","rgba("+str(self.color_r)+","+str(self.color_g)+","+str(self.color_b)+","+str(self.color_a)+")")

        