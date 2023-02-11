import pygame, ctypes, os, random

try:
    import moviepy.editor
except:
    os.system("pip install moviepy")
    import moviepy.editor

pygame.init()
pygame.mixer.init()


#*screen setup

ctypes.windll.user32.SetProcessDPIAware()
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen = pygame.display.set_mode(screensize)

scale = (screensize[0]/1920, screensize[1]/1080)


#*Classes

class player_values():
    def __init__(self, size, position,color=(255, 255, 255), image=None, speed=4):
        #scaling
        
        self.counter = 0
        
        self.name = "player"
        
        self.pos = (position[0], position[1])
        
        self.movable = [False]
        
        self.size = size
        self.speed = speed
        
        self.direction = "left"
        
        self.left = [pygame.transform.scale(pygame.image.load(f"images/player/player_walk_left/{image}").convert_alpha(), size) for image in os.listdir("images/player/player_walk_left")]
        
        self.right = [pygame.transform.scale(pygame.image.load(f"images/player/player_walk_right/{image}").convert_alpha(), size) for image in os.listdir("images/player/player_walk_right")]
        
        self.up = [pygame.transform.scale(pygame.image.load(f"images/player/player_walk_up/{image}").convert_alpha(), size) for image in os.listdir("images/player/player_walk_up")]
        
        self.down = [pygame.transform.scale(pygame.image.load(f"images/player/player_walk_down/{image}").convert_alpha(), size) for image in os.listdir("images/player/player_walk_down")]
        

        self.surface = self.left[0]
        
    def animate(self):
        
        if self.direction == "left":
            images = self.left
        elif self.direction == "right":
            images = self.right
        elif self.direction == "up":
            images = self.up
        elif self.direction == "down":
            images = self.down
        
        for i, image in enumerate(images):
            if self.counter > i*60:
                self.surface = image
            if self.counter > len(images)*60:
                self.counter = 0
        self.counter += self.speed
        return self.surface, self.counter

    def idle(self):
        if self.direction == "left":
            images = self.left[0]
        elif self.direction == "right":
            images = self.right[0]
        elif self.direction == "up":
            images = self.up[0]
        elif self.direction == "down":
            images = self.down[0]
        
        self.surface = images
        return self.surface
           
class entities():
    def __init__(self, size, position, color=(255, 255, 255), images=None, image_size=None, fill=True, name="entity", movable=[False]):
        #scaling 
  
        size = (size[0], size[1])
        
        self.movable = movable 
        
        self.name = name
        
        self.surfaces = []
      
        self.size = size
        
        self.collision_pos = position
        
        self.collision = pygame.surface.Surface(size)
        
        self.collision.fill((255, 255, 255))
        
        try:    
            image_size = (image_size[0], image_size[1])
        except:    
            image_size = size
        self.image_size = image_size    
        try:
            self.pos = (self.collision_pos[0] + size[0]/2 - image_size[0]/2, self.collision_pos[1] + size[1] - image_size[1])
        except:
            self.pos = self.collision_pos
        try:
            for image in images:
                surface = pygame.image.load(f"images/{image}").convert_alpha()
                try:
                    surface = pygame.transform.scale(surface, image_size)
                except:
                    surface = pygame.transform.scale(surface, size)         
            
                self.surfaces.append(surface)
        except:
            surface = pygame.surface.Surface(size)
            if fill:
                surface.fill(color)
            else:
                surface = surface.convert_alpha()
                surface.fill((0, 0, 0, 0))
            self.surfaces.append(surface)
            
        self.surface = self.surfaces[0]
        
            
    def image_anchoring(entity):
        #setting an anchor point for the image to the collision box
        
        image_position = (entity.collision_pos[0] + entity.size[0]/2 - entity.image_size[0]/2, entity.collision_pos[1] + entity.size[1] - entity.image_size[1])
        
        return image_position
            
class buttons():
    def __init__(self, image, size, position, hitbox):
        
        size = (size[0], size[1])
        position = (position[0], position[1])
        hitbox = (hitbox[0], hitbox[1])
        self.name = image
        button = pygame.image.load(f"images/{image}").convert_alpha()
        self.button = pygame.transform.scale(button, size)

        self.pos = position
        self.hit = hitbox
        self.outline = self.button
        self.outline_pos = position
        self.outline = pygame.transform.scale(button,((size[0] + 18), (size[1] + 13)))
        self.outline_size = (size[0] + 18), (size[1] + 13)
        self.outline_pos = ((position[0] - 9*scale[0]), (position[1] - 7*scale[1]))

    def button_click(mouse_pos, button_id, mouse_button_pressed, button_index):
        if mouse_button_pressed[0]:

            click_rect = pygame.rect.Rect((button_id.pos), (button_id.outline_size))
            if click_rect.collidepoint(mouse_pos):
                ms = button_index
                return ms

    def button_function(mouse_pos, button_id, mouse_button_pressed):
        click_rect = pygame.rect.Rect((button_id.pos), (button_id.outline_size))

        if mouse_button_pressed[0]:

            click_rect = pygame.rect.Rect((button_id.pos), (button_id.outline_size))

            if click_rect.collidepoint(mouse_pos):

                return True
            
class animator(pygame.sprite.Sprite):
    def __init__(self, images, pos_x, pos_y):
        super().__init__()
        self.x = pos_x
        self.y = pos_y

        self.image_group = images
        self.current_image = 0
        self.image = self.image_group[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
    
        self.speed = 0
        self.animation_started = False

    def start_animation(self, speed):
        self.animation_started = True
        self.speed = speed
        
    def animate(self):
        if self.animation_started:
            self.current_image += self.speed   
        
        if self.current_image >= len(self.image_group):
                self.current_image = 0
                self.animation_started = False
    
        self.image = self.image_group[int(self.current_image)]
        self.rect.topright = [self.x, self.y]

    def update(self, speed):
        self.speed = speed
        self.current_image += self.speed   
        
        if self.current_image >= len(self.image_group):
                self.current_image = 0
    
        self.image = self.image_group[int(self.current_image)]
        self.rect.topright = [self.x, self.y]

class background_load():
    def __init__(self):
        
        self.size = screensize
        
        try:
            main_menu = pygame.image.load("images/main_menu_background.png").convert()
            self.main_menu = pygame.transform.scale(main_menu, (screensize))
        except:
            self.main_menu = (0, 128, 0)
            
        try:
            main_hub = pygame.image.load("images/main_hub_background.png").convert()
            self.main_hub = pygame.transform.scale(main_hub, (screensize))

        except:
            self.main_hub = (0, 128, 0)
            
        try:
            level_one = pygame.image.load("images/level_one_background.png").convert()
            self.level_one = pygame.transform.scale(level_one, (screensize))
        except:
            self.level_one = (255, 255, 255)
        
        try:
            level_two = pygame.image.load("images/level_two_background.png").convert()
            self.level_two = pygame.transform.scale(level_two, (screensize))
        except:
            self.level_two = (0, 128, 0)
            
        try:
            level_three = pygame.image.load("images/level_three_background.png").convert()
            self.level_three = pygame.transform.scale(level_three, (screensize))
        except:
            self.level_three = (0, 128, 0)
        
        try:
            level_four = pygame.image.load("images/level_four_background.png").convert()
            self.level_four = pygame.transform.scale(level_four, (screensize))
        except:
            self.level_four = (0, 128, 0)
            
        try:
            level_five = pygame.image.load("images/level_five_background.png").convert()
            self.level_five = pygame.transform.scale(level_five, (screensize))
        except:
            self.level_five = (0, 128, 0)
        
        try:
            win_screen = pygame.image.load("images/win_screen.png").convert()
            self.win_screen = pygame.transform.scale(win_screen, (screensize))
        except:
            self.win_screen = (0, 128, 0)

class text_class():
    def __init__(self):
        self.iterable = 0
        self.iterable_2 = 0
        self.iterable_3 = 0
        self.temporary_string = ""
        self.temporary_string_2 = ""
        self.temporary_string_3 = ""
        self.done = False
        self.string_to_print = ""
        self.string_to_print_2 = ""
        self.string_to_print_3 = ""
        self.color = (255, 255, 255)
        self.line_done = False
        self.line_done_2 = False
        self.line_3 = 0
        self.line_2 = 0
        self.first = 0
        self.whos_talking_name = ""
        with open("textfile.txt") as file:
            self.lines = file.read().splitlines()
        self.box_img = pygame.image.load("images/text_box.png")
        self.box_x = 500
        self.box_y = 850
        self.font = pygame.font.Font(r"fonts\minkraft.ttf", 30)
        self.x = self.box_x + 25
        self.y = self.box_y + 50
        self.y_2 = self.y + 30
        self.y_3 = self.y_2 + 30
        self.whos_talking_x = self.box_x + 32
        self.whos_talking_y = self.box_y + 10
        self.whos_talking_color = (136, 136, 136)
        self.enter_img = pygame.image.load("images/enter.png")
        self.enter = pygame.transform.scale(self.enter_img, (136.75, 29))
        self.enter_x = self.box_x + 700
        self.enter_y = self.box_y + 125

class continuos_animation():
    def __init__(self, folder, speed, position, size) -> None:
        images = os.listdir(f"images/{folder}")

            
        for i, image in enumerate(images):
            images[i] = pygame.transform.scale(pygame.image.load(f"images/{folder}/{image}").convert_alpha(), size)
            
        self.name = "player"
        self.speed = speed
        self.images = images
        self.counter = 0
        self.surface = images[0]
        self.pos = position
        
    def animate(self):
        for i, image in enumerate(self.images):
            if self.counter > i*60:
                self.surface = image
            if self.counter > len(self.images)*60:
                self.counter = 0
        self.counter += self.speed
        return self.surface, self.counter

class one_image_animation():    
    def __init__(self, folder, size, position):
        lista = os.listdir(folder)
        self.images = []
        for image in lista:
            self.images.append(pygame.transform.scale((pygame.image.load(f"{folder}/{image}").convert_alpha()), size))
        
        self.surface = self.images[0]
        self.pos = position
        self.name = "teleport"
        
    def change_image(self):
        self.surface = self.images[1]
        return self.surface

class button_prompt():
    def __init__(self, size, position) -> None:
        
        self.size = size
        
        self.pos = position
        

        
    def show_prompt(self, player):
        entity_hitbox = pygame.rect.Rect(self.pos, self.size)

        player_hitbox = pygame.rect.Rect(player.pos, player.size)
        
        return entity_hitbox.colliderect(player_hitbox)


#*Functions

text = text_class()

def fade_in_out(surface, background, level_entities, fade_type="in out"):
    if fade_type == "out" or fade_type == "in out":
        for i in range(255):
            
            
            fade = pygame.Surface(screensize)  
            fade.set_alpha(i)                
            fade.fill((0,0,0))           
            surface.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)
    

    if fade_type == "in" or fade_type == "in out":
        for i in range(255):
            
            try:
                screen.fill(background)
            except:
                screen.blit(background, (0, 0))
            for entity in level_entities:
                screen.blit(entity.surface, entity.pos)
                
            fade = pygame.Surface(screensize)
            fade.set_alpha(225 - i)                
            fade.fill((0,0,0))           
            surface.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)

def button_interact(mouse_pos, buttox):
        click_rect = pygame.Rect(buttox.button.get_rect(center=(buttox.hit)))
        if click_rect.collidepoint(mouse_pos):
            screen.blit(buttox.outline, buttox.outline_pos)            

def player_movement(direction, player_entity, other_entities):
    global screensize
    x_change = 0
    y_change = 0
    
    if "left" in direction:
        x_change = -1
        player_entity.direction = "left"
        
    if "right" in direction:
        x_change = 1
        player_entity.direction = "right"
        
    if "up" in direction:
        y_change = -1
        player_entity.direction = "up"
        
    if "down" in direction:
        y_change = 1
        player_entity.direction = "down"

    x, y = player_entity.pos

    player_size = player_entity.size
    
    right_edge = x + player_size[0]
    down_edge = y + player_size[1]
            
    for entity in other_entities:
        if entity.name == "player":
            pass
        elif entity.name == "teleport":
            pass
        elif entity.size == (0, 0):
            pass
        else:
            directions = ""
            if entity.movable[0]:
                for direction in entity.movable[1]:
                    directions += f"{direction} "
                
                max_x, max_y = entity.movable[2][0]
                min_x, min_y = entity.movable[2][1]
                    
            size = entity.size
            
            
            x_pos, y_pos = entity.collision_pos   
            
            #*left
            if x <= x_pos + size[0] + 2 and x_change == -1:
                
                if x >= x_pos + size[0] - 2:
                    
                    if y <= y_pos + size[1] + 2:
                        
                        if down_edge >= y_pos - 2:
                            
                            if "left" in directions:
                                if x_pos > min_x: 
                                    x_change = -0.25
                                    x_pos -= 0.5
                                else:
                                    x_change = 0
                            else:
                                x_change = 0
                                    
            #*right
            if right_edge >= x_pos - 2 and x_change == 1:

                if right_edge <= x_pos + 2:

                    if y <= y_pos + size[1] + 2:
                        
                        if down_edge >= y_pos - 2:
                            
                            if "right" in directions:
                                if x_pos < max_x: 
                                    x_change = 0.25
                                    x_pos += 0.5
                                else:
                                    x_change = 0
                            else:
                                x_change = 0
                            
                            x_change = 0
                                            
            #*up    
            if y <= y_pos + size[1] + 2 and y_change == -1:

                if y >= y_pos + size[1] - 2:
                    
                    if x <= x_pos + size[0] + 2:
                        
                        if right_edge >= x_pos - 2:
                            
                            if "up" in directions:
                                if y_pos > min_y: 
                                    y_change = -0.25
                                    y_pos -= 0.5
                                else:
                                    y_change = 0
                            else:
                                y_change = 0
                                        
            #*down
            if down_edge >= y_pos - 2 and y_change == 1:
                
                if down_edge <= y_pos + 2:
                    
                    if x <= x_pos + size[0] + 2:
                        
                        if right_edge >= x_pos - 2:
                            
                            if "down" in directions:
                                if y_pos < max_y:
                                    y_change = 0.25
                                    y_pos += 0.5
                                else:
                                    
                                    y_change = 0
                            else:
                                y_change = 0
                                
            entity.pos = entity.image_anchoring()
            entity.collision_pos = (x_pos, y_pos)
    
    size = player_entity.size

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
    player_entity.animate()
    player_entity.pos = (x, y)
    
    return player_entity, level_entities    
    
    def new_image_set(picture_amount, path_name, name_, format):
        new_image_group = []
        for i in range (0, picture_amount):
            new_image_group.append(
                pygame.image.load(os.path.join(path_name, name_ + str(i) + format))
            )
        return new_image_group

def teleport(entity, player):
    entity_hitbox = pygame.rect.Rect(entity.collision_pos, entity.size)

    player_hitbox = pygame.rect.Rect(player.pos, player.size)

    return entity_hitbox.colliderect(player_hitbox)

def dialogue(first, last):
    while True:
        if not text.first > first:
            text.first = first
        text.line_2 = text.first + 1
        text.line_3 = text.first + 2
        name = first - 1

        def show_text(x, y, text, reset_key=False):
            
            if not text.done:
                with open("textfile.txt") as file:
                    for i, letter in enumerate(text.lines[text.first]):
                        if text.iterable > len(text.lines[text.first])*10:
                            text.iterable = 0
                        if text.iterable == i*10:
                            text.temporary_string += letter
                            text.string_to_print += letter
                    text.iterable += 1
                    if text.lines[text.first] == text.temporary_string:
                        text.iterable = -1
                        
                        if not last - text.first > 3:
                            for  event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        text.first += 3
                        
                        if last - text.first > 1:   
                            text.line_done = True
                            return text.line_done
                        else: 
                            screen.blit(text.enter, (text.enter_x, text.enter_y)) 

                    text.whos_talking_name = text.lines[name]
            whos_talking = text.font.render(text.whos_talking_name, True, text.whos_talking_color)
            screen.blit(whos_talking, (text.whos_talking_x, text.whos_talking_y))
                                
            text = text.font.render(text.string_to_print, True, text.color)
            screen.blit(text, (x, y))

        def show_text_2(x, y, y_2, text, reset_key=False):

            if not text.done:
                with open("textfile.txt") as file:
                    for i, letter in enumerate(text.lines[text.line_2]):
                        if text.iterable_2 > len(text.lines[text.line_2])*10:
                            text.iterable_2 = 0
                        if text.iterable_2 == i*10:
                            text.temporary_string_2 += letter
                            text.string_to_print_2 += letter

                    text.iterable_2 += 1
                    if text.lines[text.line_2] == text.temporary_string_2:

                        text.iterable_2 = -1
                        text.string_to_print_2 += ""

                        if not last - text.first > 3:
                            for  event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        text.first += 3
                        
                        if last - text.first > 2:    
                            text.line_done_2 = True
                            return text.line_done_2  
                        else: 
                            screen.blit(text.enter, (text.enter_x, text.enter_y))  

                    text.whos_talking_name = text.lines[name]
            whos_talking = text.font.render(text.whos_talking_name, True, text.whos_talking_color)
            screen.blit(whos_talking, (text.whos_talking_x, text.whos_talking_y))

            text_2 = text.font.render(text.string_to_print_2, True, text.color)
            screen.blit(text_2, (x, y_2))

            text = text.font.render(text.lines[text.first], True, text.color)
            screen.blit(text, (x, y))

        def show_text_3(x, y, y_2, y_3, text, reset_key=False):

            if not text.done:
                with open("textfile.txt") as file:
                    for i, letter in enumerate(text.lines[text.line_3]):
                        if text.iterable_3 > len(text.lines[text.line_3])*10:
                            text.iterable_3 = 0
                        if text.iterable_3 == i*10:
                            text.temporary_string_3 += letter
                            text.string_to_print_3 += letter

                    text.iterable_3 += 1
                    if text.lines[text.line_3] == text.temporary_string_3:

                        text.iterable_3 = -1
                        text.string_to_print_3 += ""
                        
                        screen.blit(text.enter, (text.enter_x, text.enter_y))

                        for  event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                            
                                    next_line = True
                                    text.first += 3

                                    text.string_to_print = ""
                                    text.string_to_print_2 = ""
                                    text.string_to_print_3 = ""
                                    text.iterable = 0
                                    text.iterable_2 = 0
                                    text.iterable_3 = 0
                                    text.temporary_string = ""
                                    text.temporary_string_2 = ""
                                    text.temporary_string_3 = ""
                                    text.done = False
                                    text.line_done = False
                                    text.line_done_2 = False
                                    text.line_2 = first + 1
                                    text.line_3 = first + 2

                                    return text.first

                    text.whos_talking_name = text.lines[name]
            whos_talking = text.font.render(text.whos_talking_name, True, text.whos_talking_color)
            screen.blit(whos_talking, (text.whos_talking_x, text.whos_talking_y))

            text_3 = text.font.render(text.string_to_print_3, True, text.color)
            screen.blit(text_3, (x, y_3))

            string_to_print_2 = text.lines[text.line_2]
            text_2 = text.font.render(text.string_to_print_2, True, text.color)
            screen.blit(text_2, (x, y_2))

            string_to_print = text.lines[text.first]
            text = text.font.render(text.string_to_print, True, text.color)
            screen.blit(text, (x, y))

        def text_box(x, y):
            screen.blit(text.box_img, (x, y))

        if not text.first >= last:
            text_box(text.box_x, text.box_y)

            show_text(text.x, text.y, text)

            if text.line_done == True:
                show_text_2(text.x, text.y, text.y_2, text)

            if text.line_done_2 == True:
                show_text_3(text.x, text.y, text.y_2, text.y_3, text)    
        else: 
            break
        pygame.display.update()

def file_saving(file_name, ):
    pass

def play_sound_effect(sound):
    
    click = pygame.mixer.Sound(f"sound_effects/{sound}")
    click.play()

def background_music():

    music = os.listdir("music")
    
    song = random.choice(music)
    
    pygame.mixer.music.load(f"music/{song}")
    pygame.mixer.music.play()

    
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

the_player = player_values((50, 100), (1200, 480), image="amogus_idle_1.png")

running = True

pygame.mixer.music.set_endevent ( pygame.USEREVENT )


#main menu

the_cheese = continuos_animation("the_cheese_logo", 10, (665, 100), (600, 338))

button_play = buttons("button_play.png", (360, 120), (780, 450), (960, 510))

button_options = buttons("button_options.png", (360, 120), (780, 600), (960, 660))
button_quit = buttons("button_quit.png", (360, 120), (780, 750), (960, 810))

save_1_button = buttons("save_1.png", (360, 120), (780, 250), (960, 310))
save_2_button = buttons("save_2.png", (360, 120), (780, 400), (960, 460))
save_3_button = buttons("save_3.png", (360, 120), (780, 550), (960, 610))
save_4_button = buttons("save_4.png", (360, 120), (780, 700), (960, 760))

back_button = buttons("back_button.png", (150, 150), (200, 120), (275, 195))

menu_screen = 1

opening_cutscene = moviepy.editor.VideoFileClip("images/opening_cutscene.mp4")

""" text_in_options = "Lol No Options For you"
game_version = "0.0.0"
font = pygame.font.Font("fonts/minkraft.ttf", 22)
text_color = (255, 255, 255)
text_game_version = font.render(f"{game_version}", True, text_color)
text_options = font.render(f"{text_in_options}", True, text_color) """


#main hub

left_border_wall_main_hub = entities((200 ,1080), (0, 0), fill=False)

right_border_wall_main_hub = entities((180 ,1080), (1740, 0), fill=False)

top_border_wall_main_hub = entities((1920, 100), (0, 0), fill=False)

bottom_border_wall_right_main_hub = entities((895, 160), (1025 ,920), fill=False)

bottom_border_wall_left_main_hub = entities((880, 170), (0 ,910), fill=False)

tree_main_hub = entities((210, 130), (870, 430), images=(["tree_main_hub.png"]), image_size=(300, 450))

exit_main_hub = entities((145, 20), (880, 1060), fill=False, name="teleport")

sensei_main_hub = continuos_animation("sensei_idle", 2, (1070, 450), (120, 120))

sensei_main_hub_hitbox = entities((100, 100), (1070, 470), fill=False)


#level one

box_level_one = entities((200, 150), (1400, 300), images=["box_level_one.png"], image_size=(200, 200), movable=[True, ["down"], [(1400, 750), (1400, 300)]])

track_level_one = entities((0, 0), (1500, 900), images=["track_level_one.png"], image_size=(100, 600))

tree_level_one = entities((110, 25), (290, 475), images=["tree_level_one.png"], image_size=(290, 402))

bush_level_one = entities((175, 125), (300, 750), images=["bush_level_one.png"], image_size=(160, 160))

cheese_level_one = entities((0, 0), (960, 100), images=["cheese_level_one.png"], image_size=(60, 60), name="teleport")

cheese_level_one_hitbox = entities((190, 30), (870, 70), fill=False, name="teleport")

level_one_shadow = entities((0, 0), (960, 1080), images=["level_one_shadow.png"], image_size=(1920, 1080))

light_level_one = one_image_animation("images/light_level_one",(60, 60), (1077, 20))

door_level_one = one_image_animation("images/door_level_one", (215, 130), (855, 20))

left_border_wall_level_one = entities((140 ,1080), (0, 0), fill=False)

right_border_wall_level_one = entities((145 ,1080), (1775, 0), fill=False)

top_border_wall_level_one = entities((1920, 70), (0, 0), fill=False)

bottom_border_wall_right_level_one = entities((860, 100), (1060 ,980), fill=False)

bottom_border_wall_left_level_one = entities((850, 100), (0 ,980), fill=False)

level_entities = []

background_music()


#*Main Loop

while running:

        
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:

            background_music()
    try:
        screen.fill(background)
    except:
        screen.blit(background, (0, 0))
        
        
    if active_location == "main menu":
        background = backgrounds.main_menu
        level_entities = []
        
        

        if menu_screen == 1:
            level_entities = [the_cheese]
            button_list = [button_play, button_options, button_quit]
            
        elif menu_screen == 2:

            button_list = [save_1_button, save_2_button, save_3_button, save_4_button, back_button]


        elif menu_screen == 3:

            button_list = [back_button]



        mouse_button_pressed = pygame.mouse.get_pressed()       

        if menu_screen == 1:

            if buttons.button_function((mouse_x, mouse_y), button_play, mouse_button_pressed):
                play_sound_effect("button_press_1.wav")

                pygame.time.delay(100)
                menu_screen = 2

            elif buttons.button_function((mouse_x, mouse_y), button_options, mouse_button_pressed):
                play_sound_effect("button_press_1.wav")
                

                pygame.time.delay(10)
                menu_screen = 3

            elif buttons.button_function((mouse_x, mouse_y), button_quit, mouse_button_pressed):
                play_sound_effect("button_press_1.wav")
                
                running = False
            
        elif menu_screen == 2:

            if buttons.button_function((mouse_x, mouse_y), back_button, mouse_button_pressed):
                play_sound_effect("button_press_1.wav")
                
                pygame.time.delay(10)
                menu_screen = 1
                
                
            for buttone in [save_1_button, save_2_button, save_3_button, save_4_button]:
                if buttons.button_function((mouse_x, mouse_y), buttone, mouse_button_pressed):
                    play_sound_effect("button_press_1.wav")
                    
                    pygame.mixer.music.stop()
                    opening_cutscene.preview()
                    opening_cutscene.close()
                    screen.fill((0, 0, 0))
                    pygame.display.update()
                    pygame.time.delay(1000)
                    fade_in_out(screen, backgrounds.main_hub, [the_player, tree_main_hub, sensei_main_hub], fade_type="in")
                    background_music()
                    
                    active_location = "main hub"
                    

        elif menu_screen == 3:

            if buttons.button_function((mouse_x, mouse_y), back_button, mouse_button_pressed):
                menu_screen = 1
                play_sound_effect("button_press_1.wav")
            
            if mouse_button_pressed[0]:
                click_rect = pygame.Rect(950, 450, 80, 100)
                if click_rect.collidepoint((mouse_x, mouse_y)):
                    pygame.mixer.music.load("sound_effects/among_us.mp3")
                    pygame.mixer.music.play()
                
        if active_location == "main menu":
            for button in button_list:
                screen.blit(button.button, button.pos)
                button_interact((mouse_x, mouse_y), button)
    
    if active_location == "main hub":
        dialogue(4, 16)
        background = backgrounds.main_hub
        sensei_main_hub.animate()

        level_entities = [left_border_wall_main_hub, right_border_wall_main_hub, top_border_wall_main_hub, bottom_border_wall_left_main_hub, 
        bottom_border_wall_right_main_hub, exit_main_hub, the_player, tree_main_hub, sensei_main_hub, sensei_main_hub_hitbox]
        
        if teleport(exit_main_hub, the_player):
             
            the_player.pos = (the_player.pos[0], 800)
            
            fade_in_out(screen, backgrounds.level_one, [track_level_one, light_level_one, the_player, bush_level_one, tree_level_one, box_level_one, door_level_one, level_one_shadow])
            active_location = "level one"         
            
    if active_location == "level one":
        background = backgrounds.level_one
        

        level_entities = [track_level_one, light_level_one, cheese_level_one, door_level_one, the_player, bush_level_one, tree_level_one, box_level_one, level_one_shadow, left_border_wall_level_one,
                          right_border_wall_level_one, top_border_wall_level_one, bottom_border_wall_left_level_one, bottom_border_wall_right_level_one, cheese_level_one_hitbox]

        if box_level_one.collision_pos == box_level_one.movable[2][0]:
            if door_level_one.surface != door_level_one.images[1]:
                light_level_one.change_image()
                pygame.time.delay(1000)
                play_sound_effect("door_open_level_one.mp3")
                door_level_one.change_image()

            else:

                
                if teleport(cheese_level_one_hitbox, the_player):
                    
                    pygame.mixer.music.stop()

                    save_data["level one complete"] = True
                    screen.blit(backgrounds.win_screen, (0, 0))
                    
                    pygame.display.update()
                    play_sound_effect("win_theme.mp3")
                    
                    pygame.time.delay(7000)
                    active_location = "main menu"
                    
                        
        
    
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


    keys = pygame.key.get_pressed()
        
    the_player.idle()
    
    if keys[pygame.K_w]:
        the_player, level_entities = player_movement("up", the_player, level_entities)    
    
    if keys[pygame.K_s]:
        the_player, level_entities = player_movement("down", the_player, level_entities)    
    
    if keys[pygame.K_a]:
        the_player, level_entities = player_movement("left", the_player, level_entities)
    
    if keys[pygame.K_d]:
        the_player, level_entities = player_movement("right", the_player, level_entities)    

    
    for entity in level_entities:
        screen.blit(entity.surface, entity.pos)
    
    if keys[pygame.K_b]:
        for box in level_entities:
            try:
                screen.blit(box.collision, box.collision_pos)
            except:
                pass
    
    the_cheese.animate()
    pygame.display.update()
