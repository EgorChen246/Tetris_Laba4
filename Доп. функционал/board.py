# board.py
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

from tetromino import Tetromino

class Board:
    def __init__(self, mode="single"): 
        self.grid = [[0 for _ in range(config["cols"])] for _ in range(config["rows"])]
        self.score = 0
        self.lines = 0
        self.game_over = False
        self.mode = mode
        self.high_score = self.load_high_score()

    def load_high_score(self):
        try:
            with open("high_scores.json", "r") as f:
                data = json.load(f)
                return data.get(self.mode, 0)
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        try:
            with open("high_scores.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        data[self.mode] = max(data.get(self.mode, 0), self.score)
        with open("high_scores.json", "w") as f:
            json.dump(data, f)

    def valid_move(self, piece):
        for x, y in piece.get_positions():
            if (x < 0 or x >= config["cols"] or y >= config["rows"] or (y >= 0 and self.grid[y][x])):
                return False
        return True

    def lock_piece(self, piece):
        for x, y in piece.get_positions():
            if y >= 0:
                self.grid[y][x] = piece.color

        rows_to_clear = []
        for row_idx, row in enumerate(self.grid):
            if all(cell for cell in row):
                rows_to_clear.append(row_idx)

        for row in rows_to_clear:
            del self.grid[row]
            self.grid.insert(0, [0] * config["cols"])

        self.lines += len(rows_to_clear)
        self.score += [0, 100, 300, 500, 800][len(rows_to_clear)]

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

        if any(self.grid[0]):
            self.game_over = True

    def new_piece(self):
        return Tetromino(config["cols"] // 2 - 1, 0)
    
    def drop_and_lock(self, piece):
        """Мгновенное падение до упора (для Space/Ctrl)"""
        while self.valid_move(piece):
            piece.y += 1
        piece.y -= 1
        self.lock_piece(piece)