# main.py
import pygame
import json
import sys
import copy

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

from board import Board
from tetromino import Tetromino, SHAPES
from renderer import draw_grid, draw_board, draw_piece, draw_ui

pygame.init()
screen = pygame.display.set_mode((config["window_width"], config["window_height"]))
pygame.display.set_caption("Тетрис — Лабораторная работа №3")
clock = pygame.time.Clock()
font = pygame.font.SysFont("segoeui", 28, bold=True)

board = Board()
current_piece = board.new_piece()
next_piece = board.new_piece()

"""
# С рывками версия

fall_time = 0
fall_speed = config["fall_speed"]

# Для мгновенного падения при нажатии ↓
hard_drop = False

running = True
while running:
    fall_time += clock.get_rawtime() / 1000
    clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not board.game_over:
            if event.key == pygame.K_LEFT:
                current_piece.x -= 1
                if not board.valid_move(current_piece):
                    current_piece.x += 1
            if event.key == pygame.K_RIGHT:
                current_piece.x += 1
                if not board.valid_move(current_piece):
                    current_piece.x -= 1
            if event.key == pygame.K_DOWN:
                fall_speed = 0.05  # ускоряем падение
            if event.key == pygame.K_UP:
                rotated = copy.deepcopy(current_piece)
                rotated.rotate()
                if board.valid_move(rotated):
                    current_piece.rotate()
            if event.key == pygame.K_SPACE:  # мгновенное падение
                while board.valid_move(current_piece):
                    current_piece.y += 1
                current_piece.y -= 1
                hard_drop = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                fall_speed = config["fall_speed"]

    # Автоматическое падение
    if fall_time >= fall_speed and not board.game_over:
        current_piece.y += 1
        if not board.valid_move(current_piece):
            current_piece.y -= 1
            board.lock_piece(current_piece)
            current_piece = next_piece
            next_piece = board.new_piece()
            hard_drop = False
        fall_time = 0

    screen.fill(config["background_color"])
    draw_grid(screen)
    draw_board(screen, board)
    draw_piece(screen, current_piece)
    draw_ui(screen, font, board, next_piece)

    if board.game_over:
        game_over_text = font.render("ИГРА ОКОНЧЕНА", True, (255, 50, 50))
        restart_text = font.render("Нажмите R для рестарта", True, (200, 200, 200))
        screen.blit(game_over_text, (120, 250))
        screen.blit(restart_text, (130, 320))
        if pygame.key.get_pressed()[pygame.K_r]:
            board = Board()
            current_piece = board.new_piece()
            next_piece = board.new_piece()

    pygame.display.flip()

pygame.quit()
sys.exit()"""


# плавная версия

piece_y_float = 0.0
base_fall_speed = config["fall_speed"]

running = True
while running:
    dt = clock.tick(60) / 1000.0
    fall_time = dt  # используем реальное время кадра

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not board.game_over:
            if event.key == pygame.K_LEFT:
                current_piece.x -= 1
                if not board.valid_move(current_piece):
                    current_piece.x += 1
            if event.key == pygame.K_RIGHT:
                current_piece.x += 1
                if not board.valid_move(current_piece):
                    current_piece.x -= 1
            if event.key == pygame.K_UP:
                rotated = copy.deepcopy(current_piece)
                rotated.rotate()
                if board.valid_move(rotated):
                    current_piece.rotate()
            if event.key == pygame.K_SPACE:
                while board.valid_move(current_piece):
                    current_piece.y += 1
                    piece_y_float += 1.0
                current_piece.y -= 1
                piece_y_float = current_piece.y
                board.lock_piece(current_piece)
                current_piece = next_piece
                next_piece = board.new_piece()
                piece_y_float = 0.0

    if board.game_over and pygame.key.get_pressed()[pygame.K_r]:
        board = Board()
        current_piece = board.new_piece()
        next_piece = board.new_piece()
        piece_y_float = 0.0

    # Определяем скорость падения
    current_speed = base_fall_speed
    if pygame.key.get_pressed()[pygame.K_DOWN] and not board.game_over:
        current_speed = 0.05

    # Плавное падение с постоянной проверкой коллизии
    if not board.game_over:
        # Сохраняем старую позицию
        old_y_int = current_piece.y
        old_y_float = piece_y_float

        # Пробуем опуститься
        piece_y_float += dt / current_speed
        current_piece.y = int(piece_y_float + 0.999)

        # Проверяем
        if not board.valid_move(current_piece):
            # НЕ влезло — возвращаем на предыдущую валидную позицию
            current_piece.y = old_y_int
            piece_y_float = float(old_y_int)
            board.lock_piece(current_piece)
            current_piece = next_piece
            next_piece = board.new_piece()
            piece_y_float = 0.0
        else:
            pass  # Всё ок — оставляем новую позицию

    # Отрисовка
    screen.fill(config["background_color"])
    draw_grid(screen)
    draw_board(screen, board)

    # Рисуем с плавным смещением
    saved_y = current_piece.y
    current_piece.y = piece_y_float
    draw_piece(screen, current_piece)
    current_piece.y = saved_y  # возвращаем целую координату для логики

    draw_ui(screen, font, board, next_piece)

    if board.game_over:
        game_over_text = font.render("ИГРА ОКОНЧЕНА", True, (255, 50, 50))
        restart_text = font.render("Нажмите R для рестарта", True, (200, 200, 200))
        screen.blit(game_over_text, (120, 250))
        screen.blit(restart_text, (130, 320))

    pygame.display.flip()

pygame.quit()
sys.exit()
