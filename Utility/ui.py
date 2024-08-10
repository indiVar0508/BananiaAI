from pygame.font import Font, SysFont
from pygame.mouse import get_pos, get_pressed
from pygame.draw import rect


def make_obj_msg(msg: str, font_definition: Font, color: tuple = (0, 0, 0)) -> tuple:
    msg_obj = font_definition.render(msg, True, color)
    return msg_obj, msg_obj.get_rect()


def message(
    gameDisplay,
    msg: str,
    color: tuple = (0, 0, 0),
    font_type: str = "freesansbold.ttf",
    font_size: int = 15,
    x: int = 10,
    y: int = 10,
):
    font_definition = Font(font_type, font_size)
    msg_surface, msg_rectangle = make_obj_msg(msg, font_definition, color)
    msg_rectangle = (x, y)
    gameDisplay.blit(msg_surface, msg_rectangle)


def text_objects(text: str, font: Font, color: tuple = (0, 0, 0)) -> tuple:
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(
    gameDisplay,
    message: str,
    x: int,
    y: int,
    width: int,
    height: int,
    inactive_color: tuple,
    active_color: tuple,
    action=None,
):
    mouse = get_pos()
    click = get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        rect(gameDisplay, active_color, (x, y, width, height))

        if click[0] == 1 and action is not None:
            action()
    else:
        rect(gameDisplay, inactive_color, (x, y, width, height))

    smallText = SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ((x + (width / 2)), (y + (height / 2)))
    gameDisplay.blit(textSurf, textRect)
