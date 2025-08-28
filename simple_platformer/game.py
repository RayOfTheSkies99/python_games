import random

# game window settings
WIDTH = 800
HEIGHT = 600
SPRITE_SIZE = 32 # crappy sprites made in paint

# list of all footstep sound files
footstep_sounds = [
    'footstep_grass_000',
    'footstep_grass_001',
    'footstep_grass_002',
    'footstep_grass_003',
    'footstep_grass_004'
]
footstep_timer = 0
FOOTSTEP_DELAY = 15 # frames to wait between footstep sounds. Lower = faster steps.

# player stats
player_x = 100
player_y = HEIGHT - 100
player_width = 30
player_height = 30
player_color = (255, 255, 0) # i wish i knew how to make a "mario"
player_speed = 5

# physics crap
player_vy = 0
GRAVITY = 0.5
JUMP_STRENGTH = -12
can_double_jump = False

# where you are and weren't
on_ground = False
was_on_ground = False

# --- "level design" ---

# main floor
ground_platform = Rect(0, HEIGHT - 100, WIDTH, 100)

# floating platforms/must be multiples of 32
floating_platforms = [
    Rect(250, HEIGHT - 170, 160, SPRITE_SIZE),
    Rect(100, HEIGHT - 260, 160, SPRITE_SIZE),
    Rect(400, HEIGHT - 350, 128, SPRITE_SIZE),
    Rect(650, HEIGHT - 290, 96, SPRITE_SIZE)
]

all_platforms = [ground_platform] + floating_platforms

# hitbox
player_rect = Rect(player_x, player_y, player_width, player_height)


def on_key_down(key):
    global player_vy, on_ground, can_double_jump

    if key == keys.SPACE:
        # regular jump
        if on_ground:
            player_vy = JUMP_STRENGTH
            can_double_jump = True
            sounds.error_007.play()
        # double jump
        elif can_double_jump:
            player_vy = JUMP_STRENGTH
            can_double_jump = False
            sounds.error_007.play()

def draw():
    # crappy sky bg
    for y in range(0, HEIGHT, SPRITE_SIZE):
        for x in range(0, WIDTH, SPRITE_SIZE):
            screen.blit('sky', (x, y))

    # dumb grass mc parody
    for plat in floating_platforms:
        for x in range(int(plat.left), int(plat.right), SPRITE_SIZE):
            screen.blit('platform_grass', (x, plat.top))

    # dumb dirt mc parody
    grass_height = SPRITE_SIZE
    grass_rect = Rect(ground_platform.left, ground_platform.top, ground_platform.width, grass_height)
    dirt_rect = Rect(ground_platform.left, grass_rect.bottom, ground_platform.width, ground_platform.height - grass_height)

    for x in range(int(grass_rect.left), int(grass_rect.right), SPRITE_SIZE):
        screen.blit('platform_grass', (x, grass_rect.top))

    for x in range(int(dirt_rect.left), int(dirt_rect.right), SPRITE_SIZE):
        for y in range(int(dirt_rect.top), int(dirt_rect.bottom), SPRITE_SIZE):
            screen.blit('platform_dirt', (x, y))

    screen.draw.filled_rect(player_rect, player_color)

def update():
    global player_x, player_y, player_vy, on_ground, was_on_ground, player_rect, footstep_timer, can_double_jump

    # dumb thing for footstep sound
    if footstep_timer > 0:
        footstep_timer -= 1
    
    is_moving_horizontally = False
    if keyboard.left:
        player_x -= player_speed
        is_moving_horizontally = True
    if keyboard.right:
        player_x += player_speed
        is_moving_horizontally = True

    # step rando
    if on_ground and is_moving_horizontally and footstep_timer == 0:
        sound_to_play = random.choice(footstep_sounds)
        getattr(sounds, sound_to_play).play()
        footstep_timer = FOOTSTEP_DELAY
    
    # --- "physics" ---

    player_vy += GRAVITY
    player_y += player_vy

    player_rect.topleft = (player_x, player_y)

    on_ground = False
    for plat in all_platforms:
        if player_rect.colliderect(plat):
            if player_vy > 0:
                player_y = plat.top - player_height
                player_vy = 0
                on_ground = True
                can_double_jump = False
                break
            elif player_vy < 0:
                player_y = plat.bottom
                player_vy = 0
                break
    
    player_rect.topleft = (player_x, player_y)
    
    if on_ground and not was_on_ground:
        sounds.toggle_001.play()

    was_on_ground = on_ground

    # --- limits and spawn (cant really die, so) ---

    if player_rect.left < 0:
        player_x = 0
        player_rect.left = 0
    if player_rect.right > WIDTH:
        player_x = WIDTH - player_width
        player_rect.right = WIDTH

    if player_rect.top >= HEIGHT:
        player_x = 100
        player_y = HEIGHT - 100
        player_vy = 0
        on_ground = False
        can_double_jump = False
        player_rect.topleft = (player_x, player_y)