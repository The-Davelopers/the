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