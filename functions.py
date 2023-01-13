import pygame, ctypes, json, os


pygame.init()

pygame.joystick.init()

active_save_file = "save_file_1"
def setup():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    screen = pygame.display.set_mode(screensize)
    
    return screen

screen = setup()



walking_right = os.listdir(r"C:\Users\Teo.ingerman\Desktop\VSCode\experiments\The\images\player\walking_right")
os.chdir(r"C:\Users\Teo.ingerman\Desktop\VSCode\experiments\The\images\player\walking_right")




class player():
    """position should be a tuple
    
    images should be a list of images
    """
    def __init__(self, pos, images, scale=(200, 200)):
        self.position = pos
        self.iterable = 0
        self.surfaces = []
        
        for x in images:
            image = pygame.transform.scale(pygame.image.load(x), scale)
            self.surfaces.append(image)
            
        self.active_surface = self.surfaces[0]
        self.size = scale

    def animate(player_character):
    
        for i, image in enumerate(player_character.surfaces):
            
            if player_character.iterable > len(player_character.surfaces)*5:
                player_character.iterable = 0
                
            if player_character.iterable > i*5:
                player_character.active_surface = image
                
        player_character.iterable += 1
        
        return player_character

player_1 = player((500, 700), walking_right)

#player_2 = player_creator((500, 700), "player.png")

#player_3 = player_creator((500, 700), "lemoncult_one.png")

level_objects = []

class entity():
    def __init__(self, image, size, position, properties=None):
        
        surface = pygame.image.load(image).convert()
        self.surface = pygame.transform.scale(surface, size)
        self.mask = pygame.mask.from_surface(self.surface)
        self.size = size
        self.position = position
        self.mode = properties
os.chdir("..\..")
print(os.listdir())
os.chdir("level_objects")
big_box = entity("daver.png", (200, 200), (400, 500), properties="heavy")
class sentity():
    #TODO: lägg till image, image_size
    def __init__(self, collision_size, position):
        self.surface = pygame.surface.Surface(collision_size)
        self.position = position
        


#big_box = sentity((400, 400), (500, 500))

level_objects.append(big_box)




          
def player_movement(the_player, level_objects, direction=None):
    
    
    """direction is to where the character is moving (left, right, up, down)
    """
    x_change = 0
    y_change = 0
    
    if direction == "left":
        x_change = -1
    elif direction == "right":
        x_change = 1    
    elif direction == "up":
        y_change = -1
    elif direction == "down":
        y_change = 1  
        


    x, y = the_player.position


    if x_change == -1:
        the_player.active_surface = the_player.surfaces[0]
    elif x_change == 1:
        the_player.animate()
    elif y_change == -1:
        the_player.active_surface = the_player.surfaces[2]
    elif y_change == 1:
        the_player.active_surface = the_player.surfaces[3]      



    for entities in level_objects:
        
        heavy = False
        size = entities.surface.get_size()
        x_pos, y_pos = entities.position
        
        player_size = the_player.active_surface.get_size()
        
        right_edge = x + player_size[0]
        down_edge = y + player_size[1]
        

        
        #if entities.mode == "heavy":
        heavy = True

        
        
        #*left
        if x <= x_pos + size[0] + 2 and x_change == -1:
            
            if x >= x_pos + size[0] - 2:
                
                if y <= y_pos + size[1] + 2:
                    
                    if down_edge >= y_pos - 2:
                        
                        x_change = 0
                        if heavy:
                            x_pos -= 0.5
                            x_change -= 0.25
                            x = x_pos + size[0]
                            y = y_pos + size[1]/2 - player_size[1]/2
                            
                    
                    
        #*right
        if right_edge >= x_pos - 2 and x_change == 1:
            
            if right_edge <= x_pos + 2:
            
                if y <= y_pos + size[1] + 2:
                    
                    if down_edge >= y_pos - 2:
                        x_change = 0
                        if heavy:
                            x_pos += 0.5
                            x_change += 0.25
                            x = x_pos - player_size[0]
                            y = y_pos + size[1]/2 - player_size[1]/2
                            
        #*up    
        if y <= y_pos + size[1] + 2 and y_change == -1:
            
            if y >= y_pos + size[1] - 2:
                
                if x <= x_pos + size[0] + 2:
                    
                    if right_edge >= x_pos - 2:
                        y_change = 0
                        if heavy:
                            y_pos -= 0.5
                            y_change -= 0.25
                            y = y_pos + size[1]
                            x = x_pos + size[0]/2 - player_size[0]/2   
                             
        #*down
        if down_edge >= y_pos - 2 and y_change == 1:
            
            if down_edge <= y_pos + 2:
            
                if x <= x_pos + size[0] + 2:
                    
                    if right_edge >= x_pos - 2:
                        y_change = 0
                        if heavy:
                            y_pos += 0.5
                            y_change += 0.25
                            y = y_pos - player_size[1]
                            x = x_pos + size[0]/2 - player_size[0]/2   
                             
        entities.position = (x_pos, y_pos)                

    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    
    size = the_player.active_surface.get_size()
    
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
    
    x += 2*x_change
    y += 2*y_change
    
    the_player.position = (x, y)
    
    return the_player, level_objects

def save(save_file, data_dictionary=None, save_point=None, save_mode="s"):
    
    """
    (your active save file, your dictionary with save information, instance you want to save, save mode)
    
    
    save_mode = "s" --> save given save_point
    
    save_mode = "l" --> load dictionary from json file
    
    save_mode = "r" --> reset save_file
    """
    
    if save_mode == "s":
        area, point = save_point.split()
        data_dictionary[area][point] = True
        with open(f"{save_file}.json", "w") as file:
            json.dump(data_dictionary, file)
                    
        
    elif save_mode == "l":
        with open(f"{save_file}.json") as file:
            data_dictionary = json.loads(file.read())
    
    elif save_mode == "r":
        data_dictionary = {
            "level_1": {
                
                "box_moved": False,
                
                "cheese_collected": False,
                
                },
            
            "level_2": False,
            
            "level_3": False,
            
            "level_4": False,
            
            "level_5": False,
        }
        with open(f"{save_file}.json", "w") as file:
            json.dump(data_dictionary, file)
    return data_dictionary
       
try:
    data = save(active_save_file, save_mode="l")
except:
    data = save(active_save_file, save_mode="r")

running = True
keys = pygame.key.get_pressed()

#print(keys)
#print(pygame.K_w)


    
print(keys)
while running:
    screen.fill((0, 128, 0))
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        player_1, level_objects = player_movement(player_1, level_objects,  direction="up")
              
    if keys[pygame.K_a]:
        player_1, level_objects = player_movement(player_1, level_objects,  direction="left")
        
    if keys[pygame.K_s]:
        player_1, level_objects = player_movement(player_1, level_objects,  direction="down")
        
    if keys[pygame.K_d]:
        player_1, level_objects = player_movement(player_1, level_objects,  direction="right")


    
    """ if keys[pygame.K_UP]:
        player_2.position, level_objects = player_movement(player_2, level_objects,  y_change=-1)
        
    if keys[pygame.K_LEFT]:
        player_2.position, level_objects = player_movement(player_2, level_objects,  x_change=-1)
        
    if keys[pygame.K_DOWN]:
        player_2.position, level_objects = player_movement(player_2, level_objects,  y_change=1)
        
    if keys[pygame.K_RIGHT]:
        player_2.position, level_objects = player_movement(player_2, level_objects,  x_change=1)
        
    if keys[pygame.K_i]:
        player_3.position, level_objects = player_movement(player_3, level_objects, y_change=-1)
        
    if keys[pygame.K_j]:
        player_3.position, level_objects = player_movement(player_3, level_objects, x_change=-1)
        
    if keys[pygame.K_k]:
        player_3.position, level_objects = player_movement(player_3, level_objects, y_change=1)
        
    if keys[pygame.K_l]:
        player_3.position, level_objects = player_movement(player_3, level_objects, x_change=1) """
    
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
                running = False
        
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RETURN:
                save(active_save_file, data, "level_1 cheese_collected", "s")
                    
            if event.key == pygame.K_LSHIFT:
                save(active_save_file, data, "level_1 box_moved", "s")

    
    screen.blit(player_1.active_surface, player_1.position)
    
    #screen.blit(player_2.surface, player_2.position)
    
    #screen.blit(player_3.surface, player_3.position)
    
    for entities in level_objects:
        screen.blit(entities.surface, entities.position)
        
    pygame.display.update()