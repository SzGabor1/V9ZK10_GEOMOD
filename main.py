import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PIL import Image

import random
def catmull_rom(p0, p1, p2, p3, t):
    t2 = t * t
    t3 = t2 * t
    x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
               (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
               (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
    y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
               (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
               (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
    return [x, y]

planet_data = {
    "sun": {"radius": 3.0, "texture": "textures/sun.jpg", "rotation_speed": 0.002},
    "earth": {"radius": 1.0, "texture": "textures/earth.jpg", "rotation_speed": 0.03},
    "mars": {"radius": 0.6, "texture": "textures/mars.jpg", "rotation_speed": 0.02},
    "venus": {"radius": 0.8, "texture": "textures/venus.jpg", "rotation_speed": 0.015},

}

def generate_random_orbit(num_points, max_radius=150, max_variation=50):
    orbit = []
    for _ in range(num_points):
        x = random.randint(-max_radius, max_radius)
        y = random.randint(-max_variation, max_variation)
        orbit.append([x, y])
    return orbit

orbits = {
    "earth": generate_random_orbit(10, max_radius=30, max_variation=10),
    "mars": generate_random_orbit(10, max_radius=40, max_variation=50),
    "venus": generate_random_orbit(10, max_radius=25, max_variation=100),

}


def generate_random_orbit(radius, num_points=12):
    return [
        [
            random.uniform(-radius, radius),
            random.uniform(-radius, radius)
        ]
        for _ in range(num_points)
    ]

def load_texture(path):
    img = Image.open(path)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGB").tobytes()
    width, height = img.size
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return texture_id

def draw_sphere(radius, texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, radius, 32, 32)

def draw_orbit(points):
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_LINE_LOOP)
    for p in points:
        glVertex3f(p[0], 0, p[1])
    glEnd()

def get_spline_position(points, t):
    segment = int(t) % len(points)
    t_frac = t - int(t)
    p0 = points[(segment - 1) % len(points)]
    p1 = points[segment % len(points)]
    p2 = points[(segment + 1) % len(points)]
    p3 = points[(segment + 2) % len(points)]
    return catmull_rom(p0, p1, p2, p3, t_frac)

def main():
    use_random_orbits = False  # Set to True to use random orbits
    pygame.init()
    display = (1000, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
    glTranslatef(0.0, 0.0, -100)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    camera_pos = [0.0, -2.0, -50]
    camera_pitch = 0
    camera_yaw = 0
    mouse_sensitivity = 0.2
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    textures = {name: load_texture(data["texture"]) for name, data in planet_data.items()}
    angle = 0
    t_values = {name: 0.0 for name in orbits}
    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == MOUSEMOTION:
                rel_x, rel_y = event.rel
                camera_yaw -= rel_x * mouse_sensitivity
                camera_pitch += rel_y * mouse_sensitivity
                camera_pitch = max(-89, min(89, camera_pitch))
        keys = pygame.key.get_pressed()
        if keys[K_w]: camera_pos[2] += 1
        if keys[K_s]: camera_pos[2] -= 1
        if keys[K_a]: camera_pos[0] += 1
        if keys[K_d]: camera_pos[0] -= 1
        if keys[K_q]: camera_pos[1] += 1
        if keys[K_e]: camera_pos[1] -= 1
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
        glRotatef(camera_pitch, 1, 0, 0)
        glRotatef(camera_yaw, 0, 1, 0)
        glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotatef(angle * planet_data["sun"]["rotation_speed"], 0, 1, 0)
        draw_sphere(planet_data["sun"]["radius"], textures["sun"])
        glPopMatrix()

        for name, data in planet_data.items():
            if name == "sun":
                continue
            orbit = orbits[name]
            draw_orbit(orbit)
            pos = get_spline_position(orbit, t_values[name])
            glPushMatrix()
            glTranslatef(pos[0], 0, pos[1])
            glRotatef(angle * data["rotation_speed"], 0, 1, 0)
            draw_sphere(data["radius"], textures[name])
            glPopMatrix()
            t_values[name] += dt * 0.5

        pygame.display.flip()
        angle += 1

    pygame.quit()

main()
