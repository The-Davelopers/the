import pygame, time, ctypes

pygame.init()

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen = pygame.display.set_mode(screensize)

screen = pygame.display.set_mode(screensize)

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
        self.box_img = pygame.image.load("text_box.png")
        self.box_x = 350
        self.box_y = 600
        self.font = pygame.font.Font(r"fonts\minkraft.ttf", 30)
        self.x = self.box_x + 25
        self.y = self.box_y + 50
        self.y_2 = self.y + 30
        self.y_3 = self.y_2 + 30
        self.whos_talking_x = self.box_x + 32
        self.whos_talking_y = self.box_y + 10
        self.whos_talking_color = (136, 136, 136)

text = text_class()

def dialogue(first, last):
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
        pass
        
running = True
while running: 

    screen.fill((0, 255, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  

    dialogue(4, 9) 

    pygame.display.update()