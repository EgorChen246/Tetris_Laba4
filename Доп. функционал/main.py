import pygame
import json
import sys
import copy

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

from board import Board
from tetromino import Tetromino
from renderer import draw_grid, draw_board, draw_piece, draw_ui, FIELD_X_LEFT, FIELD_X_RIGHT, INFO_X_LEFT, INFO_X_RIGHT

# Выбор режима
mode = input("Выберите режим: 1 - одиночный, 2 - мультиплеер: ")
multiplayer = mode == "2"
mode_str = "multi" if multiplayer else "single"

pygame.init()
screen = pygame.display.set_mode((config["window_width"], config["window_height"]))
pygame.display.set_caption(f"Тетрис — Лабораторная работа №4 | Режим: {'Мультиплеер' if multiplayer else 'Одиночный'}")
clock = pygame.time.Clock()
font = pygame.font.SysFont("segoeui", 28, bold=True)

# Игрок слева — WASD (в мультиплеере), справа — стрелки
board_left = Board(mode=mode_str)
piece_left = board_left.new_piece()
next_piece_left = board_left.new_piece()
fall_accum_left = 0.0

board_right = None
piece_right = None
next_piece_right = None
fall_accum_right = 0.0

if multiplayer:
    board_right = Board(mode=mode_str)
    piece_right = board_right.new_piece()
    next_piece_right = board_right.new_piece()

base_fall_speed = config["fall_speed"]
running = True

while running:
    dt = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Левый игрок (WASD)
            if not board_left.game_over:
                if event.key == pygame.K_a:
                    piece_left.x -= 1
                    if not board_left.valid_move(piece_left):
                        piece_left.x += 1
                elif event.key == pygame.K_d:
                    piece_left.x += 1
                    if not board_left.valid_move(piece_left):
                        piece_left.x -= 1
                elif event.key == pygame.K_w:
                    rotated = copy.deepcopy(piece_left)
                    rotated.rotate()
                    if board_left.valid_move(rotated):
                        piece_left.rotate()
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    board_left.drop_and_lock(piece_left)
                    piece_left = next_piece_left
                    next_piece_left = board_left.new_piece()
                    fall_accum_left = 0.0

            # Правый игрок (стрелки) — только в мультиплеере
            if multiplayer and board_right and not board_right.game_over:
                if event.key == pygame.K_LEFT:
                    piece_right.x -= 1
                    if not board_right.valid_move(piece_right):
                        piece_right.x += 1
                elif event.key == pygame.K_RIGHT:
                    piece_right.x += 1
                    if not board_right.valid_move(piece_right):
                        piece_right.x -= 1
                elif event.key == pygame.K_UP:
                    rotated = copy.deepcopy(piece_right)
                    rotated.rotate()
                    if board_right.valid_move(rotated):
                        piece_right.rotate()
                elif event.key == pygame.K_SPACE:
                    board_right.drop_and_lock(piece_right)
                    piece_right = next_piece_right
                    next_piece_right = board_right.new_piece()
                    fall_accum_right = 0.0

    keys = pygame.key.get_pressed()

    # Падение левого игрока
    if not board_left.game_over:
        speed = 0.05 if keys[pygame.K_s] else base_fall_speed
        fall_accum_left += dt / speed
        old_y = piece_left.y
        piece_left.y = int(fall_accum_left)
        if not board_left.valid_move(piece_left):
            piece_left.y = old_y
            fall_accum_left = old_y
            board_left.lock_piece(piece_left)
            piece_left = next_piece_left
            next_piece_left = board_left.new_piece()
            fall_accum_left = 0.0

    # Падение правого игрока
    if multiplayer and board_right and not board_right.game_over:
        speed = 0.05 if keys[pygame.K_DOWN] else base_fall_speed
        fall_accum_right += dt / speed
        old_y = piece_right.y
        piece_right.y = int(fall_accum_right)
        if not board_right.valid_move(piece_right):
            piece_right.y = old_y
            fall_accum_right = old_y
            board_right.lock_piece(piece_right)
            piece_right = next_piece_right
            next_piece_right = board_right.new_piece()
            fall_accum_right = 0.0

    # Рестарт по R
    if (board_left.game_over and (multiplayer and board_right.game_over or not multiplayer)) or \
       (multiplayer and board_left.game_over and board_right.game_over):
        if keys[pygame.K_r]:
            board_left = Board(mode=mode_str)
            piece_left = board_left.new_piece()
            next_piece_left = board_left.new_piece()
            fall_accum_left = 0.0
            if multiplayer:
                board_right = Board(mode=mode_str)
                piece_right = board_right.new_piece()
                next_piece_right = board_right.new_piece()
                fall_accum_right = 0.0

    # Отрисовка
    screen.fill(config["background_color"])

    # Левое поле (WASD)
    draw_grid(screen, FIELD_X_LEFT)
    draw_board(screen, board_left, FIELD_X_LEFT)
    draw_piece(screen, piece_left, FIELD_X_LEFT)
    draw_ui(screen, font, board_left, next_piece_left, INFO_X_LEFT, "1 (WASD)")

    if multiplayer:
        # Правое поле (стрелки)
        draw_grid(screen, FIELD_X_RIGHT)
        draw_board(screen, board_right, FIELD_X_RIGHT)
        draw_piece(screen, piece_right, FIELD_X_RIGHT)
        draw_ui(screen, font, board_right, next_piece_right, INFO_X_RIGHT, "2 (Стрелки)")

    # Game Over
    if board_left.game_over:
        text = font.render("ИГРА ОКОНЧЕНА (Левый игрок)", True, (255, 50, 50))
        screen.blit(text, (FIELD_X_LEFT - 60, 300))
    if multiplayer and board_right.game_over:
        text = font.render("ИГРА ОКОНЧЕНА (Правый игрок)", True, (255, 50, 50))
        screen.blit(text, (FIELD_X_RIGHT - 60, 300))

    pygame.display.flip()

pygame.quit()
sys.exit()