import pygame

### CLASSES
class block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect((x, y), (width, height))
        
class BirthControl:
    
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.up = None 
        self.down = None

    def button_set(self):
        self.up = pygame.draw.polygon(screen,GREEN, ((self.x,self.y), ((self.x - 15), self.y + 25), (self.x + 15, self.y + 25)))

        self.down = pygame.draw.polygon(screen,GREEN, ((self.x - 15,self.y + (margin*30)), ((self.x + 15), self.y + (margin * 30)), (self.x, self.y + 25 + (margin * 30))))

class Counter:

    def __init__(self, x, y):
        self.count = 0
        self.x = x 
        self.y = y

    def counter(self, count,up_button, up=False, down=False):
        if up:
            count +=1
        elif down:
            count -=1
        counter = font.render(str(count), True, BLACK)
        counter_rect = counter.get_rect()
        counter_rect.center = (self.x,(up_button.y + (up_button.height * 2)))
        screen.blit(counter, counter_rect)
        return count

    
### FUNCTIONS
# cells are by default "dead". Left mouse click turns the square blue ("alive")
# if the start game button is clicked, call create grid array function
def sprite_on(x, y):
    global game_active
    
    for s in all_sprites:
        if s.rect.collidepoint(x, y):
            #############
            # check if it is outside boundery of playing grid (start game button)
            # if it is, call create_grid_array()
            # return - so color doesn't change
            #############
            if x > border + num_rect * (sq_width + margin):
                create_grid_array()
                game_active = True
                return

            #turn that square on (blue)
            s.color = BLUE
            s.image.fill(s.color)
            visible_sprites.add(s)
            break

# right mouse click turns the square white (dead)     
def sprite_off(x, y):
    for s in all_sprites:
        if s.rect.collidepoint(x, y):
            s.color = WHITE
            s.image.fill(s.color)
            break

# draws a white square grid of size (num_rect X num_rect)
def draw_grid(surface):
    for j in range(num_rect):
        for i in range(num_rect):
            x = border + i * (sq_width + margin)
            y = border + j * (sq_width + margin)
            pygame.draw.rect(surface, WHITE, (x, y, sq_width, sq_width))
            b = block(x, y, sq_width, sq_width, WHITE)
            all_sprites.add(b)


def get_color_at(x, y):
    for s in visible_sprites:
        if s.rect.collidepoint(x, y):
            if s.color == BLUE:
                return BLUE
            else:
                return WHITE

    
def create_grid_array():
    global grid

    grid.clear()
    
    for j in range(num_rect):
        row = []
        for i in range(num_rect):
            
            # coordinates for central pixel in each square in grid
            x = border + i * (sq_width + margin) + (sq_width // 2)
            y = border + j * (sq_width + margin) + (sq_width // 2)
            
            if get_color_at(x,y) == BLUE:
                row.append(1)
            else:
                row.append(0)

        grid.append(row)


# print the grid for debugging purposes
def print_grid():
    global grid
    
    for row in grid:
        print(row)
    print()


# returns the number of active neighbors a cell has based on the square's grid index (x,y)
def get_nbr_count(x, y):
    global grid
    num_nbrs = 0

    for i in range(-1,2):
        for j in range(-1,2):
            if i == 0 and j == 0:   # current point
                continue
            else:
                try:    # ensure it is not off the edge
                    if grid[y+i][x+j] == 1:
                        num_nbrs += 1
                except:
                    continue
                
    return num_nbrs


# returns the sprite's coord based on grid index (x and y are done seperatly)   
def get_sprite_coords(i):
    global sq_width, margin, border
    return border + i * sq_width + (i-1) * margin + sq_width//2
    

def itterate_game_once():
    global grid, num_rect, screen  
    
    # set of coordinates that need to turn on/off based on the rules
    coords_to_update = set()

    # check each point's neighbor count
    for y in range(0, num_rect):        # TODO condense range based on min/max values
        for x in range(0, num_rect):    # TODO condense range based on min/max values

            num_neighbors = get_nbr_count(x,y)
                
            # rules for the game
            # a 'dead' cell turns on if it has 3 active neighbors
            if grid[y][x] == 0:
                if num_neighbors == 3:
                    coords_to_update.add((x,y))

            # a 'live' cell remains on if it has 2/3 active neighbors
            else:
                if num_neighbors != 2 and num_neighbors != 3:
                    coords_to_update.add((x,y))

    # change cells
    for c in coords_to_update:
        x = get_sprite_coords(c[0])
        y = get_sprite_coords(c[1])

        if grid[c[1]][c[0]]   == 1:
            sprite_off(x,y)
            grid[c[1]][c[0]]   = 0
            
        elif grid[c[1]][c[0]] == 0:
            sprite_on(x,y)
            grid[c[1]][c[0]]   = 1

# main loop for drawing 
def main():
    global screen, game_active
    
    # window setup
    pygame.display.set_caption("Conway's Game of Life")

    # "start game" button
    start_game_btn = block(border + num_rect * (sq_width + margin), border, btn_width, btn_height, GREEN)
    all_sprites.add(start_game_btn)
    visible_sprites.add(start_game_btn)
    
    new_y = (start_game_btn.y + start_game_btn.rect.height + 10)
    new_x = (start_game_btn.x + (start_game_btn.rect.width // 2))

    counter = Counter(new_x, new_y)
    count = counter.count
    # main loop
    running = True
    while running:
        
        # DRAWING
        screen.fill(RED)
        draw_grid(screen)

        visible_sprites.draw(screen)
        text = font.render("START", True, BLACK)
        screen.blit(text, [border + num_rect * (sq_width + margin), border + sq_width // 2])

        birth_ctrl = BirthControl(new_x, new_y)
        birth_ctrl.button_set()
        counter.counter(up_button=birth_ctrl.up, count=count)
        # only allow button clicks before
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if mouse[0] > birth_ctrl.up.x and ((mouse[1] > birth_ctrl.up.y) and mouse[1] <  (birth_ctrl.up.y + birth_ctrl.up.height)) and click[0]:
            count = counter.counter(up_button=birth_ctrl.up, count=count,up=True)
        elif mouse[0] > birth_ctrl.up.x and ((mouse[1] > birth_ctrl.down.y) and mouse[1] <  (birth_ctrl.down.y + birth_ctrl.down.height)) and click[0]:
            count = counter.counter(up_button=birth_ctrl.up, count=count,down=True)

        pygame.display.update()
        
        
        if game_active == True:
            itterate_game_once()
        
        # EVENTS
        for event in pygame.event.get():
            
            # left click (turn square on)
            if pygame.mouse.get_pressed()[0]:
                c = pygame.mouse.get_pos()
                sprite_on(c[0], c[1])
                
            # right click (turn square off)
            elif pygame.mouse.get_pressed()[2]:
                c = pygame.mouse.get_pos()
                sprite_off(c[0], c[1])

            # quit/close window pressed
            elif event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break


     

#initialize pygame
pygame.init()

### GLOBAL VARIABLES
SCREEN_SIZE_WIDTH = 800
SCREEN_SIZE_HEIGHT = 600
grid = []
game_active = False

# colors
WHITE   = (255, 255, 255)
BLACK   = (0,0,0)
RED     = (255, 0, 0)
BLUE    = (0, 0, 255)
GREEN   = (0, 255, 0)

# sprite groups
visible_sprites = pygame.sprite.Group()
all_sprites     = pygame.sprite.Group()

# square block information
sq_width    = 10
margin      = 3
border      = 50
num_rect    = 50

# completed drawing button info
btn_width   = 80
btn_height  = 35

# size 36 for text font
font = pygame.font.Font(None, 36)





screen = pygame.display.set_mode((SCREEN_SIZE_WIDTH, SCREEN_SIZE_HEIGHT))

main()




