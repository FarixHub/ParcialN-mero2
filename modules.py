import pygame  # Importa la biblioteca Pygame
import random  # Importa la biblioteca random para generar números aleatorios
import os  # Importa la biblioteca os para interactuar con el sistema operativo

pygame.mixer.init()  # Inicializa el mezclador de sonido de Pygame

# Define las dimensiones de la pantalla
SCREEN_WIDTH = 800  
SCREEN_HEIGHT = 600


def load_image(path):  # Define una función para cargar una imagen
    return pygame.image.load(path).convert_alpha()  # Carga la imagen y la convierte con transparencia


def load_sound(file_path):  # Define una función para cargar un sonido
    try:
        sound = pygame.mixer.Sound(file_path)  # Intenta cargar el archivo de sonido
        return sound  # Devuelve el objeto de sonido
    except pygame.error as e:  # Si hay un error al cargar el sonido
        print(f"Error loading sound: {file_path}")  # Imprime un mensaje de error
        raise SystemExit(str(e))  # Lanza una excepción y termina el programa

# Clase Player
class Player(pygame.sprite.Sprite):  # Define la clase Player que hereda de pygame.sprite.Sprite
    def __init__(self, image, x, y):  # Inicializador de la clase
        super().__init__()  # Llama al inicializador de la clase base
        self.image = image  # Asigna la imagen del jugador
        self.rect = self.image.get_rect()  # Obtiene el rectángulo de la imagen
        self.rect.center = (x, y)  # Establece la posición inicial del jugador
        self.base_speed = 5  # Velocidad base del jugador
        self.speed = self.base_speed  # Velocidad actual del jugador
        self.bullets = pygame.sprite.Group()  # Grupo de sprites para las balas
        self.last_shot = pygame.time.get_ticks()  # Tiempo del último disparo
        self.shoot_delay = 500  # Retraso entre disparos en milisegundos
        self.power_up_active = False  # Indica si el power-up está activo
        self.power_up_end_time = 0  # Tiempo en que termina el power-up

    def update(self):  # Método para actualizar el estado del jugador
        keys = pygame.key.get_pressed()  # Obtiene las teclas presionadas
        if keys[pygame.K_LEFT]:  # Si la tecla izquierda está presionada
            self.rect.x -= self.speed  # Mueve el jugador a la izquierda
        if keys[pygame.K_RIGHT]:  # Si la tecla derecha está presionada
            self.rect.x += self.speed  # Mueve el jugador a la derecha
        if keys[pygame.K_SPACE]:  # Si la tecla de espacio está presionada
            self.shoot()  # Llama al método shoot para disparar

        self.bullets.update()  # Actualiza las balas

        # Comprueba si la duración del power-up ha terminado
        if self.power_up_active and pygame.time.get_ticks() > self.power_up_end_time:
            self.revert_power_up()  # Revertir el power-up

    def shoot(self):  # Método para disparar balas
        now = pygame.time.get_ticks()  # Obtiene el tiempo actual
        if now - self.last_shot > self.shoot_delay:  # Si ha pasado suficiente tiempo desde el último disparo
            self.last_shot = now  # Actualiza el tiempo del último disparo
            bullet = Bullet(self.rect.centerx, self.rect.top)  # Crea una nueva bala
            self.bullets.add(bullet)  # Añade la bala al grupo de balas
            
    def power_up(self):  # Método para activar un power-up
        self.speed += 2  # Incrementa la velocidad
        self.power_up_active = True  # Indica que el power-up está activo
        self.power_up_end_time = pygame.time.get_ticks() + 5000  # Duración de 5 segundos

    def revert_power_up(self):  # Método para revertir el efecto del power-up
        self.speed = self.base_speed  # Restaura la velocidad base
        self.power_up_active = False  # Indica que el power-up ya no está activo
            
    def handle_event(self, event):  # Método para manejar eventos del juego
        if event.type == pygame.USEREVENT:  # Si el evento es del tipo USEREVENT
            self.revert_power_up("speed")  # Revertir el power-up de velocidad

# Clase Bullet
class Bullet(pygame.sprite.Sprite):  # Define la clase Bullet que hereda de pygame.sprite.Sprite
    def __init__(self, x, y):  # Inicializador de la clase
        super().__init__()  # Llama al inicializador de la clase base
        self.image = load_image('assets/imagens/LaserFoto.png')  # Carga la imagen de la bala
        self.rect = self.image.get_rect()  # Obtiene el rectángulo de la imagen
        self.rect.centerx = x  # Establece la posición x de la bala
        self.rect.bottom = y  # Establece la posición y de la bala
        self.speedy = -10  # Velocidad de la bala hacia arriba

    def update(self):  # Método para actualizar el estado de la bala
        self.rect.y += self.speedy  # Mueve la bala hacia arriba
        if self.rect.bottom < 0:  # Si la bala sale de la pantalla
            self.kill()  # Elimina la bala

# Clase Enemy
class Enemy(pygame.sprite.Sprite):  # Define la clase Enemy que hereda de pygame.sprite.Sprite
    def __init__(self, image):  # Inicializador de la clase
        super().__init__()  # Llama al inicializador de la clase base
        self.image = image  # Asigna la imagen del enemigo
        self.rect = self.image.get_rect()  # Obtiene el rectángulo de la imagen
        self.rect.x = random.randint(0, 800 - self.rect.width)  # Posición x aleatoria
        self.rect.y = random.randint(-100, -40)  # Posición y aleatoria fuera de la pantalla
        self.speedy = random.randint(1, 8)  # Velocidad aleatoria del enemigo

    def update(self):  # Método para actualizar el estado del enemigo
        self.rect.y += self.speedy  # Mueve el enemigo hacia abajo
        if self.rect.top > 600 + 10:  # Si el enemigo sale de la pantalla por abajo
            self.rect.x = random.randint(0, 800 - self.rect.width)  # Reposiciona el enemigo en x
            self.rect.y = random.randint(-100, -40)  # Reposiciona el enemigo en y
            self.speedy = random.randint(1, 8)  # Cambia la velocidad del enemigo

# Clase PowerUp
class PowerUp(pygame.sprite.Sprite):  # Define la clase PowerUp que hereda de pygame.sprite.Sprite
    def __init__(self, image):  # Inicializador de la clase
        super().__init__()  # Llama al inicializador de la clase base
        self.image = image  # Asigna la imagen del power-up
        self.rect = self.image.get_rect()  # Obtiene el rectángulo de la imagen
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)  # Posición x aleatoria
        self.rect.y = random.randint(-100, -40)  # Posición y aleatoria fuera de la pantalla
        self.speedy = random.randint(1, 8)  # Velocidad aleatoria del power-up

    def update(self):  # Método para actualizar el estado del power-up
        self.rect.y += self.speedy  # Mueve el power-up hacia abajo
        if self.rect.top > SCREEN_HEIGHT + 10:  # Si el power-up sale de la pantalla por abajo
            self.kill()  # Elimina el power-up

# Clase Button
class Button:  # Define la clase Button
    def __init__(self, surface, text, rect, color, text_color):  # Inicializador de la clase
        self.surface = surface  # Superficie donde se dibuja el botón
        self.rect = pygame.Rect(rect)  # Rectángulo del botón
        self.color = color  # Color del botón
        self.text_color = text_color  # Color del texto del botón
        self.text = text  # Texto del botón
        self.font = pygame.font.Font(None, 36)  # Fuente del texto
        self.text_surf = self.font.render(text, True, text_color)  # Superficie del texto
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)  # Rectángulo del texto
        self.draw()  # Dibuja el botón

    def draw(self):  # Método para dibujar el botón
        pygame.draw.rect(self.surface, self.color, self.rect)  # Dibuja el rectángulo del botón
        self.surface.blit(self.text_surf, self.text_rect)  # Dibuja el texto del botón

    def is_clicked(self, pos):  # Método para comprobar si el botón fue clickeado
        return self.rect.collidepoint(pos)  # Devuelve True si la posición está dentro del rectángulo del botón
    
