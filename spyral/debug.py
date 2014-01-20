import spyral
import pygame

class DebugText(spyral.sprite.Sprite):
    def __init__(self, view, text, color):
        spyral.sprite.Sprite.__init__(self, view)
        self.font = spyral.Font(spyral._get_spyral_path() + "resources/fonts/DejaVuSans.ttf", 15, color)
        self.render(text)

    def render(self, text):
        self.image = self.font.render(text)
    text = property(lambda self: "", render)

class FPSSprite(spyral.sprite.Sprite):
    def __init__(self, font, color):
        spyral.sprite.Sprite.__init__(self)
        self.font = font
        self.color = color
        self.render(0, 0)
        self.update_in = 5

    def render(self, fps, ups):
        self.image = self.font.render("%d / %d" % (fps, ups), 0, self.color)

    def update(self, *args, **kwargs):
        self.update_in -= 1
        if self.update_in == 0:
            self.update_in = 5
            clock = spyral.director.get_scene().clock
            self.render(clock.fps, clock.ups)
