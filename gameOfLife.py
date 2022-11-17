# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 10:36:04 2022

@author: Vincent Medrano
Conways Game of Life
"""

import time
import pygame
import numpy as np

#Set colors for game using RGB values
COLOR_BG = (0,0,0)
COLOR_GRID = (30,30,30)
COLOR_DIE_NEXT = (70,70,70)
COLOR_ALIVE_NEXT = (255,255,255)
#SIZE = 20

#Main function of game (game logic and drawing process)
#screen is the pygame screen, cells will be playing field and state,
#size of individual cell and with_progress boolean value to follow logic
def update(screen, cells, size, with_progress=False):
    #np array to apply changes to grid
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    
    #ndindex = Given the shape of an array, an ndindex instance
    #iterates over the N-dimensional index of the array.
    #At each iteration a tuple of indices is returned,
    #the LAST DIMENSION is iterated over first.
    for row, col in np.ndindex(cells.shape):
        #Calculate how many of the neighboring cells are alive +2 due to exclusion
        #subtract current cell so it is not counted as alive or dead
        #if 0 nothing, if 1, subtract 1
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        #default color will be color of background
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT
        
        #if alive, alone or overpopulated, die
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                #if with_progress is false, do not apply game rules
                if with_progress:
                    color = COLOR_DIE_NEXT
            #idea conditions for a cell to remain alive, no need to update
            #with_progress because not alive and should remain false.
            elif 2 <= alive <=3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT                    
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
                    
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
        
    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((200,200))
    
    cells = np.zeros((20,20))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)
    
    pygame.display.flip()
    pygame.display.update()
    
    running = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()
        screen.fill(COLOR_GRID)
        
        if running:
            cells = update(screen, cells, 10, with_progress = True)
            pygame.display.update()
        #how fast you plot when selecting cells    
        time.sleep(0.0001)
        
if __name__ == "__main__":
    print("Plot by using mouse\n")
    print("Spacebar to play / pause\n")
    print("To add more plots while playing, pause then plot\n")
    main()
                    