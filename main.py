import pygame
import random

class Mygame:
    def __init__(self) -> None:
        pygame.init()
        self.load_images()
        self.monster = 1
        self.level = 1
        self.load_level()
        self.scale = self.images[0].get_width()
        self.update_size()
        self.font = pygame.font.SysFont("Verdana", 20)
        pygame.display.set_caption("Hard Game")
        self.game_loop()


    def load_images(self):
        self.images = []
        for image_name in ["main_man_tile", "scar_face_tile", "floor_tile", "door_tile"]:
            image = pygame.image.load("images/" + image_name + ".png")
            # Scale the image down by 1/3
            scaled_image = pygame.transform.scale(image, (image.get_width() // 3, image.get_height() // 3))
            self.images.append(scaled_image)

    def load_level(self, is_monster=0):
        if is_monster == 0:
            levels = {
                1: self.level1,
                2: self.level2,
                3: self.level3,
                4: self.level4,
            }
            level_function = levels.get(self.level)
            if level_function:
                level_function()
        elif is_monster == 1:
            monsters = {
                1: self.monster1,
                2: self.monster2,
                3: self.monster3,
                4: self.monster4,
                5: self.monster5,
                6: self.monster6,
                7: self.monster7,
            }
            monster_function = monsters.get(self.monster)
            if monster_function:
                monster_function()
                

    def game_loop(self):
        while True:
            self.handle_events()
            self.draw_screen()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)
                if event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                if event.key == pygame.K_UP:
                    self.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    self.move(1, 0)
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()


    def move(self, move_y, move_x):
        old_char_y, old_char_x = self.find_char()
        new_char_y = old_char_y + move_y
        new_char_x = old_char_x + move_x

        if not (0 <= new_char_y < self.height and 0 <= new_char_x < self.width):
            return

        if self.map[new_char_y][new_char_x] == 3:
            self.check_level()
            return

        self.map[old_char_y][old_char_x] = 2
        self.map[new_char_y][new_char_x] = 0


    def find_char(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 0:
                    return (y, x)


    def draw_screen(self):
        self.screen.fill((18, 27, 36))

        for y in range(self.height):
            for x in range(self.width):
                tile = self.map[y][x]
                self.screen.blit(self.images[tile], (x * self.scale, y * self.scale))

        text = self.font.render("Almost impossible game", True, (255, 0, 0))
        self.screen.blit(text, (5, self.height * self.scale))

        text = self.font.render("TRY to choose the random correct door.", True, (255, 0, 0))
        self.screen.blit(text, (5, self.height * self.scale + 25))

        text = self.font.render(r"Only 4.88% can win!", True, (255, 0, 0))
        self.screen.blit(text, (5, self.height * self.scale + 50))

        text = self.font.render("LEVEL: " + str(self.level) + "     ATTEMPTS LEFT: " + str(8 - self.monster), True, (255, 0, 0))
        self.screen.blit(text, (5, self.height * self.scale + 75))

        # Display messages for winning or losing the game
        if self.game_won():
            text = self.font.render("You won, you reached the end of the game", True, (255, 0, 0))
            text_x = self.scale * self.width / 2 - text.get_width() / 2
            text_y = self.scale * self.height / 2 - text.get_height() / 2
            pygame.draw.rect(self.screen, (38, 43, 74), (text_x, text_y + 75, text.get_width(), text.get_height()))
            self.screen.blit(text, (text_x, text_y + 75))
            pygame.display.flip()
            pygame.time.wait(5000)
            exit()

        if self.game_lost():
            text = self.font.render("You lost", True, (255, 0, 0))
            text_x = self.scale * self.width / 2 - text.get_width() / 2
            text_y = self.scale * self.height / 2 - text.get_height() / 2
            pygame.draw.rect(self.screen, (38, 43, 74), (text_x, text_y + 75, text.get_width(), text.get_height()))
            self.screen.blit(text, (text_x, text_y + 75))
            pygame.display.flip()
            pygame.time.wait(1500)
            self.monster = 1
            self.level = 1

        pygame.display.flip()


    def check_level(self):
        correct_door = random.randint(1, self.level + 1)
        if correct_door == 1:
            self.level += 1
            self.update_size()
        else:
            self.lose()


    def update_size(self, monster=0):
        self.load_level(monster)
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.screen_height = self.scale * self.height + 100  # Add extra height for text
        self.screen_width = self.scale * self.width
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))


    def lose(self):
        self.update_size(1)
        self.level = 1
        self.monster += 1
        self.draw_screen()
        if self.monster == 2:
            pygame.time.wait(1000)
        else:
            pygame.time.wait(2500)

        self.update_size()
        self.draw_screen()


    def game_won(self):
        return self.level == 5
    
    def game_lost(self):
        return self.monster == 8

    def level1(self):
        self.map = [[2, 2, 2, 2, 2],
                       [2, 3, 2, 3, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 0, 2, 2]]     
    def level2(self):
        self.map = [[2, 2, 2, 2, 2, 2, 2],
                       [2, 3, 2, 3, 2, 3, 2],
                       [2, 2, 2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2, 2, 2],
                       [2, 2, 2, 0, 2, 2, 2]]     
    def level3(self):
        self.map = [[2, 2, 2, 2, 2, 2, 2, 2, 2],
                       [2, 3, 2, 3, 2, 3, 2, 3, 2],
                       [2, 2, 2, 2, 2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 0, 2, 2, 2, 2]]
    def level4(self):
        self.map = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,],
                       [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                       [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,],
                       [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,],
                       [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,],
                       [2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2,]]
    
    def monster1(self):
        self.map = [[2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 0, 2, 2]]   
    def monster2(self):
        self.map = [[2, 2, 1, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 0, 2, 2]]   
    def monster3(self):
        self.map = [[2, 2, 2, 2, 2],
                       [2, 2, 1, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 0, 2, 2]]
    def monster4(self):
        self.map = [[2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 1, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 0, 2, 2]]
    def monster5(self):
        self.map = [[2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 1, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 0, 2, 2]]
    def monster6(self):
        self.map = [[2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 1, 2, 2],
                       [2, 2, 0, 2, 2]] 
    def monster7(self):
        self.map = [[2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 2, 2, 2],
                       [2, 2, 1, 2, 2]] 


if __name__ == "__main__":
    Mygame()