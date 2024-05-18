import pygame
import subprocess
import sys
  
pygame.init()

# switch last to measured.png for competition
img = pygame.transform.scale(pygame.image.load("images/image.png"), (640, 480))
  
screen = pygame.display.set_mode((img.get_width() + 300, img.get_height()))

measuring = False
lines = [] 
line  = []

font = pygame.font.Font('freesansbold.ttf', 20)

def dist (x1, y1, x2, y2):
    return ((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))**0.5

def dist_line(l):
    return dist(l[0], l[1], l[2], l[3])

real_length = 32
done = False

t1 = None
while True:
    screen.fill((200, 200, 200))
    screen.blit(img, (0, 0))
 
    x, y = pygame.mouse.get_pos()

    # Drawing each line
    for l in lines:
        pygame.draw.line(screen, (50, 200, 255), (l[0], l[1]), (l[2], l[3]), 3)

    # drawing the start from the mouse
    if len(line) == 2:
        pygame.draw.line(screen, (50, 255, 200), (line[0], line[1]), (x, y), 3)

    # Draw known length
    if len(lines) == 0:
        text = font.render("DRAW KNOWN", True, (128, 128, 128), (255, 255, 255))
        rect = text.get_rect()
        rect.center = (img.get_width() + 75, 75)
        screen.blit(text, rect)
    elif len(lines) == 1:
        text = font.render("DRAW TOTAL HEIGHT", True, (128, 128, 128), (255, 255, 255))
        rect = text.get_rect()
        rect.center = (img.get_width() + 85, 75)
        screen.blit(text, rect)
    elif len(lines) == 2:
        text = font.render("DRAW TOTAL WIDTH", True, (128, 128, 128), (255, 255, 255))
        rect = text.get_rect()
        rect.center = (img.get_width() + 85, 75)
        screen.blit(text, rect)
    elif len(lines) == 3:
        text = font.render("DRAW LEFT WIDTH", True, (128, 128, 128), (255, 255, 255))
        rect = text.get_rect()
        rect.center = (img.get_width() + 85, 75)
        screen.blit(text, rect)
    elif len(lines) == 4:
        text = font.render("DRAW LEFT HEIGHT", True, (128, 128, 128), (255, 255, 255))
        rect = text.get_rect()
        rect.center = (img.get_width() + 85, 75)
        screen.blit(text, rect)
    elif len(lines) == 5:
        text = font.render("DRAW RIGHT WIDTH", True, (128, 128, 128), (255, 255, 255))
        rect = text.get_rect()
        rect.center = (img.get_width() + 85, 75)
        screen.blit(text, rect)
    elif len(lines) == 6:
        text = font.render("DRAW RIGHT HEIGHT", True, (128, 128, 128), (255, 255, 255))
        rect = text.get_rect()
        rect.center = (img.get_width() + 85, 75)
        screen.blit(text, rect)
    else: # drawing final calculated length
        ratio = real_length/dist_line(lines[0])
        
        total_height = dist_line(lines[1]) * ratio
        total_width  = dist_line(lines[2]) * ratio
        left_width   = dist_line(lines[3]) * ratio
        left_height  = dist_line(lines[4]) * ratio
        right_width  = dist_line(lines[5]) * ratio
        right_height = dist_line(lines[6]) * ratio

        subprocess.run(['python3', 'auto_model.py', str(36), str(32), str(total_height), str(total_width), str(left_width), str(left_height), str(right_width), str(right_height)])
        sys.exit()
     
    pygame.draw.rect(screen, (255, 0, 0), (img.get_width(), img.get_height()-40, 300, 40))
    pygame.draw.rect(screen, (0, 255, 0), (img.get_width(), img.get_height()-80, 300, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if x < img.get_width():
                    if not measuring:
                        measuring = True
                        line = [x, y]
                    else:
                        measuring = False
                        line.append(x)
                        line.append(y)
                        lines.append(line)
                else:
                    if y > img.get_height() - 40 and len(lines) > 0: # Red Pressed
                        lines.pop()
                    elif y > img.get_height() - 80: # Green Pressed
                        done = True

    pygame.display.flip()
