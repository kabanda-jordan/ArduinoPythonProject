import pygame

# initialize pygame
pygame.init()

# create a window (500x500)
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Pygame Test Window")

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # when you click the close button
            running = False

    win.fill((0, 0, 0))  # black background
    pygame.draw.circle(win, (0, 255, 0), (250, 250), 50)  # draw a green circle
    pygame.display.update()  # refresh the screen

pygame.quit()
