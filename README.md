# Лабораторная работа №4 | Простая игра | Вариант 11 – Тетрис

**ФИО:** Ченцов Егор Андреевич, Мильчуков Григорий Викторович \
**Номер студенческого:** 245136, 245141 \
**Группа:** ИД24-3 \
**Название предмета:** Практикум по программированию \
**Дата сдачи:** 09.12.2025 \
**Отметка о выполнении:** Выполнено

---

## А. Описание задания

Реализация простой аркадной игры с использованием объектно-ориентированного подхода. Требования включают творческий подход к геймдизайну, визуальному стилю и пользовательскому опыту. Проект должен демонстрировать двумерную анимацию, с возможностью изменения параметров в реальном времени.

---

## B. Описание игры

Тетрис — классическая аркадная игра, разработанная Алексеем Пажитновым в 1984 году. Фигуры (тетромино) падают сверху вниз. Игрок может перемещать их влево/вправо, вращать и ускорять падение. Заполненные горизонтальные линии исчезают, принося очки. Игра заканчивается, если фигуры достигают верхней границы поля.

### Достигнутая сложность и реализация

Выполнены все основные требования: \
• Добавлено плавное падение фигур \
• Предпросмотр следующей фигуры \
• Мгновенное падение по пробелу \
• Рестарт по клавише R в конце игры 

### Дополнительно реализовано:

• Параметры (скорость, цвета, размеры) вынесены в config.json для динамических изменений \
• Добавил пользовательский хороший интерфейс и предпросмотр \
• Использовал цвета, как в классической версии  \
• Плавная анимация 60 FPS 

### Используемые инструменты и технологии:

Python 3.10+, библиотека Pygame для графики, ввода и анимации; JSON для конфигурации

---

## С. Распределение ролей и задач

Работа выполнена в паре. Ченцов Егор отвечал за исследование механик игры, разработку базовой версии (логика падения фигур, повороты, очистка линий, счёт очков и коллизии), а также интеграцию конфигурационного файла и основной цикл. 

Мильчуков Григорий отвечал за реализацию дополнительного функционала (сохранение рекордов и прогресса в отдельный файл, с загрузкой при запуске), тестирование полной версии и отладку. 

Таким образом, объём задач распределён поровну: базовая механика и логика — Егора часть, расширения и улучшения — часть Григория.

### Методы сотрудничества и коммуникации:

Обмен идеями и кодом через Telegram и GitHub (репозиторий проекта). Проводили встречи для обсуждения прогресса и распределения задач.

### Распределение задач по созданию графических элементов:

Графические элементы (отрисовка поля, фигур и UI) реализованы Егором в базовой версии. Григорий добавил визуальные эффекты для дополнительного функционала, такие как индикатор рекорда или меню выбора режима.

---

## D. Архитектура проекта

### Структура ООП

1. Класс Board.py — связан с Tetromino для проверки коллизий (доска)
 - __init__(self) — управление сеткой
 - valid_move(self, piece) — проверка валидности перемещений
 - lock_piece(self, piece) — фиксацией фигур (интеграция фигуры в доску после падения)
 - lock_piece(self, piece) — подсчёт очков и линий
2. Класс Tetromino.py — самостоятельный класс (фигуры)
 - rotate(self) — позволяет менять ориентацию фигуры (до 4 состояний)
 - get_positions(self) — получение позиций клеток фигуры
3. Класс Renderer.py — модуль с функциями отрисовки, зависит от Board и Tetromino
 - draw_grid(screen) — отрисовка сетки поля
 - draw_board(screen, board) — отрисовка доски и зафиксированных фигур
 - draw_piece(screen, piece) — динамическая отрисовка падающей фигуры
 - draw_ui(screen, font, board, next_piece) — отрисовка пользовательского интерфейса
4. main.py —загрузка конфига, основной цикл

### Обоснование использованных шаблонов проектирования:

Мы применили объединение данных и методов для разделения логики игры в классе Board и отрисовки в модуле Renderer. Вместо наследования использовали композицию, чтобы код был проще и гибче. Настройки вынесли в файл JSON для лёгкого изменения без правки основного кода.

---

## E. Реализованный функционал

Реализована классическая механика Тетриса с анимацией падения, поворотами, очисткой линий и счётом.

1. Функция: Начало игры с предпросмотром фигуры
2. Функция: Падение и поворот фигуры
3. Функция: Очистка линии и счёт
4. Функция: игра окончена

### Фрагменты кода для ключевых алгоритмов

- Пример плавного падения из main.py:

```
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
```

### Описание решенных технических проблем

Проблема рывкового падения решена введением дробной координаты Y (piece_y_float) с проверкой коллизий каждый кадр. Проблема с отображением следующей фигуры — центрирование в renderer.py с расчётом границ.

---

## F. Инструкции по запуску и игре

### Полная схема управления:

• Стрелка влево/вправо: Перемещение фигуры. \
• Стрелка вверх: Поворот фигуры. \
• Стрелка вниз (удержание): Ускоренное падение. \
• Пробел: Мгновенное падение донизу игрового поля. \
• R: Рестарт после окончания игры. 

### Правила и цели игры

Фигуры падают, заполняйте горизонтальные линии для их удаления и набора очков (100 за линию, 300 за две и т.д.). Цель — максимум очков до заполнения поля.

### Системные требования и зависимости

Python 3.10+

### Установка Pygame 
```
pip install pygame 
```

### Запуск 
```
python main.py
```
---

## G. Полный исходный код (базовая версия)

(5 файла: config.json, board.py, tetromino.py, renderer.py, main.py)

## config.json

```
{
  "window_width": 700,
  "window_height": 750,
  "cell_size": 35,
  "cols": 10,
  "rows": 20,
  "background_color": [8, 8, 20],
  "grid_color": [40, 40, 80],
  "fall_speed": 0.5,
  "colors": {
    "I": [0, 255, 255],
    "O": [255, 255, 0],
    "T": [180, 0, 255],
    "S": [0, 255, 0],
    "Z": [255, 0, 0],
    "J": [0, 100, 255],
    "L": [255, 165, 0]
  }
}

```

## board.py

```
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

from tetromino import Tetromino


class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(config["cols"])] for _ in range(config["rows"])]
        self.score = 0
        self.lines = 0
        self.game_over = False

    def valid_move(self, piece):
        for x, y in piece.get_positions():
            if (
                x < 0
                or x >= config["cols"]
                or y >= config["rows"]
                or (y >= 0 and self.grid[y][x])
            ):
                return False
        return True

    def lock_piece(self, piece):
        for x, y in piece.get_positions():
            if y >= 0:
                self.grid[y][x] = piece.color

        # Проверка заполненных строк
        rows_to_clear = []
        for row_idx, row in enumerate(self.grid):
            if all(cell for cell in row):
                rows_to_clear.append(row_idx)

        for row in rows_to_clear:
            del self.grid[row]
            self.grid.insert(0, [0] * config["cols"])

        self.lines += len(rows_to_clear)
        self.score += [0, 100, 300, 500, 800][len(rows_to_clear)]

        # Проверка game over
        if any(self.grid[0]):
            self.game_over = True

    def new_piece(self):
        return Tetromino(config["cols"] // 2 - 1, 0)

```

## tetromino.py

```
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

```

## renderer.py

```
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
```

## main.py

```
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
```

---

## Дополнительный функционал и изменения базовой версии кода

### *Сохранение рекордов и прогресса*

добавил файл scores.json для хранения максимального счёта. В Board.py добавлен метод save_score(), вызываемый в lock_piece() при обновлении рекорда. Загрузка в init(). Фрагмент: 

```
def lock_piece(self, piece):
    # ... (основная логика)
    if self.score > self.high_score:
        self.high_score = self.score
        with open("scores.json", "w") as f:
            json.dump({"high_score": self.high_score}, f)
```

### *Режим для двух игроков*

Добавлен флаг multiplayer в config.json. При запуске спрашиваем режим в консоли. В main.py дублируем board для второго игрока, с раздельным управлением (WASD для второго). Фрагмент: 

```
def lock_piece(self, piece):
    # ... (основная логика)
    if self.score > self.high_score:
        self.high_score = self.score
        with open("scores.json", "w") as f:
            json.dump({"high_score": self.high_score}, f)
```

### *Добавление музыки*

Добавлен pygame.mixer.music.load("background.mp3") и .play(-1) в main.py после init(). Фрагмент: 

```
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
```

## main.py (с изменениями)

```
^_^
```

---

## Заключение

В ходе выполнения лабораторной работы была успешно реализована классическая аркадная игра *Тетрис* с полным соответствием требованиям задания.

**Полностью выполнены все обязательные требования:** разработана механика падения тетромино, поворотов, перемещений, очистки заполненных строк, подсчёта очков и проверки окончания игры. Обеспечено управление фигурой с помощью клавиш (стрелки для перемещения и поворота, удержание вниз для ускорения, пробел для мгновенного падения).

**Дополнительно реализованы:** плавное субпиксельное падение с анимацией 60 FPS, предпросмотр следующей фигуры с центрированием, рестарт по клавише R, вынесение всех параметров в конфигурационный файл config.json для динамических изменений (размеры, цвета, скорость), а также современный интерфейс с закруглёнными элементами и визуальными эффектами.

**Был добавлен дополнительный функционал:**

Полученная игра демонстрирует стабильную динамику с учётом физических коллизий и предоставляет пользователю удобный инструмент для экспериментов с параметрами.

*Работа выполнена в соответствии с принципами объектно-ориентированного программирования.*
