import sys
import math
import pygame

TICKRATE = 200
WINDOW_SIDE = 1000
CUBE_ROTATION_SPEED = 1
COLOR_SPEED = 2
CUBE_SPEED = 1
WINDOW_TITLE = "Cube"
LIGHT_AREA=250
LIGHT_START_CORDS=(500,500,0)
LIGHT_SPEED=1
LIGHT_START_RADIUS=30
YELLOW=(255,255,0)
BLACK=(0,0,0)
WHITE=(255,255,255)

light_coordinates=LIGHT_START_CORDS
coordinates_center=WINDOW_SIDE//2
cube_offset_x = 0
cube_offset_y = 0
cube_coordinates = []
rainbow_red = 0
rainbow_green = 0
rainbow_blue = 0
fun = False
pixels_to_print = set()
rotation_speed_rad = math.radians(CUBE_ROTATION_SPEED)

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIDE, WINDOW_SIDE))
pygame.display.set_caption(WINDOW_TITLE)

for cube_x in 1, 0:
    for cube_y in 1, 0:
        for cube_z in 1, 0:
            cube_coordinates.append(
                (-100 + cube_x * 200 + coordinates_center,
                 -100 + cube_y * 200 + coordinates_center,
                 -100 + cube_z * 200))

def x_axis_rotation(point, angle):
    x, y, z = point
    x-=coordinates_center
    y-=coordinates_center
    return (
        x+coordinates_center,
        y * math.cos(angle) + z * math.sin(angle)+coordinates_center,
        z * math.cos(angle) - y * math.sin(angle),
    )

def y_axis_rotation(point, angle):
    x, y, z = point
    x-=coordinates_center
    y-=coordinates_center
    return (
        x * math.cos(angle) + z * math.sin(angle) + coordinates_center,
        y + coordinates_center,
        z * math.cos(angle) - x * math.sin(angle),
    )

def z_axis_rotation(point, angle):
    x, y, z = point
    x-=coordinates_center
    y-=coordinates_center
    return (
        x * math.cos(angle) + y * math.sin(angle) + coordinates_center,
        y * math.cos(angle) + x * (-1) * math.sin(angle) + coordinates_center,
        z,
    )
 
def draw_full_circle(center, radius, color):
    x_c, y_c, z = center
    for y in range(y_c - radius, y_c + radius + 1):
        dy = y - y_c
        dx = int(math.sqrt(radius**2 - dy**2))
        for x in range(x_c - dx, x_c + dx + 1):
            pixels_to_print.add(((x, y, z), color))

def draw_line(point1, point2):
    xl, yl, zl = light_coordinates
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    angle_xy = math.atan2(x2 - x1, y2 - y1)
    angle_yz = math.atan2(y2 - y1, z2 - z1)
    length = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    if length == 0:
        return
    for d in range(1, length + 1):
        x = x1 + d * math.sin(angle_xy)
        y = y1 + d * math.cos(angle_xy)
        z = z1 + d * math.cos(angle_yz)
        distance_to_light=math.sqrt((x-xl)**2+(y-yl)**2+(z-zl)**2)
        brightness = max(min(1,1-distance_to_light/LIGHT_AREA),0.08)
        if fun:
            r = int(rainbow[0] * brightness)
            g = int(rainbow[1] * brightness)
            b = int(rainbow[2] * brightness)
            pixels_to_print.add(((int(x), int(y), int(z)), (r, g, b)))
        else:
            c = int(255 * brightness)
            pixels_to_print.add(((int(x), int(y), int(z)), (c, c, c)))

print("Rotate on WASD. Move on ARROWS. OLEG for fun")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        cube_offset_x -= CUBE_SPEED
    if keys[pygame.K_UP]:
        cube_offset_y -= CUBE_SPEED
    if keys[pygame.K_DOWN]:
        cube_offset_y += CUBE_SPEED
    if keys[pygame.K_RIGHT]:
        cube_offset_x += CUBE_SPEED
    if keys[pygame.K_t]:
        light_coordinates = (light_coordinates[0],
                            light_coordinates[1]-LIGHT_SPEED,
                            light_coordinates[2])
    if keys[pygame.K_g]:
        light_coordinates = (light_coordinates[0],
                            light_coordinates[1]+LIGHT_SPEED,
                            light_coordinates[2])
    if keys[pygame.K_f]:
        light_coordinates = (light_coordinates[0]-LIGHT_SPEED,
                            light_coordinates[1],
                            light_coordinates[2])
    if keys[pygame.K_h]:
        light_coordinates = (light_coordinates[0]+LIGHT_SPEED,
                            light_coordinates[1],
                            light_coordinates[2])
    if keys[pygame.K_r]:
        light_coordinates = (light_coordinates[0],
                            light_coordinates[1],
                            light_coordinates[2]-LIGHT_SPEED)
    if keys[pygame.K_y]:
        light_coordinates = (light_coordinates[0],
                            light_coordinates[1],
                            light_coordinates[2]+LIGHT_SPEED)
 
    if keys[pygame.K_o]:
        if keys[pygame.K_l]:
            if keys[pygame.K_e]:
                if keys[pygame.K_g]:
                    fun = True

    for index, _ in enumerate(cube_coordinates):
        point = cube_coordinates[index]

        if keys[pygame.K_d]:
            point = z_axis_rotation(point,rotation_speed_rad*(-1))
        if keys[pygame.K_a]:
            point = z_axis_rotation(point,rotation_speed_rad)

        if keys[pygame.K_w]:
            point = x_axis_rotation(point,rotation_speed_rad*(-1))
        if keys[pygame.K_s]:
            point = x_axis_rotation(point,rotation_speed_rad)

        if keys[pygame.K_q]:
            point = y_axis_rotation(point,rotation_speed_rad*(-1))
        if keys[pygame.K_e]:
            point = y_axis_rotation(point,rotation_speed_rad)
        cube_coordinates[index] = point

    rainbow = (
        int(127.5 * math.sin(rainbow_red / 127.5) + 127.5),
        int(127.5 * math.sin(rainbow_green / 127.5 - 42.5) + 127.5),
        int(127.5 * math.sin(rainbow_blue / 127.5 + 42.5) + 127.5),
    )
    rainbow_red = (rainbow_red + COLOR_SPEED) % (math.pi * 255)
    rainbow_green = (rainbow_green + COLOR_SPEED) % (math.pi * 255)
    rainbow_blue = (rainbow_blue + COLOR_SPEED) % (math.pi * 255)

    points = list()
    for cube_point_coordinate in cube_coordinates:
        points.append(
            (
                cube_point_coordinate[0] + cube_offset_x,
                cube_point_coordinate[1] + cube_offset_y,
                cube_point_coordinate[2],
            )
        )
    for point_x, point_y in (
        (0, 1),
        (0, 2),
        (0, 4),
        (1, 3),
        (1, 5),
        (2, 3),
        (2, 6),
        (3, 7),
        (4, 6),
        (4, 5),
        (5, 7),
        (6, 7),
        (0, 6),
        (2, 4),
    ):
        draw_line(points[point_x], points[point_y])

    light_radius=LIGHT_START_RADIUS+light_coordinates[2]//10
    draw_full_circle(light_coordinates,light_radius,YELLOW)

    sorted_data = sorted(pixels_to_print, key=lambda item: item[0][2])
    for point in sorted_data:
        print_x=point[0][0]
        print_y=point[0][1]
        screen.set_at((print_x,print_y), point[1])
    pixels_to_print.clear()
    clock.tick(TICKRATE)
