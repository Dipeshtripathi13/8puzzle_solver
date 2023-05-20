import pygame

class Drawer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def drawActual(self, pos):
        w = 60
        h = 60
        count = 1
        for column in range(3):
            for row in range(3):
                x = pos[0] + w * row
                y = pos[1] + h * column
                r = pygame.Rect(x, y, w, h)
                pygame.draw.rect(self.screen, ((count * 15) % 255, 0, 0), r)
                del r
                self.screen.blit(self.font.render(str(count % 9), True, (255, 255, 255)), (x + w / 2, y + h / 2))
                pygame.display.update()
                count += 1

        self.screen.blit(self.font.render('GOAL STATE', True, (0, 0, 0)), (pos[0], pos[1] - h))

    def draw_state(self, state, pos, text):
        w = 60
        h = 60
        for i, column in zip(state, range(3)):
            for count, row in zip(i, range(3)):
                x = pos[0] + w * row
                y = pos[1] + h * column
                rectangle_ = pygame.Rect(x, y, w, h)
                pygame.draw.rect(self.screen, ((count * 15) % 255, 0, 0), rectangle_)
                del rectangle_
                self.screen.blit(self.font.render(str(count % 9), True, (255, 255, 255)), (x + w / 2, y + h / 2))
                pygame.display.update()

        i = self.screen.blit(self.font.render(text, True, (0, 0, 0)), (pos[0], pos[1] - h))
        del i
