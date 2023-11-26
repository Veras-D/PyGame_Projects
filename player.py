import pygame
import config


class Player:
    def __init__(self, x_position, y_position):
        print("Jogador Criado")
        self.position = [x_position, y_position]

    def update(self):
        print("Jogador Atualizado")

    def update_position(self, x_change, y_change):
        self.position[0] += x_change
        self.position[1] += y_change

    def render(self, screen):
        pygame.draw.rect(screen, config.WHITE,
                         (self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE), 4)
