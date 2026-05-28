import sys
import math
import pygame
import pyautogui
import pygetwindow

# CONSTANTS YOU CAN CHANGE
TICKRATE = 60
WINDOW_SIDE_SIZE = 1000  # WINDOW IS SQUARED
COLOR_SPEED = 2
MOVING_SPEED = 5
WINDOW_TITLE = "Cube"


# INITIALIZATION PART
dx = WINDOW_SIDE_SIZE // 2
dy = WINDOW_SIDE_SIZE // 2
cube_coordinates = []
rainbow_red = 0
rainbow_green = 0
rainbow_blue = 0
fun = False
pixel_set = set()

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIDE_SIZE, WINDOW_SIDE_SIZE))
pygame.display.set_caption(WINDOW_TITLE)

# CREATING ALL DOTS FOR THE CUBE
for cube_x in 1, 0:
    for cube_y in 1, 0:
        for cube_z in 1, 0:
            cube_coordinates.append(
                (-100 + cube_x * 200, -100 + cube_y * 200, -100 + cube_z * 200)
            )


def x_matrix_transformation(point, angle):
    x, y, z = point[0], point[1], point[2]
    return (
        x,
        z * math.sin(angle) + y * math.cos(angle),
        z * math.cos(angle) - y * math.sin(angle),
    )


def y_matrix_transformation(point, angle):
    x, y, z = point[0], point[1], point[2]
    return (
        x * math.cos(angle) + z * math.sin(angle),
        y,
        z * math.cos(angle) - x * math.sin(angle),
    )


def z_matrix_transformation(point, angle):
    x, y, z = point[0], point[1], point[2]
    return (
        x * math.cos(angle) + y * math.sin(angle),
        x * (-1) * math.sin(angle) + y * math.cos(angle),
        z,
    )


def draw_line(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    angle = math.atan2(x2 - x1, y2 - y1)
    length = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    if length == 0:
        return
    for d in range(1, length + 1):
        x = x1 + d * math.sin(angle)
        y = y1 + d * math.cos(angle)
        drawen_part = d / length
        z = z1 + (z2 - z1) * drawen_part
        set_pixel(x, y, z)


def set_pixel(x, y, z):
    brightness = max(0.0, min(1.0, (z + 200) / 300))
    if fun:
        r = int(rainbow[0] * brightness)
        g = int(rainbow[1] * brightness)
        b = int(rainbow[2] * brightness)
        pixel_set.add(((int(x), int(y)), (r, g, b)))
    else:
        c = int(255 * brightness)
        pixel_set.add(((int(x), int(y)), (c, c, c)))


print("It follows your every movement... But you still can OLEG for fun!")

clock = pygame.time.Clock()

base_coordinates = cube_coordinates.copy()

# MAIN PART
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # UPDATING SCRIPT
    pygame.display.flip()
    screen.fill((0, 0, 0))

    # KEY DETECTING PART
    keys = pygame.key.get_pressed()

    ##MOVING
    if keys[pygame.K_LEFT]:
        dx -= MOVING_SPEED
    if keys[pygame.K_UP]:
        dy -= MOVING_SPEED
    if keys[pygame.K_DOWN]:
        dy += MOVING_SPEED
    if keys[pygame.K_RIGHT]:
        dx += MOVING_SPEED

    ##FUN ACTIVATION
    if keys[pygame.K_o]:
        if keys[pygame.K_l]:
            if keys[pygame.K_e]:
                if keys[pygame.K_g]:
                    fun = True

    # CALCULATING ROTATION ANGLE
    mouse_x, mouse_y = pyautogui.position()
    mouse_coordinates = (mouse_x, mouse_y, 100)
    window = pygetwindow.getWindowsWithTitle(WINDOW_TITLE)[0]
    window_center_x, window_center_y = window.center
    angle_y = math.atan2(window_center_x - mouse_x - WINDOW_SIDE_SIZE // 2 + dx, dx) * (-1)
    angle_x = math.atan2(window_center_y - mouse_y - WINDOW_SIDE_SIZE // 2 + dy, dy) * (-1)

    # ROTATING
    for index, _ in enumerate(cube_coordinates):
        cube_point = base_coordinates[index]
        cube_point = x_matrix_transformation(cube_point, angle_x)
        cube_point = y_matrix_transformation(cube_point, angle_y)
        cube_coordinates[index] = cube_point

    # FUN COLOR
    rainbow = (
        int(127.5 * math.sin(rainbow_red / 127.5) + 127.5),
        int(127.5 * math.sin(rainbow_green / 127.5 - 42.5) + 127.5),
        int(127.5 * math.sin(rainbow_blue / 127.5 + 42.5) + 127.5),
    )
    rainbow_red = (rainbow_red + COLOR_SPEED) % (math.pi * 255)
    rainbow_green = (rainbow_green + COLOR_SPEED) % (math.pi * 255)
    rainbow_blue = (rainbow_blue + COLOR_SPEED) % (math.pi * 255)

    # DRAWING
    points = []
    for cube_point_coordinate in cube_coordinates:
        points.append(
            (
                cube_point_coordinate[0] + dx,
                cube_point_coordinate[1] + dy,
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

    sorted_data = sorted(pixel_set, key=lambda item: item[1])

    for cube_point in sorted_data:
        screen.set_at(cube_point[0], cube_point[1])
    pixel_set.clear()
    clock.tick(TICKRATE)
