import pygame as pg
from matrices import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.movement_speed = 0.1
        self.rotation_speed = 0.015

        self.angle_pitch = 0
        self.angle_yaw = 0
        self.angle_roll = 0

    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_w]:
            self.position += self.forward * self.movement_speed
        if key[pg.K_a]:
            self.position -= self.right * self.movement_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.movement_speed
        if key[pg.K_d]:
            self.position += self.right * self.movement_speed
        if key[pg.K_q]:
            self.position += self.up * self.movement_speed
        if key[pg.K_e]:
            self.position -= self.up * self.movement_speed

        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)

    def camera_yaw(self, angle):
        self.angle_yaw += angle

    def camera_pitch(self, angle):
        self.angle_pitch += angle

    def axii_identity(self):
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def update_axii(self):
        rotate = rotate_x(self.angle_pitch) @ rotate_y(self.angle_yaw)
        self.axii_identity()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
            ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
            ])

    def camera_matrix(self):
        self.update_axii()
        return self.translate_matrix() @ self.rotate_matrix()