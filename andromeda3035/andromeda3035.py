import pygame
import sys
import os
import random

class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = x, y
        self.vel = vel
        self.width, self.height = width, height
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def show(self, surface):
        surface.blit(self.image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)

class Laser(Sprite):
    def __init__(self, x, y, vel, width, height, color):
        super().__init__(x, y, vel, width, height, pygame.Surface((width, height)).convert_alpha())
        self.color = color
        self.image.fill(self.color)

class Ship(Sprite):
    def __init__(self, x, y, vel, width, height, image, hp, laserColor, laserVel):
        super().__init__(x, y, vel, width, height, image)
        self.lasers = pygame.sprite.Group()
        self.hp = hp
        self.laserColor = laserColor
        self.laserVel = laserVel

    def shoot(self):
        laserWidth, laserHeight = pixelSize, pixelSize * 3
        self.lasers.add(Laser(self.x + self.width // 2 - laserWidth // 2, self.y, self.laserVel, laserWidth,
                                laserHeight, self.laserColor))

    def moveLasers(self):
        for laser in self.lasers.sprites():
            if laser.y > 0:
                laser.y -= laser.vel
                laser.show(win)
            else:
                laser.kill()

class Enemy(Ship):
    def __init__(self, x, y, vel, width, height, image, hp, laserColor, laserVel, kind):
        super().__init__(x, y, vel, width, height, image, hp, laserColor, laserVel)
        self.kind = kind

    def shoot(self):
        laserWidth, laserHeight = pixelSize, pixelSize * 3
        enemyLasers.add(Laser(self.x + self.width // 2 - laserWidth // 2, self.y + 5, self.laserVel, laserWidth,
                                laserHeight, self.laserColor))

def menu(*args):
    clock = pygame.time.Clock()
    fps = 60

    transparent = pygame.Surface((screenWidth, screenHeight)).convert()
    transparent.fill((0, 0, 0))
    transparent.set_alpha(150)

    if len(args) > 0:
        if args[0] == 'gameover':
            font = pygame.font.Font(os.path.join('assets', 'm5x7.ttf'), 128)
            font2 = pygame.font.Font(os.path.join('assets', 'm5x7.ttf'), 64)

            args = list(args)
            if args[1] < 0:
                args[1] = 0
            else:
                args[1] += 1

            highScore = 0
            with open(os.path.join('assets', 'score.txt'), 'r') as reader:
                highScore = int(reader.read())
            if args[1] > int(highScore):
                highScore = args[1]
                with open(os.path.join('assets', 'score.txt'), 'w') as writer:
                    writer.write(str(highScore))

            text = font.render('Game Over!', False, (255, 0, 0))
            text2 = font2.render('Press enter to continue...', False, (255, 255, 255))
            text3 = font2.render(f'Score: {args[1]}', False, (0, 150, 255))
            text4 = font2.render(f'High Score: {highScore}', False, (0, 150, 0))

            win.blit(transparent, (0, 0))
            win.blit(text, (screenWidth // 2 - text.get_width() // 2, 250))
            win.blit(text2, (screenWidth // 2 - text2.get_width() // 2, 500))
            win.blit(text3, (screenWidth // 2 - text3.get_width() // 2, 420))
            win.blit(text4, (screenWidth // 2 - text4.get_width() // 2, 370))
    else:
        font = pygame.font.Font(os.path.join('assets', 'm5x7.ttf'), 128)
        font2 = pygame.font.Font(os.path.join('assets', 'm5x7.ttf'), 64)

        text = font.render('Andromeda', False, (0, 150, 255))
        text2 = font2.render('3035', False, (125, 50, 175))
        text3 = font2.render('Press enter to begin...', False, (255, 255, 255))

        backgroundImg = pygame.image.load(os.path.join('assets', 'img', 'background0.png')).convert()
        background = Sprite(0, 0, 0, screenWidth, screenHeight, backgroundImg)

        playerImg = pygame.image.load(os.path.join('assets', 'img', 'player.png')).convert_alpha()
        playerWidth, playerHeight = pixelSize * 30, pixelSize * 28
        player = Ship(screenWidth // 2 - playerWidth // 2, screenHeight // 2 - playerHeight // 2, 7,
                        playerWidth, playerHeight, playerImg, 3, (0, 255, 0), 5)

        background.show(win)
        win.blit(transparent, (0, 0))
        player.show(win)
        win.blit(text, (screenWidth // 2 - text.get_width() // 2, 35))
        win.blit(text2, (screenWidth // 2 - text2.get_width() // 2, 128))
        win.blit(text3, (screenWidth // 2 - text3.get_width() // 2, 500))

    pygame.display.update()

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            break

def gameLoop():
    clock = pygame.time.Clock()
    fps = 60
    frameCount = 0

    playerHit = pygame.mixer.Sound(os.path.join('assets', 'sfx', 'hit.ogg'))
    enemyHit = pygame.mixer.Sound(os.path.join('assets', 'sfx', 'hit2.ogg'))
    playerLaser = pygame.mixer.Sound(os.path.join('assets', 'sfx', 'laser.ogg'))
    enemyLaser = pygame.mixer.Sound(os.path.join('assets', 'sfx', 'laser2.ogg'))
    powerupSound = pygame.mixer.Sound(os.path.join('assets', 'sfx', 'powerup.ogg'))
    enemyHit.set_volume(0.5)
    playerLaser.set_volume(0.05)
    enemyLaser.set_volume(0.3)

    enemyExplosionImg = pygame.image.load(os.path.join('assets', 'img', 'enemy_explosion.png'))
    playerExplosionImg = pygame.image.load(os.path.join('assets', 'img', 'player_explosion.png'))
    explosions = pygame.sprite.Group()

    heartImg = pygame.image.load(os.path.join('assets', 'img', 'heart.png'))
    heartEmptyImg = pygame.image.load(os.path.join('assets', 'img', 'heart_empty.png'))
    hearts = pygame.sprite.Group()
    heartWidth, heartHeight = 5 * pixelSize, 5 * pixelSize
    x, y = screenWidth - (heartWidth * 3 + pixelSize * 3), pixelSize
    for i in range(3):
        hearts.add(Sprite(x, y, 0, heartWidth, heartHeight, heartImg))
        x += heartWidth + pixelSize

    medkitImg = pygame.image.load(os.path.join('assets', 'img', 'medkit.png'))
    medkits = pygame.sprite.Group()

    enemyImg, enemyDestroyedImg = [], []
    for i in range(3):
        enemyImg.append(pygame.image.load(os.path.join('assets', 'img', f'enemy{i}.png')))
    for i in range(3):
        enemyDestroyedImg.append(pygame.image.load(os.path.join('assets', 'img', f'enemy_destroyed{i}.png')))
    enemyWidth, enemyHeight = pixelSize * 9, pixelSize * 7
    enemies = pygame.sprite.Group()
    global enemyLasers
    enemyLasers = pygame.sprite.Group()
    enemySpawnRate = 0
    enemySpawnRateIncrease = 80

    playerImg = pygame.image.load(os.path.join('assets', 'img', 'player.png')).convert_alpha()
    playerWidth, playerHeight = pixelSize * 15, pixelSize * 14
    player = Ship(screenWidth // 2 - playerWidth // 2, 500, 7, playerWidth, playerHeight, playerImg, 3,
                     (0, 255, 0), 5)
    player.powerup = False
    powerupCooldown = 0
    powerups = pygame.sprite.Group()
    powerupImg = pygame.image.load(os.path.join('assets', 'img', 'powerup.png')).convert_alpha()

    backgroundImg = []
    backgrounds = pygame.sprite.Group()
    backgroundY = 0
    for i in range(2):
        backgroundImg.append(pygame.image.load(os.path.join('assets', 'img', f'background{i}.png')).convert())
    for img in backgroundImg:
        backgrounds.add(Sprite(0, backgroundY, 1, screenWidth, screenHeight, img))
        backgroundY -= screenHeight

    font = pygame.font.Font(os.path.join('assets', 'm5x7.ttf'), 45)
    score = 0

    pygame.mixer.music.load(os.path.join('assets', 'music', 'DynamicFight_3.ogg'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    run = True
    while run:
        clock.tick(fps)

        if frameCount % (fps * enemySpawnRateIncrease) == 0 and enemySpawnRate <= 1:
            enemySpawnRateIncrease = 60
            enemySpawnRate += 0.5

        if frameCount % (fps / enemySpawnRate) == 0:
            kind = random.randrange(len(enemyImg))
            if kind == 0:
                vel, laserVel = 4, -5
                randomX = random.randint(0, screenWidth - (3 * enemyWidth + pixelSize * 2))
                x = [randomX, randomX + enemyWidth + pixelSize, randomX + enemyWidth * 2 + pixelSize * 2]
                y = -enemyHeight
                for x in x:
                    enemies.add(Enemy(x, y, vel, enemyWidth, enemyHeight, enemyImg[kind], 2,
                                        (255, 0, 0), laserVel, kind))
            elif kind == 1:
                vel, laserVel = 3, -4
                x = random.randint(0, screenWidth - enemyWidth)
                y = [0, -enemyHeight - pixelSize, 2 * -enemyHeight - pixelSize * 2]
                for y in y:
                    enemies.add(Enemy(x, y, vel, enemyWidth, enemyHeight, enemyImg[kind], 2,
                                        (255, 0, 0), laserVel, kind))
            else:
                vel, laserVel = 5, -6
                x = random.randint(0, screenWidth - enemyWidth * 2 - pixelSize)
                y = 0
                for i in range(2):
                    enemies.add(Enemy(x, y, vel, enemyWidth, enemyHeight, enemyImg[kind], 1,
                                        (255, 0, 0), laserVel, kind))
                    x += enemyWidth + pixelSize

        if player.hp < 3 and frameCount % (fps * 20) == 0 and random.choice([True, False]):
            medkitWidth, medkitHeight = pixelSize * 7, pixelSize * 7
            medkits.add(Sprite(random.randint(0, screenWidth - medkitWidth), -medkitHeight, 5, medkitWidth, medkitHeight, medkitImg))

        if not player.powerup and frameCount % (fps * 10) == 0 and random.choice([True, False]):
            powerupWidth, powerupHeight = pixelSize * 7, pixelSize * 7
            powerups.add(Sprite(random.randint(0, screenWidth - powerupWidth), -powerupHeight, 5, powerupWidth, powerupHeight, powerupImg))

        if player.powerup and powerupCooldown <= 0:
            player.powerup = False
            player.laserColor = (0, 255, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > 0:
            player.x -= player.vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x + player.width < screenWidth:
            player.x += player.vel
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y > 0:
            player.y -= player.vel
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player.height < screenHeight:
            player.y += player.vel
        if keys[pygame.K_SPACE] and frameCount % (fps / 10) == 0:
            player.shoot()
            playerLaser.play()

        for background in backgrounds.sprites():
            background.y += background.vel
            if background.y >= screenHeight:
                background.y = -screenHeight
            background.show(win)

        for laser in enemyLasers.sprites():
            if pygame.sprite.collide_mask(laser, player):
                laser.kill()
                player.hp -= 1
                score -= 1
                playerHit.play()
                if player.hp <= 0:
                    for laser in player.lasers.sprites():
                        laser.show(win)
                    for laser in enemyLasers.sprites():
                        laser.show(win)
                    for enemy in enemies.sprites():
                        enemy.show(win)
                    for explosion in explosions.sprites():
                        explosion.show(win)
                    win.blit(pygame.transform.scale(playerExplosionImg, (pixelSize * 15, pixelSize * 15)), (player.x, player.y))
                    for powerup in powerups.sprites():
                        powerup.show(win)
                    for medkit in medkits.sprites():
                        medkit.show(win)
                    for heart in hearts.sprites():
                        heart.show(win)
                    win.blit(scoreCounter, (pixelSize, -pixelSize))
                    pygame.display.update()
                    pygame.mixer.music.stop()
                    menu('gameover', score)
                    run = False
            else:
                if laser.y < screenHeight:
                    laser.y -= laser.vel
                    laser.show(win)
                else:
                    laser.kill()
        
        for enemy in enemies.sprites():
            for laser in player.lasers.sprites():
                if pygame.sprite.collide_mask(laser, enemy):
                    laser.kill()
                    if laser.color == (0, 150, 255):
                        enemy.hp -= 2
                    else:
                        enemy.hp -= 1
                    enemy.image = pygame.transform.scale(enemyDestroyedImg[enemy.kind], (enemy.width, enemy.height))
                    if enemy.hp <= 0:
                        enemy.kill()
                        explosion = Sprite(enemy.x, enemy.y - pixelSize, 0, pixelSize * 9, pixelSize * 9, enemyExplosionImg)
                        explosion.cooldown = 20
                        explosions.add(explosion)
                        enemyHit.play()
                        if enemy.kind == 2:
                            score += 2
                        else:
                            score += 1
            if pygame.sprite.collide_mask(enemy, player):
                enemy.kill()
                explosion = Sprite(enemy.x, enemy.y - pixelSize, 0, pixelSize * 9, pixelSize * 9, enemyExplosionImg)
                explosion.cooldown = 20
                explosions.add(explosion)
                player.hp -= 1
                score -= 1
                playerHit.play()
                enemyHit.play()
                if player.hp <= 0:
                    for laser in player.lasers.sprites():
                        laser.show(win)
                    for laser in enemyLasers.sprites():
                        laser.show(win)
                    for enemy in enemies.sprites():
                        enemy.show(win)
                    for explosion in explosions.sprites():
                        explosion.show(win)
                    win.blit(pygame.transform.scale(playerExplosionImg, (pixelSize * 15, pixelSize * 15)), (player.x, player.y))
                    for powerup in powerups.sprites():
                        powerup.show(win)
                    for medkit in medkits.sprites():
                        medkit.show(win)
                    for heart in hearts.sprites():
                        heart.show(win)
                    win.blit(scoreCounter, (pixelSize, -pixelSize))
                    pygame.display.update()
                    pygame.mixer.music.stop()
                    menu('gameover', score)
                    run = False
            else:
                if enemy.y < screenHeight:
                    if enemy.kind == 2 or enemy.kind == 1:
                        shootChoice = random.choice([True, False, False])
                        if enemy.kind == 1 and enemy.hp >= 2:
                            shootChoice = False
                    else:
                        if enemy.hp >= 2:
                            shootChoice = random.choice([True, False])
                        else:
                            shootChoice = False
                    if frameCount % fps == 0 and shootChoice:
                        enemy.shoot()
                        enemyLaser.play()
                    enemy.y += enemy.vel
                    enemy.show(win)
                else:
                    enemy.kill()
                    if (enemy.kind == 2 or enemy.hp >= 2) and enemySpawnRate < 1:
                        score -= 1
        
        for explosion in explosions.sprites():
            explosion.show(win)
            explosion.cooldown -= 1
            if explosion.cooldown <= 0:
                explosion.kill()
        
        player.moveLasers()
        player.show(win)

        for medkit in medkits.sprites():
            if medkit.y >= screenHeight:
                medkit.kill()
            else:
                if pygame.sprite.collide_mask(medkit, player):
                    player.hp = 3
                    medkit.kill()
                    powerupSound.play()
                else:
                    medkit.y += medkit.vel
                    medkit.show(win)

        for powerup in powerups.sprites():
            if powerup.y >= screenHeight:
                powerup.kill()
            else:
                if pygame.sprite.collide_mask(powerup, player):
                    powerup.kill()
                    player.powerup = True
                    if enemySpawnRate <= 0.5:
                        powerupCooldown = fps * 10
                    else:
                        powerupCooldown = fps * 20
                    player.laserColor = (0, 150, 255)
                    powerupSound.play()
                    for enemy in enemies.sprites():
                        enemy.kill()
                        explosion = Sprite(enemy.x, enemy.y - pixelSize, 0, pixelSize * 9, pixelSize * 9, enemyExplosionImg)
                        explosion.cooldown = 20
                        explosions.add(explosion)
                        score += 1
                    enemyHit.play()
                else:
                    powerup.y += powerup.vel
                    powerup.show(win)

        for i in range(player.hp):
            hearts.sprites()[i].image = pygame.transform.scale(heartImg, (heartWidth, heartHeight))

        for heart in hearts.sprites():
            heart.show(win)
            heart.image = pygame.transform.scale(heartEmptyImg, (heartWidth, heartHeight))

        if score < 0:
            score = 0
        scoreCounter = font.render(f'Score: {score}', False, (255, 255, 255))
        win.blit(scoreCounter, (pixelSize, -pixelSize))

        pygame.display.update()
        win.fill((0, 0, 0))
        frameCount += 1
        powerupCooldown -= 1

def main():
    global screenWidth, screenHeight, win, pixelSize
    pygame.init()
    displayInfo = pygame.display.Info()
    screenWidth, screenHeight = 650, 650
    windowX = displayInfo.current_w // 2 - screenWidth // 2
    windowY = displayInfo.current_h // 2 - screenHeight // 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (windowX, windowY)
    pixelSize = 5
    win = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption('Andromeda 3035')
    icon = pygame.image.load(os.path.join('assets', 'img', 'icon.png'))
    pygame.display.set_icon(icon)

    pygame.mixer.music.load(os.path.join('assets', 'music', 'DeepSpaceA.ogg'))
    pygame.mixer.music.play(-1)
    menu()
    pygame.mixer.music.stop()
    while True:
        gameLoop()

if __name__ == '__main__':
    main()