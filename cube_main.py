import sys
import math
import pygame

TICKRATE = 200
WINDOW_SIDE = 1000
CUBE_ROTATION_SPEED = 40
COLOR_SPEED = 40
CUBE_SPEED = 40
WINDOW_TITLE = "Cube"
LIGHT_AREA = 350
LIGHT_START_CORDS = (500,500,0)
LIGHT_SPEED = 40
LIGHT_RADIUS = 20
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
FOV = 300
DEPTH = 300


triangles_vertices_indexes = [
    [6, 2, 0], [6, 0, 4], # Передняя грань (+Z)
    [3, 7, 5], [3, 5, 1], # Задняя грань (-Z)
    [2, 3, 1], [2, 1, 0], # Правая грань (+X)
    [7, 6, 4], [7, 4, 5], # Левая грань (-X)
    [7, 3, 2], [7, 2, 6], # Верхняя грань (-Y)
    [4, 0, 1], [4, 1, 5]  # Нижняя грань (+Y)
]
last_pressed = ''
light_coordinates = LIGHT_START_CORDS
coordinates_center = WINDOW_SIDE//2
cube_offset_x = 0
cube_offset_y = 0
cube_offset_z = 0
cube_coordinates = []
rainbow_red = 0
rainbow_green = 0
rainbow_blue = 0
fun = False
points_to_print = set()
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
            if 0 <= x < WINDOW_SIDE and 0 <= y < WINDOW_SIDE:
                if z_buffer[y*WINDOW_SIDE+x] < z+DEPTH:
                    z_buffer[y*WINDOW_SIDE+x] = z+DEPTH
                    pixels[x][y] = color

def put_pixel(x, y, z, color):
        xl, yl, zl = light_coordinates
        if 0 <= x < WINDOW_SIDE and 0 <= y < WINDOW_SIDE:
            idx = y * WINDOW_SIDE + x
            if z_buffer[idx] < z+DEPTH:
                z_buffer[idx] = z+DEPTH

                distance_to_light = math.sqrt((x - xl)**2 + (y - yl)**2 + (z - zl)**2)
                brightness = max(min(1, 1 - distance_to_light / LIGHT_AREA), 0.08)
                if fun:
                    r = int(rainbow[0] * brightness)
                    g = int(rainbow[1] * brightness)
                    b = int(rainbow[2] * brightness)
                else:
                    r = int(color[0] * brightness)
                    g = int(color[1] * brightness)
                    b = int(color[2] * brightness)
                pixels[x][y] = (r,g,b)

def draw_line(point1, point2, color):
    x1, y1, z1 = int(point1[0]), int(point1[1]), int(point1[2])
    x2, y2, z2 = int(point2[0]), int(point2[1]), int(point2[2])

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    sz = 1 if z1 < z2 else -1

    if dx >= dy and dx >= dz:
        err_1 = 2 * dy - dx
        err_2 = 2 * dz - dx
        for _ in range(dx + 1):
            put_pixel(x1, y1, z1, color)
            if err_1 > 0:
                y1 += sy
                err_1 -= 2 * dx
            if err_2 > 0:
                z1 += sz
                err_2 -= 2 * dx
            err_1 += 2 * dy
            err_2 += 2 * dz
            x1 += sx

    elif dy >= dx and dy >= dz:
        err_1 = 2 * dx - dy
        err_2 = 2 * dz - dy
        for _ in range(dy + 1):
            put_pixel(x1, y1, z1, color)
            if err_1 > 0:
                x1 += sx
                err_1 -= 2 * dy
            if err_2 > 0:
                z1 += sz
                err_2 -= 2 * dy
            err_1 += 2 * dx
            err_2 += 2 * dz
            y1 += sy

    else:
        err_1 = 2 * dy - dz
        err_2 = 2 * dx - dz
        for _ in range(dz + 1):
            put_pixel(x1, y1, z1, color)
            if err_1 > 0:
                y1 += sy
                err_1 -= 2 * dz
            if err_2 > 0:
                x1 += sx
                err_2 -= 2 * dz
            err_1 += 2 * dy
            err_2 += 2 * dx
            z1 += sz

print("Rotate cube on WASDQE. Move on ARROWS and OP. Move light on TFGHRY. OLEG for fun")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            last_pressed += pygame.key.name(event.key)
            if len(last_pressed)>4:
                last_pressed = last_pressed[1:5]

    screen.fill((0, 0, 0))
    pixels = pygame.PixelArray(screen)
    z_buffer=[float("-Infinity") for _ in range(WINDOW_SIDE*WINDOW_SIDE)]

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        cube_offset_x -= CUBE_SPEED
    if keys[pygame.K_UP]:
        cube_offset_y -= CUBE_SPEED
    if keys[pygame.K_DOWN]:
        cube_offset_y += CUBE_SPEED
    if keys[pygame.K_RIGHT]:
        cube_offset_x += CUBE_SPEED
    if keys[pygame.K_o]:
        cube_offset_z -= CUBE_SPEED
    if keys[pygame.K_p]:
        cube_offset_z += CUBE_SPEED
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

    if last_pressed == 'oleg':
        fun = True

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
        cube_point_x = cube_point_coordinate[0] - coordinates_center  + cube_offset_x
        cube_point_y = cube_point_coordinate[1] - coordinates_center + cube_offset_y
        cube_point_z = cube_point_coordinate[2] + cube_offset_z
        points.append(
            (
                cube_point_x * FOV / (DEPTH - cube_point_z) + coordinates_center,
                cube_point_y * FOV / (DEPTH - cube_point_z) + coordinates_center,
                cube_point_z,
            )
        )
    for triangle in triangles_vertices_indexes:
        xA, yA, zA = points[triangle[0]]
        xB, yB, zB = points[triangle[1]]
        xC, yC, zC = points[triangle[2]]
        min_x = int(min(xA,xB,xC))
        max_x = int(max(xA,xB,xC))+1
        min_y = int(min(yA,yB,yC))
        max_y = int(max(yA,yB,yC))+1
        determinant = (yB - yC) * (xA - xC) + (xC - xB) * (yA - yC)
        if int(determinant) <= 0:
            continue
        for x in range(min_x+1, max_x+1):
            for y in range(min_y+1, max_y+1):
                w1 = ((yB - yC) * (x - xC) + (xC - xB) * (y - yC))/determinant
                w2 = ((yC - yA) * (x - xC) + (xA - xC) * (y - yC))/determinant
                w3 = 1 - w1 - w2
                z = w1 * zA + w2 * zB + w3 * zC
                if w1 >= 0 and w2 >= 0 and w3>=0:
                    put_pixel(x, y, z, WHITE)

                
    # for point_x, point_y in (
    #     (0, 1),
    #     (0, 2),
    #     (0, 4),
    #     (1, 3),
    #     (1, 5),
    #     (2, 3),
    #     (2, 6),
    #     (3, 7),
    #     (4, 6),
    #     (4, 5),
    #     (5, 7),
    #     (6, 7),
    # ):
    #     draw_line(points[point_x], points[point_y], RED)

    light_color_brightness=max(min(1,light_coordinates[2]/100),0.07)
    light_color=(
        YELLOW[0]*light_color_brightness,
        YELLOW[1]*light_color_brightness,
        YELLOW[2]*light_color_brightness
    )

    draw_full_circle(light_coordinates,LIGHT_RADIUS,light_color)

    del pixels
    pygame.display.flip()
    clock.tick(TICKRATE)
