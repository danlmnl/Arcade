import pygame
import sys
import random


pygame.init()
size = [600, 800]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


lives = 5
cooldown_live = 0
score = 0
ship_pos = pygame.Vector2(size[0]//2, 600)
ship_size = 40
ship_speed = 10
base_ship_speed = 10
speed_boost_until = 0
speed_boost_time = 5000

bullets = []
bullet_speed = 8
bullet_r = 8
bullet_color = (200, 100, 255)

enemys1 = []
enemy1_r = 20
enemy1_speed = 3
enemy1_cooldown = 1800
enemy1_color = (73, 66, 61)
last_generate_1 = 0

enemys2 = []
enemy2_r = 20
enemy2_speed = 3
enemy2_cooldown = 2000
hp_enemy2 = 2
enemy2_color = "BLACK"
last_generate_2 = 0

bonuses = []
bonus_r = 20
bonus_speed_fall = 3
bonus_cooldown_speed = 10000
bonus_cooldown_live = 20000
bonus_cooldown_speed_bullet_regenerate = 17000
bonus_speed_bullet_time = 5000
boost_bullet_time = 10000
boost_bullet_until = 0
cd_for_bullet = 150
last_bullet_time = 0
boost_bullet = False
last_generate_bonus_speed = 0
last_generate_bonus_live = 0
last_generate_bonus_speed_bullet = 0
bonus_speed_ch = 1.3

stars = []
booms = []

live_image = pygame.image.load('live.png')
enemy1_image = pygame.image.load('asteroid1.png')
enemy2_image = pygame.image.load('asteroid2.png')
bonus_speed_image = pygame.image.load('bonus_speed.png')
bonus_speed_bullet_image = pygame.image.load('speed_bullet.png')
boom_image = pygame.image.load('boom.png')
ship_image = pygame.image.load('ship.png')

bonus_speed_image = pygame.transform.scale(bonus_speed_image, (50, 50))
live_image = pygame.transform.scale(live_image, (50, 50))
bonus_speed_bullet_image = pygame.transform.scale(bonus_speed_bullet_image, (50, 50))
enemy1_image = pygame.transform.scale(enemy1_image, (50, 50))
enemy2_image = pygame.transform.scale(enemy2_image, (50, 50))
ship_image = pygame.transform.scale(ship_image, (80, 80))


def act_bull():
    nose = pygame.Vector2(ship_pos.x + 20, ship_pos.y - ship_size*0.2)
    bullets.append(nose)
    nose = pygame.Vector2(ship_pos.x - 20, ship_pos.y - ship_size * 0.2)
    bullets.append(nose)


def stars_draw():
    r1 = random.randint(0, 600)
    r2 = random.randint(-50, 0)
    falling = pygame.Vector2(r1, r2)
    stars.append([(falling), random.uniform(0, 3), random.uniform(1, 5)])


def generate_enemy1():
    global enemys1
    new_enemy = pygame.Rect(random.randint(50, 550), 0, 50, 50)
    enemys1.append(new_enemy)

def generate_enemy2():
    global enemys2
    new_enemy = pygame.Rect(random.randint(50, 550), 0, 50, 50)
    enemys2.append([new_enemy, hp_enemy2])


def generate_bonus_speed():
    x = random.randint(0, size[0]-50)
    new_bonus = pygame.Rect(x, -50, 50, 50)
    bonuses.append([new_bonus, "speed"])

def generate_bonus_live():
    x = random.randint(0, size[0] - 50)
    new_bonus = pygame.Rect(x, -50, 50, 50)
    bonuses.append([new_bonus, "live"])

def generate_bonus_speed_bullet():
    x = random.randint(0, size[0] - 50)
    new_bonus = pygame.Rect(x, -50, 50, 50)
    bonuses.append([new_bonus, "speed-bullet"])

def draw_boom(pos):
    booms.append([pygame.Vector2(pos.center), 0])


def load_score():
    try:
        with open('score.txt', 'r') as f:
            score = int(f.readline())
            return score
    except FileNotFoundError:
        return 0

def save_score(score):
    with open('score.txt', 'w') as f:
        f.write(str(score))

score = load_score()
game_res = False
done = True

while True:
    clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_score(score)
            pygame.quit()
            sys.exit()

        if not game_res and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            act_bull()

    if not game_res:
        data = pygame.key.get_pressed()
        if data[pygame.K_LEFT] or data[pygame.K_a]:
            ship_pos.x -= ship_speed
        elif data[pygame.K_RIGHT] or data[pygame.K_d]:
            ship_pos.x += ship_speed
        elif data[pygame.K_UP] or data[pygame.K_w]:
            ship_pos.y -= ship_speed
        elif data[pygame.K_DOWN] or data[pygame.K_s]:
            ship_pos.y += ship_speed

        ship_rect = pygame.Rect(ship_pos.x - ship_size, ship_pos.y - ship_size * 0.2, ship_size * 2, ship_size * 1.2)

        if now - last_generate_1 >= enemy1_cooldown:
            generate_enemy1()
            last_generate_1 = now

        if now - last_generate_2 >= enemy2_cooldown:
            generate_enemy2()
            last_generate_2 = now

        if now - last_generate_bonus_speed >= bonus_cooldown_speed:
            generate_bonus_speed()
            last_generate_bonus_speed = now

        if now - last_generate_bonus_live >= bonus_cooldown_live:
            generate_bonus_live()
            last_generate_bonus_live = now

        if now - last_generate_bonus_speed_bullet >= bonus_cooldown_speed_bullet_regenerate:
            generate_bonus_speed_bullet()
            last_generate_bonus_speed_bullet = now

        if now >= speed_boost_until:
            ship_speed = base_ship_speed

        if boost_bullet and now - last_bullet_time >= cd_for_bullet:
            act_bull()
            last_bullet_time = now

        if boost_bullet and now >= boost_bullet_until:
            boost_bullet = False

        for i in range(3):
            stars_draw()

        for star in stars:
            star[0].y += star[2]
        for bullet in bullets:
            bullet.y -= bullet_speed
        for enemy in enemys1:
            enemy.y += enemy1_speed
        for enemy in enemys2:
            enemy[0].y += enemy2_speed
        for b in bonuses:
            b[0][1] += bonus_speed_fall

        screen.fill((49, 0, 98))

        stars = [star for star in stars if star[0].y <= size[1] + 10]
        if ship_pos.y <= 600:
            ship_pos.y = 600

        if ship_pos.y >= 800:
            ship_pos.y = 800

        if ship_pos.x >= 800:
            ship_pos.x = 800

        if ship_pos.x <= -200:
            ship_pos.x = -200

        deleted_bullets = []
        deleted_enemys1 = []
        deleted_enemys2 = []
        deleted_bonus = []

        for b in bullets:
            for enemy in enemys1:
                if enemy.collidepoint(b.x, b.y):
                    deleted_bullets.append(b)
                    deleted_enemys1.append(enemy)
                    draw_boom(enemy)
                    score+=100
            for enemy in enemys2:
                if enemy[0].collidepoint(b.x, b.y):
                    deleted_bullets.append(b)
                    if enemy[1]>0:
                        enemy[1]-=1
                    elif enemy[1] ==0:
                        deleted_enemys2.append(enemy)
                        draw_boom(enemy[0])
                    score+=200

        if now>= cooldown_live:

            for enemy in enemys1:
                if enemy.colliderect(ship_rect):
                    lives -= 1
                    deleted_enemys1.append(enemy)
                    score-=50
                    cooldown_live = now + 1000
                    break
            for enemy in enemys2:
                if enemy[0].colliderect(ship_rect):
                    lives -= 1
                    deleted_enemys2.append(enemy)
                    score-=100
                    cooldown_live = now + 1000
                    break
            if lives <=0:
                game_res = True
                save_score(score)


        for b in bonuses:
            if ship_rect.colliderect(b[0]):
                if b[1] == "speed":
                    deleted_bonus.append(b)
                    speed_boost_until = now + speed_boost_time
                    ship_speed = int(base_ship_speed * bonus_speed_ch)
                elif b[1] == "live":
                    deleted_bonus.append(b)
                    lives+=1
                elif b[1] == "speed-bullet":
                    deleted_bonus.append(b)
                    boost_bullet = True
                    boost_bullet_until = now + boost_bullet_time






        bullets = [b for b in bullets if b.y >= - 20 and b not in deleted_bullets]
        deleted_bullets = []
        enemys1 = [enemy for enemy in enemys1 if enemy.y <=size[1]+10 and enemy not in deleted_enemys1]
        deleted_enemys1 = []
        enemys2 = [enemy for enemy in enemys2 if enemy[0].y <=size[1] + 10 and enemy not in deleted_enemys2]
        deleted_enemys2 = []
        bonuses = [b for b in bonuses if b[0][1] <= size[1] + 10 and b not in deleted_bonus]
        deleted_bonus = []

        for star in stars:
            pygame.draw.circle(screen, "WHITE", (star[0].x, star[0].y), star[1])

        for enemy in enemys1:
            rect = enemy1_image.get_rect(center=enemy.center)
            screen.blit(enemy1_image, rect)

        for enemy in enemys2:
            rect = enemy2_image.get_rect(center=enemy[0].center)
            screen.blit(enemy2_image, rect)

        for b in bonuses:
            if b[1] == "speed":
                screen.blit(bonus_speed_image, bonus_speed_image.get_rect(center=b[0].center))
            elif b[1] == "live":
                screen.blit(live_image, bonus_speed_image.get_rect(center=b[0].center))
            elif b[1] == "speed-bullet":
                screen.blit(bonus_speed_bullet_image, bonus_speed_image.get_rect(center=b[0].center))


        for bullet in bullets:
            pygame.draw.circle(screen, bullet_color, (bullet.x, bullet.y), bullet_r)

        for b in booms:
            boom_size = 10 + b[1]*5
            img = pygame.transform.scale(boom_image, (boom_size, boom_size))
            screen.blit(img, img.get_rect(center=b[0]))
            b[1]+=1
        booms = [b for b in booms if b[1] < 15]

        if now >= cooldown_live or (now //100)%2 !=0:
            screen.blit(ship_image, ship_image.get_rect(center=ship_pos))

    font = pygame.font.Font(None, 40)
    screen.blit(font.render(f"SCORE: {score}", True, "WHITE"), (10, 725))

    if lives > 5:
        lives = 5

    for i in range(lives):
        screen.blit(live_image, (10 + i*50, 750))


    if now < speed_boost_until:
        bar_w = int(180 * (speed_boost_until / speed_boost_time))
        pygame.draw.rect

    bx, by1, bw, bh = 400, 732, 190, 18
    pygame.draw.rect(screen, (49, 0, 98), (bx, by1, bw, bh))
    if now < speed_boost_until:
        bar_w = int(bw * ((speed_boost_until - now) / speed_boost_time))
        pygame.draw.rect(screen, (100, 255, 100), (bx, by1, bar_w, bh))
    pygame.draw.rect(screen, "WHITE", (bx, by1, bw, bh), 2)

    by2 = by1 + 30
    pygame.draw.rect(screen, (49, 0, 98), (bx, by2, bw, bh))
    if now < boost_bullet_until:
        bar_w = int(bw * ((boost_bullet_until - now) / boost_bullet_time))
        pygame.draw.rect(screen, (100, 255, 100), (bx, by2, bar_w, bh))
    pygame.draw.rect(screen, "WHITE", (bx, by2, bw, bh), 2)

    font_small = pygame.font.Font(None, 22)
    screen.blit(font_small.render("SPEED", True, "WHITE"), (325, 733))
    screen.blit(font_small.render("FIRE", True, "WHITE"), (340, 763))


    if game_res:
        font = pygame.font.Font(None, 70)
        screen.blit(font.render("GAME OVER", True, "WHITE"), (150, 400))

    pygame.display.flip()
