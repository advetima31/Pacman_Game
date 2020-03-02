import pygame
from os import path
from random import randint


def load_image(name: str):
    fullname = path.join('Images', name)
    image = pygame.image.load(fullname).convert()
    image.set_colorkey((0, 0, 0))
    return image


class Field:
    def __init__(self, screen_size: tuple):
        self.sc_s = tuple(i // 64 * 64 for i in screen_size)
        self.screen = pygame.display.set_mode(self.sc_s)
        self.__clock = pygame.time.Clock()
        self.get_time = lambda: self.__clock.tick() / 1000
        self.field = [[1 for i in range(screen_size[0] // 64)]] + \
                     [[1] + [None for y in range(1, screen_size[0] // 64 - 1)] + [1]
                      for i in range(1, screen_size[1] // 64 - 1)] + [[1 for i in range(screen_size[0] // 64)]]
        self.walls = pygame.sprite.Group()
        self.points = pygame.sprite.Group()
        shifr = {(i % 3 - 1, i // 3 - 1): (2, 3, 5, 7, 1, 11, 13, 17, 19)[i] for i in range(9)}
        for i in range(2, screen_size[1] // 64 - 2, 2):
            dead_end, run = False, False
            if randint(1, 3) // 3:
                continue
            for j in range(1, screen_size[0] // 64 - 1):
                if run:
                    self.field[i][j] = 1
                    if (self.field[i - 1][j + 1] or self.field[i + 1][j + 1]):
                        run = dead_end = False
                    elif (self.field[i][j + 2] or self.field[i - 1][j + 2] or self.field[i + 1][j + 2]
                          and randint(1, 2) // 2) or dead_end:
                        run = dead_end = False
                    elif randint(1, 2) // 2 and not (self.field[i][j + 2] or self.field[i - 1][j + 2] \
                                                     or self.field[i + 1][j + 2]) and not (self.field[i - 1][j + 1] \
                                                                                           or self.field[i + 1][j + 1]):
                        run = dead_end = False
                elif (self.field[i - 1][j - 1] or self.field[i + 1][j - 1]) and randint(1, 2) // 2:
                    dead_end = True
                    run = True
                elif (self.field[i][j - 2] or self.field[i - 1][j - 2] or self.field[i + 1][j - 2]) \
                        and randint(1, 3) // 2:
                    run = True
                elif randint(1, 3) // 3 and not (self.field[i][j - 2] or self.field[i - 1][j - 2] \
                                                 or self.field[i + 1][j - 2]) and not (self.field[i - 1][j - 1] \
                                                                                       or self.field[i + 1][j - 1]):
                    run = True
        run = False
        for j in range(2, screen_size[0] // 64 - 2, 2):
            dead_end, run = False, False
            for i in range(1, screen_size[1] // 64 - 1):
                if run:
                    self.field[i][j] = 1
                    if (self.field[i + 1][j + 1] or self.field[i + 1][j - 1]):
                        run = dead_end = False
                    elif ((self.field[i + 2][j] or self.field[i + 2][j - 1] or self.field[i + 2][j + 1]) \
                          and randint(1, 2) // 2) or dead_end:
                        run = dead_end = False
                    elif randint(1, 2) // 2 and not (self.field[i + 2][j + 1] or self.field[i + 2][j - 1] \
                                                     or self.field[i + 2][j]) and not (self.field[i + 1][j - 1] \
                                                                                       or self.field[i + 1][j + 1]):
                        run = dead_end = False
                elif (self.field[i - 1][j + 1] or self.field[i - 1][j - 1]) and randint(1, 2) // 2:
                    dead_end = True
                    run = True
                elif (self.field[i - 2][j] or self.field[i - 2][j + 1] or self.field[i - 2][j - 1]) \
                        and randint(1, 3) // 2:
                    run = True
                elif randint(1, 3) // 3 and not (self.field[i - 2][j - 1] or self.field[i - 2][j + 1] \
                                                 or self.field[i - 2][j]) and not (self.field[i - 1][j + 1] \
                                                                                   or self.field[i - 1][j - 1]):
                    run = True
        for i in range(screen_size[1] // 64):
            for j in range(screen_size[0] // 64):
                if self.field[i][j]:
                    lt, rt, lb, rb = 1, 1, 1, 1
                    for y in range(i - 1, i + 2):
                        if y != -1 and y != screen_size[1] // 64:
                            for x in range(j - 1, j + 2):
                                if x != -1 and x != screen_size[0] // 64:
                                    if self.field[y][x] is None:
                                        if x - j >= 0 <= y - i:
                                            rt *= shifr[(x - j, y - i)]
                                        if x - j >= 0 >= y - i:
                                            rb *= shifr[(x - j, y - i)]
                                        if x - j <= 0 <= y - i:
                                            lt *= shifr[(x - j, y - i)]
                                        if x - j <= 0 >= y - i:
                                            lb *= shifr[(x - j, y - i)]
                    lt, rt, rb, lb = lb, rb, rt, lt
                    self.walls.add(Wall(lt, (j * 64, i * 64)))
                    self.walls.add(Wall(rt, (j * 64 + 32, i * 64)))
                    self.walls.add(Wall(lb, (j * 64, i * 64 + 32)))
                    self.walls.add(Wall(rb, (j * 64 + 32, i * 64 + 32)))
                else:
                    if randint(1, 10) // 10:
                        self.points.add(Point(coords=(j * 64, i * 64), score=100, image='big_point.png', rage=True))
                    elif randint(1, 20) // 20:
                        self.points.add(Point(coords=(j * 64, i * 64), score=250, image='cherry.jpg'))
                    else:
                        self.points.add(Point(coords=(j * 64, i * 64)))
        self.score = 0
        self.creatures = pygame.sprite.Group()
        direction = [lambda: 1, lambda: -1, lambda: randint(-1, 1), lambda: randint(0, 1) * 2 - 1]
        for j in range(4):
            coords = (randint(1, len(self.field[0]) - 2), randint(1, len(self.field) - 2))
            while not self.field[coords[1]][coords[0]] is None:
                coords = (randint(1, len(self.field[0]) - 2), randint(1, len(self.field) - 2))
            self.creatures.add(Ghosts(tuple(i * 64 + 8 for i in coords),
                                      image=['pink', 'yellow', 'green', 'red'][j] +'.png', main_direction=direction[j]))
        pygame.init()

    def flip(self, time: float):
        self.screen.fill((0, 0, 0))
        for point in self.points:
            if point.flip():
                self.score += point.flip()
                self.points.remove(point)
        for creature in self.creatures:
            score = creature.flip(time, self.field)
            if score:
                self.score += score
                self.creatures.remove(creature)
        self.points.draw(self.screen)
        self.creatures.draw(self.screen)
        self.walls.draw(self.screen)
        self.creatures.draw(self.screen)
        font = pygame.font.Font(None, 50)
        text = font.render("score: " + str(self.score), 1, (100, 255, 100))
        text_x = self.sc_s[0] - text.get_width() - 30
        text_y = - text.get_height() // 2 + 30
        text_w = text.get_width()
        text_h = text.get_height()
        self.screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, (200, 255, 200), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
        pygame.display.flip()


class Wall(pygame.sprite.Sprite):
    def __init__(self, image: int, coords: tuple):
        super().__init__()
        self.image = load_image(str(image) + '.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords


class Point(pygame.sprite.Sprite):
    def __init__(self, coords: tuple, score: int = 1, image: str = 'point.png', rage: bool=False):
        super().__init__()
        self.image = load_image(image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (32 - self.rect[2 + i] // 2 + coords[i] for i in range(2))
        self.score = score
        self.rage = rage

    def flip(self):
        if pygame.sprite.collide_mask(self, pacman):
            if not pacman.rage:
                pacman.rage = self.rage
            return self.score
        return 0


class Pacman(pygame.sprite.Sprite):
    def __init__(self, speed: int, coords: tuple = (72, 72)):
        super().__init__()
        self.image = load_image('none.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.frames = [load_image(i) for i in ['none.png', 'top.png', 'right.png', 'bottom.png', 'left.png']]
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.speed = speed
        self.coords = [i for i in coords]
        self.direction = 1
        self.next_direction = None
        self.rage = False
        self.time = 0

    def flip(self, time: float, field):
        if self.rage:
            self.time += time
        if self.time > 3.5:
            self.rage = False
            self.time = 0
        cell_coords = tuple(int((self.coords[i]) // 64 * int((self.coords[i] + 32) > 0)) for i in range(2))
        cell_coords = [cell_coords[i] if cell_coords[i] < (len(field[0]), len(field))[i] else cell_coords[i] < (
            len(field[0]), len(field))[i] - 1 for i in range(2)]
        rx, ry = tuple(round(self.coords[i] % 64) == 32 - self.rect[2 + i] // 2 for i in range(2))
        if self.next_direction is None:
            pass
        elif abs(self.next_direction - self.direction) == 2:
            self.direction, self.next_direction = self.next_direction, None
        else:
            if self.next_direction == 0:
                if field[cell_coords[1] - 1][cell_coords[0]] is None and rx:
                    self.direction, self.next_direction = 0, None
            elif self.next_direction == 2:
                if field[cell_coords[1] + 1][cell_coords[0]] is None and rx:
                    self.direction, self.next_direction = 2, None
            elif self.next_direction == 1:
                if field[cell_coords[1]][cell_coords[0] + 1] is None and ry:
                    self.direction, self.next_direction = 1, None
            elif self.next_direction == 3:
                if field[cell_coords[1]][cell_coords[0] - 1] is None and ry:
                    self.direction, self.next_direction = 3, None
        if self.direction == 0 and not (field[cell_coords[1] - 1][cell_coords[0]] and ry):
            self.coords[1] -= self.speed * time
            if self.coords[1] < -self.rect[3]:
                self.coords[1] = len(field) * 64 + self.rect[3]
        elif self.direction == 1 and not (field[cell_coords[1]][cell_coords[0] + 1] and rx):
            self.coords[0] += self.speed * time
            if self.coords[0] > len(field[0]) * 64 + self.rect[2]:
                self.coords[0] = -self.rect[2]
        elif self.direction == 2 and not (field[cell_coords[1] + 1][cell_coords[0]] and ry):
            self.coords[1] += self.speed * time
            if self.coords[1] > len(field) * 64 + self.rect[3]:
                self.coords[1] = -self.rect[3]
        elif self.direction == 3 and not (field[cell_coords[1]][cell_coords[0] - 1] and rx):
            self.coords[0] -= self.speed * time
            if self.coords[0] < -self.rect[2]:
                self.coords[0] = len(field[0]) * 64 + self.rect[2]
        self.rect.x, self.rect.y = self.coords

    def animation(self):
        if self.image == self.frames[0]:
            self.image = self.frames[1 + self.direction]
        else:
            self.image = self.frames[0]


class Ghosts(pygame.sprite.Sprite):
    def __init__(self, coords: tuple, main_direction, score: int = 200, image: str = 'pink.png', speed: int = 60):
        super().__init__()
        self.color = self.image =load_image(image)
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.coords = [i for i in coords]
        self.score = score
        self.direction = 0
        self.main_direction = main_direction

    def flip(self, time: float, field):
        cell_coords = tuple(int((self.coords[i]) // 64 * int((self.coords[i] + 32) > 0)) for i in range(2))
        cell_coords = [cell_coords[i] if cell_coords[i] < (len(field[0]), len(field))[i] else cell_coords[i] < (
            len(field[0]), len(field))[i] - 1 for i in range(2)]
        rx, ry = tuple(round(self.coords[i] % 64) == 32 - self.rect[2 + i] // 2 for i in range(2))
        if abs(self.main_direction() + self.direction) % 4 == 0:
            if field[cell_coords[1] - 1][cell_coords[0]] is None and rx:
                self.direction = 0
        elif abs(self.main_direction() + self.direction) % 4 == 2:
            if field[cell_coords[1] + 1][cell_coords[0]] is None and rx:
                self.direction = 2
        elif abs(self.main_direction() + self.direction) % 4 == 1:
            if field[cell_coords[1]][cell_coords[0] + 1] is None and ry:
                self.direction = 1
        elif abs(self.main_direction() + self.direction) % 4 == 3:
            if field[cell_coords[1]][cell_coords[0] - 1] is None and ry:
                self.direction = 3
        if self.direction == 0:
            if (field[cell_coords[1] - 1][cell_coords[0]] and ry):
                self.direction = 2
            else:
                self.coords[1] -= self.speed * time
                if self.coords[1] < -self.rect[3]:
                    self.coords[1] = len(field) * 64 + self.rect[3]
        elif self.direction == 1:
            if (field[cell_coords[1]][cell_coords[0] + 1] and rx):
                self.direction = 3
            else:
                self.coords[0] += self.speed * time
                if self.coords[0] > len(field[0]) * 64 + self.rect[2]:
                    self.coords[0] = -self.rect[2]
        elif self.direction == 2:
            if (field[cell_coords[1] + 1][cell_coords[0]] and ry):
                self.direction = 0
            else:
                self.coords[1] += self.speed * time
                if self.coords[1] > len(field) * 64 + self.rect[3]:
                    self.coords[1] = -self.rect[3]
        elif self.direction == 3:
            if (field[cell_coords[1]][cell_coords[0] - 1] and rx):
                self.direction = 1
            else:
                self.coords[0] -= self.speed * time
                if self.coords[0] < -self.rect[2]:
                    self.coords[0] = len(field[0]) * 64 + self.rect[2]
        if pacman.rage:
            self.image = load_image('thick.png')
            if pygame.sprite.collide_mask(self, pacman):
                return self.score
        else:
            self.image = self.color
            if pygame.sprite.collide_mask(self, pacman):
                global run
                run = False
        self.rect.x, self.rect.y = self.coords
        return 0


if __name__ == '__main__':
    run = True
    game = Field((1080, 720))
    pacman = Pacman(64)
    game.creatures.add(pacman)
    animation_time = 0
    while run:
        time = game.get_time()
        animation_time += time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            pacman.next_direction = 0
        elif key[pygame.K_d]:
            pacman.next_direction = 1
        elif key[pygame.K_s]:
            pacman.next_direction = 2
        elif key[pygame.K_a]:
            pacman.next_direction = 3
        pacman.flip(time, game.field)
        game.flip(time)
        if animation_time >= 0.5:
            pacman.animation()
            animation_time -= 0.5
