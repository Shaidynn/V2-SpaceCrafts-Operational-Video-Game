import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("V2 SpaceCrafts")

border = pygame.Rect(500 + 15, 0, 10, 800)
Black = (0, 0, 0) # --> Black Display for Central Border
RED = (255, 0, 0) # --> Red Bullets
BLUE = (0, 0, 255) # --> Blue Bullets
WHITE = (255, 255, 255)
FPS = 120
MaxBullets = 3
BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
HEALTH_FONT = pygame.font.SysFont("comicsans", 30)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)
red_health = 10
blue_health = 10

backroundmusic = pygame.mixer.music.load(("backround.mp3")) 
pygame.mixer.music.play(-1)

BLTHITSOUNDS = pygame.mixer.Sound(
    os.path.join("BulletHit.mp3"))

BLTFIRESOUNDS = pygame.mixer.Sound(
    os.path.join("bulletFire.mp3"))

FINISHER = pygame.mixer.Sound(
    os.path.join("endgame.mp3"))

SpaceShip1 = pygame.image.load(
    os.path.join('ships.png')).convert_alpha()

SpaceShip2 = pygame.image.load(
    os.path.join('ship2.png')).convert_alpha()

space = pygame.image.load(
    os.path.join('galaxy.png')).convert()

SpaceShip1Resize = pygame.transform.rotate(pygame.transform.scale(SpaceShip1, (130, 110)), 270)

SpaceShip2Resize = pygame.transform.rotate(pygame.transform.scale(SpaceShip2, (130, 110)), 90)

spaceResize = pygame.transform.scale(space, (screen_width, screen_height))

def blue_movement(UserInterface, blue):
    if UserInterface[pygame.K_a] and blue.x - 4 > 0: # Left
        blue.x -= 4
    elif UserInterface[pygame.K_d] and blue.x + 4 < 405: # Right
        blue.x += 4
    elif UserInterface[pygame.K_w] and blue.y - 4 > 0: # Up
        blue.y -= 4
    elif UserInterface[pygame.K_s] and blue.y + 4 < 582: # Down
        blue.y += 4

def red_movement(UserInterface, red):
    if UserInterface[pygame.K_LEFT] and red.x - 4 > 524: # Left
        red.x -= 4
    elif UserInterface[pygame.K_RIGHT] and red.x + 4 < 888: # Right
        red.x += 4
    elif UserInterface[pygame.K_UP] and red.y - 4 > 0: # Up
        red.y -= 4
    elif UserInterface[pygame.K_DOWN] and red.y + 4 < 582: # Down
        red.y += 4


def draw(red, blue, red_bullets, blue_bullets, red_health, blue_health):
    #screen.fill((255, 255, 255)) # --> White Display
    screen.blit(space, (0, 0))
    pygame.draw.rect(screen, Black, border)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    blue_health_text = HEALTH_FONT.render(
        "Health: " + str(blue_health), 1, WHITE)
    screen.blit(
        red_health_text, (screen_width - red_health_text.get_width() - 10, 10))
    screen.blit(blue_health_text, (10, 10))
    screen.blit(SpaceShip1Resize, (blue.x, blue.y))
    screen.blit(SpaceShip2Resize, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(screen, RED, bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(screen, BLUE, bullet)

    pygame.display.update()   

def handleBullets(blue_bullets, red_bullets, blue, red):
    for bullet in blue_bullets:
        bullet.x += 4
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > screen_width:
            blue_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= 4
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
        
def winner(text):
    winner = WINNER_FONT.render(text, 1, WHITE)
    screen.blit(winner, (screen_width/2 - winner.get_width() /2,
                 screen_height/2 - winner.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(7500)


def main():
    global red_health, blue_health

    red = pygame.Rect(700, 300, 130, 110)
    blue = pygame.Rect(100, 300, 130, 110)

    red_bullets = []
    blue_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False     
                pygame.quit()
            

            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(blue_bullets) < MaxBullets:
                    bullet = pygame.Rect(
                        blue.x + blue.width, blue.y + blue.height // 2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BLTFIRESOUNDS.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MaxBullets:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BLTFIRESOUNDS.play()

           
            if event.type == BLUE_HIT:
                blue_health -= 1
                BLTHITSOUNDS.play()

            
            if event.type == RED_HIT:
                red_health -= 1
                BLTHITSOUNDS.play()
        
            
        winner_text = ""
        if red_health <= 0:
            pygame.mixer.pause()
            FINISHER.play()
            winner_text = "BLUE WINS!"

        
        if blue_health <= 0:
            pygame.mixer.pause()
            pygame.mixer.unpause()
            FINISHER.play()
            winner_text = "GREEN WINS!"
        
        if winner_text != "":
         winner(winner_text)
         break
        
        UserInterface = pygame.key.get_pressed()
        blue_movement(UserInterface, blue)
        red_movement(UserInterface, red)

        handleBullets(blue_bullets, red_bullets , blue, red )

        draw(red, blue, red_bullets, blue_bullets, red_health, blue_health)

    main()

if __name__ == "__main__":
    main()

