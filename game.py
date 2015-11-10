import simplegui
import math
import random

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
            self.x, self.y, self.z = draw_engine.ThreeDPoint(self.x+x_change,self.y+y_change,self.z+z_change).get_rotated(self.x_rotate, self.y_rotate, self.z_rotate, self.x, self.y, self.z)
            
        def turn(self, x_change, y_change, z_change):
            self.x_rotate += x_change
            self.y_rotate += y_change
            self.z_rotate += z_change
            
    def __init__(self, fl, vpX, vpY, cam):
        self.focalLength = fl
        self.vanishingPointX, self.vanishingPointY = vpX, vpY
        self.camera = cam 
    
    #3D Point - immutable
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
        
            cos_x = math.cos(angle_x)
            sin_x = math.sin(angle_x)
            cos_y = math.cos(angle_y)
            sin_y = math.sin(angle_y)
            cos_z = math.cos(angle_z)
            sin_z = math.sin(angle_z)
            
            y = (y - center_y) * cos_x - (z - center_z) * sin_x + center_y
            z = (z - center_z) * cos_x + (y - center_y) * sin_x + center_z
            
            x = (x - center_x) * cos_y - (z - center_z) * sin_y + center_x
            z = (z - center_z) * cos_y + (x - center_x) * sin_y + center_z
            
            
            x = (x - center_x) * cos_z - (y - center_y) * sin_z + center_x
            y = (y - center_y) * cos_z + (x - center_x) * sin_z + center_y
            
            return draw_engine.ThreeDPoint(x,y,z)


            #transforms 3D world point to 2D screen cordinates
        def transform(self):
            global draw_engine
            
            x_rotate = draw_engine.camera.x_rotate
            y_rotate = draw_engine.camera.y_rotate
            z_rotate = draw_engine.camera.z_rotate
            
            #should rotate around the camera
            #I dont understand why this works but rotating around this point dosnt
            x = self.x + draw_engine.camera.x
            y = self.y + draw_engine.camera.y 
            z = self.z + draw_engine.camera.z
            
            x,y,z = draw_engine.ThreeDPoint(x,y,z).get_rotated(x_rotate, y_rotate, z_rotate, 0, 0, -draw_engine.focalLength)
            
            scale = draw_engine.focalLength/(draw_engine.focalLength + z)
            newX = draw_engine.vanishingPointX + x * scale
            newY = draw_engine.vanishingPointY + y * scale

            return draw_engine.TwoDPoint(newX, newY, scale)
            
        def draw(self, canvas):
            line_width = 5 #placeholder
            radius = 5
            xNew, yNew, scale = self.transform(draw_engine.camera.X_rotate, draw_engine.camera.Y_rotate, draw_engine.camera.Z_rotate)
            canvas.draw_circle((xNew, yNew), radius * scale, line_width, 'White','Grey')
    
    #immutable?
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
            
            self.color_r = random.randrange(100,255)
            self.color_g = random.randrange(100,255)
            self.color_b = random.randrange(100,255)

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
            
            #need to figure out this
            #if plane intersects veiwplane: oh no!
            if z1 > 0 and z2 > 0 and z3 > 0 and z4 > 0:
                canvas.draw_polygon( [(x1, y1), 
                                      (x2, y2), 
                                      (x3, y3), 
                                      (x4, y4)], line_thinkness, 'White',"rgb("+str(self.color_r)+","+str(self.color_g)+","+str(self.color_b)+")")

#ISSUES:
# - When looking at things backwords ( i. e. in more negative z then object looking direction negative z)
#       objects are malformed
# - issue when objects

render_list = list()
    
WIDTH = 1200
HEIGHT = 400

draw_engine = DrawEngine(200.0, WIDTH/2, HEIGHT/2, DrawEngine.Camera(0,0,0,0,0,0))
        
#Maze Gen code from http://rosettacode.org/wiki/Maze_generation#Python
def make_maze(w = 16, h = 8):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
 
    def walk(x, y):
        vis[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)
 
    walk(random.randrange(w), random.randrange(h))
    
    #for a in 
    rtr = ""
    for (a, b) in zip(hor, ver):
        rtr += ''.join(a + ['\n'] + b) + '\n'
    return rtr
 
n = 3
maze = make_maze(n,n)

print maze

l = 100
for y in range(0,n):
    for x in range(0,n):
        b = draw_engine.ThreeDPoint(0+x*l, l, 0+y*l)
        a = draw_engine.ThreeDPoint(l+x*l, l, 0+y*l)
        c = draw_engine.ThreeDPoint(0+x*l, l, l+y*l)
        d = draw_engine.ThreeDPoint(l+x*l, l, l+y*l)
    
        render_list.append(draw_engine.ThreeDQuad(a, b, c, d)) #bottem
        
for row in range(0,n):
    for x in range(0,n-1):
        c = draw_engine.ThreeDPoint(x*l, l, row*l)
        g = draw_engine.ThreeDPoint((x+1)*l, l, row*l)
        
        d = draw_engine.ThreeDPoint((x+1)*l, 0, row*l)
        h = draw_engine.ThreeDPoint(x*l, 0, row*l)
        
        if row == 0 or row == n-1 or maze[2*row*(n*3+2)+3*x + 1] == '-':
            render_list.append(draw_engine.ThreeDQuad(a, b, c, d))
        
        
       # if x == n-1: # or maze[2*y*(n*3+2)+3*x + 1] == '-':
        #    render_list.append(draw_engine.ThreeDQuad(d, h, g, c))
            
      #  if x == 0 or maze[2*y*(n*3+2)+3*x - 1] == '-':
      #      render_list.append(draw_engine.ThreeDQuad(b, f, e, a))
            
            
        #render_list.append(draw_engine.ThreeDQuad(a, e, h, d)) #top
        
      #  if (2*y+1)*(n*3+2)+3*x < len(maze):
      #      print str(x) + " " + str(y) + " " + maze[2*(y+1)*(n*3+2)+3*x]
            
        #if (2*y+1)*(n*3+2)+3*x < len(maze) :
       #     if maze[(2*y+1)*(n*3+2)+3*x] == '|':
       #          render_list.append(draw_engine.ThreeDQuad(a, b, c, d))
      #  else:
      #      render_list.append(draw_engine.ThreeDQuad(a, b, c, d))
        
      #  if (2*y-1)*(n*3+2)+3*x > 0 :
      #      if maze[(2*y-1)*(n*3+2)+3*x] == '-':
      #          render_list.append(draw_engine.ThreeDQuad(h, g, f, e))
      #  else:
      #      render_list.append(draw_engine.ThreeDQuad(h, g, f, e))





def render_field(canvas):
    global render_list
    
    render_list.sort()
    
    for thing in render_list:
        thing.draw(canvas)
          
def key_handler(key):
    global Z_rotate_angle, X_rotate_angle, Y_rotate_angle,draw_engine
 
    if key == simplegui.KEY_MAP["up"]:
        draw_engine.camera.turn(math.pi * 0.025,0,0)
    if key == simplegui.KEY_MAP["down"]:
        draw_engine.camera.turn(math.pi * -0.025,0,0)
    if key == simplegui.KEY_MAP["left"]:
        draw_engine.camera.turn(0,math.pi * 0.025,0)
    if key == simplegui.KEY_MAP["right"]:
        draw_engine.camera.turn(0,math.pi * -0.025,0)
    if key == simplegui.KEY_MAP["o"]:
        draw_engine.camera.turn(0,0,math.pi * 0.025)
    if key == simplegui.KEY_MAP["p"]:
        draw_engine.camera.turn(0,0,math.pi * -0.025)
        
        
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
