import simplegui
import math
import random

#####################################################################
#### Class Draw Engine
# meant to encapsulate all the drawing code
# It would be preferable to have this in a seperate file and import
# it but I dont think codeskulptor supports that

#? Is there another way to seperate the rendering engine from game?
class DrawEngine:

    #TODO: Class drawable- parent class for anything that can be rendered
    #must have cmp so can decide rendeirng order (probly average depth)
    #must have draw function (duh)
    
    #### Class camera - represents users perspective in space
    # (a vector) defined by a point, angle and magnitude
    # intended to support 1st person style movement
    # i. e. can move camera relative to itself
    # and rotate
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
        #! BROKEN TODO HELP
        def move(self, x_change, y_change, z_change):
            xc, yc, zc = draw_engine.ThreeDPoint(x_change,y_change,z_change).get_rotated(self.x_rotate, self.y_rotate, self.z_rotate, 0,0,0)
            #print x_change, y_change, z_change
            self.x += xc
            self.y += yc
            self.z += zc
            
        #TODO Eventualy turning should be relative to self as well
        def turn(self, x_change, y_change, z_change):
            self.x_rotate += x_change
            self.y_rotate += y_change
            self.z_rotate += z_change
    #End Camera Class
    
    #Draw Engine init
    #Essentialy global variables
    #! Why is focalLength here? Shouldnt that be part of camera?
    def __init__(self, fl, vpX, vpY, cam):
        self.focalLength = fl
        self.vanishingPointX, self.vanishingPointY = vpX, vpY
        self.camera = cam 
    
    #### Class 3D Point
    # reperesents point in the 3D world
    # contains functions to convert to 2D screen space for rendering
    class ThreeDPoint:
        def __init__(self,x,y,z):
            self.x = x
            self.y = y
            self.z = z
        
        #? Why does this fuction exist I thought 3D point was emmutable?
        #def move(self,xChange,yChange,zChange):
        #    self.x += xChange
        #    self.y += yChange
        #    self.z += zChange

        # indexing of point [0] = x [1] = y [2] = z
        def __getitem__(self,key):
            if key == 0:
                return self.x
            if key == 1:
                return self.y
            if key == 2:
                return self.z
            
        # returns rotate form of self
        #!!! Need to test this function - could be source of bugs
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
            
            #Rotate on x
            old_y = y
            y = (y - center_y) * cos_x - (z - center_z) *     sin_x + center_y
            z = (z - center_z) * cos_x + (old_y - center_y) * sin_x + center_z
            
            #Rotate around x
            old_x = x
            x = (x - center_x) * cos_y - (z - center_z) *     sin_y + center_x
            z = (z - center_z) * cos_y + (old_x - center_x) * sin_y + center_z
            
            #Rotate around z
            old_x = x
            x = (x - center_x) * cos_z - (y - center_y) *     sin_z + center_x
            y = (y - center_y) * cos_z + (old_x - center_x) * sin_z + center_y
            
            return draw_engine.ThreeDPoint(x,y,z)


        #transforms 3D world point to 2D screen cordinates
        #! Also need to confirm its correct
        def transform(self):
            global draw_engine
            
            x_rotate = draw_engine.camera.x_rotate
            y_rotate = draw_engine.camera.y_rotate
            z_rotate = draw_engine.camera.z_rotate
            
            #should rotate around the camera
            #?!?!I dont understand why this works but rotating around this point dosnt
            
            x = self.x + draw_engine.camera.x
            y = self.y + draw_engine.camera.y 
            z = self.z + draw_engine.camera.z
            
            x,y,z = draw_engine.ThreeDPoint(x,y,z).get_rotated(x_rotate, y_rotate, z_rotate, 0, 0, -draw_engine.focalLength)
            
            #!? Why dosnt the below line do same as above???
            #x,y,z = draw_engine.ThreeDPoint(self.x,self.y,self.z).get_rotated(x_rotate, y_rotate, z_rotate, draw_engine.camera.x, draw_engine.camera.y , draw_engine.camera.z-draw_engine.focalLength)
            
            if draw_engine.focalLength + z == 0:
                scale = 100000000000000000 #some really big number
            else:
                scale = draw_engine.focalLength/(draw_engine.focalLength + z)
            newX = draw_engine.vanishingPointX + x * scale
            newY = draw_engine.vanishingPointY + y * scale

            return draw_engine.TwoDPoint(newX, newY, scale)
    #End Class ThreeDPoint
    
    
    #### Class 2D Point
    # represents a point on the screen
    # deceptive - is actualy the 2 screen demensions AND a depth demension
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
            
        #Draws point as a circle
        #size of circle defined by how far away it is
        #TODO line_width/radius/color shouldnt just be constant
        def draw(self, canvas):
            line_width = 5 #placeholder
            radius = 5
            canvas.draw_circle((self.x, self.y), radius * self.scale, line_width, 'White','Grey')
    #End Class 2D point
            
    #### Class Three D Quad
    # represents 3 demsnional quadralateral
    # supports comparision so can be sorted by rendering order
    # primary thing I expect to be drawn
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

        #TODO implment cmp for other renderables so they all can be sorted together
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
            line_thinkness = 1 # min(z1+z2+z3+z4, 10)
            
            #need to figure out this
            #if plane intersects veiwplane: oh no!
            #HELP
            if z1 > 0 and z2 > 0 and z3 > 0 and z4 > 0:
                canvas.draw_polygon( [(x1, y1), 
                                      (x2, y2), 
                                      (x3, y3), 
                                      (x4, y4)], line_thinkness, 'White',"rgb("+str(self.color_r)+","+str(self.color_g)+","+str(self.color_b)+")")
    # END class 3D Quad
    
    #END draw engine
    
###################
#ISSUES:
# - When looking at things backwords ( i. e. in more negative z then object looking direction negative z)
#       objects are malformed




#eventualy move render_list into draw engine
render_list = list()

#move into draw_engine eventauly
WIDTH = 1200
HEIGHT = 400

draw_engine = DrawEngine(500.0, WIDTH/2, HEIGHT/2, DrawEngine.Camera(0,0,0,0,0,0))
        
#Maze Gen code from http://rosettacode.org/wiki/Maze_generation#Python
##Maze gen magic
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
##End maze gen magic
 
n = 7 #maze size nxn

maze = make_maze(n,n)
print maze

l = 300 #size of each maze peice - sence only thing in world essentaily how fast you move

###Convert 2D maze to 3D Maze

#Bottom Tiles
#could be one big tile but then would render over stuff sometimes
for y in range(0,n):
    for x in range(0,n):
        render_list.append(draw_engine.ThreeDQuad(draw_engine.ThreeDPoint(l+x*l, l, l+y*l),
                                                  draw_engine.ThreeDPoint(0+x*l, l, l+y*l),
                                                  draw_engine.ThreeDPoint(0+x*l, l, 0+y*l), 
                                                  draw_engine.ThreeDPoint(l+x*l, l, 0+y*l))) #bottem
#horizontal tiles ( --- in 2D version)
for row in range(0,n+1):
    for x in range(0,n):
        if row == 0 or row == n or maze[2*row*(n*3+2)+3*x + 1] == '-':
            render_list.append(draw_engine.ThreeDQuad(draw_engine.ThreeDPoint(x*l, l, row*l), 
                                                      draw_engine.ThreeDPoint((x+1)*l, l, row*l), 
                                                      draw_engine.ThreeDPoint((x+1)*l, 0, row*l), 
                                                      draw_engine.ThreeDPoint(x*l, 0, row*l)))
#verticle tiles ( | in 2D version )     
for col in range(0,n+1):
    for y in range(0,n):
        if col == 0 or col == n or maze[(2*y+1)*(n*3+2)+3*col] == '|':
            render_list.append(draw_engine.ThreeDQuad(draw_engine.ThreeDPoint(col*l, l, y*l), 
                                                      draw_engine.ThreeDPoint(col*l, l, (y+1)*l), 
                                                      draw_engine.ThreeDPoint(col*l, 0, (1+y)*l), 
                                                      draw_engine.ThreeDPoint(col*l, 0, y*l)))
### Rendering function     
def render_field(canvas):
    global render_list
    
    render_list.sort()
    
    for thing in render_list:
        #Speed up by putting conditions here
        # i. e. if thing far from camera
        #if thing behind camera
        #then move things into draw functon itself
        thing.draw(canvas)
          
#####################################################################
#### Key handler stuff for testing
    
keys_down = {
    simplegui.KEY_MAP['up']: False,
    simplegui.KEY_MAP['down']: False,
    simplegui.KEY_MAP['left']: False,
    simplegui.KEY_MAP['right']: False,
    simplegui.KEY_MAP['o']: False,
    simplegui.KEY_MAP['p']: False,
    simplegui.KEY_MAP['w']: False,
    simplegui.KEY_MAP['a']: False,
    simplegui.KEY_MAP['s']: False,
    simplegui.KEY_MAP['d']: False,
    simplegui.KEY_MAP['q']: False,
    simplegui.KEY_MAP['e']: False
}
    
def set_keydown_handler(k):
    global keys_down
    keys_down[k] = True
    
def set_keyup_handler(k):
    global keys_down
    keys_down[k] = False
            
def key_action():
    global draw_engine,keys_down
 
    if keys_down[simplegui.KEY_MAP["up"]]:
        draw_engine.camera.turn(math.pi * 0.025,0,0)
    if keys_down[simplegui.KEY_MAP["down"]]:
        draw_engine.camera.turn(math.pi * -0.025,0,0)
    if keys_down[simplegui.KEY_MAP["left"]]:
        draw_engine.camera.turn(0,math.pi * 0.025,0)
    if keys_down[simplegui.KEY_MAP["right"]]:
        draw_engine.camera.turn(0,math.pi * -0.025,0)
    if keys_down[simplegui.KEY_MAP["o"]]:
        draw_engine.camera.turn(0,0,math.pi * 0.025)
    if keys_down[simplegui.KEY_MAP["p"]]:
        draw_engine.camera.turn(0,0,math.pi * -0.025)
        
    if keys_down[simplegui.KEY_MAP["w"]]:
        draw_engine.camera.move(0,0,-10) #should be relative
    if keys_down[simplegui.KEY_MAP["a"]]:
        draw_engine.camera.move(10,0,0)
    if keys_down[simplegui.KEY_MAP["s"]]:
        draw_engine.camera.move(0,0,10)
    if keys_down[simplegui.KEY_MAP["d"]]:
        draw_engine.camera.move(-10,0,0)
    if keys_down[simplegui.KEY_MAP["q"]]:
        draw_engine.camera.move(0,-10,0)
    if keys_down[simplegui.KEY_MAP["e"]]:
        draw_engine.camera.move(0,10,0)

#######################################################################
##### game loop and make frame
    
def game_loop(canvas):
    render_field(canvas)
    key_action()



frame = simplegui.create_frame("", WIDTH, HEIGHT)
frame.set_draw_handler(game_loop)
frame.set_keydown_handler(set_keydown_handler)
frame.set_keyup_handler(set_keyup_handler)

frame.start()
