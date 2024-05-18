import pygame
from sys import argv

length = argv[1]
height = argv[2]

screen = pygame.display.set_mode((300, 100))
font = pygame.font.Font('freesansbold.ttf', 20)
while True:
    screen.fill((200, 200, 200))
    text = font.render("Length: " + length + "cm", True, (128, 128, 128), (255, 255, 255))
    rect = text.get_rect()
    rect.center = (20, 50)
    screen.blit(text, rect)
    text = font.render("Height: " + height + "cm", True, (128, 128, 128), (255, 255, 255))
    rect = text.get_rect()
    rect.center = (80, 50)
    screen.blit(text, rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    pygame.display.flip()