import pygame


def make_obj_msg(msg, font_definition, color=(0, 0, 0)):
    msg_obj=font_definition.render(msg, True, color)
    return msg_obj, msg_obj.get_rect()


def message(gameDisplay, msg, color=(0, 0, 0), font_type='freesansbold.ttf', font_size=15, x=10, y=10):
    font_definition=pygame.font.Font(font_type, font_size)
    msg_surface, msg_rectangle=make_obj_msg(msg, font_definition, color)
    msg_rectangle=(x, y)
    gameDisplay.blit(msg_surface, msg_rectangle)


def text_objects(text, font, color=(0, 0, 0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(gameDisplay, message, x, y, width, height, inactive_color, active_color, action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active_color,(x, y, width, height))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width, height))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ( (x+(width/2)), (y+(height/2)) )
    gameDisplay.blit(textSurf, textRect)