# tetromino.py
import pygame
import random
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Все фигуры (в формате 4 поворота)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]


class Tetromino:
    def __init__(self, x, y, shape=None):
        self.x = x
        self.y = y
        self.shape = shape or random.choice(SHAPES)
        self.color = random.choice(list(config["colors"].values()))
        self.rotation = 0

    def rotate(self):
        # Поворот по часовой стрелке
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def get_positions(self):
        positions = []
        for row_idx, row in enumerate(self.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    positions.append((self.x + col_idx, self.y + row_idx))
        return positions