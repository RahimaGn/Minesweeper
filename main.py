import pygame
import random
from pygame import mixer

pygame.init()

screen_width, screen_height = 900, 700
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Minesweeper")

mixer.music.load('music.mp3')
mixer.music.play(-1)

homebutton = pygame.image.load('home.png')
homebutton = pygame.transform.scale(homebutton, (120, 120))
homebutton_rect = homebutton.get_rect(topleft=(723, 50))

infobutton = pygame.image.load('info.png')
infobutton = pygame.transform.scale(infobutton, (120, 120))
infobutton_rect = infobutton.get_rect(topleft=(723, 200))

nomusicbutton = pygame.image.load('nomusic.png')
nomusicbutton = pygame.transform.scale(nomusicbutton, (120, 120))
nomusicbutton_rect = nomusicbutton.get_rect(topleft=(723, 350))

background2 = pygame.image.load('gamestartedbackground.png')
background2 = pygame.transform.scale(background2, (900, 700))

laceframe = pygame.image.load('laceframe2.png')
laceframe = pygame.transform.scale(laceframe, (728, 680))

background = pygame.image.load('ffond.png')
background = pygame.transform.scale(background, (900, 700))

font_title = pygame.font.Font("Gathen.ttf", 85)
font_button = pygame.font.Font("Gathen.ttf", 30)
title_text = font_title.render("Minesweeper Game", True, 'beige')
button_text = font_button.render("Play", True, 'beige')
text_title = pygame.font.Font("Gathen.ttf", 30)

button_rect = pygame.Rect((900 - 200) / 2, (700 + 60) / 2, 200, 75)
flag_button_rect = pygame.Rect(730, 510, 110, 50)

class Cell:
    def __init__(self, x, y, bomb=False):
        self.x = x
        self.y = y
        self.bomb = bomb
        self.size = 40
        self.revealed = False
        self.flagged = False
        self.rect = pygame.Rect(
            (screen_width - 14 * self.size) // 2 - 100 + x * self.size,
            (screen_height - 14 * self.size) // 2 + y * self.size,
            self.size, self.size)

class Game:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cell_size = 40
        self.offset_x = (screen_width - w * self.cell_size) // 2 - 100
        self.offset_y = (screen_height - h * self.cell_size) // 2
        self.game_started = False
        self.flag_mode = False
        self.grid = [[Cell(x, y) for y in range(h)] for x in range(w)]
        self.place_bombs()

    def place_bombs(self):
        total_bombs = random.randint(20, 25)
        while total_bombs > 0:
            x = random.randint(0, self.w - 1)
            y = random.randint(0, self.h - 1)
            cell = self.grid[x][y]
            if not cell.bomb:
                cell.bomb = True
                total_bombs -= 1

    def get_cell_at_pos(self, pos):
        for row in self.grid:
            for cell in row:
                if cell.rect.collidepoint(pos):
                    return cell
        return None

    def bombs_around(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.w and 0 <= ny < self.h:
                    if self.grid[nx][ny].bomb:
                        count += 1

        return count

    def reveal_cell(self, x, y):
        cell = self.grid[x][y]
        if cell.revealed or cell.flagged:
            return
        else:
          cell.revealed = True
          n = self.bombs_around(x, y)
          if n == 0:
             for i in range(-1, 2):
                for ii in range(-1, 2):
                    dx = x + i
                    dy = y + ii
                    if 0 <= dx < self.w and 0 <= dy < self.h:
                        self.reveal_cell(dx, dy)

    def drawgame(self, screen):
        for row in self.grid:
            for cell in row:
                if cell.revealed:
                    if cell.flagged:
                        if cell.bomb:
                           pygame.draw.rect(screen, 'darkseagreen', cell.rect)
                           pygame.draw.rect(screen, 'navajowhite4', cell.rect, width=5)
                        else:
                            pygame.draw.rect(screen, 'silver', cell.rect)
                            pygame.draw.rect(screen, 'navajowhite4', cell.rect, width=5)
                    elif cell.bomb:
                        pygame.draw.rect(screen, 'darkred', cell.rect)
                        pygame.draw.rect(screen, 'navajowhite4', cell.rect, width=5)
                    else:
                        pygame.draw.rect(screen, 'navajowhite3', cell.rect)
                        pygame.draw.rect(screen, 'navajowhite4', cell.rect, width=5)
                        bombs = self.bombs_around(cell.x, cell.y)
                        if bombs > 0:
                            text = font_button.render(str(bombs), True, 'black')
                            screen.blit(text, (cell.rect.x + 12, cell.rect.y + 5))

                else:
                  pygame.draw.rect(screen, 'snow3', cell.rect)
                  pygame.draw.rect(screen, 'white', cell.rect, 1)


        pygame.draw.rect(screen, 'rosybrown1' if self.flag_mode else 'navajowhite3', flag_button_rect,border_radius=25)
        pygame.draw.rect(screen, 'navajowhite4', flag_button_rect, width=5, border_radius=25)
        label = font_button.render('Flag', True, 'black')
        screen.blit(label, (flag_button_rect.x + 25, flag_button_rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN :
            if flag_button_rect.collidepoint(event.pos):
                self.flag_mode = not self.flag_mode
            else:
                cell = self.get_cell_at_pos(event.pos)
                if cell and not cell.revealed:
                    if self.flag_mode:
                        cell.flagged = not cell.flagged
                        cell.revealed = True
                    else:
                        self.reveal_cell(cell.x, cell.y)

game = Game(14, 14)
showinfo = False
stopmusic = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game.game_started:
              if button_rect.collidepoint(event.pos):
                game = Game(14, 14)
                game.game_started = True
            else:
                if homebutton_rect.collidepoint(event.pos):
                    game.game_started = False
                elif infobutton_rect.collidepoint(event.pos):
                    showinfo = not showinfo

                elif nomusicbutton_rect.collidepoint(event.pos):
                    stopmusic = not stopmusic
                    if stopmusic:
                        mixer.music.pause()
                    else:
                        mixer.music.unpause()
                else:
                    game.handle_event(event)

    if game.game_started:

        screen.blit(background2, (0, 0))
        screen.blit(laceframe, (-10, 15))
        screen.blit(homebutton, (723, 50))
        screen.blit(infobutton, (723, 200))
        screen.blit(nomusicbutton, (723, 350))
        game.drawgame(screen)
        if showinfo:
            pygame.draw.rect(screen, 'papayawhip', pygame.Rect(110, 170, 700, 400),border_radius=25)
            pygame.draw.rect(screen,'tan',pygame.Rect(110, 170, 700, 400),width=5,border_radius=25)

            info_font = pygame.font.Font('Gathen.ttf', 15)

            info_text=['Rules',' When you click on a cell, a number will appear indicating how many bombs are in the surrounding cells.',
                       'To mark a suspected bomb, select the flag mode and click on the cell to place a flag.',' ','Color codes:',
                       '- Red cell: You clicked on a bomb.','- Green cell: You correctly flagged a bomb.',"- Grey cell: You flagged a cell that doesn't contain a bomb.",
                       " ","To restart the game, go back to the main menu and click 'Play'."," "," Have fun! :)"]
            for index,element in enumerate(info_text):
                text=info_font.render(element,True,'black')
                screen.blit(text,(130,200 + index*25))

    else:
        screen.blit(background, (0, 0))
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 250))
        pygame.draw.rect(screen, 'steelblue4', button_rect, border_radius=25)
        pygame.draw.rect(screen, 'beige', button_rect, width=5, border_radius=25)
        screen.blit(button_text, (
            button_rect.x + (button_rect.width - button_text.get_width()) / 2,
            button_rect.y + (button_rect.height - button_text.get_height()) / 2))

    pygame.display.flip()

pygame.quit()
