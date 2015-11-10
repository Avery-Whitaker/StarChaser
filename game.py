import simplegui
import math
import random

POLYS = True

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
        def move(self, x_change, y_change, z_change):
                                                                                                                      #WHY????
            xc, yc, zc = draw_engine.ThreeDPoint(x_change,y_change,z_change).get_rotated(self.x_rotate, self.y_rotate, math.pi-self.z_rotate, 0,0,0)
            self.x += xc
            self.y += yc
            self.z += zc
            
        #TODO Eventualy turning should be relative to self as well
        def turn(self, x_change, y_change, z_change):
            xc, yc, zc = draw_engine.ThreeDPoint(x_change,y_change,z_change).get_rotated(self.x_rotate, self.y_rotate, self.z_rotate, 0,0,0)
            
            print xc, yc, zc
           
            self.x_rotate += xc
            self.y_rotate += yc
            self.z_rotate += zc
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
                scale = 1000000000000 #some really big number
            else:
                scale = draw_engine.focalLength/(draw_engine.focalLength + z)
            newX = draw_engine.vanishingPointX + x * abs(scale)
            newY = draw_engine.vanishingPointY + y * abs(scale)

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
            self.priority = None
            
            self.color_r = random.randrange(40,60)
            self.color_g = random.randrange(40,60)
            self.color_b = random.randrange(40,60)
                    
        def pre_render(self):
            self.x1, self.y1, self.z1 = self.a.transform()
            self.x2, self.y2, self.z2 = self.b.transform()
            self.x3, self.y3, self.z3 = self.c.transform()
            self.x4, self.y4, self.z4 = self.d.transform()

            self.priority = (self.z1+self.z2+self.z3+self.z4)/4.0
            
            #???????? NO idea why this works but it does
            if self.z1 < 0 or self.z2 < 0 or self.z3 < 0 or self.z4 < 0:
                self.priority = 1000000000000

            
        #TODO implment cmp for other renderables so they all can be sorted together
        def __cmp__(self, other):
            
            if self.priority == None:
                self.pre_render()
                
            if self.priority < other.priority:
                return -1
            elif self.priority == other.priority:
                return 0
            return 1

        def draw(self, canvas):
            global draw_engine
            
            if self.priority == None:
                self.pre_render()
                
            line_thinkness = 1 # min(z1+z2+z3+z4, 10)
            
            points = [ (self.x1, self.y1, self.z1) , 
                       (self.x2, self.y2, self.z2) , 
                       (self.x3, self.y3, self.z3) , 
                       (self.x4, self.y4, self.z4) ]
            
            #Trim polygon
            if self.z1 > 0 or self.z2 > 0 or self.z3 > 0 or self.z4 > 0:
                if self.z1 < 0 or self.z2 < 0 or self.z3 < 0 or self.z4 < 0:
                    #print "In + " + str(points)
                    i = 0
                    backface = points[1][0] < points[0][0] #WRONG TODO FIX BACKFACE FGUCNTION
                    while points[i][2] < 0:
                        i = (i+1)%len(points)
                        
                    while points[i][2] > 0:
                        i = (i+1)%len(points)
                    point_a = ( ((max(points[i-1][0],points[i][0])-min(points[i][0],points[i-1][0]))*(abs(points[i][2])/( abs(points[i][2])+abs(points[i-1][2])))+min(points[i][0],points[i-1][0])),
                               ((max(points[i-1][1],points[i][1])-min(points[i][1],points[i-1][1]))*(abs(points[i][2])/( abs(points[i][2])+abs(points[i-1][2])))+min(points[i][1],points[i-1][1])),0) 
                    cut_start = i
                    while points[i][2] < 0:
                        i = (i+1)%len(points)
                    point_b = ( ((max(points[i-1][0],points[i][0])-min(points[i][0],points[i-1][0]))*(abs(points[i][2])/( abs(points[i][2])+abs(points[i-1][2])))+min(points[i][0],points[i-1][0])),
                               ((max(points[i-1][1],points[i][1])-min(points[i][1],points[i-1][1]))*(abs(points[i][2])/( abs(points[i][2])+abs(points[i-1][2])))+min(points[i][1],points[i-1][1])),0)
                    cut_end = i
                    if cut_start > cut_end:
                        for  i in range(cut_start,len(points)):
                            points.pop(cut_start)
                        for  i in range(0,cut_end):
                            points.pop(0)
                        points.insert(cut_start,point_a)
                        points.insert(cut_start,point_b)
                    else:
                        for  i in range(cut_start,cut_end):
                            points.pop(cut_start)
                    
                    if backface:
                        if point_b[0] > point_a[0]:
                            points.insert(cut_start,point_a)
                            points.insert(cut_start,point_b)
                        else:
                            points.insert(cut_start,point_b)
                            points.insert(cut_start,point_a)
                    else:
                        if point_b[0] > point_a[0]:
                            points.insert(cut_start,point_a)
                            points.insert(cut_start,point_b)
                        else:
                            points.insert(cut_start,point_b)
                            points.insert(cut_start,point_a)
                        
                        
                    #print "Out + " + str(points)

                new = []
                for point in points:
                    new.append((point[0], point[1]))
                points = new

                #if self.priority > 0:
                #brightness = 200*self.priority/draw_engine.focalLength
                brightness = 5
                #print brightness
                if brightness > 0.2:

                    if POLYS:
                        canvas.draw_polygon( points, line_thinkness, 'rba(0,0,0,0)',"rgb("+str(max(min(int(self.color_r*brightness),self.color_r),0))+","+str(max(min(int(self.color_g*brightness),self.color_g),0))+","+str(max(min(int(self.color_b*brightness),self.color_b),0))+")")
                        #                     (self.x4, self.y4)], line_thinkness, 'White',"rgb("+str(self.color_r,255)+","+str(self.color_g)+","+str(self.color_b)+")")
                    else:
                        canvas.draw_polygon( points, 5, 'rgba(255,255,255,1)',"rgba(0,0,0,0)")

        
            self.priority = None
    # END class 3D Quad
    
    #END draw engine
    
###################
#ISSUES:
# - Camera angle change wrong




#eventualy move render_list into draw engine
render_list = list()

#move into draw_engine eventauly
WIDTH = 800
HEIGHT = 800

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
 
n = 3 #maze size nxn

maze = make_maze(n,n)
print maze

l = 300 #size of each maze peice - sence only thing in world essentaily how fast you move

###Convert 2D maze to 3D Maze

#Bottom Tiles
#could be one big tile but then would render over stuff sometimes
for y in range(0,n):
    for x in range(0,n):
        render_list.append(draw_engine.ThreeDQuad(draw_engine.ThreeDPoint(l+x*l, 0, l+y*l),
                                                  draw_engine.ThreeDPoint(0+x*l, 0, l+y*l),
                                                  draw_engine.ThreeDPoint(0+x*l, 0, 0+y*l), 
                                                  draw_engine.ThreeDPoint(l+x*l, 0, 0+y*l))) #bottem
        render_list.append(draw_engine.ThreeDQuad(draw_engine.ThreeDPoint(l+x*l, l, l+y*l),
                                                  draw_engine.ThreeDPoint(0+x*l, l, l+y*l),
                                                  draw_engine.ThreeDPoint(0+x*l, l, 0+y*l), 
                                                  draw_engine.ThreeDPoint(l+x*l, l, 0+y*l))) #top

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

#Adapted from http://np6.nfshost.com/tech/coding/python/inversecircle/
def flashlgight_effect(canvas, color, center, radius, n):
    global HEIGHT, WIDTH
    left = center[0] - radius
    right = center[0] + radius
    top = center[1] - radius
    bottom = center[1] + radius
    screen_width = WIDTH
    screen_height = HEIGHT

    canvas.draw_polygon([[0, 0],         [left, 0],      [left, screen_height],  [0, screen_height]], 1, 'rgba(0,0,0,0', color)
    canvas.draw_polygon([[right, 0],     [screen_width, 0],     [screen_width, screen_height], [right, screen_height]], 1, 'rgba(0,0,0,0', color)
    canvas.draw_polygon([[left, 0],      [right, 0],      [right, top],  [left, top]], 1, 'rgba(0,0,0,0', color)
    canvas.draw_polygon([ [left, bottom], [right, bottom], [right, screen_height],  [left, screen_height] ], 1, 'rgba(0,0,0,0', color)

    #fill in the corners with pretty roundness

    # list of numbers, 0 through n - 1
    points = range(n) 

    # list of n numbers evenly distributed from 0 to 1.0 inclusive
    points = map(lambda pt: pt / (len(points) - 1.0), points) 

    # list of n radians evenly distributed from 0 to pi/4 inclusive
    points = map(lambda pt: pt * 3.1415926535 * 2 / 4, points) 

    # list of points evenly distributed around the circumference in the first quadrant of a unit circle
    points = map(lambda pt: (math.cos(pt), math.sin(pt)), points) 

    # list of points evenly distributed around the circumference of the circle of desired size centered on the origin
    points = map(lambda pt: (radius * pt[0], radius * pt[1]), points) 

    # we'll draw these points with trapezoids that connect to the 
    # top or bottom rectangle and flip them around each quadrant
    for quadrant in ((1, 1), (-1, 1), (-1, -1), (1, -1)): 
        x_flip = quadrant[0]
        y_flip = quadrant[1]
        edge = center[1] + radius * y_flip
        for i in xrange(len(points) - 1):
            A = (points[i][0] * x_flip + center[0], points[i][1] * y_flip + center[1])
            B = (points[i + 1][0] * x_flip + center[0], points[i + 1][1] * y_flip + center[1])
            A_edge = (A[0], edge)
            B_edge = (B[0], edge)

            canvas.draw_polygon((A,B,B_edge,A_edge), 1, 'rgba(0,0,0,0)',color)

def render_field(canvas):
    global render_list, a_change, a,keys_down
    
    render_list.sort()
    
    for thing in render_list:
        #Speed up by putting conditions here
        # i. e. if thing far from camera
        #if thing behind camera
        #then move things into draw functon itself
        thing.draw(canvas)
        
    #for i in range(10,40):
    #    flashlgight_effect(canvas, 'rgba(0,0,0,'+str(0.3*i/20)+')', (WIDTH/2, HEIGHT/2),WIDTH/10+WIDTH*i*0.03, 6)

    #flashlgight_effect(canvas, 'rgba(0,0,0,0.3)', (WIDTH/2, HEIGHT/2),WIDTH/7, 10)


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
        draw_engine.camera.turn(0,math.pi * -0.025,0)
    if keys_down[simplegui.KEY_MAP["right"]]:
        draw_engine.camera.turn(0,math.pi * 0.025,0)
    if keys_down[simplegui.KEY_MAP["o"]]:
        draw_engine.camera.turn(0,0,math.pi * 0.025)
    if keys_down[simplegui.KEY_MAP["p"]]:
        draw_engine.camera.turn(0,0,math.pi * -0.025)
        
    if keys_down[simplegui.KEY_MAP["w"]]:
        draw_engine.camera.move(0,0,-10) #should be relative
    if keys_down[simplegui.KEY_MAP["a"]]:
        draw_engine.camera.move(-10,0,0)
    if keys_down[simplegui.KEY_MAP["s"]]:
        draw_engine.camera.move(0,0,10)
    if keys_down[simplegui.KEY_MAP["d"]]:
        draw_engine.camera.move(10,0,0)
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
