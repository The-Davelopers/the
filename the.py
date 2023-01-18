import pygame, ctypes, os


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
            self.surface = pygame.image.load(image)
            self.surface = pygame.transform.scale(size)
        except:
            self.surface = pygame.surface.Surface(size)
            self.surface.fill(color)
            
              
class entities():
    def __init__(self, size, position, color=(255, 255, 255), image=None, image_size=None):
        #scaling 
        size = (size[0] * scale[0], size[1] * scale[1])
        
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
            surface = pygame.image.load(f"images/{image}")
            
            try:
                self.surface = pygame.transform.scale(surface, image_size)
            except:
                self.surface = pygame.transform.scale(surface, size) 
                print("ok")               
            
        except:
            self.surface = pygame.surface.Surface(size)
            self.surface.fill(color)
        
            
        def image_anchoring(entity):
            #setting an anchor point for the image to the collision box
            
            image_position = entity.position[1] - entity.image_size[1] + entity.size[1]
            
            return image_position
            
class buttons():
    def __init__(self, image, size, position, hitbox):

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

def button_interact(mouse_pos,buttox):
        click_rect = pygame.Rect(buttox.button.get_rect(center=(buttox.hit)))
        if click_rect.collidepoint(mouse_pos):
            screen.blit(buttox.outline, buttox.outline_pos)                   
        
           
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

def player_movement(direction, player_entity, level_entities, scale, keys):
    pass

def animation(surfaces):
    
    for i, frame in enumerate(surfaces):
                
        if animation_counter > (i)*10:
            level_objects = [frame]
            print(frame)
            
        if animation_counter > len(surfaces)*10:
            animation_counter = 0


#*Main variables

active_location = "main hub"

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

the_player = player_values((50, 50), (300, 300))

running = True

#main menu

button_play = buttons(r"images\button_play.png", (360, 120), (780, 450), (960, 510))
button_options = buttons(r"images\button_options.png", (360, 120), (780, 600), (960, 660))
button_quit = buttons(r"images\button_quit.png", (360, 120), (780, 750), (960, 810))

pressed_button_play = buttons(r"images\pressed_button_play.png", (360, 120), (780, 450), (960, 510))

save_1_button = buttons(r"images\save_1.png", (360, 120), (780, 250), (960, 310))
save_2_button = buttons(r"images\save_2.png", (360, 120), (780, 400), (960, 460))
save_3_button = buttons(r"images\save_3.png", (360, 120), (780, 550), (960, 610))
save_4_button = buttons(r"images\save_4.png", (360, 120), (780, 700), (960, 760))

back_button = buttons(r"images\back_button.png", (150, 150), (200, 120), (275, 195))

text_in_options = "Lol No Options For you"
game_version = "0.0.0"
font = pygame.font.Font(r"fonts\minkraft.ttf", 22)
text_color = (255, 255, 255)
text_game_version = font.render(f"{game_version}", True, text_color)
text_options = font.render(f"{text_in_options}", True, text_color)

bgi = pygame.image.load(r"images\undah_da_sea.jpg").convert_alpha()
icon = pygame.image.load(r"images\icon.png").convert_alpha()

icon = pygame.transform.scale(icon, (970, 500))


#main hub

#level one

box_level_one = entities((200, 200), (1400, 300))

track_level_one = entities((0, 0), (1550, 900), image="track_one.png", image_size=(100, 600))

tree_level_one = entities((150, 50), (300, 600), image="tree_level_one.png", image_size=(400, 600))

bush_level_one = entities((175, 125), (400, 750), image="bush_level_one.png", image_size=(175, 175))

exit_level_one = entities((960, 0), (25, 10))

level_entities = [bush_level_one, tree_level_one, track_level_one]

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
    
    if active_location == "main hub":
        background = backgrounds.main_hub            
            
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
        screen.blit(entity.surface, entity.pos)
    
    

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_b]:
        for box in level_entities:
            screen.blit(box.collision, box.collision_pos)
    
    pygame.display.update()