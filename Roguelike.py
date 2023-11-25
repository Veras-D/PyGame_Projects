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
        self.pontos_vida = 120
        self.vivo = True
        self.dash_cooldown = 0
        self.dash_duration = 30
        self.dash_speed = 15
        self.dashing = False

    def atacar(self, alvo):
        alvo.receber_dano(10)

    def receber_dano(self, dano):
        self.pontos_vida -= dano
        if self.pontos_vida <= 0:
            print(f"{self.nome} foi derrotado!")
            self.vivo = False
            self.kill()

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
                distancia = math.sqrt(abs((self.rect.x - sprite.rect.x) ** 2 + (self.rect.y - sprite.rect.y) ** 2))
                if keys[pygame.K_SPACE]:
                    if distancia < 10:  # Ajuste esse valor conforme necessário para a sua proximidade desejada
                        self.atacar(sprite)

        # Atualiza o cooldown do dash
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        # Mecânica de dash
        if keys[pygame.K_f] and not self.dashing and self.dash_cooldown == 0:
            self.dashing = True

        if self.dashing:
            self.dash_duration -= 1
            if self.dash_duration > 0:
                # Mova-se para frente na direção atual do personagem
                angle = math.atan2(keys[pygame.K_UP] - keys[pygame.K_DOWN], keys[pygame.K_LEFT] - keys[pygame.K_RIGHT])
                self.rect.x += self.dash_speed * math.cos(angle)
                self.rect.y += self.dash_speed * math.sin(angle)
            else:
                self.dashing = False
                self.dash_duration = 30
                self.dash_cooldown = 90

    def mostrar_mensagem_cooldown(self, screen, font):
        if self.dash_cooldown > 0:
            mensagem = f"Recarga do Dash: {math.ceil(self.dash_cooldown / 30)}s"
            texto_cooldown = font.render(mensagem, True, BLACK)
            screen.blit(texto_cooldown, (WIDTH // 2 - 100, HEIGHT - 50))


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

    jogador.mostrar_mensagem_cooldown(screen, font)

    screen.blit(texto_jogador, (10, 10))

    pygame.display.flip()

    # Controle de frames por segundo
    clock.tick(30)
