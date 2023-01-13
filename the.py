import pygame, ctypes, os

#i'm tired
#savetheenviroment
pygame.init()

#*screen setup

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen = pygame.display.set_mode(screensize)

scale = (screensize[0]/1920, screensize[1]/1080)


print(scale)

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
    def __init__(self, size, position, color=(255, 255, 255), image=None):
        #scaling 
        size = (size[0] * scale[0], size[1] * scale[1])
        
        self.pos = (position[0] * scale[0], position[1] * scale[1])
        
        try:
            self.surface = pygame.image.load(image)
            self.surface = pygame.transform.scale(size)
        except:
            self.surface = pygame.surface.Surface(size)
            self.surface.fill(color)
            
class background_load():
    def __init__(self) -> None:
        
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
        
#*Functions

def player_movement(direction, player_entity, level_entities):
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

level_objects = []

the_player = player_values((50, 50), (300, 300))

#main hub

#level one

box_level_one = entities((100, 100), (400, 400))

animation_counter = 0

running = True


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
    
    for image in level_objects:
        screen.blit(image.surface, image.pos)
    
    
    pygame.display.update()