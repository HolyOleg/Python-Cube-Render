import sys
import math
import pygame

message='Rotate on WASD. Move on ARROWS. OLEG for fun'
tickrate=200
side=1000
coordinates=[]
degree=1
radian=math.radians(degree)
color_speed=2
color1=0
color2=0
color3=0
delta=1
dx=side//2
dy=side//2
fun=False
pixel_set=set()

pygame.init()
screen = pygame.display.set_mode((side, side))
pygame.display.set_caption("Cube")
window_title = 'Cube'

for x in 1,0:
    for y in 1,0:
        for z in 1,0:
            coordinates.append((-100+x*200,-100+y*200,-100+z*200))

WHITE = (255, 255, 255)
BLACK = (0,0,0)



def line(point1,point2):
    x1=point1[0]
    y1=point1[1]
    z1=point1[2]
    x2=point2[0]
    y2=point2[1]
    z2=point2[2]
    angle=math.atan2(x2-x1,y2-y1)
    length=int(math.sqrt((x2-x1)**2+(y2-y1)**2))
    if length==0:
        return
    for d in range(1,length+1):
        x=int(x1+d * math.sin(angle))
        y=int(y1+d * math.cos(angle))
        t = d / length
        z = z1 + (z2 - z1) * t
        brightness = max(0.0, min(1.0, (z + 200) / 300))
        if fun:
            r = int(RAINBOW[0] * brightness)
            g = int(RAINBOW[1] * brightness)
            b = int(RAINBOW[2] * brightness)
            pixel_set.add(((x, y), (r, g, b)))
        else:
            c = int(255 * brightness)
            pixel_set.add(((x, y), (c, c, c)))

print(message)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    screen.fill(BLACK)
    
    keys = pygame.key.get_pressed()

    #MOVING
    if keys[pygame.K_LEFT]:
        dx-=delta
    if keys[pygame.K_UP]:
        dy-=delta
    if keys[pygame.K_DOWN]:
        dy+=delta
    if keys[pygame.K_RIGHT]:
        dx+=delta

    #FUN ACTIVATION
    if keys[pygame.K_o]:
        if keys[pygame.K_l]:
            if keys[pygame.K_e]:
                if keys[pygame.K_g]:
                    fun=True
    
    #ROTATING
    for dot_index in range(len(coordinates)):
        dot=coordinates[dot_index]
        #Z-AXIS
        if keys[pygame.K_d]:
            dot=(dot[0]*math.cos(radian)-dot[1]*math.sin(radian),
                 dot[0]*math.sin(radian)+dot[1]*math.cos(radian),
                 dot[2])
        if keys[pygame.K_a]:
            dot=(dot[0]*math.cos(radian)+dot[1]*math.sin(radian),
                 dot[0]*math.sin(radian)*(-1)+dot[1]*math.cos(radian),
                 dot[2])
        #X-AXIS
        if keys[pygame.K_s]:
            dot=(dot[0],
                 dot[1]*math.cos(radian)+dot[2]*math.sin(radian),
                 dot[1]*math.sin(radian)*(-1)+dot[2]*math.cos(radian))
        if keys[pygame.K_w]:
            dot=(dot[0],
                 dot[1]*math.cos(radian)-dot[2]*math.sin(radian),
                 dot[1]*math.sin(radian)+dot[2]*math.cos(radian))
        #Z-AXIS
        if keys[pygame.K_q]:
            dot=(dot[0]*math.cos(radian)-dot[2]*math.sin(radian),
                dot[1],
                dot[0]*math.sin(radian)+dot[2]*math.cos(radian))
        if keys[pygame.K_e]:
            dot=(dot[0]*math.cos(radian)+dot[2]*math.sin(radian),
                dot[1],
                dot[0]*math.sin(radian)*(-1)+dot[2]*math.cos(radian))
        coordinates[dot_index]=dot

    #FUN COLOR
    RAINBOW= (int(127.5*math.sin(color1/127.5)+127.5),int(127.5*math.sin(color2/127.5-42.5)+127.5),int(127.5*math.sin(color3/127.5+42.5)+127.5))
    color1=(color1+color_speed)%(math.pi*255)
    color2=(color2+color_speed)%(math.pi*255)
    color3=(color3+color_speed)%(math.pi*255)

    #DRAWING
    dots=[]
    for i in range(len(coordinates)):
        dots.append((coordinates[i][0]+dx, coordinates[i][1]+dy, coordinates[i][2]))
    for a,b in ((0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),(3,7),(4,6),(4,5),(5,7),(6,7)):
        line(dots[a], dots[b])

    sorted_data = sorted(pixel_set, key=lambda item: item[1])

    for pixel in sorted_data:
        screen.set_at(pixel[0],pixel[1])
    pixel_set.clear()


    clock.tick(tickrate)