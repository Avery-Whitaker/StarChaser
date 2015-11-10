
import simplegui
import math


# Rotates a certain point, by default, around the vanishing points
def TD_func_rotateX(y, z, angleX, centerY, centerZ):
    global focalLength,vanishingPointX,vanishingPointY
    cosX = math.cos(angleX)
    sinX = math.sin(angleX)
    y1 = (y - centerY) * cosX - (z - centerZ) * sinX
    z1 = (z - centerZ) * cosX + (y - centerY) * sinX
    return y1 + centerY, z1 + centerZ

def TD_func_rotateY(x, z, angleY, centerX, centerZ):
    global focalLength,vanishingPointX,vanishingPointY
    cosY = math.cos(angleY)
    sinY = math.sin(angleY)
    x1 = (x - centerX) * cosY - (z - centerZ) * sinY
    z1 = (z - centerZ) * cosY + (x - centerX) * sinY
    return x1 + centerX, z1 + centerZ

def TD_func_rotateZ(x, y, angleZ, centerX, centerY):
    global focalLength,vanishingPointX,vanishingPointY
    cosZ = math.cos(angleZ)
    sinZ = math.sin(angleZ)
    x1 = (x - centerX) * cosZ - (y - centerY) * sinZ
    y1 = (y - centerY) * cosZ + (x - centerX) * sinZ
    return x1 + centerX, y1 + centerY

class ThreeDPoint:
    def __init__(self,x,y,z):
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
        
    def transform(self, X_rotate, Y_rotate, Z_rotate):
        global focalLength,vanishingPointX,vanishingPointY
    
        y,z = TD_func_rotateX(self.y, self.z, X_rotate, 0, 0)
        x,z = TD_func_rotateY(self.x, z, Y_rotate, 0, 0)
        x,y = TD_func_rotateZ(x, y, Z_rotate, 0, 0)

        scale = abs(focalLength/(focalLength + z))
        newX = vanishingPointX + x * scale
        newY = vanishingPointY + y * scale

        return TwoDPoint(newX, newY, scale)
    
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

def TD_config(fl=250, vpX=0, vpY=0):
    global focalLength,vanishingPointX,vanishingPointY
    focalLength = fl
    vanishingPointX, vanishingPointY = vpX, vpY
    
# Draws a quadrilateral
def TD_graphics_quad(canvas, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
    global focalLength,vanishingPointX,vanishingPointY,X_rotate_angle,Y_rotate_angle,Z_rotate_angle
    x1New, y1New = ThreeDPoint(x1, y1, z1).transform(X_rotate_angle,Y_rotate_angle,Z_rotate_angle)
    x2New, y2New = ThreeDPoint(x2, y2, z2).transform(X_rotate_angle,Y_rotate_angle,Z_rotate_angle)
    x3New, y3New = ThreeDPoint(x3, y3, z3).transform(X_rotate_angle,Y_rotate_angle,Z_rotate_angle)
    x4New, y4New = ThreeDPoint(x4, y4, z4).transform(X_rotate_angle,Y_rotate_angle,Z_rotate_angle)
    canvas.draw_polygon( [(x1New, y1New), 
                         (x2New, y2New), 
                         (x3New, y3New), 
                         (x4New, y4New)], 2, 'White','Grey')

    # love.graphics.quad(mode, x1New, y1New, x2New, y2New, x3New, y3New, x4New, y4New)



WIDTH = 1200
HEIGHT = 400

x,y,z = 0,0,0
        
X_rotate_angle = 0
Y_rotate_angle = 0
Z_rotate_angle = 0

x = 10
# Handler to draw on canvas
def render_field(canvas):
    global x, WIDTH, HEIGHT
    
    TD_graphics_quad(canvas, -WIDTH/4, -HEIGHT/4, 10, 
                            WIDTH/4, -HEIGHT/4, 10, 
                            WIDTH/4, HEIGHT/4, 10, 
                            -WIDTH/4, HEIGHT/4, 10)
    
    TD_graphics_quad(canvas, -WIDTH/14 + x, -HEIGHT/4 + y, 100 + z, 
                            -WIDTH/14 + x, -HEIGHT/4 + y, z, 
                            -WIDTH/14 + x, HEIGHT/4 + y, z, 
                            -WIDTH/14 + x, HEIGHT/4 + y, 100 + z)
    
    TD_graphics_quad(canvas, WIDTH/14 + x, -HEIGHT/4 + y, 100 + z, 
                            WIDTH/14 + x, -HEIGHT/4 + y, 0 + z, 
                            WIDTH/14 + x, HEIGHT/4 + y, 0 + z, 
                            WIDTH/14 + x, HEIGHT/4 + y, 100 + z)
    TD_graphics_quad(canvas, 0, 0, -5, WIDTH, 0, -5, WIDTH, HEIGHT, 10, 0, HEIGHT, 10)

def key_handler(key):
    global focalLength,vanishingPointX,vanishingPointY, x, y, z, Z_rotate_angle, X_rotate_angle, Y_rotate_angle
    
    if key == simplegui.KEY_MAP["W"]:
        TD_config(focalLength, vanishingPointX+0, vanishingPointY+10)
    if key == simplegui.KEY_MAP["S"]:
        TD_config(focalLength, vanishingPointX+0, vanishingPointY-10)
    if key == simplegui.KEY_MAP["A"]:
        TD_config(focalLength, vanishingPointX-10, vanishingPointY)
    if key == simplegui.KEY_MAP["D"]:
        TD_config(focalLength, vanishingPointX+10, vanishingPointY)
    if key == simplegui.KEY_MAP["Q"]:
        TD_config(focalLength+10, vanishingPointX, vanishingPointY)
    if key == simplegui.KEY_MAP["E"]:
        TD_config(focalLength-10, vanishingPointX, vanishingPointY)
      
    if key == simplegui.KEY_MAP["R"]:
        X_rotate_angle += math.pi * 0.05
    if key == simplegui.KEY_MAP["T"]:
        X_rotate_angle -= math.pi * 0.05
    if key == simplegui.KEY_MAP["F"]:
        Y_rotate_angle += math.pi * 0.05
    if key == simplegui.KEY_MAP["G"]:
        Y_rotate_angle -= math.pi * 0.05
    if key == simplegui.KEY_MAP["V"]:
        Z_rotate_angle += math.pi * 0.05
    if key == simplegui.KEY_MAP["B"]:
        Z_rotate_angle -= math.pi * 0.05
        
    if key == simplegui.KEY_MAP["left"]:
        x -= 10
    if key == simplegui.KEY_MAP["right"]:
        x += 10
    if key == simplegui.KEY_MAP["up"]:
        y += 10
    if key == simplegui.KEY_MAP["down"]:
        y -= 10
        
    if key == simplegui.KEY_MAP["j"]:
        z += 10
    if key == simplegui.KEY_MAP["k"]:
        z -= 10


def game_loop(canvas):
    render_field(canvas)
    
TD_config(250.0, WIDTH/2, HEIGHT/2)

frame = simplegui.create_frame("", WIDTH, HEIGHT)
frame.set_draw_handler(game_loop)
frame.set_keydown_handler(key_handler)

frame.start()
