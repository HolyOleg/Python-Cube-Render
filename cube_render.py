import sys
import math
import pygame
import pyautogui
import pygetwindow

#VARIABLES YOU CAN CHANGE
tickrate=60
window_side_size=1000 #WINDOW IS SQUARED
rotation_speed=1
color_speed=2
moving_speed=1

#CONSTANTS
dx=window_side_size//2
dy=window_side_size//2
radian=math.radians(rotation_speed)


#INITIALIZATION PART
coordinates=[]
rainbow_red=0
rainbow_green=0
rainbow_blue=0
fun=False
pixel_set=set()

pygame.init()
screen = pygame.display.set_mode((window_side_size, window_side_size))
window_title = 'Cube'
pygame.display.set_caption(window_title)

#CREATING ALL DOTS FOR THE CUBE
for x in 1,0:
    for y in 1,0:
        for z in 1,0:
            coordinates.append((-100+x*200,-100+y*200,-100+z*200))

def x_matrix_transformation(coordinates,angle):
    x,y,z=coordinates[0],coordinates[1],coordinates[2]
    return (x,
            z*math.sin(angle)+y*math.cos(angle),
            z*math.cos(angle)-y*math.sin(angle))
    
def y_matrix_transformation(coordinates,angle):
    x,y,z=coordinates[0],coordinates[1],coordinates[2]
    return (x*math.cos(angle)+z*math.sin(angle),
            y,
            z*math.cos(angle)-x*math.sin(angle))
def z_matrix_transformation(coordinates,angle):
    x,y,z=coordinates[0],coordinates[1],coordinates[2]
    return (x*math.cos(angle)+y*math.sin(angle),
            x*(-1)*math.sin(angle)+y*math.cos(angle),
            z)
def draw_line(point1,point2):
    x1,y1,z1=point1
    x2,y2,z2=point2
    angle=math.atan2(x2-x1,y2-y1)
    length=int(math.sqrt((x2-x1)**2+(y2-y1)**2))
    if length==0:
        return
    for d in range(1,length+1):
        x=x1+d * math.sin(angle)
        y=y1+d * math.cos(angle)
        t = d / length
        z = z1 + (z2 - z1) * t
        brightness = max(0.0, min(1.0, (z + 200) / 300))
        if fun:
            r = int(RAINBOW[0] * brightness)
            g = int(RAINBOW[1] * brightness)
            b = int(RAINBOW[2] * brightness)
            pixel_set.add(((int(x), int(y)), (r, g, b)))
        else:
            c = int(255 * brightness)
            pixel_set.add(((int(x), int(y)), (c, c, c)))

print('It follows your every movement... But you still can OLEG for fun!')

clock = pygame.time.Clock()

base_coordinates=coordinates.copy()

#MAIN PART
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #UPDATING SCRIPT
    pygame.display.flip()
    screen.fill((0,0,0))
    
    #KEY DETECTING PART
    keys = pygame.key.get_pressed()

    ##MOVING
    if keys[pygame.K_LEFT]:
        dx-=moving_speed
    if keys[pygame.K_UP]:
        dy-=moving_speed
    if keys[pygame.K_DOWN]:
        dy+=moving_speed
    if keys[pygame.K_RIGHT]:
        dx+=moving_speed

    ##FUN ACTIVATION
    if keys[pygame.K_o]:
        if keys[pygame.K_l]:
            if keys[pygame.K_e]:
                if keys[pygame.K_g]:
                    fun=True

    #CALCULATING ROTATION ANGLE
    mouse_x, mouse_y = pyautogui.position()
    mouse_coordinates=(mouse_x,mouse_y,100)
    window = pygetwindow.getWindowsWithTitle(window_title)[0]
    window_center_x, window_center_y = window.center
    angle_y=math.atan2(window_center_x-mouse_x,dx)*(-1)
    angle_x=math.atan2(window_center_y-mouse_y,dy)*(-1)
    
    #ROTATING
    for point_index in range(len(coordinates)):
        point=base_coordinates[point_index]
        point=x_matrix_transformation(point,angle_x)
        point=y_matrix_transformation(point,angle_y)
        coordinates[point_index]=point

    #FUN COLOR
    RAINBOW= (
        int(127.5*math.sin(rainbow_red/127.5)+127.5),
        int(127.5*math.sin(rainbow_green/127.5-42.5)+127.5),
        int(127.5*math.sin(rainbow_blue/127.5+42.5)+127.5))
    rainbow_red=(rainbow_red+color_speed)%(math.pi*255)
    rainbow_green=(rainbow_green+color_speed)%(math.pi*255)
    rainbow_blue=(rainbow_blue+color_speed)%(math.pi*255)

    #DRAWING
    points=[]
    for index in range(len(coordinates)):
        points.append((coordinates[index][0]+dx, coordinates[index][1]+dy, coordinates[index][2]))
    for a,b in ((0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),(3,7),(4,6),(4,5),(5,7),(6,7),(0,6),(2,4)):
        draw_line(points[a], points[b])

    sorted_data = sorted(pixel_set, key=lambda item: item[1])

    for point in sorted_data:
        screen.set_at(point[0],point[1])
    pixel_set.clear()
    clock.tick(tickrate)