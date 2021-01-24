import pygame, math, block


def get_neighbor_count(block):
    count = 0
    for n in block.neighbors:
        if n.color == BLUE:
            count += 1
    return count


# left mouse click turns the block blue (alive)
def sprite_on(x, y):
    global blocks, h_radius

    for b in blocks:
        if abs(b.x - x) < h_radius and abs(b.y - y) < h_radius:
            # turn that block on (blue)
            b.color = BLUE
            break

# right mouse click turns the block white (dead)
def sprite_off(x, y):
    global blocks, h_radius

    for b in blocks:
        if abs(b.x - x) < h_radius and abs(b.y - y) < h_radius:
            # turn that block off (white)
            b.color = WHITE
            break


def create_hex_grid(border, grid_size, block_radius, block_margin):
    global blocks

    for row in range(grid_size):
        if row % 2 == 1:
            offset = block_radius
        else:
            offset = 0

        for col in range(grid_size):
            x = border + col * (block_margin + block_radius * 2) + offset
            y = border + block_margin + row * block_radius * 2

            b = block.block(x, y, 6, block_radius, WHITE, screen, math.pi / 2)
            blocks.append(b)

def assign_hex_neighbors():
    global blocks

    for block in blocks:
        east = (block.x + 2 * h_radius, block.y)
        west = (block.x - 2 * h_radius, block.y)
        n_e  = (block.x + h_radius, block.y - 2 * h_radius)
        n_w  = (block.x - h_radius, block.y - 2 * h_radius)
        s_e  = (block.x + h_radius, block.y + 2 * h_radius)
        s_w  = (block.x - h_radius, block.y + 2 * h_radius)

        for b in blocks:
            if abs(b.x - east[0]) < h_radius and abs(b.y - east[1]) < h_radius:
                block.neighbors.append(b)
            elif abs(b.x - west[0]) < h_radius and abs(b.y - west[1]) < h_radius:
                block.neighbors.append(b)
            elif abs(b.x - n_e[0]) < h_radius and abs(b.y - n_e[1]) < h_radius:
                block.neighbors.append(b)
            elif abs(b.x - n_w[0]) < h_radius and abs(b.y - n_w[1]) < h_radius:
                block.neighbors.append(b)
            elif abs(b.x - s_e[0]) < h_radius and abs(b.y - s_e[1]) < h_radius:
                block.neighbors.append(b)
            elif abs(b.x - s_w[0]) < h_radius and abs(b.y - s_w[1]) < h_radius:
                block.neighbors.append(b)

def create_sq_grid(border, grid_size, block_radius, block_margin):
    global blocks

    for row in range(grid_size):
        for col in range(grid_size):
            x = border + col * (block_margin + block_radius * 2)
            y = border + row * (block_margin + block_radius * 2)

            b = block.block(x, y, 4, block_radius, WHITE, screen, math.pi / 4)
            blocks.append(b)

def assign_sq_neighbors():
    global blocks

    for block in blocks:
        east  = (block.x + 2 * sq_radius, block.y)
        west  = (block.x - 2 * sq_radius, block.y)
        north = (block.x, block.y - 2 * sq_radius)
        south = (block.x, block.y + 2 * sq_radius)

        for b in blocks:
            if abs(b.x - east[0]) < sq_radius and abs(b.y - east[1]) < sq_radius:
                block.neighbors.append(b)
            elif abs(b.x - west[0]) < sq_radius and abs(b.y - west[1]) < sq_radius:
                block.neighbors.append(b)
            elif abs(b.x - north[0]) < sq_radius and abs(b.y - north[1]) < sq_radius:
                block.neighbors.append(b)
            elif abs(b.x - south[0]) < sq_radius and abs(b.y - south[1]) < sq_radius:
                block.neighbors.append(b)

def create_oct_sq_grid(border, grid_size, oct_radius, sq_radius, block_margin):
    global blocks

    # create octagons
    for row in range(grid_size):
        for col in range(grid_size):
            x = border + col * (block_margin + oct_radius * 2)
            y = border + row * (block_margin + oct_radius * 2)

            b = block.block(x, y, 8, oct_radius, WHITE, screen, math.pi / 8)
            blocks.append(b)

    # create squares
    apothem   = oct_radius * math.cos(math.pi / 8)
    for row in range(grid_size - 1):
        for col in range(grid_size - 1):
            x = border + apothem + block_margin + col * ((block_margin) + oct_radius * 2)
            y = border + apothem + block_margin + row * ((block_margin) + oct_radius * 2)

            b = block.block(x, y, 4, sq_radius, WHITE, screen)
            blocks.append(b)

def assign_oct_sq_neighbors(oct_radius, sq_radius):
    global blocks

    for block in blocks:
        # current block is an octagon
        if block.num_sides == 8:
            #octagon neighbors
            east  = (block.x + 2 * oct_radius, block.y)
            west  = (block.x - 2 * oct_radius, block.y)
            north = (block.x, block.y - 2 * oct_radius)
            south = (block.x, block.y + 2 * oct_radius)
            # square neighbors
            n_e = (block.x + oct_radius + sq_radius, block.y - oct_radius - sq_radius)
            n_w = (block.x - oct_radius - sq_radius, block.y - oct_radius - sq_radius)
            s_e = (block.x + oct_radius + sq_radius, block.y + oct_radius + sq_radius)
            s_w = (block.x - oct_radius - sq_radius, block.y + oct_radius + sq_radius)
            for b in blocks:
                if b.num_sides == 8:    # neighbor (b) is an octagon
                    if abs(b.x - east[0]) < oct_radius and abs(b.y - east[1]) < oct_radius:
                        block.neighbors.append(b)
                    elif abs(b.x - west[0]) < oct_radius and abs(b.y - west[1]) < oct_radius:
                        block.neighbors.append(b)
                    elif abs(b.x - south[0]) < oct_radius and abs(b.y - south[1]) < oct_radius:
                        block.neighbors.append(b)
                    elif abs(b.x - north[0]) < oct_radius and abs(b.y - north[1]) < oct_radius:
                        block.neighbors.append(b)
                elif b.num_sides == 4:  # neighbor (b) is a square
                    if abs(b.x - n_e[0]) < oct_radius and abs(b.y - n_e[1]) < oct_radius:
                        block.neighbors.append(b)
                    elif abs(b.x - n_w[0]) < oct_radius and abs(b.y - n_w[1]) < oct_radius:
                        block.neighbors.append(b)
                    elif abs(b.x - s_e[0]) < oct_radius and abs(b.y - s_e[1]) < oct_radius:
                        block.neighbors.append(b)
                    elif abs(b.x - s_w[0]) < oct_radius and abs(b.y - s_w[1]) < oct_radius:
                        block.neighbors.append(b)

        # current block is a square
        else:
            # only octagon neighbors
            n_e = (block.x + oct_radius + sq_radius, block.y - oct_radius - sq_radius)
            n_w = (block.x - oct_radius - sq_radius, block.y - oct_radius - sq_radius)
            s_e = (block.x + oct_radius + sq_radius, block.y + oct_radius + sq_radius)
            s_w = (block.x - oct_radius - sq_radius, block.y + oct_radius + sq_radius)
            for b in blocks:
                if b.num_sides == 8:
                    if abs(b.x - n_e[0]) < sq_radius and abs(b.y - n_e[1]) < sq_radius:
                        block.neighbors.append(b)
                    elif abs(b.x - n_w[0]) < sq_radius and abs(b.y - n_w[1]) < sq_radius:
                        block.neighbors.append(b)
                    elif abs(b.x - s_e[0]) < sq_radius and abs(b.y - s_e[1]) < sq_radius:
                        block.neighbors.append(b)
                    elif abs(b.x - s_w[0]) < sq_radius and abs(b.y - s_w[1]) < sq_radius:
                        block.neighbors.append(b)


def itterate_game_once():
    blocks_to_flip = []
    for b in blocks:
        n = get_neighbor_count(b)

        # if block is dead (BIRTH RATE)
        if b.color == WHITE and n >= birth_min and n <= birth_max:
            blocks_to_flip.append(b)

        # if block is alive (SURVIVAL RATE)
        elif b.color == BLUE and (n < survive_min or n > survive_max):
            blocks_to_flip.append(b)

    for b in blocks_to_flip:
        if b.color == WHITE:
            b.color = BLUE
        else:
            b.color = WHITE


# hexagonal grid setup
def hex_grid_setup():
    global margin, blocks
    blocks.clear()
    margin = 2 # adjust margin for this shape
    create_hex_grid(border, num_hex, h_radius, margin)
    assign_hex_neighbors()
# square grid setup
def square_grid_setup():
    global margin, blocks
    blocks.clear()
    margin = 0 # adjust margin for this shape
    create_sq_grid(border, num_sq, sq_radius, margin)
    assign_sq_neighbors()
# octagon-square grid setup
def oct_sq_grid_setup():
    global margin, blocks
    blocks.clear()
    margin = 2 # adjust margin for this shape
    sq_radius = oct_radius * math.sin(math.pi / 8) * math.sqrt(2)
    create_oct_sq_grid(border, num_oct, oct_radius, sq_radius, margin)
    assign_oct_sq_neighbors(oct_radius, sq_radius)


def clear_grid():
    global blocks
    for b in blocks:
        b.color = WHITE

def button_pressed(x, y):
    global birth_min, birth_max, survive_min, survive_max

    # coordinates of the middle of each image
    (oct_mid_x, oct_mid_y) = (oct_img_x + (img_size / 2), oct_img_y + (img_size / 2))
    (hex_mid_x, hex_mid_y) = (hex_img_x + (img_size / 2), hex_img_y + (img_size / 2))
    (sq_mid_x, sq_mid_y)   = (sq_img_x  + (img_size / 2), sq_img_y + (img_size / 2))

    # --- forward one generation ---
    if abs(play_btn_x - x) < play_btn_radius and abs(play_btn_y - y) < play_btn_radius:
        itterate_game_once()

    # --- clear grid ---
    elif abs(clear_btn_x - x) < clear_btn_radius and abs(clear_btn_y - y) < clear_btn_radius:
        clear_grid()

    # --- switch grid ---
    elif abs(oct_mid_x - x) < (img_size / 2) and abs(oct_mid_y - y) < (img_size / 2):
        oct_sq_grid_setup()
    elif abs(hex_mid_x - x) < (img_size / 2) and abs(hex_mid_y - y) < (img_size / 2):
        hex_grid_setup()
    elif abs(sq_mid_x - x) < (img_size / 2) and abs(sq_mid_y - y) < (img_size / 2):
        square_grid_setup()

    # --- birth rate ---
    # birth min value
    elif abs(b_min_up_btn_x - x) < cntrl_btn_r and abs(b_min_up_btn_y - y) < cntrl_btn_r:
        if birth_min < birth_max:
            birth_min += 1
    elif abs(b_min_dn_btn_x - x) < cntrl_btn_r and abs(b_min_dn_btn_y - y) < cntrl_btn_r:
        if birth_min > 0:
            birth_min -= 1
    # birth max value
    elif abs(b_max_up_btn_x - x) < cntrl_btn_r and abs(b_max_up_btn_y - y) < cntrl_btn_r:
        birth_max += 1
    elif abs(b_max_dn_btn_x - x) < cntrl_btn_r and abs(b_max_dn_btn_y - y) < cntrl_btn_r:
        if birth_max > birth_min:
            birth_max -= 1

    # --- survival rate ---
    # survive min value
    elif abs(s_min_up_btn_x - x) < cntrl_btn_r and abs(s_min_up_btn_y - y) < cntrl_btn_r:
        if survive_min < survive_max:
            survive_min += 1
    elif abs(s_min_dn_btn_x - x) < cntrl_btn_r and abs(s_min_dn_btn_y - y) < cntrl_btn_r:
        if survive_min > 0:
            survive_min -= 1
    # suvive max value
    elif abs(s_max_up_btn_x - x) < cntrl_btn_r and abs(s_max_up_btn_y - y) < cntrl_btn_r:
        survive_max += 1
    elif abs(s_max_dn_btn_x - x) < cntrl_btn_r and abs(s_max_dn_btn_y - y) < cntrl_btn_r:
        if survive_max > survive_min:
            survive_max -= 1



def main():
    global screen
    pygame.display.set_caption("Conway's Game of Life")

    while True:
        screen.fill(GREY)

        # vertical divider line
        pygame.draw.line(screen, BLACK, v_divider_line_start, v_divider_line_end, 3)
        # horizontal divider line
        pygame.draw.line(screen, BLACK, h_divider_line_start, h_divider_line_end, 3)
        # horizontal divider line
        pygame.draw.line(screen, BLACK, h2_divider_line_start, h2_divider_line_end, 3)

        for b in blocks:
            b.update_color()
        for b in buttons:
            b.update_color()

        # LABELS
        # go label
        text = font.render("Go", True, BLACK)
        screen.blit(text, [play_btn_x + 30, play_btn_y - 10])
        # clear label
        text = font.render("Clear", True, BLACK)
        screen.blit(text, [clear_btn_x + 30, clear_btn_y - 10])
        # birth rate range label
        text = s_font.render("Birth rate:", True, WHITE)
        screen.blit(text, [b_min_up_btn_x - 10, b_min_up_btn_y - 30])
        text = s_font.render(str(birth_min) + " - " + str(birth_max), True, WHITE)
        screen.blit(text, [b_min_up_btn_x + 30, b_min_up_btn_y])
        # survival rate range label
        text = s_font.render("Survival rate:", True, WHITE)
        screen.blit(text, [s_min_up_btn_x - 10, s_min_up_btn_y - 30])
        text = s_font.render(str(survive_min) + " - " + str(survive_max), True, WHITE)
        screen.blit(text, [s_min_up_btn_x + 30, s_min_up_btn_y])

        # GRID IMAGES
        # oct_sq grid image
        screen.blit(oct_img, (oct_img_x, oct_img_y))
        # hex grid image
        screen.blit(hex_img, (hex_img_x, hex_img_y))
        # sq grid image
        screen.blit(sq_img, (sq_img_x, sq_img_y))

        pygame.display.update()

        # EVENTS
        for event in pygame.event.get():
            # left click (turn block on)
            if pygame.mouse.get_pressed()[0]:
                c = pygame.mouse.get_pos()
                # button is pressed
                if c[0] > v_divider_line_start[0]:
                    button_pressed(c[0], c[1])
                # block is pressed
                else:
                    # turn block on
                    sprite_on(c[0], c[1])

            # right click (turn block off)
            elif pygame.mouse.get_pressed()[2]:
                c = pygame.mouse.get_pos()
                sprite_off(c[0], c[1])


            if event.type == pygame.QUIT:
                pygame.quit()
                break




### GLOBAL VARIABLES
SCREEN_SIZE_WIDTH  = 900
SCREEN_SIZE_HEIGHT = 700
blocks  = []
buttons = []

#initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE_WIDTH, SCREEN_SIZE_HEIGHT))

# colors
WHITE  = (255, 255, 255)
BLACK  = (0,0,0)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
GREEN  = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY   = (100, 100, 100)

# grid layout
margin = 2
border = 40

# size 36 for text font
font   = pygame.font.Font(None, 36)
s_font = pygame.font.Font(None, 24)

# hex dimensions
h_radius = 8
num_hex  = 35
# square dimensions
sq_radius = 8
num_sq    = 40
# oct-square dimensions
oct_radius = 7
num_oct    = 40




### BUTTONS ###
# play button
(play_btn_x, play_btn_y) = (700, 100)
play_btn_radius          = 20
play_btn = block.block(play_btn_x, play_btn_y, 3, play_btn_radius, GREEN, screen)
buttons.append(play_btn)
# clear button
(clear_btn_x, clear_btn_y) = (700, 150)
clear_btn_radius = 15
clear_btn = block.block(clear_btn_x, clear_btn_y, 8, clear_btn_radius, RED, screen, math.pi / 8)
buttons.append(clear_btn)

# divider lines
divider_x = 680
v_divider_line_start  = (divider_x, 0)
v_divider_line_end    = (divider_x, SCREEN_SIZE_HEIGHT)
h_divider_line_start  = (divider_x, clear_btn_y + 30)
h_divider_line_end    = (SCREEN_SIZE_WIDTH, clear_btn_y + 30)
h2_divider_line_start = (divider_x, 500)
h2_divider_line_end   = (SCREEN_SIZE_WIDTH, 500)

# grid selection images (tiling options)
img_size = 40
# oct_sq grid img
(oct_img_x, oct_img_y) = (690, 200)
oct_img = pygame.image.load('oct.png')
oct_img = pygame.transform.scale(oct_img, (img_size, img_size))
# hex grid img
(hex_img_x, hex_img_y) = (690, 250)
hex_img = pygame.image.load('hex.png')
hex_img = pygame.transform.scale(hex_img, (img_size, img_size))
# sq grid img
(sq_img_x, sq_img_y) = (690, 300)
sq_img = pygame.image.load('sq.png')
sq_img = pygame.transform.scale(sq_img, (img_size, img_size))


# control buttons
cntrl_btn_r = 10
(birth_min, birth_max)     = (0, 2)
(survive_min, survive_max) = (2, 3)
# birth control minimum
(b_min_up_btn_x, b_min_up_btn_y) = (700, 550)
(b_min_dn_btn_x, b_min_dn_btn_y) = (700, b_min_up_btn_y + 15)
b_min_up_btn = block.block(b_min_up_btn_x, b_min_up_btn_y, 3, cntrl_btn_r, WHITE, screen, - math.pi / 2)
b_min_dn_btn = block.block(b_min_up_btn_x, b_min_dn_btn_y, 3, cntrl_btn_r, WHITE, screen, math.pi / 2)
buttons.append(b_min_up_btn)
buttons.append(b_min_dn_btn)
# birth control maximum
(b_max_up_btn_x, b_max_up_btn_y) = (800, 550)
(b_max_dn_btn_x, b_max_dn_btn_y) = (800, b_max_up_btn_y + 15)
b_max_up_btn = block.block(b_max_up_btn_x, b_max_up_btn_y, 3, cntrl_btn_r, WHITE, screen, - math.pi / 2)
b_max_dn_btn = block.block(b_max_up_btn_x, b_max_dn_btn_y, 3, cntrl_btn_r, WHITE, screen, math.pi / 2)
buttons.append(b_max_up_btn)
buttons.append(b_max_dn_btn)

# survival control minimum
(s_min_up_btn_x, s_min_up_btn_y) = (700, 625)
(s_min_dn_btn_x, s_min_dn_btn_y) = (700, s_min_up_btn_y + 15)
s_min_up_btn = block.block(s_min_up_btn_x, s_min_up_btn_y, 3, cntrl_btn_r, WHITE, screen, - math.pi / 2)
s_min_dn_btn = block.block(s_min_up_btn_x, s_min_dn_btn_y, 3, cntrl_btn_r, WHITE, screen, math.pi / 2)
buttons.append(s_min_up_btn)
buttons.append(s_min_dn_btn)
# survival control maximum
(s_max_up_btn_x, s_max_up_btn_y) = (800, 625)
(s_max_dn_btn_x, s_max_dn_btn_y) = (800, s_max_up_btn_y + 15)
s_max_up_btn = block.block(s_max_up_btn_x, s_max_up_btn_y, 3, cntrl_btn_r, WHITE, screen, - math.pi / 2)
s_max_dn_btn = block.block(s_max_up_btn_x, s_max_dn_btn_y, 3, cntrl_btn_r, WHITE, screen, math.pi / 2)
buttons.append(s_max_up_btn)
buttons.append(s_max_dn_btn)




main()
