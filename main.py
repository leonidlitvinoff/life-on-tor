import pygame
from board import Board
import copy


class Life(Board):
    def __init__(self, width, height, rect, pos, width_w=500, height_w=500):
        super().__init__(width, height, rect, pos)
        self.width_w = width_w
        self.height_w = height_w
        self.screen = pygame.display.set_mode((self.width_w, self.height_w))
        self.run()

    def next_move(self):
        new_life = copy.deepcopy(self.board)
        for i in range(self.height):
            for j in range(self.width):
                peoples = 0
                data = [(i - 1, j),
                        (i - 1, j - 1),
                        (i, j - 1),
                        (i + 1, j - 1),
                        (i + 1, j),
                        (i + 1, j + 1),
                        (i, j + 1),
                        (i - 1, j + 1)]
                parsed_data = []
                for k in data:
                    parsed_data.append([])
                    if k[0] < 0:
                        parsed_data[-1].append(k[0] + self.width)
                    elif k[0] >= self.width:
                        parsed_data[-1].append(k[0] - self.width)
                    else:
                        parsed_data[-1].append(k[0])
                    if k[1] < 0:
                        parsed_data[-1].append(k[1] + self.height)
                    elif k[1] >= self.height:
                        parsed_data[-1].append(k[1] - self.height)
                    else:
                        parsed_data[-1].append(k[1])
                for k in parsed_data:
                    peoples += self.re_checker(k[0], k[1])
                if peoples == 3:
                    new_life[i][j] = 1
                elif new_life[i][j] == 1 and peoples == 2 or peoples == 3:
                    pass
                else:
                    new_life[i][j] = 0
        self.board = new_life

    def render(self, screen):
        screen.fill((0, 0, 0))
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (i * self.rect[0] + self.pos[0], j * self.rect[1] + self.pos[1],
                                                               self.rect[0], self.rect[1]), 1)
                else:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (i * self.rect[0] + self.pos[0], j * self.rect[1] + self.pos[1],
                                      self.rect[0], self.rect[1]), 0)

    def run(self):
        pygame.init()
        running = True
        self.screen.fill((0, 0, 0))
        emode = 1
        reader = 0
        fps = 60
        clock = pygame.time.Clock()
        while running:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and emode == 1:
                        reader = 1
                    if event.button == 4 and emode == 0:
                        fps += 5
                    if event.button == 5 and emode == 0:
                        fps -= 5
                    if fps > 100:
                        fps = 100
                    elif fps <= 0:
                        fps = 1
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        reader = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        emode = self.checker(emode)
                        reader = 0
                        if emode == 1:
                            fps = 60
                try:
                    if reader == 1:
                        self.get_click(event.pos)
                except:
                    pass
            if emode == 0:
                self.next_move()
            self.render(self.screen)
            pygame.display.flip()

            
Life(50, 50, (10, 10), (0, 0))