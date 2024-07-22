import random
from collections import defaultdict

class Tetris:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "move_left": ("BOOLEAN", {"default": False}),
                "move_right": ("BOOLEAN", {"default": False}),
                "move_down": ("BOOLEAN", {"default": False}),
                "rotate": ("BOOLEAN", {"default": False}),
                "dummy": ("INT", {"default": 0, "min": 0, "max": 1000000, "step": 1, "forceInput": True}), #need this so comfy will refresh
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "play_tetris"

    CATEGORY = "Tetris"

    def __init__(self):
        self.WIDTH = 10
        self.HEIGHT = 20
        self.SHAPES = [
            [(0,0), (0,1), (1,0), (1,1)],  # Square
            [(0,0), (0,1), (0,2), (0,3)],  # Line
            [(0,0), (0,1), (0,2), (1,1)],  # T
            [(0,0), (0,1), (1,1), (1,2)],  # S
            [(0,1), (0,2), (1,0), (1,1)],  # Z
            [(0,0), (1,0), (1,1), (1,2)],  # L
            [(0,2), (1,0), (1,1), (1,2)]   # J
        ]
        self.board = defaultdict(bool)
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        shape = random.choice(self.SHAPES)
        return [(sh[0], sh[1] + self.WIDTH // 2 - 1) for sh in shape]

    def valid_move(self, piece):
        return all(0 <= x < self.WIDTH and y < self.HEIGHT and not self.board[(x, y)]
                   for x, y in piece)

    def clear_lines(self):
        lines_to_clear = [y for y in range(self.HEIGHT) if all(self.board[(x, y)] for x in range(self.WIDTH))]
        for line in lines_to_clear:
            for y in range(line, 0, -1):
                for x in range(self.WIDTH):
                    self.board[(x, y)] = self.board[(x, y-1)]
        return len(lines_to_clear)

    def place_piece(self):
        for x, y in self.current_piece:
            self.board[(x, y)] = True
        cleared = self.clear_lines()
        self.score += cleared * cleared * 100
        self.current_piece = self.new_piece()
        if not self.valid_move(self.current_piece):
            self.game_over = True

    def move(self, dx, dy):
        new_piece = [(x + dx, y + dy) for x, y in self.current_piece]
        if self.valid_move(new_piece):
            self.current_piece = new_piece
        elif dy > 0:
            self.place_piece()

    def rotate(self):
        center = self.current_piece[0]
        new_piece = [(center[0] - center[1] + y, center[0] + center[1] - x) for x, y in self.current_piece]
        if self.valid_move(new_piece):
            self.current_piece = new_piece

    def get_board_state(self):
        board = [[' ' for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        for x, y in self.board:
            if self.board[(x, y)]:
                board[y][x] = '□'
        for x, y in self.current_piece:
            board[y][x] = '■'
        board_str = '\n'.join('|' + ''.join(row) + '|' for row in board)
        board_str += f'\n{"-" * (self.WIDTH + 2)}\nScore: {self.score}'
        return board_str

    def play_tetris(self, move_left, move_right, move_down, rotate, dummy):
        if self.game_over:
            self.__init__()  # Reset the game if it's over

        if move_left:
            self.move(-1, 0)
        if move_right:
            self.move(1, 0)
        if rotate:
            self.rotate()
        if move_down:
            self.move(0, 1)

        # Always move down one step (tick)
        self.move(0, 1)

        return (self.get_board_state(),)

NODE_CLASS_MAPPINGS = {
    "Tetris": Tetris,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Tetris": "Tetris",
}