import pygame
import random


def play_main_music():
    main_musics = ['main_music01.mp3']
    pygame.mixer.music.load(random.choice(main_musics))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
