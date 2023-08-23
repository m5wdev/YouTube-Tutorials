import pygame
import numpy as np
import time


SCREEN_SIZE = (500, 500)
CELL_SIZE = 10
SCREEN_CELLS_FILL = (SCREEN_SIZE[0] // 10, SCREEN_SIZE[1] // 10)
# print('SCREEN_CELLS_FILL', SCREEN_CELLS_FILL) # (50, 50)

COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (50, 50, 50)
COLOR_GREEN = (51, 204, 51)
COLOR_RED = (255, 0, 0)


def game(screen, cells, evolution=False):
    # print(cells.shape) # (50, 50)
    # print(cells.shape[0], cells.shape[1]) # 50 50

    # updated_cells = np.zeros(SCREEN_CELLS_FILL)
    # updated_cells = np.zeros(cells.shape)
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    # print(updated_cells)

    for row, col in np.ndindex(cells.shape):
        alive_cells = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        # print(alive_cells)
        color = COLOR_BLACK if cells[row, col] == 0 else COLOR_GREEN

        if cells[row, col] == 1:
            if alive_cells < 2 or alive_cells > 3:
                if evolution:
                    color = COLOR_RED
            elif 2 <= alive_cells <= 3:
                updated_cells[row, col] = 1
                if evolution:
                    color = COLOR_GREEN
        else:
            if alive_cells == 3:
                updated_cells[row, col] = 1
                if evolution:
                    color = COLOR_RED

        pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

    return updated_cells


def main():
    pygame.init()
    pygame.display.set_caption('Draw grid')

    screen = pygame.display.set_mode(SCREEN_SIZE)
    # cells = np.zeros(SCREEN_CELLS_FILL)
    cells = np.zeros((SCREEN_CELLS_FILL[1], SCREEN_CELLS_FILL[0]))
    # print(cells)
    screen.fill(COLOR_GREY)
    game(screen, cells)

    pygame.display.update()

    evolution_runs = False

    while True:
        for event in pygame.event.get():
            # user quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # user press space button
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # evolution_runs = not evolution_runs
                    evolution_runs = True
                    game(screen, cells)
                    pygame.display.update()

            # user clicked left mouse button (add cell)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                # print(pos)
                if pos[0] < SCREEN_SIZE[0] and pos[1] < SCREEN_SIZE[1]: # avoid IndexError
                    cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 1
                    game(screen, cells)
                    pygame.display.update()

            # user clicked right mouse button (remove cell)
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                # print(pos)
                if pos[0] < SCREEN_SIZE[0] and pos[1] < SCREEN_SIZE[1]: # avoid IndexError
                    cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 0
                    game(screen, cells)
                    pygame.display.update()

        screen.fill(COLOR_GREY)

        if evolution_runs:
            cells = game(screen, cells, evolution=True)
            pygame.display.update()

        time.sleep(0.05)


if __name__ == '__main__':
    main()
