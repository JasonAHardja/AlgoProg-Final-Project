import pygame
import sys
import random

opponent_knocked_out = False

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Boxing Game')


#health
player_health = 100
opponent_health = 100

#variables
player = pygame.Rect(200, 420, 50, 100)
opponent = pygame.Rect(600, 420, 50, 100)
player_speed = 4
opponent_speed = 5
player_punching = False
opponent_punching = False
hit_cooldown = 0

points = 0

#colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#fonts
font = pygame.font.SysFont('Arial', 30)

#background image
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_rect = background_image.get_rect()

background_x = 0

#jump variables
is_jumping = False
jump_count = 10

#player position
initial_player_y = player.y
ground_level = screen_height - 80  # Adjust this value as needed

# Function for drawing text
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

#player and opponent images
player_image = pygame.image.load("play.png")
player_image = pygame.transform.scale(player_image, (50, 100))

opponent_image = pygame.image.load("opp.png")
opponent_image = pygame.transform.scale(opponent_image, (50, 100))

#Main Loop
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for Enter key press
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            player_punching = True

    keys = pygame.key.get_pressed()

    #player can move only if they still have health
    if player_health > 0:
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < screen_width:
            player.x += player_speed

    #jump mechanics
    if not is_jumping and player_health > 0:
        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player.y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10
            player.y = ground_level - player.height

    #opponent AI
    if opponent.left > player.right:
        opponent.x -= opponent_speed
    elif opponent.right < player.left:
        opponent.x += opponent_speed

    if random.randint(0, 100) < 2 and not opponent_punching and opponent_health > 0:
        opponent_punching = True

    #handle punches
    if player_punching and player_health > 0:
        if hit_cooldown == 0 and player.colliderect(opponent):
            opponent_punching = False
            hit_cooldown = 30
        else:
            player_punching = False

        opponent_health -= 0.5
        points += 0.5

        if opponent_health <= 0:
            opponent_health = 0
            print("Opponent knocked out!")
            #stop opponent movement when knocked out
            opponent_speed = 0

    if opponent_punching and opponent_health > 0:
        if hit_cooldown == 0 and opponent.colliderect(player):
            player_punching = False
            hit_cooldown = 30
            

            #deduct player health
            player_health -= 35

            # Check if player health is below zero
            if player_health <= 0:
                player_health = 0
                print("Player knocked out!")
                # Stop player movement when knocked out
                player_speed = 0

        else:
            opponent_punching = False

    #hit cooldown
    if hit_cooldown > 0:
        hit_cooldown -= 1

    #win/lose conditions
    if player_health <= 0:
        draw_text("YOU LOSE", font, RED, screen_width // 2 - 70, screen_height // 2 - 30)
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds before quitting
        running = False
    elif opponent_health <= 0:
        draw_text("YOU WIN", font, WHITE, screen_width // 2 - 70, screen_height // 2 - 30)
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds before quitting
        running = False

    # Blit the background image onto the screen
    screen.blit(background_image, (background_x, 0))

    #player and opponent images
    screen.blit(player_image, player.topleft)
    screen.blit(opponent_image, opponent.topleft)

    #health bars
    pygame.draw.rect(screen, WHITE, (10, screen_height - 30, player_health, 20))
    pygame.draw.rect(screen, WHITE, (screen_width - 10 - opponent_health, screen_height - 30, opponent_health, 20))

    #texts on the screen
    draw_text("!! BOXKING !!", font, WHITE, 10, 10)
    draw_text(f"Punches: {points}", font, WHITE, screen_width - 190, 10)
    draw_text(f"Player Health: {player_health}", font, WHITE, 10, screen_height - 60)
    draw_text(f"Opponent Health: {opponent_health}", font, WHITE, screen_width - 220, screen_height - 60)

    #display
    pygame.display.flip()

    #frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()