import pygame, sys
import random
import numpy as np
import time
import copy


color_dict = {
    2: [245, 245, 220],
    4: [255, 250, 205],
    8: [244, 164, 96],
    16: [205, 133, 63],
    32: [205, 92, 92],
    64: [255, 0, 0],
    128: [255, 246, 143],
    256: [255, 236, 139	],
    512: [255, 215, 0],
    1024: [255, 185, 15],
    2048: [255, 193, 37],
    4096: [72, 118, 255],
    8192: [58, 95, 205],
    16384: [39, 64, 139],
    32768: [0, 0, 238],
    65536: [0, 0, 139]
}

value_post = {
    1: (50, [38, 25]),
    2: (50, [25, 25]),
    3: (50, [11, 25]),
    4: (40, [13, 30]),
    5: (30, [14, 34])
}

class GameView(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2048")
        self.score = 0
        self.screen = pygame.display.set_mode([490, 590])
        self.screen.fill([255, 255, 255])
        self.bind_color = [210, 210, 210]
        # self._matrix = np.array([[2,4,8,16],[256,128,64,32],[512,1024,2048,4096],[65536,32768,16384,8192]])
        self._matrix = np.array([[2,2,4,4],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.__BindInit()
        pygame.display.flip()
        
    def __BindInit(self):
        # 横向
        pygame.draw.rect(self.screen, self.bind_color, [0, 100, 490, 30], 0)
        pygame.draw.rect(self.screen, self.bind_color, [0, 230, 490, 10], 0) # 100
        pygame.draw.rect(self.screen, self.bind_color, [0, 340, 490, 10], 0) # 100
        pygame.draw.rect(self.screen, self.bind_color, [0, 450, 490, 10], 0) # 100
        pygame.draw.rect(self.screen, self.bind_color, [0, 560, 490, 30], 0) # 100
        # 纵向
        pygame.draw.rect(self.screen, self.bind_color, [0, 100, 30, 590], 0)
        pygame.draw.rect(self.screen, self.bind_color, [130, 100, 10, 590], 0) # 100
        pygame.draw.rect(self.screen, self.bind_color, [240, 100, 10, 590], 0) # 100
        pygame.draw.rect(self.screen, self.bind_color, [350, 100, 10, 590], 0) # 100
        pygame.draw.rect(self.screen, self.bind_color, [460, 100, 30, 590], 0) # 100
        pygame.display.flip()
        
    def show_window(self):
        self.__BindInit()
        for x in range(4):
            for y in range(4):
                if self._matrix[y][x] != 0:
                    color = color_dict[self._matrix[y][x]]
                    pygame.draw.rect(self.screen, color, [30+110*x, 130+110*y, 100, 100], 0)
                    str_num = str(self._matrix[y][x])
                    value = value_post[len(str_num)]
                    font = pygame.font.SysFont("timesnewroman", value[0])
                    score_text = font.render(str_num, 1, (0, 0, 0))
                    self.screen.blit(score_text, [30+110*x+value[1][0], 130+110*y+value[1][1]])
                else:
                    pygame.draw.rect(self.screen, [255, 255, 255], [30+110*x, 130+110*y, 100, 100], 0)
        # 分数覆盖
        pygame.draw.rect(self.screen, [255, 255, 255], [0, 0, 490, 100], 0)
        str_num = "score:" + str(self.score)
        font = pygame.font.SysFont("timesnewroman", 40)
        score_text = font.render(str_num, 1, (0, 0, 0))
        self.screen.blit(score_text, [30, 20])
        
        pygame.display.flip()
        
    def data_process(self, y_list):
        new_list = y_list[::-1]
        index = 0
        score = 0
        for x in range(1,4):
            if new_list[x] == 0:
                continue
            if new_list[x] == new_list[index]:
                new_list[index] *= 2
                score += new_list[index]
                new_list[x] = 0
                index = x
            else:
                index = x
        index = 0
        for x in range(4):
            if new_list[x]!=0:
                if index == x:
                    index += 1
                    continue
                else:
                    new_list[index] = new_list[x]
                    new_list[x] = 0
                    index += 1

        self.score += score
        return new_list[::-1]
        
    def get_next(self):
        random_list = []
        for y in range(4):
            for x in range(4):
                if self._matrix[y][x] == 0:
                    random_list.append((y,x))
        (y,x) = random.choice(random_list)
        self._matrix[y][x] = 2
        return 

    def slide_left(self, matrix):
        for y in range(4):
            matrix[y] = self.data_process(matrix[y][::-1])[::-1]
        return matrix
        
    def slide_up(self, matrix):
        for y in range(4):
            matrix[:,y] = self.data_process(matrix[:,y][::-1])[::-1]
        return matrix
    
    def slide_down(self, matrix):
        for y in range(4):
            matrix[:,y] = self.data_process(matrix[:,y])
        return matrix
            
    def slide_right(self, matrix):
        for y in range(4):
            matrix[y] = self.data_process(matrix[y])
        return matrix
                   
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    new_matrix = copy.deepcopy(self._matrix)
                    if event.key == pygame.K_UP:
                        new_matrix = self.slide_up(new_matrix)
                    elif event.key == pygame.K_DOWN:
                        new_matrix = self.slide_down(new_matrix)
                    elif event.key == pygame.K_LEFT:
                        new_matrix = self.slide_left(new_matrix)
                    elif event.key == pygame.K_RIGHT:
                        new_matrix = self.slide_right(new_matrix)
                    if (new_matrix == self._matrix).all() == False:
                        self._matrix = copy.deepcopy(new_matrix)
                        self.get_next()
                        self.score += 2
            self.show_window()
            time.sleep(0.2)
            
        
if __name__ == "__main__":
    game_view = GameView()
    game_view.run()
    
    
        
