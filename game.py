import simplegui
import math

#Is there another way to seperate the rendering engine from game?
class DrawEngine:
    

    
    
    class Camera:
        def __init__(self, x, y, z, xAngle, yAngle, zAngle):
            self.vpX = x
            self.x = x
            self.y = y
            self.z = z
            self.x_rotate = xAngle
            self.y_rotate = yAngle
            self.z_rotate = zAngle
            
        #moves camera (note from cameras perspective)
        def move(self, x_change, y_change, z_change):
          
            # Rotates a certain point, by default, around the vanishing points
            def rotateX(y, z, angleX, centerY, centerZ):
                cosX = math.cos(angleX)
                sinX = math.sin(angleX)
                y1 = (y - centerY) * cosX - (z - centerZ) * sinX
                z1 = (z - centerZ) * cosX + (y - centerY) * sinX
                return y1 + centerY, z1 + centerZ

            def rotateY(x, z, angleY, centerX, centerZ):
                cosY = math.cos(angleY)
                sinY = math.sin(angleY)
                x1 = (x - centerX) * cosY - (z - centerZ) * sinY
                z1 = (z - centerZ) * cosY + (x - centerX) * sinY
                return x1 + centerX, z1 + centerZ

            def rotateZ(x, y, angleZ, centerX, centerY):
                cosZ = math.cos(angleZ)
                sinZ = math.sin(angleZ)
                x1 = (x - centerX) * cosZ - (y - centerY) * sinZ
                y1 = (y - centerY) * cosZ + (x - centerX) * sinZ
                return x1 + centerX, y1 + centerY

            x = x_change
            y = y_change
            z = z_change
            
            y,z = rotateX(y, z, self.x_rotate, 0, 0)
            x,z = rotateY(x, z, self.y_rotate, 0, 0)
            x,y = rotateZ(x, y, self.z_rotate, 0, 0)

            
            self.x += x
            self.y += y
            self.z += z
            
        def turn(self, x_change, y_change, z_change):
            self.x_rotate += x_change
            self.y_rotate += y_change
            self.z_rotate += z_change
            
    
    def __init__(self, fl, vpX, vpY, cam):
        self.focalLength = fl
        self.vanishingPointX, self.vanishingPointY = vpX, vpY
        self.camera = cam 
    
    #3D Point - enmutable
    class ThreeDPoint:
        def __init__(self,x,y,z):
            self.x = x
            self.y = y
            self.z = z
            
        def move(self,xChange,yChange,zChange):
            self.x += xChange
            self.y += yChange
            self.z += zChange

        def __getitem__(self,key):
            if key == 0:
                return self.x
            if key == 1:
                return self.y
            if key == 2:
                return self.z
            
        #helper function <3
        #not sure where to put this - in 3D point I guess
        def get_rotated(self,angle_x,angle_y,angle_z,center_x,center_y,center_z):
            x = self.x
            y = self.y
            z = self.z
        
            # Rotates a certain point, by default, around the vanishing points
            # Returns rotated version
            def rotateX(y, z, angleX, centerY, centerZ):
                cosX = math.cos(angleX)
                sinX = math.sin(angleX)
                y1 = (y - centerY) * cosX - (z - centerZ) * sinX
                z1 = (z - centerZ) * cosX + (y - centerY) * sinX
                return y1 + centerY, z1 + centerZ

            def rotateY(x, z, angleY, centerX, centerZ):
                cosY = math.cos(angleY)
                sinY = math.sin(angleY)
                x1 = (x - centerX) * cosY - (z - centerZ) * sinY
                z1 = (z - centerZ) * cosY + (x - centerX) * sinY
                return x1 + centerX, z1 + centerZ

            def rotateZ(x, y, angleZ, centerX, centerY):
                cosZ = math.cos(angleZ)
                sinZ = math.sin(angleZ)
                x1 = (x - centerX) * cosZ - (y - centerY) * sinZ
                y1 = (y - centerY) * cosZ + (x - centerX) * sinZ
                return x1 + centerX, y1 + centerY

            y,z = rotateX(y, z, angle_x, center_y, center_z)
            x,z = rotateY(x, z, angle_y, center_x, center_z)
            x,y = rotateZ(x, y, angle_z, center_x, center_y)

            return ThreeDPoint(x,y,z)


            #transforms 3D world point to 2D screen cordinates
        def transform(self, x_rotate = None, y_rotate = None,  z_rotate = None):
            global draw_engine
            
            if x_rotate == None:
                 x_rotate = draw_engine.camera.x_rotate
            if y_rotate == None:
                 y_rotate = draw_engine.camera.y_rotate
            if z_rotate == None:
                 z_rotate = draw_engine.camera.z_rotate
            
            # Rotates a certain point, by default, around the vanishing points
            def rotateX(y, z, angleX, centerY, centerZ):
                cosX = math.cos(angleX)
                sinX = math.sin(angleX)
                y1 = (y - centerY) * cosX - (z - centerZ) * sinX
                z1 = (z - centerZ) * cosX + (y - centerY) * sinX
                return y1 + centerY, z1 + centerZ

            def rotateY(x, z, angleY, centerX, centerZ):
                cosY = math.cos(angleY)
                sinY = math.sin(angleY)
                x1 = (x - centerX) * cosY - (z - centerZ) * sinY
                z1 = (z - centerZ) * cosY + (x - centerX) * sinY
                return x1 + centerX, z1 + centerZ

            def rotateZ(x, y, angleZ, centerX, centerY):
                cosZ = math.cos(angleZ)
                sinZ = math.sin(angleZ)
                x1 = (x - centerX) * cosZ - (y - centerY) * sinZ
                y1 = (y - centerY) * cosZ + (x - centerX) * sinZ
                return x1 + centerX, y1 + centerY

            #should rotate around the camera
            x = self.x + draw_engine.camera.x
            y = self.y + draw_engine.camera.y
            z = self.z + draw_engine.camera.z
            
            y,z = rotateX(y, z, x_rotate, 0, -draw_engine.focalLength)
            x,z = rotateY(x, z, y_rotate, 0, -draw_engine.focalLength)
            x,y = rotateZ(x, y, z_rotate, 0, -draw_engine.focalLength)

            scale = abs(draw_engine.focalLength/(draw_engine.focalLength + z))
            newX = draw_engine.vanishingPointX + x * scale
            newY = draw_engine.vanishingPointY + y * scale

            return draw_engine.TwoDPoint(newX, newY, scale)
            
        def draw(self, canvas):
            line_width = 5 #placeholder
            radius = 5
            xNew, yNew, scale = self.transform(draw_engine.camera.X_rotate, draw_engine.camera.Y_rotate, draw_engine.camera.Z_rotate)
            canvas.draw_circle((xNew, yNew), radius * scale, line_width, 'White','Grey')
    
    #unmutable
    class TwoDPoint:
        def __init__(self,x,y,scale):
            self.x = x
            self.y = y
            self.scale = scale

        def __getitem__(self,key):
            if key == 0:
                return self.x
            if key == 1:
                return self.y
            if key == 2:
                return self.scale

    class ThreeDQuad:
        def __init__(self,a,b,c,d):
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.priority = -1

        def __cmp__(self, other):
            if self.priority < other.priority:
                return -1
            elif self.priority == other.priority:
                return 0
            return 1

        def draw(self, canvas):
            x1, y1, z1 = self.a.transform()
            x2, y2, z2 = self.b.transform()
            x3, y3, z3 = self.c.transform()
            x4, y4, z4 = self.d.transform()

            self.priority = (z1+z2+z3+z4)/2
            line_thinkness = min(z1+z2+z3+z4, 10)
                
            canvas.draw_polygon( [(x1, y1), 
                             (x2, y2), 
                             (x3, y3), 
                             (x4, y4)], line_thinkness, 'White','Grey')

WIDTH = 1200
HEIGHT = 400

draw_engine = DrawEngine(250.0, WIDTH/2, HEIGHT/2, DrawEngine.Camera(0,0,0,0,0,0))
        


l = 100
    
a = draw_engine.ThreeDPoint(0, 0, 0)
b = draw_engine.ThreeDPoint(0, l, 0)
c = draw_engine.ThreeDPoint(l, l, 0)
d = draw_engine.ThreeDPoint(l, 0, 0)
e = draw_engine.ThreeDPoint(0, 0, l)
f = draw_engine.ThreeDPoint(0, l, l)
g = draw_engine.ThreeDPoint(l, l, l)
h = draw_engine.ThreeDPoint(l, 0, l)


stuff = list()

stuff.append(draw_engine.ThreeDQuad(a, b, c, d))
stuff.append(draw_engine.ThreeDQuad(c, b, f, g))
stuff.append(draw_engine.ThreeDQuad(b, f, e, a))
stuff.append(draw_engine.ThreeDQuad(a, e, h, d))
stuff.append(draw_engine.ThreeDQuad(d, h, g, c))
stuff.append(draw_engine.ThreeDQuad(h, g, f, e))

def render_field(canvas):
    global stuff
    
    stuff.sort()
    
    for thing in stuff:
        thing.draw(canvas)
          
def key_handler(key):
    global Z_rotate_angle, X_rotate_angle, Y_rotate_angle,draw_engine
 
    if key == simplegui.KEY_MAP["up"]:
        draw_engine.camera.turn(math.pi * 0.075,0,0)
    if key == simplegui.KEY_MAP["down"]:
        draw_engine.camera.turn(math.pi * -0.075,0,0)
    if key == simplegui.KEY_MAP["left"]:
        draw_engine.camera.turn(0,math.pi * 0.075,0)
    if key == simplegui.KEY_MAP["right"]:
        draw_engine.camera.turn(0,math.pi * -0.075,0)
    if key == simplegui.KEY_MAP["o"]:
        draw_engine.camera.turn(0,0,math.pi * 0.075)
    if key == simplegui.KEY_MAP["p"]:
        draw_engine.camera.turn(0,0,math.pi * -0.075)
        
        
        #TODO make camera its own class containing direction
        #i.e. encaspulate cmera behavior in DrawEngine
        #then encapsulate drawing order behavior in DrawEngine
        
    if key == simplegui.KEY_MAP["w"]:
        draw_engine.camera.move(0,10,0) #should be relative
    if key == simplegui.KEY_MAP["a"]:
        draw_engine.camera.move(10,0,0)
    if key == simplegui.KEY_MAP["s"]:
        draw_engine.camera.move(0,-10,0)
    if key == simplegui.KEY_MAP["d"]:
        draw_engine.camera.move(-10,0,0)
    if key == simplegui.KEY_MAP["q"]:
        draw_engine.camera.move(0,0,10)
    if key == simplegui.KEY_MAP["e"]:
        draw_engine.camera.move(0,0,-10)

def game_loop(canvas):
    render_field(canvas)
    
frame = simplegui.create_frame("", WIDTH, HEIGHT)
frame.set_draw_handler(game_loop)
frame.set_keydown_handler(key_handler)

frame.start()
