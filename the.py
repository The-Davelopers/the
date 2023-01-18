import pygame, ctypes, os, pickle


pygame.init()

#*screen setup

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen = pygame.display.set_mode(screensize)

scale = (screensize[0]/1920, screensize[1]/1080)


#*Classes

class player_values():
    def __init__(self, size, position,color=(255, 255, 255), image=None, speed=2):
        #scaling
        self.pos = (position[0] * scale[0], position[1] * scale[1])
        
        size = (size[0] * scale[0], size[1] * scale[1])
        
        self.speed = speed
        
        try:
            surface = pygame.image.load(f"images/{image}")
            self.surface = pygame.transform.scale(surface, size)
        except:
            self.surface = pygame.surface.Surface(size)
            self.surface.fill(color)
              
class entities():
    def __init__(self, size, position, color=(255, 255, 255), images=None, image_size=None):
        #scaling 
        self.counter = 0
        
        size = (size[0] * scale[0], size[1] * scale[1])
        
        self.surfaces = []
        
        
        self.collision_pos = (position[0] * scale[0], position[1] * scale[1])
        
        self.collision = pygame.surface.Surface(size)
        
        self.collision.fill((255, 255, 255))
        
        try:    
            image_size = (image_size[0] * scale[0], image_size[1] * scale[1])
        except:    
            image_size = size
            
        try:
            self.pos = (self.collision_pos[0] + size[0]/2 - image_size[0]/2, self.collision_pos[1] + size[1] - image_size[1])
        except:
            self.pos = self.collision_pos
        try:
            for image in images:
                surface = pygame.image.load(f"images/{image}")
                try:
                    surface = pygame.transform.scale(surface, image_size)
                except:
                    surface = pygame.transform.scale(surface, size)         
            
                self.surfaces.append(surface)
        except:
            surface = pygame.surface.Surface(size)
            surface.fill(color)
            self.surfaces.append(surface)
            
        self.surface = self.surfaces[0]
        
            
        def image_anchoring(entity):
            #setting an anchor point for the image to the collision box
            
            image_position = (self.collision_pos[0] + size[0]/2 - image_size[0]/2, self.collision_pos[1] + size[1] - image_size[1])
            
            return image_position
            
class buttons():
    def __init__(self, image, size, position, hitbox):


        """ size = (size[0] * scale[0], size[1] * scale[1])
        position = (position[0] * scale[0], position[1] * scale[1])
        hitbox = (hitbox[0] * scale[0], hitbox[1] * scale[1]) """

        button = pygame.image.load(image).convert_alpha()
        self.button = pygame.transform.scale(button, size)
        self.pos = position
        self.hit = hitbox
        self.outline = pygame.transform.scale(button,((size[0] + 18), (size[1] + 13)))
        self.outline_pos = ((position[0] - 9), (position[1] - 7))

    def button_click(mouse_pos, button_id, mouse_button_pressed, button_index):
        if mouse_button_pressed[0]:
            click_rect = pygame.Rect(button_id.button.get_rect(center=(button_id.hit)))
            if click_rect.collidepoint(mouse_pos):
                ms = button_index
                return ms

    def button_function(mouse_pos, button_id, mouse_button_pressed, tru):
        if mouse_button_pressed[0]:
            click_rect = pygame.Rect(button_id.button.get_rect(center=(button_id.hit)))
            if click_rect.collidepoint(mouse_pos):
                truu = tru
                return truu


class background_load():
    def __init__(self):
        
        self.size = screensize
        
        try:
            self.main_menu = pygame.image.load("main_menu_background.png")
        except:
            self.main_menu = (0, 128, 0)
            
        try:
            self.main_hub = pygame.image.load("main_hub_background.png")
        except:
            self.main_hub = (0, 128, 0)
            
        try:
            self.level_one = pygame.image.load("level_one_background.png")
        except:
            self.level_one = (0, 128, 0)
        
        try:
            self.level_two = pygame.image.load("level_two_background.png")
        except:
            self.level_two = (0, 128, 0)
            
        try:
            self.level_three = pygame.image.load("level_three_background.png")
        except:
            self.level_three = (0, 128, 0)
        
        try:
            self.level_four = pygame.image.load("level_four_background.png")
        except:
            self.level_four = (0, 128, 0)
            
        try:
            self.level_five = pygame.image.load("level_five_background.png")
        except:
            self.level_five = (0, 128, 0)
          
#*Functions

def button_interact(mouse_pos,buttox):
        click_rect = pygame.Rect(buttox.button.get_rect(center=(buttox.hit)))
        if click_rect.collidepoint(mouse_pos):
            screen.blit(buttox.outline, buttox.outline_pos)            

def player_movement(direction, player_entity, level_entities):
    
    x_change = 0
    y_change = 0
    
    x, y = player_entity.pos

    if "left" in direction:
        x_change = -1
        
    if "right" in direction:
        x_change = 1
    
    if "up" in direction:
        y_change = -1
    
    if "down" in direction:
        y_change = 1
            
    x += 2*x_change 
    y += 2*y_change
    
    player_entity.pos = (x, y)
    print(player_entity.pos)
    
    return player_entity, level_entities    
    

def file_saving():
    pass

def animation(entity):
    
    #surfaces = os.listdir(f"images/{path}")
    
    for i, frame in enumerate(entity.surfaces):
                
        if entity.counter > (i)*10:
            entity.surface = frame
            print(entity.surface)
        if entity.counter > len(entity.surfaces)*10:
            entity.counter = 0
    
    return entity


#*Main variables

active_location = "main menu"

backgrounds = background_load()

background = backgrounds.main_hub

save_data = {
    "level one complete" : False,
    "level two complete" : False,
    "level three complete" : False,
    "level four complete" : False,
    "level five complete" : False,
}

level_entities = []

the_player = player_values((50, 100), (300, 300), image="amogus_idle_1.png")

running = True

#main menu

button_play = buttons("images/button_play.png", (360, 120), (780, 450), (960, 510))
button_options = buttons("images/button_options.png", (360, 120), (780, 600), (960, 660))
button_quit = buttons("images/button_quit.png", (360, 120), (780, 750), (960, 810))

save_1_button = buttons("images/save_1.png", (360, 120), (780, 250), (960, 310))
save_2_button = buttons("images/save_2.png", (360, 120), (780, 400), (960, 460))
save_3_button = buttons("images/save_3.png", (360, 120), (780, 550), (960, 610))
save_4_button = buttons("images/save_4.png", (360, 120), (780, 700), (960, 760))

back_button = buttons("images/back_button.png", (150, 150), (200, 120), (275, 195))

menu_screen = 1
""" text_in_options = "Lol No Options For you"
game_version = "0.0.0"
font = pygame.font.Font("fonts/minkraft.ttf", 22)
text_color = (255, 255, 255)
text_game_version = font.render(f"{game_version}", True, text_color)
text_options = font.render(f"{text_in_options}", True, text_color) """

#main hub

#level one


box_level_one = entities((200, 200), (1400, 300), images=os.listdir("images/amogus/"))

track_level_one = entities((0, 0), (1550, 900), images=["track_one.png"], image_size=(100, 600))

tree_level_one = entities((150, 50), (300, 600), images=["tree_level_one.png"], image_size=(400, 600))

bush_level_one = entities((175, 125), (400, 750), images=["bush_level_one.png"], image_size=(175, 175))

exit_level_one = entities((960, 0), (25, 10))

level_entities = []

#*Main Loop

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
    try:
        screen.fill(background)
    except:
        screen.blit(background, (0, 0))
        

    if active_location == "main menu":
        background = backgrounds.main_menu

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if menu_screen == 1:

            button_list = [button_play, button_options, button_quit]
            
        elif menu_screen == 2:

            button_list = [save_1_button, save_2_button, save_3_button, save_4_button, back_button]


        elif menu_screen == 3:

            button_list = [back_button]

        for event in pygame.event.get():

            mouse_button_pressed = pygame.mouse.get_pressed()       

            if menu_screen == 1:

                if buttons.button_function((mouse_x, mouse_y), button_play, mouse_button_pressed, True):

                    menu_screen = buttons.button_click((mouse_x, mouse_y), button_play, mouse_button_pressed, 2)

                elif buttons.button_function((mouse_x, mouse_y), button_options, mouse_button_pressed, True):

                    menu_screen = buttons.button_click((mouse_x, mouse_y), button_options, mouse_button_pressed, 3)

                elif buttons.button_function((mouse_x, mouse_y), button_quit, mouse_button_pressed, True):
                    pygame.quit()
                
            elif menu_screen == 2:

                if buttons.button_function((mouse_x, mouse_y), back_button, mouse_button_pressed, True):
                    menu_screen = buttons.button_click((mouse_x, mouse_y), back_button, mouse_button_pressed, 1)

            elif menu_screen == 3:

                if buttons.button_function((mouse_x, mouse_y), back_button, mouse_button_pressed, True):
                    menu_screen = buttons.button_click((mouse_x, mouse_y), back_button, mouse_button_pressed, 1)

        for button in button_list:
            screen.blit(button.button, button.pos)
            button_interact((mouse_x, mouse_y), button)
    
    if active_location == "main hub":
        background = backgrounds.main_hub

        level_entities = [track_level_one, bush_level_one, tree_level_one, box_level_one]         
            
    if active_location == "level one":
        background = backgrounds.level_one
    
        if "player completes level":
            save_data["level one complete"] = True
    
    if active_location == "level two":
        background = backgrounds.level_two
        
        if "player completes level":
            save_data["level two complete"] = True
            
    if active_location == "level three":
        background = backgrounds.level_three
    
        if "player completes level":
            save_data["level three complete"] = True
    
    if active_location == "level four":
        background = backgrounds.level_four
    
        if "player completes level":
            save_data["level four complete"] = True
    
    if active_location == "level five":
        background = backgrounds.level_five
    
        if "player completes level":
            save_data["level five complete"] = True
    

    for entity in level_entities:
        animation(entity)
        screen.blit(entity.surface, entity.pos)
    
    keys = pygame.key.get_pressed()
        
        
    if keys[pygame.K_a]:
        the_player, level_entities = player_movement("left", the_player, level_entities)
    
    if keys[pygame.K_d]:
        the_player, level_entities = player_movement("right", the_player, level_entities)    

    if keys[pygame.K_w]:
        the_player, level_entities = player_movement("up", the_player, level_entities)    
    
    if keys[pygame.K_s]:
        the_player, level_entities = player_movement("down", the_player, level_entities)    
        

    if keys[pygame.K_b]:
        for box in level_entities:
            screen.blit(box.collision, box.collision_pos)
    
    pygame.display.update()