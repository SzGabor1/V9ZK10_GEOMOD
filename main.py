import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from PIL import Image
import random

G = 6.67430e-11
TIME_STEP = 360000

planet_data = {
    "sun": {"mass": 1.989e30, "radius": 3.0, "position": [0.0, 0.0], "velocity": [0.0, 0.0], "texture": "textures/sun.jpg", "rotation_speed": 0.002},
    "mercury": {"mass": 3.285e23, "radius": 0.5, "position": [5.7e11, 0.0], "velocity": [0.0, 4.79e4], "texture": "textures/mercury.jpg", "rotation_speed": 0.005},
    "venus": {"mass": 4.867e24, "radius": 0.8, "position": [1.08e12, 0.0], "velocity": [0.0, 3.5e4], "texture": "textures/venus.jpg", "rotation_speed": 0.004},
    "earth": {
        "mass": 5.972e24,
        "radius": 1.0,
        "position": [1.496e12, 0.0],
        "velocity": [0.0, 2.978e4],
        "texture": "textures/earth.jpg",
        "rotation_speed": 0.03,
        "moon": {
            "radius": 0.3,
            "distance": 1.84e11,
            "orbit_speed": 0.01,
            "texture": "textures/moon.jpg"
        }
    },
    "mars": {"mass": 6.39e23, "radius": 0.6, "position": [2.279e12, 0.0], "velocity": [0.0, 2.41e4], "texture": "textures/mars.jpg", "rotation_speed": 0.02},
    "jupiter": {"mass": 1.898e27, "radius": 2.5, "position": [7.78e12, 0.0], "velocity": [0.0, 1.31e4], "texture": "textures/jupiter.jpg", "rotation_speed": 0.015},
    "saturn": {"mass": 5.683e26, "radius": 2.0, "position": [1.43e13, 0.0], "velocity": [0.0, 9.69e3], "texture": "textures/saturn.jpg", "rotation_speed": 0.01},
    "uranus": {"mass": 8.681e25, "radius": 1.5, "position": [2.87e13, 0.0], "velocity": [0.0, 6.81e3], "texture": "textures/uranus.jpg", "rotation_speed": 0.008},
    "neptune": {"mass": 1.024e26, "radius": 1.4, "position": [4.5e13, 0.0], "velocity": [0.0, 5.43e3], "texture": "textures/neptune.jpg", "rotation_speed": 0.006}
}

sun_mass = planet_data["sun"]["mass"]

for name, planet in planet_data.items():
    if name == "sun":
        continue
    r = math.sqrt(planet["position"][0]**2 + planet["position"][1]**2)
    orbital_velocity = math.sqrt(G * sun_mass / r)
    planet["velocity"] = [-orbital_velocity * (planet["position"][1] / r),
                          orbital_velocity * (planet["position"][0] / r)]

def load_texture(file_path):
    img = Image.open(file_path)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGB").tobytes()
    width, height = img.size
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return texture_id

def calculate_gravitational_force(body1, body2):
    dx = body2["position"][0] - body1["position"][0]
    dy = body2["position"][1] - body1["position"][1]
    distance = math.sqrt(dx**2 + dy**2)
    force = G * body1["mass"] * body2["mass"] / (distance**2)
    angle = math.atan2(dy, dx)
    return force * math.cos(angle), force * math.sin(angle)

def update_positions_and_velocities():
    forces = {name: [0.0, 0.0] for name in planet_data}
    for name1, body1 in planet_data.items():
        for name2, body2 in planet_data.items():
            if name1 != name2:
                fx, fy = calculate_gravitational_force(body1, body2)
                forces[name1][0] += fx
                forces[name1][1] += fy
    for name, body in planet_data.items():
        ax = forces[name][0] / body["mass"]
        ay = forces[name][1] / body["mass"]
        body["velocity"][0] += ax * TIME_STEP
        body["velocity"][1] += ay * TIME_STEP
        body["position"][0] += body["velocity"][0] * TIME_STEP
        body["position"][1] += body["velocity"][1] * TIME_STEP

def draw_orbit(distance):
    glLineWidth(5.0)
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        x = distance * math.cos(angle) * 1e-11
        z = distance * math.sin(angle) * 1e-11
        glVertex3f(x, 0, z)
    glEnd()
    glLineWidth(1.0)

def draw_sphere(radius, texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 50, 50)

def draw_planets(textures, angle):
    for name, body in planet_data.items():
        glPushMatrix()
        if name != "sun":
            draw_orbit(math.sqrt(body["position"][0]**2 + body["position"][1]**2))
        planet_x = body["position"][0] * 1e-11
        planet_z = body["position"][1] * 1e-11
        glTranslatef(planet_x, 0, planet_z)
        glRotatef(-90, 1, 0, 0)
        glRotatef(angle * body["rotation_speed"], 0, 0, 1)
        draw_sphere(body["radius"], textures[name])
        if name == "earth":
            moon = body["moon"]
            moon_angle = angle * moon["orbit_speed"]
            moon_x = moon["distance"] * math.cos(moon_angle) * 1e-11
            moon_z = moon["distance"] * math.sin(moon_angle) * 1e-11
            glPushMatrix()
            glRotatef(-90, 1, 0, 0)
            draw_orbit(moon["distance"])
            glPopMatrix()
            glPushMatrix()
            glTranslatef(moon_x, moon_z, 0)
            draw_sphere(moon["radius"], textures["moon"])
            glPopMatrix()
        glPopMatrix()


def create_random_meteor():
    return {
        "position": [random.uniform(-5e13, 5e13), random.uniform(-5e13, 5e13)],
        "velocity": [random.uniform(-1e4, 1e4), random.uniform(-1e4, 1e4)],
        "radius": random.uniform(0.1, 0.3)
    }

def update_meteors(meteors):
    for meteor in meteors:
        meteor["position"][0] += meteor["velocity"][0] * TIME_STEP
        meteor["position"][1] += meteor["velocity"][1] * TIME_STEP
        

def draw_meteors(meteors):
    for meteor in meteors:
        glPushMatrix()
        meteor_x = meteor["position"][0] * 1e-11
        meteor_z = meteor["position"][1] * 1e-11
        glTranslatef(meteor_x, 0, meteor_z)

        # Glowing Meteor Core
        glDisable(GL_TEXTURE_2D)
        glColor3f(1.0, 0.3, 0.0)  
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, meteor["radius"], 20, 20)


        glEnable(GL_TEXTURE_2D)
        glPopMatrix()


def main():
    
    meteors = []
# Generate a few random meteors
    for _ in range(100):  # Adjust the number of meteors as needed
        meteors.append(create_random_meteor())
    
    pygame.init()
    display = (1000, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
    camera_pos = [0.0, -2.0, -50]
    camera_pitch = 0
    camera_yaw = 0
    mouse_sensitivity = 0.2
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    angle = 0
    glEnable(GL_TEXTURE_2D)
    textures = {name: load_texture(planet["texture"]) for name, planet in planet_data.items()}
    textures["moon"] = load_texture(planet_data["earth"]["moon"]["texture"])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == MOUSEMOTION:
                rel_x, rel_y = event.rel
                camera_yaw -= rel_x * mouse_sensitivity
                camera_pitch += rel_y * mouse_sensitivity
                camera_pitch = max(-89, min(89, camera_pitch))
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            camera_pos[2] += 1
        if keys[K_s]:
            camera_pos[2] -= 1
        if keys[K_a]:
            camera_pos[0] += 1
        if keys[K_d]:
            camera_pos[0] -= 1
        if keys[K_q]:
            camera_pos[1] += 1
        if keys[K_e]:
            camera_pos[1] -= 1
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
        glRotatef(camera_pitch, 1, 0, 0)
        glRotatef(camera_yaw, 0, 1, 0)
        glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        update_positions_and_velocities()
        draw_planets(textures, angle)


        update_meteors(meteors)
        draw_meteors(meteors)
        pygame.display.flip()
        pygame.time.wait(10)
        angle += 1
    pygame.quit()

main()