import math
import user40_hIgQ2QMFUJ_1 as trim
import random

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
        return ScreenPoint(camera.vanishingPointX + x * abs(scale), camera.vanishingPointY + y * abs(scale), -scale)
    
class WorldSphere(WorldPoint, Color):
    def __init__(self, x, y, z, radius, r, g, b, a):
        WorldPoint.__init__(self, x, y, z)
        Color.__init__(self, r, g, b, a)
        self.radius = radius
        
    def transform(self,camera):
        s = WorldPoint.transform(self,camera)
        return ScreenCircle(s[0],s[1],s[2],self.radius,self.color_r,self.color_g,self.color_b,self.color_a)
    


class Camera(WorldAngle, WorldPoint):
    def draw(self, canvas, world_objects):
        canvas.draw_polygon([[self.screen_x, self.screen_y], [self.screen_x+self.screen_width, self.screen_y], [self.screen_x+self.screen_width, self.screen_y+self.screen_height], [self.screen_x, self.screen_y+self.screen_height]], 1, 'White','Grey')
            
        list = []
        for a in world_objects:
            if a is not None:
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
                    trim.trimZero(points, 2, 3)
                return ScreenPoly(points, self.color_r, self.color_g, self.color_b )
            return None
        
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
    
class ScreenCircle(ScreenPoint, Color):
    def __init__(self,x,y,scale,radius, r,g,b,a):
        ScreenPoint.__init__(self,x,y,scale)
        Color.__init__(self,r,g,b,a)
        
        self.radius = radius
        self.priority += radius
        
    def __cmp__(self, other):
        if self.priority < other.priority:
            return -1
        elif self.priority == other.priority:
            return 0
        return 1
            
    def draw(self, canvas, camera):
        if self.scale > 0 and self.x > 0 and self.y > 0 and self.x < camera.screen_width and self.y < camera.screen_height :
            canvas.draw_circle((self.x+camera.screen_x, self.y+camera.screen_y), self.radius * self.scale, 1, self.rgba(), self.rgba())

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
            canvas.draw_polygon(new, 1, 'rgba(200,200,255,1)',"rgba("+str(self.color_r)+","+str(self.color_g)+","+str(self.color_b)+","+str(0.8)+")")
            
