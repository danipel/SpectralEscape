import pygame

# Definimos algunos colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BEIGE = (245, 245, 220)
RED = (255, 0, 0)
LIGHT_YELLOW = (255, 255, 224)

class Wall(pygame.sprite.Sprite):        
    def __init__(self, x, y, weight, height):
        super().__init__()

        self.image = pygame.Surface([weight, height], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()

        self.image = img  
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Door(Wall): 
    room = None
    def __init__(self, x, y, weight, height):
        super().__init__(x, y, weight, height)

        self.image = pygame.Surface([weight, height])

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
class Entity(pygame.sprite.Sprite):
    # Set speed vector
    change_x = 0
    change_y = 0
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([x, y])
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    
    def changespeed(self, x, y):
        # Change the speed of the player. Called with a keypress.
        self.change_x += x
        self.change_y += y


class Player(Entity):

    def __init__(self, x, y):
        super().__init__(x, y)

        # Set height, width
        self.image = pygame.Surface([30, 25], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.walking_frames_u = []
        self.walking_frames_d = []
        self.walking_frames_l = []
        self.walking_frames_r = []

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.key_list = pygame.sprite.Group()  
    
    def move(self, walls):  # walls = pygame.sprite.Group()
        # Move Left - Right ---
        self.rect.x += self.change_x
        # Did this update cause us to hit a wall?
        hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in hit_list:
            # If we are moving right,
            # set our right side to the left side of the wall we hit
            if self.change_x > 0:
                self.rect.right = wall.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = wall.rect.right

        # Move up/down ---
        self.rect.y += self.change_y
        # Check and see if we hit anything
        hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in hit_list:
            # Reset our position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

    def walk(self, direction, index):
        if direction == "left":
            self.image = self.walking_frames_l[index]
        elif direction == "right":
            self.image = self.walking_frames_r[index]
        elif direction == "up":
            self.image = self.walking_frames_u[index]
        elif direction == "down":
            self.image = self.walking_frames_d[index]

class Ghost(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface([40, 60], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.active = True

    def kill(self):
        self.active = False
        self.image = pygame.Surface([0, 0])  # Make the ghost invisible

    def respawn(self):
        self.active = True
        self.image = pygame.Surface([40, 60]) # Make the ghost visible again

#  White Ghost: Moves left and right
class WhiteGhost(Ghost):    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.change_x = 1
        self.walking_frames_l = [pygame.image.load("characters/ghost_1/left_1.png").convert(),
                                 pygame.image.load("characters/ghost_1/left_2.png").convert()]
        self.walking_frames_r = [pygame.image.load("characters/ghost_1/right_1.png").convert(),
                                 pygame.image.load("characters/ghost_1/right_2.png").convert()]
        self.cooldown = 600
        self.index = 0
        self.tick_count = pygame.time.get_ticks()
        self.initial_x = x
    
    def ghost_move(self, dir):
        if self.active:
            if dir == "left":
                self.rect.x -= self.change_x
                if self.rect.x < self.initial_x - 478:
                    self.changespeed(-1, 0)
                elif self.rect.x > self.initial_x:
                    self.changespeed(1, 0)
            elif dir == "right":
                self.rect.x += self.change_x
                if self.rect.x > self.initial_x + 478:
                    self.changespeed(-1, 0)
                elif self.rect.x < self.initial_x:
                    self.changespeed(1, 0)
            
    
    def change_sprite(self, dir):
        if self.cooldown < pygame.time.get_ticks() - self.tick_count:
            self.index += 1
            if self.index > 1:
                self.index = 0
            if dir == "right":
                if self.change_x > 0:
                    self.image = self.walking_frames_r[self.index]
                else:
                    self.image = self.walking_frames_l[self.index]
            elif dir == "left":
                if self.change_x > 0:
                    self.image = self.walking_frames_l[self.index]
                else:
                    self.image = self.walking_frames_r[self.index]
            self.tick_count = pygame.time.get_ticks()

#  BlueGhost: enemy that moves up and down
class BlueGhost(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.change_y = 1
        self.walking_frames_u = [pygame.image.load("characters/ghost_2/up_1.png").convert(),
                                 pygame.image.load("characters/ghost_2/up_2.png").convert()]
        self.walking_frames_d = [pygame.image.load("characters/ghost_2/down_1.png").convert(),
                                 pygame.image.load("characters/ghost_2/down_2.png").convert()]
        self.cooldown = 600
        self.index = 0
        self.tick_count = pygame.time.get_ticks()
        self.initial_y = y

    def ghost_move(self, dir):
        if self.active:
            if dir == "up":
                self.rect.y -= self.change_y
                if self.rect.y < self.initial_y - 147:
                    self.changespeed(0, -1)
                elif self.rect.y > self.initial_y:
                    self.changespeed(0, 1)
            elif dir == "down":
                self.rect.y += self.change_y
                if self.rect.y > self.initial_y + 147:
                    self.changespeed(0, -1)
                elif self.rect.y < self.initial_y:
                    self.changespeed(0, 1)

    def change_sprite(self, dir):
        if self.cooldown < pygame.time.get_ticks() - self.tick_count:
            self.index += 1
            if self.index > 1:
                self.index = 0
            if dir == "up":
                if self.change_y > 0:
                        self.image = self.walking_frames_u[self.index]
                else:
                        self.image = self.walking_frames_d[self.index]
            elif dir == "down":
                if self.change_y > 0:
                    self.image = self.walking_frames_d[self.index]
                else:
                    self.image = self.walking_frames_u[self.index]
            self.tick_count = pygame.time.get_ticks()

#  BlackGhost: enemy rebounds on walls
class BlackGhost(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.change_x = 2
        self.change_y = 2
        self.walking_frames_l = [pygame.image.load("characters/ghost_3/left_1.png").convert(),
                                 pygame.image.load("characters/ghost_3/left_2.png").convert()]
        self.walking_frames_r = [pygame.image.load("characters/ghost_3/right_1.png").convert(),
                                 pygame.image.load("characters/ghost_3/right_2.png").convert()]
        for image in self.walking_frames_l + self.walking_frames_r:
            image.set_colorkey((0, 0, 0))
        self.cooldown = 500
        self.index = 0
        self.tick_count = pygame.time.get_ticks()
        self.initial_x = x
        self.initial_y = y

    def ghost_move(self):
        if self.active:
            self.rect.x += self.change_x
            self.rect.y += self.change_y
            if self.rect.y <= 227 or self.rect.y >= 517:
                self.change_y *= -1
            if self.rect.x <= 30 or self.rect.x >= 760:
                self.change_x *= -1

    
    def change_sprite(self):
        if self.cooldown < pygame.time.get_ticks() - self.tick_count:
            self.index += 1
            if self.index > 1:
                self.index = 0
            if self.change_x > 0:
                self.image = self.walking_frames_r[self.index]
            if self.change_x < 0:
                self.image = self.walking_frames_l[self.index]
            self.tick_count = pygame.time.get_ticks()

            
#  --- Rooms ---
class Room():
    # --- Parent class for all rooms. ---
    # Each room has a list of walls and a list of enemys.
    wall_list = None
    door_list = None
    interactives_list = None
    enemy_list = None

    def __init__(self):
        self.wall_list = []
        self.interactives_list = []
        # Each list will actually be a group of sprites.
        self.wall_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()

class Room1(Room):  # Main hall
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("scenarios/main_hall.png").convert()
        # List of walls. Each in the form [x, y, weight, height]
        walls = [[0, 0, 5, 483],
                 [0, 480, 326, 40],
                 [470, 480, 330, 40],
                 [320, 513, 153, 10],
                 [795, 0, 5, 483],
                 [64, 473, 40, 8],
                 [174, 473, 40, 8],
                 [283, 473, 43, 8],
                 [470, 473, 40, 8],
                 [585, 473, 40, 8],
                 [712, 260, 11, 88],
                 [132, 210, 540, 36],
                 [670, 217, 12, 22],
                 [682, 230, 12, 22],
                 [694, 235, 12, 22],
                 [704, 243, 12, 22],
                 [127, 136, 545, 11],
                 [670, 145, 12, 16],
                 [682, 158, 12, 16],
                 [694, 163, 12, 16],
                 [704, 171, 12, 16],
                 [716, 182, 80, 10],
                 [704, 171, 12, 16],
                 [70, 260, 11, 88],
                 [84, 178, 10, 13],
                 [90, 170, 10, 13],
                 [100, 160, 10, 13],
                 [110, 150, 10, 13],
                 [84, 246, 10, 13],
                 [90, 236, 10, 13],
                 [100, 226, 10, 13],
                 [110, 216, 10, 13],
                 [0, 183, 80, 11],
                 [83, 305, 630, 7],
                 [393, 275, 14, 73],
                 [620, 275, 14, 73],
                 [166, 275, 14, 73],
                 [603, 359, 19, 16],
                 [38, 409, 14, 8],
                 [84, 365, 13, 9],
                 [664, 355, 14, 10],
                 [738, 428, 11, 520]
                 ]
        # Add the walls to the group of the Room1.
        for item in walls:
            self.wall_list.add(Wall(item[0], item[1], item[2], item[3]))
        
        # List of doors. Each in the form [x, y, weight, height]
        self.door_list = [Door(334, 305, 57, 13),
                          Door(412, 302, 51, 13),
                          Door(378, 136, 42, 14),
                          Door(190, 136, 42, 14),
                          Door(568, 136, 42, 14)
                          ]
        # Add the room every door leads to.
        for d_num in range(len(self.door_list)):
            self.door_list[d_num].room = d_num + 1
        # We add the enemys to the group of the Room1.
        self.enemy_list.add(WhiteGhost(137, 155))

class Room2(Room):  # kitchen
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("scenarios/down_left.png").convert()
        # List of walls. Each in the form [x, y, weight, height]
        walls = [[0, 460, 11, 520],
                 [0, 505, 604, 35],
                 [604, 538, 76, 5],
                 [677, 505, 113, 35],
                 [780, 460, 12, 52],
                 [771, 393, 20, 52],
                 [762, 335, 30, 44],
                 [755, 275, 36, 44],
                 [699, 227, 55, 20],
                 [650, 246, 50, 29],
                 [572, 249, 52, 27],
                 [473, 247, 45, 26],
                 [520, 232, 49, 16],
                 [307, 233, 163, 15],
                 [97, 246, 207, 27],
                 [48, 234, 47, 17],
                 [10, 393, 14, 549],
                 [12, 332, 23, 43],
                 [13, 267, 30, 46],
                 [180, 424, 26, 18],
                 [705,441, 8, 9],
                 [728, 414, 12, 12],
                 [456, 295, 11, 13],
                 [527, 388, 21, 21],
                 [753, 250, 37, 24],
                 [20, 250, 25, 17],
                 [622, 232, 32, 17]
                ]
        # Add the walls to the group of the Room2.
        for item in walls:
            self.wall_list.add(Wall(item[0], item[1], item[2], item[3]))
        # List of doors. Each in the form [x, y, weight, height]
        self.door_list = [Door(606, 526, 71, 17)]
        # Add the room every door leads to.
        self.door_list[0].room = 0
        # List of others interactive objects. Each in the form [x, y]
        self.interactives_list = [Key(57, 259)]
        # Add the room every key leads to.
        self.interactives_list[0].room = 4
        # We add the enemys to the group of the Room2. 
        self.enemy_list.add(BlueGhost(55, 418))
        self.enemy_list.add(BlueGhost(255, 286))
        self.enemy_list.add(BlueGhost(435, 434))

class Room3(Room):  # Book room
    def __init__(self):
            super().__init__()
            self.background = pygame.image.load("scenarios/down_right.png").convert()
            # List of walls. Each in the form [x, y, weight, height]
            walls = [[1, 454, 7, 51],
                    [7, 490, 219, 27],
                    [221, 516, 91, 8],
                    [309, 490, 480, 22],
                    [4, 403, 18, 42],
                    [7, 338, 17, 43],
                    [4, 280, 22, 40],
                    [55, 287, 299, 21],
                    [380, 290, 128, 16],
                    [533, 290, 196, 15],
                    [760, 300, 14, 49],
                    [762, 367, 17, 45],
                    [774, 427, 17, 47],
                    [552, 414, 111, 58],
                    [320, 443, 31, 23],
                    [255, 328, 29, 19],
                    [508, 327, 17, 14],
                    [145, 428, 33, 51],
                    [192, 399, 31, 46],
                    [711, 360, 8, 8],
                    [730, 280, 35, 16]
                    ]
            # Add the walls to the group of the Room3.
            for item in walls:
                self.wall_list.add(Wall(item[0], item[1], item[2], item[3]))
            # List of doors. Each in the form [x, y, weight, height]
            self.door_list = [Door(222, 506, 89, 13)] 
            # Add the room every door leads to.
            self.door_list[0].room = 0
            # List of others interactive objects. Each in the form [x, y, weight, height]
            self.interactives_list = [Key(724, 313), Key(44, 445)]
            # Add the room every key leads to.
            self.interactives_list[0].room = 6
            self.interactives_list[1].room = 5
            # We add the enemys to the group of the Room3.
            self.enemy_list.add(WhiteGhost(40, 375))
            self.enemy_list.add(WhiteGhost(668, 312))

class Room4(Room):  # Final Room
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("scenarios/top_center.png").convert()
        # List of walls. Each in the form [x, y, weight, height]
        walls = [[60, 433, 26, 70],
                 [65, 354, 24, 54],
                 [110, 290, 62, 47],
                 [190, 264, 27, 50],
                 [190, 205, 164, 28],
                 [405, 205, 168, 27],
                 [560, 350, 45, 48],
                 [355, 232, 49, 26],
                 [570, 230, 45, 24],
                 [648, 237, 32, 78],
                 [663, 342, 31, 69],
                 [514, 444, 48, 50],
                 [609, 400, 45, 46],
                 [450, 483, 52, 28],
                 [607, 480, 53, 26],
                 [680, 442, 16, 64],
                 [522, 506, 79, 8],
                 [255, 483, 49, 26],
                 [98, 484, 53, 23],
                 [150, 504, 104, 13],
                 [446, 541, 133, 25],
                 [339, 298, 34, 19],
                 [620, 208, 29, 25],
                 [660, 316, 23, 27],
                 [167, 237, 25, 25],
                 [69, 410, 16, 25],
                 [81, 337, 25, 16],
                 [676, 416, 18, 23]
                 ]
        # Add the walls to the group of the Room4.
        for item in walls:
            self.wall_list.add(Wall(item[0], item[1], item[2], item[3]))
        # List of doors. Each in the form [x, y, weight, height]
        self.door_list = [Door(309, 508, 144, 40)]
        # Add the room every door leads to.
        self.door_list[0].room = 0
        self.interactives_list = pygame.sprite.Group()
        

class Room5(Room):  # Dance room
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("scenarios/top_left.png").convert()
        # List of walls. Each in the form [x, y, weight, height]
        walls = [[94, 500, 202, 51],
                 [295, 535, 176, 46],
                 [470, 500, 222, 50],
                 [596, 422, 66, 60],
                 [110, 416, 66, 60],
                 [50, 340, 66, 60],
                 [663, 372, 66, 60],
                 [661, 300, 66, 60],
                 [744, 198, 27, 82],
                 [643, 200, 1022, 20],
                 [490, 215, 153, 20],
                 [388, 198, 105, 20],
                 [210, 220, 34, 24],
                 [244, 211, 137, 20],
                 [60, 226, 75, 25],
                 [25, 254, 16, 80],
                 [75, 475, 31, 24],
                 [140, 198, 62, 22]
                 ]
        # Add the walls to the group of the Room5.
        for item in walls:
            self.wall_list.add(Wall(item[0], item[1], item[2], item[3]))
        # List of doors. Each in the form [x, y, weight, height]
        self.door_list = [Door(295, 526, 175, 16)]
        # Add the room every door leads to.
        self.door_list[0].room = 0
        # We add the enemys to the group of the Room5. 
        self.enemy_list.add(WhiteGhost(260, 247))
        self.enemy_list.add(WhiteGhost(470, 370))
        self.enemy_list.add(BlueGhost(536, 450))
        self.enemy_list.add(BlueGhost(130, 234))     

class Room6(Room):  # Girls room
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("scenarios/top_right.png").convert()
        # List of walls. Each in the form [x, y, weight, height]
        walls = [[21, 517, 81, 37],
                 [100, 552, 75, 14],
                 [175, 518, 597, 32],
                 [17, 424, 16, 71],
                 [24, 320, 22, 90],
                 [34, 288, 26, 25],
                 [70, 234, 127, 62],
                 [215, 225, 105, 41],
                 [320, 206, 314, 30],
                 [634, 237, 77, 28],
                 [727, 253, 23, 73],
                 [740, 340, 22, 76],
                 [750, 450, 18, 68]
                 ]
        # Add the walls to the group of the Room6.
        for item in walls:
            self.wall_list.add(Wall(item[0], item[1], item[2], item[3]))
        # List of doors. Each in the form [x, y, weight, height]
        self.door_list = [Door(100, 540, 77, 13), Door(643, 253, 62, 18)]
        # Add the room every door leads to.
        self.door_list[0].room = 0
        self.door_list[1].room = 6
        # We add the enemys to the group of the Room6. 
        self.enemy_list.add(BlackGhost(166, 311))
        self.enemy_list.add(BlackGhost(600, 311))
        self.enemy_list.add(BlackGhost(414, 460))
        #self.enemy_list.add(Wall(394, 255, 127, 48))  In process
    
class Key(pygame.sprite.Sprite):
    # Room it belongs to
    room = None
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("sources/key.png").convert() 
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
