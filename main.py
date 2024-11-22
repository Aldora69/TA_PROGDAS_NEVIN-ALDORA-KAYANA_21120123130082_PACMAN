import pygame
import random
pygame.init()
# Constants
WIDTH = 28
HEIGHT = 31
TILE_SIZE = 20
PACMAN = 'C'
GHOST = 'M'
WALL = '#'
DOT = '.'
EMPTY = ' '
POWER_PELLET = 'O'
LARGE_TEXT = pygame.font.Font("Pacmania Italic.otf", 50)
SMALL_TEXT = pygame.font.Font("Pacmania Italic.otf", 15)

# Movement directions
dx = [0, 0, -1, 1]
dy = [-1, 1, 0, 0]

# Initialize pygame
pygame.init()
    
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Entity Class
class Entity:
    def __init__(self, start_x, start_y, symbol):
        self.x = start_x
        self.y = start_y
        self.symbol = symbol

    def get_position(self):
        return self.x, self.y

    def set_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

# Pacman Class
class Pacman(Entity):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, PACMAN)
        self.score = 0
        self.power_mode = False
        self.power_mode_timer = 0

    def move(self, maze, direction):
        new_x = self.x + dx[direction]
        new_y = self.y + dy[direction]

        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and maze[new_y][new_x] != WALL:
            self.x = new_x
            self.y = new_y

    def add_score(self, points):
        self.score += points

    def get_score(self):
        return self.score

    def activate_power_mode(self):
        self.power_mode = True
        self.power_mode_timer = 50

    def update_power_mode(self):
        if self.power_mode:
            self.power_mode_timer -= 1
            if self.power_mode_timer <= 0:
                self.power_mode = False

    def is_powered(self):
        return self.power_mode

# Ghost Class
class Ghost(Entity):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, GHOST)
        self.direction = random.randint(0, 3)

    def move(self, maze):
        new_x = self.x + dx[self.direction]
        new_y = self.y + dy[self.direction]

        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and maze[new_y][new_x] != WALL:
            self.x = new_x
            self.y = new_y
        else:
            self.direction = random.randint(0, 3)



# Game Class
class Game:
    def __init__(self):
        self.maze = []
        self.pacman = Pacman(14, 23)
        self.ghosts = [Ghost(6, 11)]
        self.dots_remaining = 0
        self.game_over = False
        self.home_screen = True
        self.paused = False  # Tambahkan atribut untuk mengelola status pause
        self.font = pygame.font.SysFont('Courier', 20)

        self.initialize_maze()

    def draw_pause_screen(self, window):
        pause_text = LARGE_TEXT.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH * TILE_SIZE // 2, HEIGHT * TILE_SIZE // 2))
        window.blit(pause_text, pause_rect)

        resume_text = SMALL_TEXT.render("Press P to Resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(WIDTH * TILE_SIZE // 2, HEIGHT * TILE_SIZE // 2 + 40))
        window.blit(resume_text, resume_rect)

        pygame.display.flip()

   
    def draw_home_screen(self, window):
        """Menggambar tampilan home screen."""
        window.fill(BLACK)

        # Teks Judul
        title_text = LARGE_TEXT.render("PACMAN", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH * TILE_SIZE // 2, HEIGHT * TILE_SIZE // 3))
        window.blit(title_text, title_rect)

        # Instruksi
        start_text = SMALL_TEXT.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH * TILE_SIZE // 2, HEIGHT * TILE_SIZE // 2))
        window.blit(start_text, start_rect)

        exit_text = SMALL_TEXT.render("Press ESC to Exit", True, WHITE)
        exit_rect = exit_text.get_rect(center=(WIDTH * TILE_SIZE // 2, HEIGHT * TILE_SIZE // 2 + 40))
        window.blit(exit_text, exit_rect)

        pygame.display.flip()

    def initialize_maze(self):
        self.maze = [
            "############################",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#O####.#####.##.#####.####O#",
            "#.####.#####.##.#####.####.#",
            "#..........................#",
            "#.####.##.########.##.####.#",
            "#.####.##.########.##.####.#",
            "#......##....##....##......#",
            "######.##### ## #####.######",
            "     #.##### ## #####.#     ",
            "     #.##          ##.#     ",
            "     #.## ###--### ##.#     ",
            "######.## #      # ##.######",
            "      .   #      #   .      ",
            "######.## #      # ##.######",
            "     #.## ######## ##.#     ",
            "     #.##          ##.#     ",
            "     #.## ######## ##.#     ",
            "######.## ######## ##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#.####.#####.##.#####.####.#",
            "#O..##................##..O#",
            "###.##.##.########.##.##.###",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################"
        ]
        self.dots_remaining = sum(row.count(DOT) for row in self.maze)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Pause logic
        if keys[pygame.K_p]:
            pygame.time.wait(200)  # Tambahkan delay untuk mencegah input berulang
            self.paused = not self.paused  # Toggle pause state

        if self.paused:
            return  # Jika permainan sedang pause, abaikan input lainnya

        if self.game_over:
            if keys[pygame.K_r]:  # Restart game
                self.__init__()  # Reinitialize game
            elif keys[pygame.K_ESCAPE]:  # Exit game
                pygame.quit()
                exit()

        else:
            if keys[pygame.K_SPACE] and self.home_screen:
                self.home_screen = False
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

            if not self.home_screen:
                if keys[pygame.K_w]:
                    self.pacman.move(self.maze, 0)
                elif keys[pygame.K_s]:
                    self.pacman.move(self.maze, 1)
                elif keys[pygame.K_a]:
                    self.pacman.move(self.maze, 2)
                elif keys[pygame.K_d]:
                    self.pacman.move(self.maze, 3)


    def update(self):
        if self.game_over or self.paused:
            return  # Jangan update jika game over atau pause

        self.pacman.update_power_mode()
        pac_x, pac_y = self.pacman.get_position()

        # Check for collisions with dots and power pellets
        if self.maze[pac_y][pac_x] == DOT:
            self.maze[pac_y] = self.maze[pac_y][:pac_x] + EMPTY + self.maze[pac_y][pac_x + 1:]
            self.pacman.add_score(10)
            self.dots_remaining -= 1
        elif self.maze[pac_y][pac_x] == POWER_PELLET:
            self.maze[pac_y] = self.maze[pac_y][:pac_x] + EMPTY + self.maze[pac_y][pac_x + 1:]
            self.pacman.add_score(50)
            self.pacman.activate_power_mode()

        # Check if ghosts catch pacman
        for ghost in self.ghosts:
            ghost.move(self.maze)
            if ghost.get_position() == (pac_x, pac_y):
                self.game_over = True
                break

        if self.dots_remaining == 0:
            self.game_over = True


    def draw_game_over_screen(self, window):
        window.fill(BLACK)

        # Teks Game Over
        game_over_text = LARGE_TEXT.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH * TILE_SIZE // 2, HEIGHT * TILE_SIZE // 3))
        window.blit(game_over_text, game_over_rect)

        # Tampilkan skor akhir
        score_text = SMALL_TEXT.render(f"Final Score: {self.pacman.get_score()}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH * TILE_SIZE // 2, HEIGHT * TILE_SIZE // 2))
        window.blit(score_text, score_rect)

        # Instruksi untuk restart/keluar
        restart_text = SMALL_TEXT.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH * TILE_SIZE // 2, HEIGHT * TILE_SIZE // 2 + 40))
        window.blit(restart_text, restart_rect)

        exit_text = SMALL_TEXT.render("Press ESC to Exit", True, WHITE)
        exit_rect = exit_text.get_rect(center=(WIDTH * TILE_SIZE // 2, HEIGHT * TILE_SIZE // 2 + 80))
        window.blit(exit_text, exit_rect)

        pygame.display.flip()

    def render(self, window):
        if self.home_screen:
            self.draw_home_screen(window)
        elif self.game_over:
            self.draw_game_over_screen(window)
        elif self.paused:
            self.draw_pause_screen(window)  # Tampilkan layar pause
        else:
            window.fill(BLACK)
            tile_size = TILE_SIZE

            # Gambar maze
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    if self.maze[y][x] == WALL:
                        pygame.draw.rect(window, BLUE, (x * tile_size, y * tile_size, tile_size, tile_size))
                    elif self.maze[y][x] == DOT:
                        pygame.draw.circle(window, WHITE, (x * tile_size + tile_size // 2, y * tile_size + tile_size // 2), tile_size // 6)
                    elif self.maze[y][x] == POWER_PELLET:
                        pygame.draw.circle(window, YELLOW, (x * tile_size + tile_size // 2, y * tile_size + tile_size // 2), tile_size // 3)

            # Gambar Pacman
            pacman_x, pacman_y = self.pacman.get_position()
            pygame.draw.circle(window, YELLOW, (pacman_x * tile_size + tile_size // 2, pacman_y * tile_size + tile_size // 2), tile_size // 2)

            # Gambar Ghosts
            for ghost in self.ghosts:
                ghost_x, ghost_y = ghost.get_position()
                pygame.draw.circle(window, RED, (ghost_x * tile_size + tile_size // 2, ghost_y * tile_size + tile_size // 2), tile_size // 2)

            # Gambar Skor
            score_text = self.font.render(f"Score: {self.pacman.get_score()}", True, WHITE)
            window.blit(score_text, (10, HEIGHT * TILE_SIZE + 5))

            pygame.display.flip()




# Main loop
def main():
    window = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE + 40))
    pygame.display.set_caption("Pacman")

    game = Game()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # if not game.game_over:
        #     game.handle_input()
        #     game.update()
        game.handle_input()

        if not game.home_screen:
            game.update()  

        game.render(window)
        clock.tick(25)

if __name__ == "__main__":
    main()
    