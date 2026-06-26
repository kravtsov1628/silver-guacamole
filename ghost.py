import random
import pygame
import math
from settings import T_SIZE, G_SPEED, BG_COLOR

DIRECTIONS = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0)
]


class Ghost:
    def __init__(self, col, row, color, name="Ghost"):
        self.col = col
        self.row = row
        self.pixel_x = col * T_SIZE
        self.pixel_y = row * T_SIZE

        self.direction = random.choice(DIRECTIONS)
        self.color = color
        self.speed = G_SPEED
        self.name = name

    def update(self, maze):
        if self.pixel_x % T_SIZE == 0 and self.pixel_y % T_SIZE == 0:
            self.col = self.pixel_x // T_SIZE
            self.row = self.pixel_y // T_SIZE
            possible = []
            dc, dr = self.direction
            reverse = (-dc, -dr)

            for next_dc, next_dr in DIRECTIONS:
                if maze.is_free(self.col + next_dc, self.row + next_dr):
                    possible.append((next_dc, next_dr))
            if reverse in possible and len(possible) > 1:
                possible.remove(reverse)
            if possible:
                self.direction = random.choice(possible)
            else:
                self.direction = (0, 0)
        dc, dr = self.direction
        self.pixel_x += dc * self.speed
        self.pixel_y += dr * self.speed

    def draw(self, screen, frame_count, idx=0):
        bob = math.sin((frame_count + idx * 15) * 0.15) * 2.5
        cx = self.pixel_x + T_SIZE // 2
        cy = self.pixel_y + T_SIZE // 2 + bob
        r = T_SIZE // 2 - 2
        body_rect = pygame.Rect(cx - r, cy - 2, r * 2, r + 2)
        pygame.draw.rect(screen, self.color, body_rect)
        pygame.draw.circle(screen, self.color, (cx, cy - 2), r)

        wave_offset = (frame_count // 6) % 2
        bottom_y = cy + r

        for i in range(3):
            wx = cx - r + (i * 2 + 1) * (r / 3)
            wy = bottom_y
            if (i % 2 == wave_offset):
                wy -= 3
            pygame.draw.circle(screen, BG_COLOR, (int(wx), int(wy)), int(r / 3) + 1)

        eye_spacing = 4.5
        eye_radius = 3.5
        left_eye_x = cx - eye_spacing
        right_eye_x = cx + eye_spacing
        eye_y = cy - 3
        pygame.draw.circle(screen, (255, 255, 255), (int(left_eye_x), int(eye_y)), int(eye_radius))
        pygame.draw.circle(screen, (255, 255, 255), (int(right_eye_x), int(eye_y)), int(eye_radius))
        dc, dr = self.direction
        shift_x = dc * 1.8
        shift_y = dr * 1.8
        pupil_radius = 1.8
        pupil_color = (15, 23, 42)

        pygame.draw.circle(screen, pupil_color, (int(left_eye_x + shift_x), int(eye_y + shift_y)), int(pupil_radius))
        pygame.draw.circle(screen, pupil_color, (int(right_eye_x + shift_x), int(eye_y + shift_y)), int(pupil_radius))
