import pygame, random, sys
from tinydb import TinyDB

enemy_speed = 5
WIDTH = 1000
HEIGHT = 1000
difficulty = 70  # More = easier
spaceship_x = 450
spaceship_y = HEIGHT - 150
spaceship_w = 70
spaceship_h = 70
laser_w = 20
laser_h = 20
SPACESHIP = pygame.transform.scale(pygame.image.load("obrazky\ship.png"), (spaceship_w, spaceship_h))
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nejtezsi Hra")
bg = pygame.transform.scale(pygame.image.load("obrazky/space.png"), (1000, 1000))
clock = pygame.time.Clock()
image_count = 0
health = 5
START = True

pygame.mixer.init()

click_sound = pygame.mixer.Sound('sfx/click.wav')
select_sound = pygame.mixer.Sound('sfx/select.wav')
ost = pygame.mixer.music.load('sfx/game_ost.wav')

pygame.mixer.music.play(-1)

class Laser(pygame.sprite.Sprite):
    def __init__(self, spaceship_x, spaceship_y):
        super().__init__()
        color = random.choice(["11", "18"])
        self.image = pygame.transform.scale(pygame.image.load(f"obrazky\{color}.png"), (100, 100))
        self.rect = self.image.get_rect(center=(spaceship_x + spaceship_w // 2, spaceship_y + spaceship_h // 2))
        self.hitbox = pygame.Rect(spaceship_x + spaceship_w // 2 - laser_w // 2,
                                  spaceship_y + spaceship_h // 2 - laser_h // 2, laser_w, laser_h)

    def update(self):
        self.rect.y -= 15
        self.hitbox.y -= 15

        if self.rect.y <= 0:
            self.kill()
        if self.hitbox.y <= 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, enemy_speed, score):
        super().__init__()
        self.score = score
        nova_velikost = ()
        nepratele = {"cplus": (100, 120), "cshard": (200, 200),
                     "java": (160, 160), "js": (165, 100), "php": (180, 100),
                     "scratch": (100, 100), "sql": (125, 125), "swift": (100, 100),
                     "vb": (100, 100)}
        nepritel, velikost = random.choice(list(nepratele.items()))
        nahodna_velikost = random.choice([0.5, 0.75, 1, 1])
        x_velikost = velikost[0] * nahodna_velikost
        y_velikost = velikost[1] * nahodna_velikost
        self.image = pygame.transform.scale(pygame.image.load(f"enemies\{nepritel}.png"), (x_velikost, y_velikost))

        self.rect = self.image.get_rect(center=(x, 100))
        self.speed = enemy_speed
        self.hitbox = self.rect.copy()

    def update(self):
        global health
        self.rect.y += self.speed
        self.hitbox.y += self.speed
        if self.rect.y >= 850:
            self.speed = (self.speed) * 2
            hp_down_sound = pygame.mixer.Sound('sfx/minushp.wav')
            hp_down_sound.play()
        if self.rect.y >= HEIGHT:
            health -= 1
            s = pygame.Surface((1000, 1000), pygame.SRCALPHA)  # per-pixel alpha
            s.fill((255, 0, 0, 128))
            SCREEN.blit(s, (0, 0))
            print(health)
            if health == 0:
                health += 5
                game_over(self.score)
                print(health)

            self.kill()


def hitbox_collide(sprite, other_sprite):
    if sprite.hitbox.colliderect(other_sprite.hitbox):
        return True
    return False


def create_laser(spaceship_x, spaceship_y):
    laser = Laser(spaceship_x, spaceship_y)
    return laser


def create_enemy(enemy_speed, score):
    x = get_random_pos()
    enemy = Enemy(x, enemy_speed, score)
    return enemy


# def create_end():
#     end = End()
#     return end

def make_text(i, color, size_x, size_y, size_text):
    custom_font = pygame.font.Font("fnt/ARCADECLASSIC.TTF", size_text)
    custom_font = custom_font.render(i, True, (255, 255, 255))
    custom_font_rect = custom_font.get_rect()
    custom_font_rect.center = (size_x, size_y)
    SCREEN.blit(custom_font, custom_font_rect)


def main(spaceship_x, spaceship_y, bg, difficulty, enemy_speed):
    # give_cor("a")
    expl = False
    enemy_group = pygame.sprite.Group()
    laser_group = pygame.sprite.Group()

    p = 6
    # end_group = pygame.sprite.Group()
    # end_group.add(create_end())
    image_count = 0
    pygame.init()
    start_screen()
    previous = "00"
    TO_LEVEL_UP = 4
    enemy_spawn_delay = 0
    level_num = 1
    score = 0
    # health = 5
    ship_speed = 10
    print(score, "SKÉÉÉÉÉÉÉÉÉRE")
    while True:
        if enemy_spawn_delay == difficulty:
            enemy_group.add(create_enemy(enemy_speed, score))
            enemy_spawn_sound = pygame.mixer.Sound('sfx/enemyspawn.wav')
            enemy_spawn_sound.play()
            if score >= TO_LEVEL_UP:
                print(TO_LEVEL_UP)
                TO_LEVEL_UP = score + TO_LEVEL_UP
                enemy_speed += 4
                level_num += 1
                if ship_speed < 19:
                    ship_speed += 3
                if difficulty != 10:
                    difficulty -= 10


            enemy_spawn_delay = 0

        # if enemy_spawn_delay % 50 == 0:
        #     enemy_group.add(create_enemy(enemy_speed, score))
        #     enemy_spawn_sound = pygame.mixer.Sound('sfx/enemyspawn.wav')
        #     enemy_spawn_sound.play()

        hits = pygame.sprite.groupcollide(enemy_group, laser_group, True,True, collided=hitbox_collide)
        for hit in hits:
            enemy_kill_sound = pygame.mixer.Sound('sfx/enemykill.wav')
            enemy_kill_sound.play()
            score += 1
            hit_xy = hit
            expl = True

        # animace exploze

        if expl:
            if int(p) == p:
                p = int(p)
                y = pygame.transform.scale(pygame.image.load(f"obrazky/regularExplosion0{p}.png"), (100, 100))
                SCREEN.blit(y, (hit_xy))
            if p <= 0:
                p = 8
                expl = False
            p -= 1
            print(p)

        spaceship_x = what_pressed(spaceship_x, spaceship_y, True, laser_group, True, ship_speed)
        what_pressed(spaceship_x, spaceship_y, True, laser_group, True, ship_speed)

        make_text(str(f"Level  {level_num}"), (200, 200, 200), 100, 30, 50)

        make_text(str(f"Score  {score}"), (200, 200, 200), 800, 30, 50)
        make_health(health)
        laser_group.draw(SCREEN)
        laser_group.update()

        enemy_group.draw(SCREEN)
        enemy_group.update()


        SCREEN.blit(SPACESHIP, (spaceship_x, spaceship_y))

        pygame.display.update()
        image_count += 0.5
        if image_count == 47:
            image_count = 1

        update_bg(image_count, previous)
        previous = update_bg(image_count, previous)
        enemy_spawn_delay += 1
        clock.tick(60)


def update_bg(image_count, previous):
    if image_count == int(image_count):
        image_count = int(image_count)
        count = ("0" + str(image_count))[-2:]
        previous = count
        bg = pygame.transform.scale(pygame.image.load(f"pozadi/frame_{count}_delay-0.05s.jpg"), (1000, 1000))
        SCREEN.blit(bg, (0, 0))
    else:
        bg = pygame.transform.scale(pygame.image.load(f"pozadi/frame_{previous}_delay-0.05s.jpg"), (1000, 1000))
        SCREEN.blit(bg, (0, 0))
    return previous


def terminate():
    pygame.quit()
    sys.exit()


def what_pressed(spaceship_x=1, spaceship_y=1, sound_k=False, laser_group=[], move=False, ship_speed = 50):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if move:
                if sound_k:
                    laser_sound = pygame.mixer.Sound('sfx/lasermby.wav')
                    laser_sound.play()
                laser_group.add(create_laser(spaceship_x, spaceship_y))
    #
    if keys[pygame.K_LEFT]:
        if spaceship_x > 0:
            spaceship_x -= ship_speed

    elif keys[pygame.K_RIGHT]:
        if spaceship_x < 930:
            spaceship_x += ship_speed
    return spaceship_x


def make_health(health):

    x = 300
    y = 6
    for i in range(health):
        heart = pygame.transform.scale(pygame.image.load("obrazky\zivot.png"), (45, 45))
        x += 50
        SCREEN.blit(heart, (x, y))

    return


def get_random_pos():
    pos_x = random.randint(100, WIDTH - 100)
    return pos_x


def next_level(difficulty, TO_LEVEL_UP):
    return [int(difficulty - 10), TO_LEVEL_UP + 10]


def start_screen():
    loop = 40
    play_select_sound = True
    play_select_sound2 = True
    while True:
        for i in range(10):
            bg = pygame.transform.scale(pygame.image.load(f"start_screen/frame_0{i}_delay-0.1s.png"), (1000, 1000))
            SCREEN.blit(bg, (0, 0))
            MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
            if 600 > MOUSE_X > 380 and 545 > MOUSE_Y > 470:
                if play_select_sound:
                    select_sound.play()
                    play_select_sound = False
                pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(370, 460, 240, 95), 2)
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        start_sound = pygame.mixer.Sound('sfx/startsound.wav')
                        start_sound.play()
                        moving_screen()
                        return
            else:
                play_select_sound = True

            make_text(str("LEADERBOARD"), (200, 200, 200), 800, 900, 50)
            if 878 > MOUSE_X > 641 and 923 > MOUSE_Y > 877:
                if play_select_sound2:
                    select_sound.play()
                    play_select_sound2 = False
                pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(641, 878, 315, 50), 2)
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        click_sound.play()
                        database()
            else:
                play_select_sound2 = True
            pygame.display.update()
            clock.tick(loop)

        what_pressed()


def moving_screen():
    loop = 40
    while True:
        for i in range(10):
            bg = pygame.transform.scale(pygame.image.load(f"moving_start/frame_0{i}_delay-0.1s.png")
                                        , (1000, 1000))
            SCREEN.blit(bg, (0, 0))
            clock.tick(loop)
            pygame.display.update()
        loop -= 5
        if loop == 5:
            print("konec")
            return

def database():
    db = TinyDB(r"vysledky.json")
    seznam = {}
    y = []
    play_select_sound = True

    for i in db.all():
        y.append(i)

    for _ in y:
        for i in _.items():
            seznam[i[1]] = i[0]
    print(seznam)
    list_best = dict(sorted(seznam.items(), reverse=True))
    x, y = 0, 0
    while True:
        for i in range(10):
            bg = pygame.transform.scale(pygame.image.load(f"moving_start/frame_0{i}_delay-0.1s.png"), (1000, 1000))
            SCREEN.blit(bg, (0, 0))
            nu = 1
            lenght = 50
            for i in list_best.items():
                lenght += 50
                make_text(f" {i[1]}", (0, 0, 0), WIDTH // 2, 100 + lenght, 60)
                make_text(f"{nu}", (0, 0, 0), 300, 100 + lenght, 60)
                make_text(f"{i[0]}", (0, 0, 0), 750, 100 + lenght, 60)

                nu += 1
                if nu >= 4:
                    break
            make_text("NAME", (0, 0, 0), WIDTH // 2, 100 + 100 - 80, 60)
            make_text("RANK", (0, 0, 0), 300, 100 + 100 - 80, 60)
            make_text("SCORE", (0, 0, 0), 750, 100 + 100 - 80, 60)

            if x < 260:
                x += 10
                y += 10

            pygame.draw.line(SCREEN, (255, 255, 255), (501, 150), (530 - y, 150), 5)
            pygame.draw.line(SCREEN, (255, 255, 255), (501, 150), (530 + x, 150), 5)

            MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()

            make_text(str("GO BACK"), (200, 200, 200), 800, 900, 50)
            if 878 > MOUSE_X > 641 and 923 > MOUSE_Y > 877:
                if play_select_sound:
                    select_sound.play()
                    play_select_sound = False
                pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(641, 878, 315, 50), 2)
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        click_sound.play()
                        return

            else:
                play_select_sound = True

            pygame.display.update()
            what_pressed()
            clock.tick(40)


def input_name():
    loop = 40
    user_text = ""
    while True:
        play_select_sound = True
        for i in range(10):
            bg = pygame.transform.scale(pygame.image.load(f"moving_start/frame_0{i}_delay-0.1s.png")
                                        , (1000, 1000))
            SCREEN.blit(bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += (event.unicode).upper()

                elif event.type == pygame.MOUSEBUTTONUP:
                    MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()
                    if 878 > MOUSE_X > 641 and 923 > MOUSE_Y > 877:
                        if event.type == pygame.MOUSEBUTTONUP:
                            return user_text

            MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()

            make_text(str("SAVE"), (200, 200, 200), 800, 900, 50)
            print(pygame.mouse.get_pos())
            if 878 > MOUSE_X > 641 and 923 > MOUSE_Y > 877:
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        return user_text
                print("ye")
                if play_select_sound:
                    select_sound.play()
                    play_select_sound = False
                pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(641, 878, 315, 50), 2)

            else:
                play_select_sound = True

            make_text(f"ENTER YOUR NAME ", (255, 255, 255), WIDTH // 2, 200, 100)
            make_text(f"{user_text}", (255, 255, 255), WIDTH // 2, 350, 100)

            pygame.display.update()
            clock.tick(loop)

        what_pressed(False, False)


def game_over(score):
    game_over_sound = pygame.mixer.Sound('sfx/gameover.wav')
    game_over_sound.play()
    loop = 40
    play_select_sound = True
    play_select_sound2 = True
    play_select_sound3 = True
    while True:
        for i in range(10):
            bg = pygame.transform.scale(pygame.image.load(f"game_over/frame_0{i}_delay-0.1s.jpg"), (1000, 1000))
            SCREEN.blit(bg, (0, 0))
            make_text(str(f"YOUR SCORE IS  {score}"), (200, 200, 200), WIDTH // 2, HEIGHT // 2 + 200, 100)
            MOUSE_X, MOUSE_Y = pygame.mouse.get_pos()

            # play again
            if 427 > MOUSE_X > 60 and 545 > MOUSE_Y > 475:
                print("!")
                if play_select_sound:
                    select_sound.play()
                    play_select_sound = False
                pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(55, 460, 375, 100), 2)
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        main(spaceship_x, spaceship_y, bg, difficulty, enemy_speed)
                        return

            else:
                play_select_sound = True

            # save score
            if 918 > MOUSE_X > 566 and 545 > MOUSE_Y > 475:
                if play_select_sound3:
                    select_sound.play()
                    play_select_sound3 = False
                pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(560, 460, 363, 100), 2)
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        click_sound.play()
                        x = input_name()
                        db = TinyDB(r"vysledky.json")
                        db.insert({x: score})
            else:
                play_select_sound3 = True

            # leaderboard
            make_text(str("LEADERBOARD"), (200, 200, 200), 800, 900, 50)
            if 878 > MOUSE_X > 641 and 923 > MOUSE_Y > 877:
                if play_select_sound2:
                    select_sound.play()
                    play_select_sound2 = False
                pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(641, 878, 315, 50), 2)
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        click_sound.play()
                        database()
            else:
                play_select_sound2 = True
            pygame.display.update()
            clock.tick(loop)

        what_pressed(False, False)

main(spaceship_x, spaceship_y, bg, difficulty, enemy_speed)