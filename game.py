import simplegui
import math

#Is there another way to seperate the rendering engine from game?
class DrawEngine:
    
    def __init__(self, fl, vpX, vpY, cam):
        self.focalLength = fl
        self.vanishingPointX, self.vanishingPointY = vpX, vpY
        self.camera = cam 
        
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

        def transform(self, X_rotate, Y_rotate, Z_rotate):
            global draw_engine
            
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
            
            y,z = rotateX(y, z, X_rotate, 0, -draw_engine.focalLength)
            x,z = rotateY(x, z, Y_rotate, 0, -draw_engine.focalLength)
            x,y = rotateZ(x, y, Z_rotate, 0, -draw_engine.focalLength)

            scale = abs(draw_engine.focalLength/(draw_engine.focalLength + z))
            newX = draw_engine.vanishingPointX + x * scale
            newY = draw_engine.vanishingPointY + y * scale

            return draw_engine.TwoDPoint(newX, newY, scale)
            
        def draw(self, canvas):
            global X_rotate_angle,Y_rotate_angle,Z_rotate_angle
            line_width = 5 #placeholder
            radius = 5
            xNew, yNew, scale = self.transform(X_rotate_angle, Y_rotate_angle, Z_rotate_angle)
            canvas.draw_circle((xNew, yNew), radius * scale, line_width, 'White','Grey')
    
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
            global X_rotate_angle,Y_rotate_angle,Z_rotate_angle
            x1, y1, z1 = self.a.transform(X_rotate_angle, Y_rotate_angle, Z_rotate_angle)
            x2, y2, z2 = self.b.transform(X_rotate_angle, Y_rotate_angle, Z_rotate_angle)
            x3, y3, z3 = self.c.transform(X_rotate_angle, Y_rotate_angle, Z_rotate_angle)
            x4, y4, z4 = self.d.transform(X_rotate_angle, Y_rotate_angle, Z_rotate_angle)

            self.priority = (z1+z2+z3+z4)/2

            canvas.draw_polygon( [(x1, y1), 
                             (x2, y2), 
                             (x3, y3), 
                             (x4, y4)], 2, 'White','Grey')

WIDTH = 1200
HEIGHT = 400

draw_engine = DrawEngine(250.0, WIDTH/2, HEIGHT/2, DrawEngine.ThreeDPoint(0,0,0))
        

    
X_rotate_angle = 0
Y_rotate_angle = 0
Z_rotate_angle = 0

stuff = list()
stuff.append(draw_engine.ThreeDQuad(draw_engine.ThreeDPoint(-WIDTH/4, -HEIGHT/4, 10), 
                        draw_engine.ThreeDPoint(WIDTH/4, -HEIGHT/4, 10), 
                        draw_engine.ThreeDPoint( WIDTH/4, HEIGHT/4, 10), 
                        draw_engine.ThreeDPoint(-WIDTH/4, HEIGHT/4, 10)))
stuff.append(draw_engine.ThreeDQuad(draw_engine.ThreeDPoint(-WIDTH/4, -HEIGHT/4, 100), 
                        draw_engine.ThreeDPoint(WIDTH/4, -HEIGHT/4, 100), 
                        draw_engine.ThreeDPoint( WIDTH/4, HEIGHT/4, 100), 
                        draw_engine.ThreeDPoint(-WIDTH/4, HEIGHT/4, 100)))
stuff.append(draw_engine.ThreeDQuad(draw_engine.ThreeDPoint(-WIDTH/14, -HEIGHT/4, 100), 
                        draw_engine.ThreeDPoint(-WIDTH/14, -HEIGHT/4, 0), 
                        draw_engine.ThreeDPoint(-WIDTH/14, HEIGHT/4, 0), 
                        draw_engine.ThreeDPoint( -WIDTH/14, HEIGHT/4, 100)))
stuff.append(draw_engine.ThreeDQuad(draw_engine.ThreeDPoint( WIDTH/14, -HEIGHT/4, 100), 
                        draw_engine.ThreeDPoint(WIDTH/14, -HEIGHT/4, 0), 
                        draw_engine.ThreeDPoint( WIDTH/14, HEIGHT/4, 0), 
                        draw_engine.ThreeDPoint( WIDTH/14, HEIGHT/4, 100)))

def render_field(canvas):
    global stuff
    
    stuff.sort()
    
    for thing in stuff:
        thing.draw(canvas)
          
def key_handler(key):
    global Z_rotate_angle, X_rotate_angle, Y_rotate_angle,draw_engine
 
    if key == simplegui.KEY_MAP["up"]:
        X_rotate_angle += math.pi * 0.075
    if key == simplegui.KEY_MAP["down"]:
        X_rotate_angle -= math.pi * 0.075
    if key == simplegui.KEY_MAP["left"]:
        Y_rotate_angle += math.pi * 0.075
    if key == simplegui.KEY_MAP["right"]:
        Y_rotate_angle -= math.pi * 0.075
    if key == simplegui.KEY_MAP["o"]:
        Z_rotate_angle += math.pi * 0.075
    if key == simplegui.KEY_MAP["p"]:
        Z_rotate_angle -= math.pi * 0.075
        
        
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
