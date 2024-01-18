import pyxel
import random

class App:
    def __init__(self):
        pyxel.init(100, 100)
        self.maze = Maze(10, 10)
        self.player = Player(45, 45)

        # ゴールの座標を端に設定
        self.goal_x, self.goal_y = self.maze.create_goal()
        self.game_clear = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.game_clear:
            self.player.move(self.maze)
            self.check_goal()

    def draw(self):
        pyxel.cls(7)
        self.maze.draw()
        self.player.draw()
        pyxel.rect(self.goal_x, self.goal_y, 5, 5, 8)

        if self.game_clear:
            pyxel.text(40, 50, "Game Clear!", pyxel.frame_count % 16)

    def check_goal(self):
        if self.player.x == self.goal_x and self.player.y == self.goal_y:
            self.game_clear = True

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 7
        self.h = 7
        pyxel.image(0).set(0, 0, ["777A777","77AAA77","7AAAAA7","AAAAAAA","7AAAAA7","77AAA77","777A777"])

    def draw(self):
        pyxel.blt(self.x - 3, self.y - 3, 0, 0, 0, 7, 7, 7)

    def move(self, maze):
        new_x, new_y = self.x, self.y
        if pyxel.btn(pyxel.KEY_RIGHT):
            new_x += 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            new_x -= 1
        elif pyxel.btn(pyxel.KEY_UP):
            new_y -= 1
        elif pyxel.btn(pyxel.KEY_DOWN):
            new_y += 1

        new_x = max(0, min(new_x, pyxel.width - self.w))
        new_y = max(0, min(new_y, pyxel.height - self.h))

        if not maze.is_wall(new_x, new_y):
            self.x, self.y = new_x, new_y

class Maze:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.maze = self.generate_maze()

    def generate_maze(self):
        return [[random.randint(0, 1) for _ in range(self.width)] for _ in range(self.height)]

    def create_goal(self):
        goal_x, goal_y = 95, 95
        self.clear_path_to_goal(goal_x, goal_y)
        return goal_x, goal_y

    def clear_path_to_goal(self, goal_x, goal_y):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                x = (goal_x + dx) // 10
                y = (goal_y + dy) // 10
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.maze[y][x] = 0

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 1:
                    pyxel.rect(x * 10, y * 10, 10, 10, 0)

    def is_wall(self, x, y):
        maze_x, maze_y = x // 10, y // 10
        if 0 <= maze_x < self.width and 0 <= maze_y < self.height:
            return self.maze[maze_y][maze_x] == 1
        return False

App()
