import pygame
import math
import string
from l_system_1 import generate_l_system


WIDTH, HEIGHT = 1920, 1080

ls = {
    'axiom': 'F',
    'rules': {'F': 'FF-[-F+F+F]+[+F-F-F]'},
    'iterations': 4,
    'angle': math.radians(22.5),
    'length': 10,
    'start': {'x': WIDTH // 2, 'y': HEIGHT - 10},
    # 'x': WIDTH // 2,
    # 'y': HEIGHT - 10,
    'theta': math.pi / 2,
    'positions': [],
}

gen_ls = generate_l_system(ls['axiom'], ls['rules'], ls['iterations'])
print(gen_ls)


pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('L-System \\ dev-ed.ru')
clock = pygame.time.Clock()

running = True
pause = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if not pause:
        display.fill('black')

        # draw L-System
        ls['theta'] = math.pi / 2
        ls['x'], ls['y'] = ls['start']['x'], ls['start']['y']

        for char in gen_ls:
            # if char in ('A', 'B', 'F', 'G', 'X', 'Y'):
            if char in tuple(string.ascii_uppercase):
                x2 = ls['x'] - ls['length'] * math.cos(ls['theta'])
                y2 = ls['y'] - ls['length'] * math.sin(ls['theta'])
                pygame.draw.line(display, (255, 255, 255), (ls['x'], ls['y']), (x2, y2))
                ls['x'], ls['y'] = x2, y2
            elif char == '+':
                ls['theta'] += ls['angle']
            elif char == '-':
                ls['theta'] -= ls['angle']
            elif char == '[':
                ls['positions'].append({'x': ls['x'], 'y': ls['y'], 'theta': ls['theta']})
            elif char == ']':
                position = ls['positions'].pop()
                ls['x'], ls['y'], ls['theta'] = position['x'], position['y'], position['theta']

        pause = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
