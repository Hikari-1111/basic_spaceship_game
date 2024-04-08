#Basic spaceship game

import random
import pygame

from pygame.locals import(
    RLEACCEL,
    KEYDOWN,
    K_ESCAPE,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    QUIT
)

pygame.mixer.init()                             
pygame.init()

move_up_sound = pygame.mixer.Sound("docs/assets/up_button.wav")
move_down_sound = pygame.mixer.Sound("docs/assets/down_button.wav")
collision_sound = pygame.mixer.Sound("docs/assets/collision_sound.wav")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("docs/assets/rocket_image.png").convert()       
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 3)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-3, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(3, 0)

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("docs/assets/missile_image.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 50),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(2, 3)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("docs/assets/cloud_image.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 70, SCREEN_WIDTH + 120),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = 1
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
gamescreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player1 = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)

enemies = pygame.sprite.Group()
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

clouds = pygame.sprite.Group()
CLOUDAPPEAR = pygame.USEREVENT + 2
pygame.time.set_timer(CLOUDAPPEAR, 500)

clock = pygame.time.Clock()                                      

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        
        elif event.type == CLOUDAPPEAR:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
    
    gamescreen.fill((52, 81, 92))
    for entity in all_sprites:
        gamescreen.blit(entity.surf, entity.rect)

    pressed_keys = pygame.key.get_pressed()
    player1.update(pressed_keys)
    enemies.update()
    clouds.update()

    if pygame.sprite.spritecollideany(player1, enemies):
        player1.kill()

        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
 
        pygame.time.delay(1000)                        

        running = False
    
    pygame.display.flip()

    clock.tick(150)                                    #adjusts the frame rate of the program to 150 frames/sec
