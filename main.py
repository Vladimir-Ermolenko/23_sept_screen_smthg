import pygame
from random import random
from math import sqrt

SCREEN_SIZE = (1280, 720)


class Vector:

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Vector((self.x - other.x, self.y - other.y))

    def __mul__(self, other):
        return Vector((self.x * other, self.y * other))

    def scalar_mul(self, other):
        return self.x * other + self.y * other

    def __len__(self):
        return sqrt(self.x + self.y)

    def int_pair(self):
        return self.x, self.y


class Line:

    def __init__(self):
        pass

    @staticmethod
    def draw_points(vectors, color_, style="points", width=10):
        if style == "line":
            for point_number in range(-1, len(vectors) - 1):
                pygame.draw.line(gameDisplay, color_, (int(vectors[point_number].x), int(vectors[point_number].y)),
                                 (int(vectors[point_number + 1].x), int(vectors[point_number + 1].y)), width)

        elif style == "points":
            for vector_ in vectors:
                pygame.draw.circle(gameDisplay, (232, 138, 104), (int(vector_.x), int(vector_.y)), width)

    def get_point(self, vector, alpha, deg=None):
        if deg is None:
            deg = len(vector) - 1
        if deg == 0:
            return vector[0]

        line = Line()
        return Vector.__add__(Vector.__mul__(vector[deg], alpha), Vector.__mul__(Line.get_point(line, vector, alpha,
                                                                                                deg - 1), 1 - alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        result = []
        for i in range(count):
            line = Line()
            result.append(Line.get_point(line, base_points, i * alpha))
        return result

    @staticmethod
    def set_points(vectors, speeds):
        for vector_ in range(len(vectors)):
            vectors[vector_] = Vector.__add__(vectors[vector_], speeds[vector_])
            if vectors[vector_].x > SCREEN_SIZE[0] or vectors[vector_].x < 0:
                speeds[vector_] = Vector((- speeds[vector_].x, speeds[vector_].y))
            if vectors[vector_].y > SCREEN_SIZE[1] or vectors[vector_].y < 0:
                speeds[vector_] = Vector((speeds[vector_].x, -speeds[vector_].y))


class Joint(Line):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_joint(vectors, count):
        if len(vectors) < 3:
            return []
        result = []
        for i in range(-2, len(vectors) - 2):
            vct = []
            vct.append(Vector.__mul__(Vector.__add__(vectors[i], vectors[i + 1]), 0.5))
            vct.append(vectors[i + 1])
            vct.append(Vector.__mul__(Vector.__add__(vectors[i + 1], vectors[i + 2]), 0.5))

            line = Line()
            result.extend(Line.get_points(line, vct, count))
        return result


def display_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("Courier", 30)
    font2 = pygame.font.SysFont("Courier New", 30)
    data = []
    data.append(["F1", "Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Play/Pause"])
    data.append(["F2", "Add point"])
    data.append(["F3", "Delete point"])
    data.append(["", ""])
    data.append([str(steps), "points in a line"])

    pygame.draw.lines(gameDisplay, (235, 224, 152), True, [
                      (0, 0), (600, 0), (600, 400), (0, 400)], 2)

    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver 2.0")

    steps = 20
    working = True
    vectors = []
    speeds = []
    show_help = False
    pause = False

    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    vectors = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_F2:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_F3:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                vect = Vector(event.pos)
                vectors.append(vect)
                speeds.append(Vector((random() * 2, random() * 2)))

        gameDisplay.fill((114, 122, 166))
        color_hue = (color_param + 1) % 360
        color.hsla = (color_hue, 80, 85, 100)
        Line.draw_points(vectors, (232, 138, 104))
        Line.draw_points(Joint.get_joint(vectors, steps), color, "line", 7)
        if not pause:
            Line.set_points(vectors, speeds)
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
