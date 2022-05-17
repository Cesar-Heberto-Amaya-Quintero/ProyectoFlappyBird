
import pygame, sys, time, random
from pygame.locals import *
from StreamThread import * 

width = 500
height = 700
play_surface = pygame.display.set_mode((width, height))
fps = pygame.time.Clock()
jugador = pygame.image.load("Assets/Tiburoncin.png")
fondo = pygame.image.load("Assets/Fondo3.png")
tuboArriba = pygame.image.load("Assets/TuboArriba.png")
tuboAbajo = pygame.image.load("Assets/TuboAbajo.png")
fondoMenu = pygame.image.load("Assets/fondoMenu.png")
fondoGameOver = pygame.image.load("Assets/fondoGameOver.png")

jugadorAnimado = [pygame.image.load("Assets/Tiburoncin1.png"),
                  pygame.image.load("Assets/Tiburoncin.png"),
                  pygame.image.load("Assets/Tiburoncin2.png"),
                  pygame.image.load("Assets/Tiburoncin.png"),]

cuentaPasos=0


pygame.init()
pygame.mixer.init()

pygame.display.set_icon(jugador)


def pipe_random_height():
    pipe_h = [random.randint(200, (height/2)-60), random.randint((height/2)+60, height-200)]
    return pipe_h

def get_font(size):
    return pygame.font.Font("8-BIT-WONDER.TTF", size)

class App:
    comprobar_movimiento = False
        
    def Menu(self):
        global play_surface
        pygame.mixer.music.stop()
        pygame.mixer.music.load('Musica/Menu.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        while True:
            pygame.display.set_caption("Sharky")
            play_surface.blit(fondoMenu, (0,0))
            
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.main()


            pygame.display.update()

    def GameOver(self, score):
        global play_surface

        pygame.mixer.music.load('Musica/GameOver.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        while True:
            pygame.display.set_caption("Sharky")
            # play_surface.blit(fondoMenu, (0,0))
            play_surface.blit(fondoGameOver, [0,0])
            
            # menu_text = get_font(35).render("GAME OVER", True, "#ffffff")
            # menu_rect = menu_text.get_rect(center=(250, 100))
            
            # play_surface.blit(menu_text, menu_rect)

            play_text = get_font(15).render(f"Puntuacion {score}", True, "#ffffff")
            play_rect = play_text.get_rect(center=(250, 350))
            
            play_surface.blit(play_text, play_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    self.Menu()
                    
            pygame.display.update()
                    
            

    def main(self):
        global app
        global cuentaPasos

        pygame.display.set_caption("Sharky")
        pygame.mixer.music.stop()

        score = 0
        player_pos = [50,350]

        fondo_pos = [0,0]

        pipe_pos = 700
        pipe_widht = 50
        pipe_height = pipe_random_height()

        #Inicializar el Stream Thread
        self.stream_thread = StreamThread(self)
        self.stream_thread.daemon = True
        self.stream_thread.start()
        run = True


        #Main Loop
        while run:

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #         speed += jump
            fondo_pos[0] = fondo_pos[0] - 2
            if fondo_pos[0] <= - 2580:
                fondo_pos[0] = 0

            if pipe_pos >= -100:
                pipe_pos -= 10
            else:
                pipe_pos = 700
                pipe_height = pipe_random_height()
                score += 1
            
            #Fondo
            # play_surface.fill((0,0,0))
            play_surface.blit(fondo, fondo_pos)

            
            if (self.comprobar_movimiento):
                player_pos[1] -= 10
            else: 
                player_pos[1] += 10

            #TIBURON
            if cuentaPasos +1 >= 5:
                cuentaPasos = 0


            play_surface.blit(jugadorAnimado[cuentaPasos], (int(player_pos[0]), int(player_pos[1])))
            cuentaPasos = cuentaPasos + 1

            #TUBERIAS
            play_surface.blit(tuboArriba, [pipe_pos - 50, pipe_height[0]- 330, pipe_widht, pipe_height[0]])
            play_surface.blit(tuboAbajo, [pipe_pos -50, pipe_height[1], pipe_widht, 500])
            

            #Pipe
            # pygame.draw.rect(play_surface, (200,200,200), [pipe_pos, 0, pipe_widht, pipe_height[0]], 0)
            # pygame.draw.rect(play_surface, (200,200,200), [pipe_pos, pipe_height[1], pipe_widht, 500], 0)   

            if player_pos[1] <= pipe_height[0] or player_pos[1] >= pipe_height[1]:
                if player_pos[0] in list(range(pipe_pos, pipe_pos + pipe_widht)): 
                    print(f"Game Over. Score {score} ")
                    self.GameOver(score)        

            if player_pos[1] >= height:
                player_pos[1] = height

            elif player_pos[1] <= 0:
                player_pos[1] = 0


            #PUNTUACION
            play_text = get_font(15).render(f"Puntuacion {score}", True, "#ffffff")
            play_rect = play_text.get_rect(center=(400, 20))
            
            play_surface.blit(play_text, play_rect)
            
                
            pygame.display.flip()
            fps.tick(30)

        self.stream_thread.stream.abort()
        self.stream_thread.event.set()
        self.stream_thread.join()

# main()
# pygame.quit()

app = None

if __name__ == "__main__":

    app = App()
    app.Menu()