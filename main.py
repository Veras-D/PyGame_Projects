import pygame
import sys
import math
import random
import play_music

# Inicialização do Pygame
pygame.init()

# Musica
play_music.play_main_music()

# Definição de cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Configurações da tela

info = pygame.display.Info()
WIDTH, HEIGHT = int(info.current_w * 0.5), int(info.current_h * 0.5)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Jogo RPG Pygame")

# Classe Personagem
class Personagem(pygame.sprite.Sprite):
    def __init__(self, nome, cor, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(cor)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.nome = nome
        self.pontos_vida = 100
        self.vivo = True  # Adiciona um atributo para verificar se o personagem está vivo

    def atacar(self, alvo):
        alvo.receber_dano(10)  # Simples exemplo de dano fixo

    def receber_dano(self, dano):
        self.pontos_vida -= dano
        if self.pontos_vida <= 0:
            print(f"{self.nome} foi derrotado!")
            self.vivo = False  # Define o personagem como derrotado
            self.kill()  # Remove o personagem do grupo de sprites

    def update(self, keys, all_sprites):
        # Atualiza a posição do personagem com base nas teclas pressionadas
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5

        # Mantém o personagem dentro das bordas da tela
        self.rect.x = max(0, min(self.rect.x, WIDTH - 50))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - 50))

        # Verifica a proximidade com outros sprites
        for sprite in all_sprites:
            if isinstance(sprite, Personagem) and sprite != self and sprite.vivo and self.vivo:
                distancia = math.sqrt(abs((self.rect.x - sprite.rect.x)*2 + (self.rect.y - sprite.rect.y)*2))
                if keys[pygame.K_SPACE]:
                    if distancia < 10:  # Ajuste esse valor conforme necessário para a sua proximidade desejada
                        self.atacar(sprite)


# Inicialização do jogador, posição inicial do jogador
jogador = Personagem("Jogador", RED, (WIDTH / 2), (HEIGHT / 2))

# Grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(jogador)

# Adiciona alguns NPCs
num_npcs = 10
for _ in range(num_npcs):
    cor_npc = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    npc = Personagem("NPC", cor_npc, random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50))
    npc.velocidade_x = random.randint(-3, 3)  # Adiciona velocidade aleatória no eixo X
    npc.velocidade_y = random.randint(-3, 3)  # Adiciona velocidade aleatória no eixo Y
    all_sprites.add(npc)

# Loop do jogo
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT:
            play_music.play_main_music()

    # Captura as teclas pressionadas
    keys = pygame.key.get_pressed()

    # Lógica do jogo
    jogador.update(keys, all_sprites)

    # Atualização da tela
    screen.fill(WHITE)

    # Movimenta NPCs e mantém dentro das bordas
    for sprite in all_sprites:
        if isinstance(sprite, Personagem) and sprite != jogador and sprite.vivo:
            # Salva as posições anteriores do NPC
            old_x, old_y = sprite.rect.x, sprite.rect.y

            # Atualiza as posições do NPC
            sprite.rect.x += sprite.velocidade_x
            sprite.rect.y += sprite.velocidade_y

            # Verifica se o NPC ultrapassa as bordas da tela
            if not (0 <= sprite.rect.x < WIDTH - 50 and 0 <= sprite.rect.y < HEIGHT - 50):
                # Se ultrapassar, reverte para as posições anteriores
                sprite.rect.x, sprite.rect.y = old_x, old_y

    # Desenha os sprites na tela
    all_sprites.draw(screen)

    # Adiciona informações de saúde na tela
    font = pygame.font.Font(None, 36)
    texto_jogador = font.render(f"Jogador: {jogador.pontos_vida} HP", True, BLACK)
    
    for sprite in all_sprites:
        if isinstance(sprite, Personagem) and sprite.nome == "NPC" and sprite.vivo:
            texto_npc = font.render(f"NPC: {sprite.pontos_vida} HP", True, BLACK)
            screen.blit(texto_npc, (sprite.rect.x, sprite.rect.y - 30))  # Exibe a vida acima do NPC

    screen.blit(texto_jogador, (10, 10))

    pygame.display.flip()

    # Controle de fps
    clock.tick(30)
