import pygame  # Importa el módulo pygame, usado para crear juegos.
import sys  # Importa el módulo sys, utilizado para funciones del sistema.
import random  # Importa el módulo random, utilizado para generar números aleatorios.
import csv  # Importa el módulo csv, usado para trabajar con archivos CSV.
import json  # Importa el módulo json, utilizado para trabajar con archivos JSON.
from modules import Player, Enemy, PowerUp, load_image, load_sound, Button  # Importa clases y funciones desde el módulo custom 'modules'.

# Inicializa pygame
pygame.init()  # Inicializa todos los módulos de pygame.
pygame.mixer.init()  # Inicializa el módulo de mezclador de sonido de pygame.

# INICIALIZAMOS LAS VARIABLES PARA UTILIZARLAS LUEGO (ANCHO, LARGO, FPS Y COLORES)
SCREEN_WIDTH = 800  # Ancho de la pantalla.
SCREEN_HEIGHT = 600  # Alto de la pantalla.
FPS = 60  # Cuadros por segundo.
WHITE = (255, 255, 255)  # Color blanco en formato RGB.
BLACK = (0, 0, 0)  # Color negro en formato RGB.

# CONFIGURACIONES PARA LA PANTALLA (RESOLUCIÓN, FPS, FUENTE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Configura la pantalla con el tamaño especificado.
pygame.display.set_caption("Juego Arcade")  # Establece el título de la ventana del juego.
clock = pygame.time.Clock()  # Crea un objeto reloj para controlar el tiempo.
font = pygame.font.Font(None, 36)  # Carga una fuente con tamaño 36.

# CARGAMOS LAS IMÁGENES Y SONIDOS DE /ASSETS
background = load_image('assets/imagens/Background.png')  # Carga la imagen de fondo.
background = pygame.transform.scale(background, (800, 600))  # Redimensiona la imagen de fondo.
player_image = load_image('assets/imagens/Player.png')  # Carga la imagen del jugador.
enemy_image = load_image('assets/imagens/Enemigo.png')  # Carga la imagen del enemigo.
enemy_image = pygame.transform.scale(enemy_image, (180, 180))  # Redimensiona la imagen del enemigo.
powerup_image = load_image('assets/imagens/Powerup.png')  # Carga la imagen del powerup.
powerup_image = pygame.transform.scale(powerup_image, (130, 130))  # Redimensiona la imagen del powerup.
inicio_image = load_image('assets/imagens/Inicio.png')  # Carga la imagen de inicio.
inicio_image = pygame.transform.scale(inicio_image, (800, 600))  # Redimensiona la imagen de inicio.
shoot_image = load_image('assets/imagens/LaserFoto.png').convert_alpha()  # Carga la imagen del disparo con transparencia.
final_image = load_image('assets/imagens/GameOver.png')  # Carga la imagen de Game Over.
final_image = pygame.transform.scale(final_image, (800, 600))  # Redimensiona la imagen de Game Over.
options_image = load_image('assets/imagens/Opciones.png')  # Carga la imagen de opciones.
options_image = pygame.transform.scale(options_image, (800, 600))  # Redimensiona la imagen de opciones.
shoot_sound = load_sound('assets/sounds/Laser.wav')  # Carga el sonido del disparo.
pygame.mixer.music.load('assets/sounds/MusicaFondo.mp3')  # Carga la música de fondo.
game_over_sound = pygame.mixer.Sound('assets/sounds/Muerte.mp3')  # Carga el sonido de Game Over.

# Variables del juego
all_sprites = pygame.sprite.Group()  # Grupo de todos los sprites.
enemies = pygame.sprite.Group()  # Grupo de los enemigos.
powerups = pygame.sprite.Group()  # Grupo de los powerups.
player = Player(player_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)  # Crea un objeto jugador.
all_sprites.add(player)  # Añade el jugador al grupo de todos los sprites.
score = 0  # Inicializa la puntuación.
lives = 3  # Inicializa el número de vidas.

# CARGA LA CONFIGURACIÓN SUMINISTRADA DENTRO DEL ARCHIVO JSON SOBRE EL JUEGO EN GENERAL
with open('configs/config.json') as f:  # Abre el archivo config.json.
    config = json.load(f)  # Carga la configuración desde el archivo JSON.

# Pantallas del juego
# BOTÓN DE START, OPCIONES, SALIR
def show_start_screen():
    inicio_image = pygame.image.load('assets/imagens/Inicio.png').convert()  # Carga la imagen de inicio.
    inicio_image = pygame.transform.scale(inicio_image, (800, 600))  # Redimensiona la imagen de inicio.
    screen.blit(inicio_image, (0, 0))  # Dibuja la imagen de inicio en la pantalla.
    title = font.render("Simpson´s Family", True, BLACK, WHITE)  # Renderiza el título del juego.
    start_button = Button(screen, "Start", (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 25, 100, 50), WHITE, BLACK)  # Crea el botón de inicio.
    options_button = Button(screen, "Options", (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 + 50, 100, 50), WHITE, BLACK)  # Crea el botón de opciones.
    quit_button = Button(screen, "Quit", (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 + 125, 100, 50), WHITE, BLACK)  # Crea el botón de salir.
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//4))  # Dibuja el título en la pantalla.
    pygame.display.flip()  # Actualiza la pantalla.
    
    # MIENTRAS EL USUARIO ESTE EN LA PANTALLA DE ESPERA
    waiting = True  # Variable de espera.
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana.
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):  # Si se hace click en el botón de inicio.
                    waiting = False
                elif options_button.is_clicked(event.pos):  # Si se hace click en el botón de opciones.
                    show_options_screen()
                elif quit_button.is_clicked(event.pos):  # Si se hace click en el botón de salir.
                    pygame.quit()
                    sys.exit()
                    
def show_options_screen():
    options_image = pygame.image.load('assets/imagens/Opciones.png').convert()  # Carga la imagen de opciones.
    options_image = pygame.transform.scale(options_image, (800, 600))  # Redimensiona la imagen de opciones.
    screen.blit(options_image, (0, 0))  # Dibuja la imagen de opciones en la pantalla.
    options_title = font.render("Options", True, BLACK, WHITE)  # Renderiza el título de opciones.
    back_button = Button(screen, "Back", (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 + 125, 100, 50), WHITE, BLACK)  # Crea el botón de regresar.
    screen.blit(options_title, (SCREEN_WIDTH//2 - options_title.get_width()//2, SCREEN_HEIGHT//4))  # Dibuja el título de opciones en la pantalla.
    pygame.display.flip()  # Actualiza la pantalla.
    
    # MIENTRAS EL USUARIO ESTE EN LA PANTALLA DE ESPERA
    waiting = True  # Variable de espera.
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana.
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.is_clicked(event.pos):  # Si se hace click en el botón de regresar.
                waiting = False
                
# DEFINIMOS UNA FUNCIÓN PARA LA FINALIZACIÓN DEL JUEGO
def show_game_over_screen(final_score):
    game_over_sound.play()  # Reproduce el sonido de Game Over.
    final_image = pygame.image.load('assets/imagens/GameOver.png').convert()  # Carga la imagen de Game Over.
    final_image = pygame.transform.scale(final_image, (800, 600))  # Redimensiona la imagen de Game Over.
    screen.blit(final_image, (0, 0))  # Dibuja la imagen de Game Over en la pantalla.
    game_over_title = font.render("Game Over", True, BLACK)  # Renderiza el título de Game Over.
    score_text = font.render(f"Score: {final_score}", True, BLACK)  # Renderiza el texto de la puntuación final.
    restart_button = Button(screen, "Restart", (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 - 25, 100, 50), WHITE, BLACK)  # Crea el botón de reiniciar.
    quit_button = Button(screen, "Quit", (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2 + 50, 100, 50), WHITE, BLACK)  # Crea el botón de salir.
    screen.blit(game_over_title, (SCREEN_WIDTH//2 - game_over_title.get_width()//2, SCREEN_HEIGHT//4))  # Dibuja el título de Game Over en la pantalla.
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//6))  # Dibuja la puntuación final en la pantalla.
    pygame.display.flip()  # Actualiza la pantalla.
    
    # MIENTRAS EL USUARIO ESTE EN LA PANTALLA DE ESPERA
    waiting = True  # Variable de espera.
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana.
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_clicked(event.pos):  # Si se hace clic en el botón de reiniciar.
                    main()
                elif quit_button.is_clicked(event.pos):  # Si se hace clic en el botón de salir.
                    pygame.quit()
                    sys.exit()

# CONFIGURACIÓN PRINCIPAL DEL JUEGO
def main():
    global score, lives, powerups_collected
    pygame.mixer.music.play(-1)  # Reproduce la música de fondo en bucle.
    score = 0  # Reinicia la puntuación.
    lives = 3  # Reinicia el número de vidas.
    powerups_collected = 0  # Reinicia el contador de powerups.
    bullets = pygame.sprite.Group()  # Crea un grupo para las balas.
    all_sprites.empty()  # Vacía el grupo de todos los sprites.
    enemies.empty()  # Vacía el grupo de enemigos.
    powerups.empty()  # Vacía el grupo de powerups.
    player = Player(player_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)  # Crea un nuevo jugador.
    all_sprites.add(player)  # Añade el jugador al grupo de todos los sprites.

    for _ in range(5):  # Crea 5 enemigos.
        enemy = Enemy(enemy_image)
        enemies.add(enemy)
        all_sprites.add(enemy)

    running = True  # Variable para el bucle del juego.
    game_over = False  # Variable para el estado de Game Over.
    while running:
        clock.tick(FPS)  # Controla la velocidad del juego.
        if random.random() < 0.01:  # Genera un powerup aleatoriamente.
            powerup = PowerUp(powerup_image)
            powerups.add(powerup)
            all_sprites.add(powerup)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana.
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Si se presiona la barra espaciadora.
                    player.shoot()
                    shoot_sound.play()

        all_sprites.update()  # Actualiza todos los sprites.

        hits = pygame.sprite.groupcollide(enemies, player.bullets, True, True)  # Detecta colisiones entre balas y enemigos.
        for hit in hits:
            score += 10  # Incrementa la puntuación.
            powerups_collected += 1  # Incrementa el contador de powerups.
            save_score("Player", score, powerups_collected)  # Guarda la puntuación.
            enemy = Enemy(enemy_image)  # Crea un nuevo enemigo.
            enemies.add(enemy)
            all_sprites.add(enemy)

        enemy_hits = pygame.sprite.spritecollide(player, enemies, False)  # Detecta colisiones entre el jugador y los enemigos.
        if enemy_hits:
            lives -= 1  # Decrementa las vidas.
            for enemy in enemy_hits:
                enemy.kill()  # Elimina al enemigo.
            if lives <= 0:
                game_over = True  # Activa el estado de Game Over.
                game_over_sound.play()
            else:
                player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)  # Reposiciona al jugador.

        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)  # Detecta colisiones entre el jugador y los powerups.
        for powerup in powerup_hits:
            player.power_up()  # Aplica el powerup al jugador.

        screen.blit(background, (0, 0))  # Dibuja el fondo en la pantalla.
        all_sprites.draw(screen)  # Dibuja todos los sprites en la pantalla.
        draw_text(screen, f"Score: {score}", 18, SCREEN_WIDTH // 2, 10)  # Dibuja la puntuación en la pantalla.
        draw_text(screen, f"Lives: {lives}", 18, SCREEN_WIDTH // 2, 40)  # Dibuja el número de vidas en la pantalla.
        pygame.display.flip()  # Actualiza la pantalla.

        if game_over:  # Si el juego ha terminado.
            show_game_over_screen(score)  # Muestra la pantalla de Game Over.
            game_over = False

    pygame.quit()  # Cierra pygame.
       
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)  # Carga una fuente con el tamaño especificado.
    text_surface = font.render(text, True, WHITE)  # Renderiza el texto.
    text_rect = text_surface.get_rect()  # Obtiene el rectángulo del texto.
    text_rect.midtop = (x, y)  # Posiciona el rectángulo.
    surf.blit(text_surface, text_rect)  # Dibuja el texto en la pantalla.
    
# DEFINIMOS UNA FUNCIÓN PARA QUE SE CARGUEN LOS DATOS DENTRO DEL ARCHIVO CSV
def save_score(username, final_score, final_powerups_collected):
    with open('configs/scores.csv', 'a', newline='') as f:  # Abre el archivo scores.csv en modo de adición.
        writer = csv.writer(f)  # Crea un objeto escritor de CSV.
        writer.writerow([username, final_score, final_powerups_collected])  # Escribe una nueva fila con los datos.
    

if __name__ == "__main__":
    show_start_screen()  # Muestra la pantalla de inicio.
    main()  # Inicia el juego.