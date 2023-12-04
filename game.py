import pygame
from player import Player
import config
from game_state import GameState

class Game:
  def __init__(self,screen):
    self.screen = screen
    self.objects = []
    self.game_state= GameState.NONE
    self.map = []

  def set_up(self):
    player=Player(1,1)
    self.player = player
    self.objects.append(player)
    print("configure")
    self.game_state= GameState.RUNNING

   
    
  def update(self):
    self.screen.fill(config.BLACK)
    print("atualizando")
    self.handle_events()

    

    for object in self.objects:
      object.render(self.screen)

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.game_state= GameState.ENDED
        #eventos de chave
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.game_state= GameState.ENDED
        elif event.key == pygame.K_w:
          self.player.update_position(0,-10) 
        elif event.key == pygame.K_s:
          self.player.update_position(0,1)
        elif event.key == pygame.K_a:
          self.player.update_position(-1,0)
        elif event.key == pygame.K_d:
          self.player.update_position(1,0)



     

