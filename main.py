import pygame
import numpy as np
from collections import OrderedDict
pygame.init()

class Game(object):

    def __init__(self, gameWidth=800, gameHeight=650):
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        self.cube_size = 5
        self.gameDisplay = pygame.display.set_mode((gameWidth, gameHeight))
        self.deleted = np.zeros((self.gameWidth // self.cube_size, self.gameHeight // self.cube_size))
        self.f_score = np.full((self.gameWidth // self.cube_size, self.gameHeight // self.cube_size), np.inf)
        self.g_score = np.zeros((self.gameWidth // self.cube_size, self.gameHeight // self.cube_size))
        self.wall = np.zeros((self.gameWidth // self.cube_size, self.gameHeight // self.cube_size))
        self.startPos = (0, 0)
        self.endPos = (self.deleted.shape[0]-1, self.deleted.shape[1]-1)
        # self.endPos = (50, 50)

        self.notvisited = []
        self.visited = []
        self.neighbours = OrderedDict()
        self.cameFrom = OrderedDict()
        for i in range(self.deleted.shape[0]):
            for j in range(self.deleted.shape[1]):
                self.neighbours[(i, j)] = self.get_neighbours(i, j)
                if np.random.random() < 0.25: self.wall[i][j] = 1

    def get_neighbours(self, i, j):
        possible_neighbours = []
        if i > 0:
            possible_neighbours.append((i-1, j))
        if i < self.deleted.shape[0] - 1:
            possible_neighbours.append((i + 1, j))
        if j > 0:
            possible_neighbours.append((i, j - 1))
        if j < self.deleted.shape[1] - 1:
            possible_neighbours.append((i, j + 1))
        if i > 0 and j > 0:
            possible_neighbours.append((i-1, j-1))
        if i < self.deleted.shape[0] - 1 and j < self.deleted.shape[1] - 1:
            possible_neighbours.append((i + 1, j+1))
        if j > 0 and i < self.deleted.shape[0] - 1:
            possible_neighbours.append((i+1, j - 1))
        if j < self.deleted.shape[1] - 1 and i > 0:
            possible_neighbours.append((i-1, j + 1))
        return possible_neighbours

    def draw_grid(self, current):
        for notvisited in self.notvisited:
            pygame.draw.rect(self.gameDisplay, (0, 200, 0), (notvisited[0]*self.cube_size, notvisited[1]*self.cube_size, self.cube_size, self.cube_size))
        for visited in self.visited:
            pygame.draw.rect(self.gameDisplay, (255, 0, 0),
                             (visited[0]*self.cube_size, visited[1]*self.cube_size, self.cube_size, self.cube_size))
        to_draw = []
        to_draw.append(current)
        while current in self.cameFrom.keys():
            current = self.cameFrom[current]
            to_draw.append(current)
        for val in to_draw:
            pygame.draw.rect(self.gameDisplay, (0, 0, 250),
                             (val[0] * self.cube_size, val[1] * self.cube_size, self.cube_size, self.cube_size))

        for i in range(self.wall.shape[0]):
            for j in range(self.wall.shape[1]):
                if self.wall[i][j] == 1:
                    pygame.draw.rect(self.gameDisplay, (0, 0, 0),
                                     (i * self.cube_size, j * self.cube_size, self.cube_size, self.cube_size))


        for i in range(0, self.gameWidth, self.cube_size): pygame.draw.line(self.gameDisplay, (0, 0, 0), (i, 0),
                                                                            (i, self.gameHeight))
        for i in range(0, self.gameHeight, self.cube_size): pygame.draw.line(self.gameDisplay, (0, 0, 0), (0, i),
                                                                             (self.gameWidth, i))

    # def start(self):
    #
    #     self.notvisited += [self.startPos]
    #     self.g_score[self.startPos] = 0
    #     self.wall[self.endPos] = 0
    #     self.wall[self.startPos] = 0
    #
    #     while len(self.notvisited) > 0:
    #
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 return
    #
    #         # current_idx = tuple(np.argwhere(self.f_score.min() == self.f_score)[0])
    #         current_idx = self.notvisited[0]
    #         for i, j in self.notvisited:
    #             if self.f_score[i, j] < self.f_score[current_idx]:
    #                 current_idx = (i, j)
    #
    #
    #
    #         if current_idx == self.endPos:
    #             print("Done")
    #             self.gameDisplay.fill((225, 225, 225))
    #             self.draw_grid(current_idx)
    #             pygame.display.update()
    #             pause = True
    #             while pause:
    #                 for event in pygame.event.get():
    #                     if event.type == pygame.KEYDOWN:
    #                         pause=False
    #             return
    #         self.notvisited.remove(current_idx)
    #         for neighbour in self.neighbours[current_idx]:
    #             if self.wall[neighbour] != 1:
    #                 estimated_g_score = self.g_score[current_idx] + self.cube_size
    #                 if estimated_g_score < self.g_score[neighbour]:
    #                     self.cameFrom[neighbour] = current_idx
    #                     self.g_score[neighbour] = estimated_g_score
    #                     self.f_score[neighbour] = estimated_g_score + abs(neighbour[0] - current_idx[0]) + abs(neighbour[1] - current_idx[1])
    #                     if neighbour not in self.notvisited:
    #                         self.notvisited.append(neighbour)
    #         self.gameDisplay.fill((225, 225, 225))
    #         self.draw_grid(current_idx)
    #         pygame.display.update()
    #
    #     print("No Path")
    #     pause = True
    #     while pause:
    #         for event in pygame.event.get():
    #             if event.type == pygame.KEYDOWN:
    #                 pause = False
    def makeobjMsg(self, msg, fontD, color=(0, 0, 0)):
        return fontD.render(msg, True, color), fontD.render(msg, True, color).get_rect()

    def message(self, msg, color=(0, 0, 0), fontType='freesansbold.ttf', fontSize=15, xpos=10, ypos=10):
        fontDefination = pygame.font.Font(fontType, fontSize)
        msgSurface, msgRectangle = self.makeobjMsg(msg, fontDefination, color)
        msgRectangle = (xpos, ypos)
        self.gameDisplay.blit(msgSurface, msgRectangle)

    def pauseGame(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_z:
                        return
            self.gameDisplay.fill((125, 125, 125))
            self.message(msg='During LockDown:!', color=(255, 255, 255), fontSize=30, xpos=100,
                         ypos=100)
            self.message(msg='She: I miss you :"(', color=(255, 255, 255), fontSize=30, xpos=100,
                         ypos=150)
            self.message(msg="Me: But it\'s lockdown rn..", color=(255, 255, 255), fontSize=30, xpos=100,
                         ypos=200)
            self.message(msg="She: I have ordered KFC for you in my house..", color=(255, 255, 255), fontSize=30, xpos=100,
                         ypos=250)
            self.message(msg='Me: ...', color=(255, 255, 255), fontSize=30, xpos=100,
                         ypos=300)

            pygame.display.update()

    def start(self):

        self.notvisited += [self.startPos]
        self.g_score[self.startPos] = 0
        self.wall[self.endPos] = 0
        self.wall[self.startPos] = 0
        self.pauseGame()

        while len(self.notvisited) > 0:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            current_idx = self.notvisited[0]
            for i, j in self.notvisited:
                if self.f_score[i, j] < self.f_score[current_idx]:
                    current_idx = (i, j)

            if current_idx == self.endPos:
                print("Done")
                self.gameDisplay.fill((225, 225, 225))
                self.draw_grid(current_idx)
                pygame.display.update()
                pause = True
                while pause:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            pause=False
                return
            self.notvisited.remove(current_idx)
            self.visited.append(current_idx)
            self.deleted[current_idx] = 1
            for neighbour in self.neighbours[current_idx]:

                if neighbour not in self.visited and self.wall[neighbour] == 0:
                    estimated_g_score = self.g_score[current_idx] + self.cube_size

                    if neighbour not in self.notvisited:
                        self.notvisited.append(neighbour)
                    elif self.g_score[neighbour] <= estimated_g_score:
                        continue
                    self.g_score[neighbour] = estimated_g_score
                    self.f_score[neighbour] = estimated_g_score + np.sqrt((self.cube_size*neighbour[0] - self.cube_size*self.endPos[0]) ** 2 + (self.cube_size*neighbour[1] - self.cube_size*self.endPos[1]) ** 2)
                    # self.f_score[neighbour] = estimated_g_score + self.cube_size*abs(neighbour[0] - self.endPos[0]) + self.cube_size*abs(neighbour[1] - self.endPos[1]) # multiply cube_size for scalibility
                    self.cameFrom[neighbour] = current_idx

            self.gameDisplay.fill((225, 225, 225))
            self.draw_grid(current_idx)
            pygame.display.update()
        print("No Path")
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pause = False


if __name__ == "__main__":
    game = Game()
    game.start()