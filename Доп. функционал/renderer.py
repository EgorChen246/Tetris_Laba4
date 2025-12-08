import pygame
import json
from tetromino import Tetromino

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

FIELD_X_LEFT  = 100    # Левое поле (WASD)
FIELD_X_RIGHT = 780    # Правое поле — сдвинуто вправо (+140 от предыдущего)
INFO_X_LEFT   = 500    # UI слева
INFO_X_RIGHT  = 1180   # UI справа — теперь полностью помещается
FIELD_Y       = 40

def draw_grid(screen, x_offset):
    w = config["cols"] * config["cell_size"]
    h = config["rows"] * config["cell_size"]
    for i in range(config["cols"] + 1):
        x = x_offset + i * config["cell_size"]
        pygame.draw.line(screen, config["grid_color"], (x, FIELD_Y), (x, FIELD_Y + h))
    for i in range(config["rows"] + 1):
        y = FIELD_Y + i * config["cell_size"]
        pygame.draw.line(screen, config["grid_color"], (x_offset, y), (x_offset + w, y))

def draw_board(screen, board, x_offset):
    for y, row in enumerate(board.grid):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    x_offset + x * config["cell_size"] + 1,
                    FIELD_Y + y * config["cell_size"] + 1,
                    config["cell_size"] - 2,
                    config["cell_size"] - 2
                )
                pygame.draw.rect(screen, cell, rect)
                pygame.draw.rect(screen, (100, 100, 150), rect, 1)

def draw_piece(screen, piece, x_offset):
    for x, y in piece.get_positions():
        if y >= 0:
            rect = pygame.Rect(
                x_offset + x * config["cell_size"] + 1,
                FIELD_Y + y * config["cell_size"] + 1,
                config["cell_size"] - 2,
                config["cell_size"] - 2
            )
            pygame.draw.rect(screen, piece.color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)

def draw_ui(screen, font, board, next_piece, info_x, player_title):
    score_text = font.render(f"Счёт: {board.score}", True, (255, 255, 255))
    lines_text = font.render(f"Линии: {board.lines}", True, (255, 255, 255))
    high_text = font.render(f"Рекорд: {board.high_score}", True, (255, 255, 0))

    screen.blit(score_text, (info_x, 60))
    screen.blit(lines_text, (info_x, 110))
    screen.blit(high_text, (info_x, 160))

    # Превью следующей фигуры
    preview_rect = pygame.Rect(info_x - 20, 210, 190, 190)
    pygame.draw.rect(screen, (40, 40, 80), preview_rect, border_radius=15)
    pygame.draw.rect(screen, (120, 120, 255), preview_rect, 4, border_radius=15)

    temp = Tetromino(0, 0, next_piece.shape)
    temp.color = next_piece.color
    positions = temp.get_positions()
    min_x = min(p[0] for p in positions)
    max_x = max(p[0] for p in positions)
    min_y = min(p[1] for p in positions)
    max_y = max(p[1] for p in positions)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    offset_x = info_x + 95 - (width * config["cell_size"]) // 2
    offset_y = 210 + 95 - (height * config["cell_size"]) // 2

    for x, y in positions:
        rect = pygame.Rect(
            offset_x + (x - min_x) * config["cell_size"],
            offset_y + (y - min_y) * config["cell_size"],
            config["cell_size"] - 2,
            config["cell_size"] - 2
        )
        pygame.draw.rect(screen, temp.color, rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

    # каждая строка отдельно
    y_pos = 430
    title = font.render(player_title, True, (255, 255, 255))
    screen.blit(title, (info_x - 20, y_pos))
    y_pos += 40

    small_font = pygame.font.SysFont("segoeui", 24, bold=False)  # чуть меньше шрифт для читаемости

    if "WASD" in player_title:
        controls = [
            "W  —  поворот",
            "A  —  влево",
            "D  —  вправо",
            "S  —  ускорение",
            "Ctrl  —  мгновенное",
            "        падение"
        ]
    else:
        controls = [
            "↑      —  поворот",
            "←  →  —  движение",
            "↓      —  ускорение",
            "Пробел —  мгновенное",
            "          падение"
        ]

    for line in controls:
        surf = small_font.render(line, True, (200, 220, 255))
        screen.blit(surf, (info_x - 15, y_pos))
        y_pos += 32
