# renderer.py
import pygame
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

from tetromino import Tetromino

FIELD_X = 80
FIELD_Y = 40
INFO_X = 480


def draw_grid(screen):
    w = config["cols"] * config["cell_size"]
    h = config["rows"] * config["cell_size"]

    for i in range(config["cols"] + 1):
        x = FIELD_X + i * config["cell_size"]
        pygame.draw.line(screen, config["grid_color"], (x, FIELD_Y), (x, FIELD_Y + h))
    for i in range(config["rows"] + 1):
        y = FIELD_Y + i * config["cell_size"]
        pygame.draw.line(screen, config["grid_color"], (FIELD_X, y), (FIELD_X + w, y))


def draw_board(screen, board):
    for y, row in enumerate(board.grid):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    FIELD_X + x * config["cell_size"] + 1,
                    FIELD_Y + y * config["cell_size"] + 1,
                    config["cell_size"] - 2,
                    config["cell_size"] - 2,
                )
                pygame.draw.rect(screen, cell, rect)
                pygame.draw.rect(screen, (100, 100, 150), rect, 1)


def draw_piece(screen, piece):
    for x, y in piece.get_positions():
        if y >= 0:
            rect = pygame.Rect(
                FIELD_X + x * config["cell_size"] + 1,
                FIELD_Y + y * config["cell_size"] + 1,
                config["cell_size"] - 2,
                config["cell_size"] - 2,
            )
            pygame.draw.rect(screen, piece.color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)


def draw_ui(screen, font, board, next_piece):
    # Счёт и линии
    score_text = font.render(f"Счёт: {board.score}", True, (255, 255, 255))
    lines_text = font.render(f"Линии: {board.lines}", True, (255, 255, 255))
    screen.blit(score_text, (INFO_X, 60))
    screen.blit(lines_text, (INFO_X, 110))

    # Рамка следующей фигуры
    preview_rect = pygame.Rect(INFO_X - 20, 180, 190, 190)
    pygame.draw.rect(screen, (40, 40, 80), preview_rect, border_radius=15)
    pygame.draw.rect(screen, (120, 120, 255), preview_rect, 4, border_radius=15)

    # по центру
    temp = Tetromino(0, 0, next_piece.shape)
    temp.color = next_piece.color

    # Находим границы фигуры
    positions = temp.get_positions()
    min_x = min(pos[0] for pos in positions)
    max_x = max(pos[0] for pos in positions)
    min_y = min(pos[1] for pos in positions)
    max_y = max(pos[1] for pos in positions)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Центрируем в рамке
    offset_x = INFO_X + 95 - (width * config["cell_size"]) // 2
    offset_y = 285 - (height * config["cell_size"]) // 2

    for x, y in positions:
        rect = pygame.Rect(
            offset_x + (x - min_x) * config["cell_size"],
            offset_y + (y - min_y) * config["cell_size"],
            config["cell_size"] - 2,
            config["cell_size"] - 2,
        )
        pygame.draw.rect(screen, temp.color, rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
