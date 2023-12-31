import pygame
from player import Player
from game_state import GameState
import config


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.object = []
        self.game_state = GameState.NONE

    def set_up(self):
        player = Player(1, 1)
        self.player = player
        self.objects.append(player)
        print("configurar")
        self.game_state = GameState.RUNNIG

    def update(self):
        self.screen.fill(config.BLACK)
        print("Atualizando")

        for object in self.objects:
            object.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w:  # cima
                    self.player.update_position(0, -1)
                elif event.key == pygame.K_s:  # cima
                    self.player.update_position(0, 1)
                elif event.key == pygame.K_a:  # cima
                    self.player.update_position(-1, 0)
                elif event.key == pygame.K_d:  # cima
                    self.player.update_position(1, 0)
