
import simplegui
import math

def TD_config(fl=250, vpX=0, vpY=0):
    global focalLength,vanishingPointX,vanishingPointY
    focalLength = fl
    vanishingPointX, vanishingPointY = vpX, vpY
    

X_rotate_angle = 0.0
Y_rotate_angle = 0.0
Z_rotate_angle = 0.0

# Calculate point position by transforming the 3D coordinates to 2D
def TD_calculate_point_position(x, y, z):
    global focalLength,vanishingPointX,vanishingPointY, X_rotate_angle, Y_rotate_angle, Z_rotate_angle
    
    y,z = TD_func_rotateX(y, z, X_rotate_angle, 0, 0)
    x,z = TD_func_rotateY(x, z, Y_rotate_angle, 0, 0)
    x,y = TD_func_rotateZ(x, y, Z_rotate_angle, 0, 0)
    
    
    scale = abs(focalLength/(focalLength + z))
    newX = vanishingPointX + x * scale
    newY = vanishingPointY + y * scale
    
    
    return (newX, newY, scale)

# Checks if it's the backface
def TD_is_back_face(sx1, sy1, sx2, sy2, sx3, sy3):
    global focalLength,vanishingPointX,vanishingPointY
    cax = sx3 - sx1
    cay = sy3 - sy1
    bcx = sx2 - sx3
    bcy = sy2 - sy3
    return cax * bcy > cay * bcx

# Draws a 2D Circle
def TD_draw_circle2D(canvas, x, y, z, radius, segments):
    global focalLength,vanishingPointX,vanishingPointY
    xNew, yNew, scale = TD_calculate_point_position(x, y, z)
    
    line_width = 5 #placeholder
    
    canvas.draw_circle((xNew, yNew), radius * scale, line_width, 'Green', 'Green')
    
   # love.graphics.circle(mode, xNew, yNew, radius * scale, segments)


# Draws a quadrilateral
def TD_graphics_quad(canvas, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
    global focalLength,vanishingPointX,vanishingPointY
    x1New, y1New = TD_calculate_point_position(x1, y1, z1)
    x2New, y2New = TD_calculate_point_position(x2, y2, z2)
    x3New, y3New = TD_calculate_point_position(x3, y3, z3)
    x4New, y4New = TD_calculate_point_position(x4, y4, z4)
    canvas.draw_polygon( [(x1New, y1New), 
                         (x2New, y2New), 
                         (x3New, y3New), 
                         (x4New, y4New)], 2, 'White','Grey')

    # love.graphics.quad(mode, x1New, y1New, x2New, y2New, x3New, y3New, x4New, y4New)

# Draws a triangle
def TD_graphics_triangle(canvas, bfc, x1, y1, z1, x2, y2, z2, x3, y3, z3):
    global focalLength,vanishingPointX,vanishingPointY
    x1New, y1New = love3D.calculatePointPosition(x1, y1, z1)
    x2New, y2New = love3D.calculatePointPosition(x2, y2, z2)
    x3New, y3New = love3D.calculatePointPosition(x3, y3, z3)
    if bfc and TD_is_back_face(x1New, y1New, x2New, y2New, x3New, y3New):
        return
    
    canvas.draw_polygon([(x1New, y1New), (x2New, y2New), (x3New, y3New)], 12, 'Green')

# Draws a 2D Line segment
def TD_graphics_lineSegment2D(canvas, width, x1, y1, z1, x2, y2, z2):
    global focalLength,vanishingPointX,vanishingPointY
    x1New, y1New = love3D.calculatePointPosition(x1, y1, z1)
    x2New, y2New = love3D.calculatePointPosition(x2, y2, z2)
    
    canvas.draw_line((x1New, y1New), (x2New, y2New), width, 'Red')

# Draws a 2D drawable, isScaling determines whether the drawable will be scaled according to the Z position
def TD_graphics_draw2D(drawable, x, y, z, r, sx, sy, ox, oy, isScaling):
    global focalLength,vanishingPointX,vanishingPointY
    xNew, yNew, scale = love3D.calculatePointPosition(x, y, z)
    if isScaling :
        love.graphics.draw(drawable, xNew, yNew, r, sx * scale, sy * scale, ox, oy)
    else:
        love.graphics.draw(drawable, xNew, yNew, r, sx, sy, ox, oy)

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


# Checks 3D distance collision
def TD_func_checkDistCollision(ax, ay, az, ar, bx, by, bz, br):
    global focalLength,vanishingPointX,vanishingPointY
    dx = bx - ax
    dy = by - ay
    dz = bz - az
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    return dist < ar + br

# Finds the average Z
def TD_func_getAvgZTriangle(az, bz, cz):
    global focalLength,vanishingPointX,vanishingPointY
    avgZ = (az + bz + cz)/3
    return avgZ


def TD_func_getAvgZQuad(az, bz, cz, dz):
    global focalLength,vanishingPointX,vanishingPointY
    avgZ = (az + bz + cz + dz)/4
    return avgZ

# Sorts which triangle/quadrilateral face goes in front, and goes in back
def TD_func_zSortTriangle(triangleTable, verticesTable):
    global focalLength,vanishingPointX,vanishingPointY
    for i, v in ipairs(triangleTable) :
        v.avgZ = TD_func_getAvgZTriangle(verticesTable[v[1]].z, verticesTable[v[2]].z, verticesTable[v[3]].z)
    #table.sort(triangleTable, function(A, B) return A.avgZ > B.avgZ end)
    #???
    
def TD_func_zSortTriangle2(triangleTable, verticesTable):
    global focalLength,vanishingPointX,vanishingPointY
    for i, v in ipairs(triangleTable) :
        v.minZ = math.min(verticesTable[v[1]].z, verticesTable[v[2]].z, verticesTable[v[3]].z)
    #???
    #table.sort(triangleTable, function(A, B) return A.minZ > B.minZ end)


def TD_func_zSortQuad(quadTable, verticesTable):
    global focalLength,vanishingPointX,vanishingPointY
    for i, v in ipairs(quadTable) :
        v.avgZ = TD_func_getAvgZTriangle(verticesTable[v[1]].z, verticesTable[v[2]].z, verticesTable[v[3]].z, verticesTable[v[4]].z)
    #table.sort(quadTable, function(A, B) return A.avgZ > B.avgZ end)
    #??
    
# Sorts points according to the z position
def TD_func_zSortPoint(pointTable):
    global focalLength,vanishingPointX,vanishingPointY
    #table.sort(pointTable, function(A, B) return A.z > B.z end)
    #???
    pass
    
# Moves a shape or a table of points
def TD_func_moveShape(pointTable, x, y, z):
    global focalLength,vanishingPointX,vanishingPointY
    for i, v in ipairs(pointTable) :
        v.x = v.x + x
        v.y = v.y + y
        v.z = v.z + z

        #####################################
        
WIDTH = 1200
HEIGHT = 400

x,y,z = 0,0,0

x = 10
# Handler to draw on canvas
def render_field(canvas):
    global x, WIDTH, HEIGHT
    
    a = (0,0,0)
    b = (0,0,0)
    c =  (0,0,0)
    d =  (0,0,0)
    e =  (0,0,0)
    f =  (0,0,0)
    
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

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT)

frame.set_draw_handler(game_loop)

frame.set_keydown_handler(key_handler)

# Start the frame animation
frame.start()


