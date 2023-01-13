import pygame, ctypes, random


pygame.init()

pygame.mixer.init()

def setup():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    screen = pygame.display.set_mode(screensize)
    
    return screen, screensize



screen, screensize = setup()

print(screensize)

location = "main menu"

running = True
grass = pygame.image.load("grass.jpg").convert()
grass = pygame.transform.scale(grass, screensize)

win_screen = pygame.image.load("win_screen.jpg").convert()
win_screen = pygame.transform.scale(win_screen, screensize)

main_menu_background = pygame.image.load("main_menu_background.jpg").convert()
main_menu_background = pygame.transform.scale(main_menu_background, screensize)


class player():
    def __init__(self, size, position, color=(128, 128, 128), image=None):
        self.size = size
        
        if image == None:
            self.surface = pygame.surface.Surface(size)
            self.surface.fill(color)
        
        else:
            surface = pygame.image.load(image).convert()
            self.surface = pygame.transform.scale(surface, size)
            
        self.position = position

class entities():
    def __init__(self, size, position, color=(128, 128, 128), image=None, properties=None):
        
        self.size = size
        
        if image == None:
            self.surface = pygame.surface.Surface(size)
            self.surface.fill(color)
        
        else:
            surface = pygame.image.load(image).convert_alpha()
            self.surface = pygame.transform.scale(surface, size)
        
        self.position = position
        
        self.properties = properties



the_player = player((100, 125), (500.5, 500), color=(128, 0, 0), image="the_player.jpg")

box_one = entities((200, 200), (1400, 300), image="box_one.jpg", properties=["pushable", "down"])

track_one = entities((100, 600), (1450, 300), color=(205, 127, 50), properties="background", image="track_one.jpg")

door_one = entities((50, 20), (935, 0), color=(255, 255, 255), properties=["transport", "main hub"])

door_hub = entities((20, 50), (1900, 515), color=(255, 255, 255), properties=["transport", "level one"])

start_button = entities((300, 125), (810, 350), color=(0, 255, 0), image="start_button.png")



level_objects = []

background_color = (0, 0, 0)

button_covered = False

first_pressed = True

has_won = False

def player_movement(player_entity, other_entities, keys, location, button_covered, first_pressed):
    
    
    x_change = 0
    
    y_change = 0
    
    if keys[pygame.K_w]:
        y_change -= 1
              
    if keys[pygame.K_a]:
        x_change -= 1
        
    if keys[pygame.K_s]:
        y_change += 1
        
    if keys[pygame.K_d]:
        x_change += 1
    
    player_size = player_entity.surface.get_size()
    
    x, y = player_entity.position    
    
    right_edge = x + player_size[0]
    down_edge = y + player_size[1]
    
    
    
    for entity in other_entities:
        non_interactable = False
        pushable = False
        direction = None
        if "background" != entity.properties: 
            
            if entity.properties != None:
                
                for z in entity.properties:
                    
                    size = entity.size
            
                    x_pos, y_pos = entity.position
                    if z == "transport":
                        non_interactable = True
                        if entity.surface.get_rect(x=x_pos,y=y_pos).colliderect(player_entity.surface.get_rect(x=x,y=y)):
                            button_covered = False
                            for z in entity.properties:
                                
                                if z == "main menu":
                                    
                                    location = "main menu"
                                    
                                if z == "main hub":
                                    
                                    location = "main hub"
                                    
                                if z == "level one":
                                    
                                    location = "level one"
                    
                    elif z == "pushable":
                        pushable = True
                        
                    elif z == "left":
                        direction = "left"
                        
                    elif z == "right":
                        direction = "right"
                        
                    elif z == "up":
                        direction = "up"
                        
                    elif z == "down":
                        direction = "down"
            
            
            
            
            if not non_interactable:
                #*left
                if x <= x_pos + size[0] + 2 and x_change == -1:
                    
                    if x >= x_pos + size[0] - 2:
                        
                        if y <= y_pos + size[1] + 2:
                            
                            if down_edge >= y_pos - 2:
                                
                                if pushable and direction == "left":
                                    x_pos -= 0.5
                                    x_change -= 0.25
                                else:
                                    x_change = 0
                                    
                #*right
                if right_edge >= x_pos - 2 and x_change == 1:

                    if right_edge <= x_pos + 2:

                        if y <= y_pos + size[1] + 2:
                            
                            if down_edge >= y_pos - 2:
                                
                                if pushable and direction == "right":
                                    x_pos += 0.5
                                    x_change += 0.25
                                else:
                                    x_change = 0
                                                
                #*up    
                if y <= y_pos + size[1] + 2 and y_change == -1:

                    if y >= y_pos + size[1] - 2:
                        
                        if x <= x_pos + size[0] + 2:
                            
                            if right_edge >= x_pos - 2:
                                
                                if pushable and direction == "up":
                                    y_pos -= 0.5
                                    y_change -= 0.25
                                else:
                                    y_change = 0
                                            
                #*down
                if down_edge >= y_pos - 2 and y_change == 1:
                    
                    if down_edge <= y_pos + 2:
                        
                        if x <= x_pos + size[0] + 2:
                            
                            if right_edge >= x_pos - 2:
                                
                                
                                if pushable == True and direction == "down":
                                    if y_pos >= 900 - size[1]:
                                        y_change = 0
                                        button_covered = True
                                        first_pressed = False
                                    else:
                                        
                                        y_pos += 0.5
                                        y_change = 0.25
                                        #y = y_pos - player_size[1]
                                        #x = x_pos + size[0]/2 - player_size[0]/2   
                                else:
                                    y_change = 0
                                            
                entity.position = (x_pos, y_pos)
                           
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    size = player_entity.surface.get_size()
    
    right_edge = x + size[0]
    down_edge = y + size[1]
    
    if x <= 2 and x_change == -1:
        x_change = 0
        
    if right_edge >= screensize[0] - 2 and x_change == 1:
        x_change = 0
        
    if y <= 2 and y_change == -1:
        y_change = 0
        
    if down_edge >= screensize[1] - 2 and y_change == 1:
        y_change = 0
    x += 2 * x_change
    y += 2 * y_change
    
    player_entity.position = (x, y)
    
    return player_entity, other_entities, location, button_covered, first_pressed

    
player_active = False

pygame.mixer.music.load("the.mp3")

pygame.mixer.music.play(loops=-1)

pygame.mixer.music.set_volume(0.5)

while running:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False    
    try:
        screen.fill(background_color)
    except:
        screen.blit(background_color, (0, 0))
        
    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    mouse_button_pressed = pygame.mouse.get_pressed()
        
    if location == "main menu":
        background_color = main_menu_background
        player_active = False
        level_objects = [start_button]
        
        click_rect = pygame.Rect(start_button.surface.get_rect(x=810, y=350))
        if click_rect.collidepoint((mouse_x, mouse_y)):
            start_button = entities((360, 150), (780, 338), color=(0, 255, 0), image="start_button.png")
            if mouse_button_pressed[0]:
                location = "main hub"
                
        else:
            start_button = entities((300, 125), (810, 350), color=(0, 255, 0), image="start_button.png")
            
        for event in pygame.event.get():
        
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_RETURN:
                    location = "main hub"
                
    if location == "main hub":
        
        if not first_pressed or has_won:
            background_color = win_screen
            has_won = True
        else:
            background_color = grass
        level_objects = [door_hub]
        player_active = True

        box_one = entities((200, 200), (1400, 300), image="box_one.jpg", properties=["pushable", "down"])

        track_one = entities((100, 600), (1450, 300), color=(205, 127, 50), properties="background", image="track_one.jpg")

        door_one = entities((50, 20), (935, 0), color=(255, 255, 255), properties=["transport", "main hub"])
    
        the_player, level_objects, location, button_covered, first_pressed = player_movement(the_player, level_objects, keys, location, button_covered, first_pressed)
        #print(button_covered)
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_7:
                    location = "level one"
                                  
        
    if location == "level one":
        
  
        background_color = (0, 0, 128)
        player_active = True
        
        level_objects = [track_one, box_one]
        
        if button_covered:
            level_objects = [track_one, box_one, door_one]
            button_covered = True

        
        the_player, level_objects, location, button_covered, first_pressed = player_movement(the_player, level_objects, keys, location, button_covered, first_pressed)
    
    for entity in level_objects:
        screen.blit(entity.surface, entity.position)
        
    if player_active:
        screen.blit(the_player.surface, the_player.position)
                
    
    pygame.display.update()