import pygame
import serial
import random
import math

# --- SERIAL SETUP ---
# Change "COM3" to your Arduino's port
ser = serial.Serial("COM3", 9600, timeout=1)

# --- PYGAME SETUP ---
pygame.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎆 Joystick Fireworks Show")
clock = pygame.time.Clock()

# --- FIREWORK CLASS ---
class Firework:
    def __init__(self, x, y):
        self.particles = []
        color = random.choice([(255,0,0),(0,255,0),(0,0,255),
                               (255,255,0),(255,0,255),(0,255,255),
                               (255,165,0),(255,255,255)])
        for _ in range(50):
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(2, 6)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append({
                "x": x, "y": y,
                "dx": dx, "dy": dy,
                "life": random.randint(30, 60),
                "color": color
            })

    def update(self):
        for p in self.particles:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["dy"] += 0.05  # gravity
            p["life"] -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

    def draw(self, surface):
        for p in self.particles:
            pygame.draw.circle(surface, p["color"], (int(p["x"]), int(p["y"])), 3)

# --- GAME LOOP ---
fireworks = []
running = True
x, y = WIDTH//2, HEIGHT//2  # joystick-controlled "launch spot"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- READ JOYSTICK DATA ---
    line = ser.readline().decode().strip()
    if line:
        try:
            vx, vy, button = map(int, line.split(","))
            # map joystick movement to screen
            if vx < 400: x -= 10
            elif vx > 600: x += 10
            if vy < 400: y -= 10
            elif vy > 600: y += 10
            # button spawns a firework
            if button == 0:
                fireworks.append(Firework(x, y))

            # keep inside screen
            x = max(0, min(WIDTH, x))
            y = max(0, min(HEIGHT, y))

        except:
            pass

    # --- UPDATE FIREWORKS ---
    for fw in fireworks:
        fw.update()
    fireworks = [fw for fw in fireworks if fw.particles]

    # --- DRAW ---
    win.fill((0, 0, 20))  # dark night sky
    for fw in fireworks:
        fw.draw(win)
    # optional: draw launch point
    pygame.draw.circle(win, (200,200,200), (x,y), 5)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
