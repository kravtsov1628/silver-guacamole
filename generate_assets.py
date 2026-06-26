import os
import math
import pygame


pygame.init()
sprite_canvas = pygame.Surface((32, 32), pygame.SRCALPHA)

os.makedirs("assets_pack", exist_ok=True)

Y = (250, 204, 21, 255)
R = (239, 68, 68, 255)
PINK = (244, 114, 182, 255)
CYAN = (34, 211, 238, 255)
ORANGE = (251, 146, 60, 255)
WHITE = (255, 255, 255, 255)
PUPIL = (15, 23, 42, 255)


def save_pacman(filename, mouth_open, direction="RIGHT"):
    sprite_canvas.fill((0, 0, 0, 0))
    cx, cy = 16, 16
    r = 13
    pygame.draw.circle(sprite_canvas, Y, (cx, cy), r)
    theta = 0
    if direction == "RIGHT":
        theta = 0
    elif direction == "LEFT":
        theta = math.pi
    elif direction == "DOWN":
        theta = math.pi / 2
    elif direction == "UP":
        theta = 3 * math.pi / 2

    points = [(cx, cy)]
    start_angle = theta + mouth_open
    end_angle = theta + 2 * math.pi - mouth_open
    steps = 24
    for i in range(steps + 1):
        angle = start_angle + (end_angle - start_angle) * i / steps
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        points.append((int(px), int(py)))
    pygame.image.save(sprite_canvas, os.path.join("assets_pack", filename))

def save_ghost(filename, color, wave_offset, look_dir="DOWN"):
    sprite_canvas.fill((0, 0, 0, 0))
    cx, cy = 16, 16
    r = 13
    pygame.draw.circle(sprite_canvas, color, (cx, cy - 2), r)
    pygame.draw.rect(sprite_canvas, color, pygame.Rect(cx - r, cy - 2, r * 2, r + 2))
    bottom_y = cy + r
    for i in range(3):
        wx = cx - r + (i * 2 + 1) * (r / 3)
        wy = bottom_y
        if i % 2 == wave_offset:
            wy -= 3
        pygame.draw.circle(sprite_canvas, (0, 0, 0, 0), (int(wx), int(wy)), int(r / 3) + 1)

    eye_spacing = 4.5
    eye_radius = 3.5
    left_eye_x = cx - eye_spacing
    right_eye_x = cx + eye_spacing
    eye_y = cy - 3

    pygame.draw.circle(sprite_canvas, WHITE, (int(left_eye_x), int(eye_y)), int(eye_radius))
    pygame.draw.circle(sprite_canvas, WHITE, (int(right_eye_x), int(eye_y)), int(eye_radius))
    dc_x, dc_y = 0, 0
    if look_dir == "UP":
        dc_x, dc_y = 0, -1
    elif look_dir == "DOWN":
        dc_x, dc_y = 0, 1
    elif look_dir == "LEFT":
        dc_x, dc_y = -1, 0
    elif look_dir == "RIGHT":
        dc_x, dc_y = 1, 0

    shift_x = dc_x * 1.8
    shift_y = dc_y * 1.8
    pygame.draw.circle(sprite_canvas, PUPIL, (int(left_eye_x + shift_x), int(eye_y + shift_y)), 2)
    pygame.draw.circle(sprite_canvas, PUPIL, (int(right_eye_x + shift_x), int(eye_y + shift_y)), 2)

    pygame.image.save(sprite_canvas, os.path.join("assets_pack", filename))
    print(f"Exported: assets_pack/{filename}")

for d in ["RIGHT", "LEFT", "UP", "DOWN"]:
    save_pacman(f"pacman_open_{d.lower()}.png", 0.45, d)
    save_pacman(f"pacman_mid_{d.lower()}.png", 0.25, d)
    save_pacman(f"pacman_closed_{d.lower()}.png", 0.05, d)

ghost_configs = [
    ("blinky", R),
    ("pinky", PINK),
    ("inky", CYAN),
    ("clyde", ORANGE)
]

for name, col in ghost_configs:
    for look in ["RIGHT", "LEFT", "UP", "DOWN"]:
        save_ghost(f"{name}_wave1_{look.lower()}.png", col, 0, look)
        save_ghost(f"{name}_wave2_{look.lower()}.png", col, 1, look)

pygame.quit()
