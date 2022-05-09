from turtle import width
import pygame, sys, time, random
from pygame.locals import *
from StreamThread import * 

pygame.init()
width = 500
height = 700
play_surface = pygame.display.set_mode((width, height))
fps = pygame.time.Clock()

def pipe_random_height():
    pipe_h = [random.randint(200, (height/2)-20), random.randint((height/2)+20, height-200)]
    return pipe_h

class App:
    comprobar_color = False

    def main(self):
        global app

        score = 0
        player_pos = [100,350]
        gravity = 1
        speed = 0
        jump = -30

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
                    run = False

                # if (self.comprobar_color == True):
                #     # speed += jump
                #     player_pos[1] -= 10
                # # else:
                # #     player_pos[1] += 10
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        speed += jump

            speed += gravity
            speed *= 0.95
            player_pos[1] += speed

            if pipe_pos >= -20:
                pipe_pos -= 10
            else:
                pipe_pos = 700
                pipe_height = pipe_random_height()
                score += 1
            
            #Fondo
            play_surface.fill((0,0,0))

            
            if (self.comprobar_color):
                color = (255, 0,0)
                # player_pos[1] -= 5
            else: 
                color = (255,160,60)
                # player_pos[1] += 5

            #Jugador
            pygame.draw.circle(play_surface, color, (int(player_pos[0]), int(player_pos[1])), 20)

            #Pipe
            pygame.draw.rect(play_surface, (200,200,200), [pipe_pos, 0, pipe_widht, pipe_height[0]], 0)
            pygame.draw.rect(play_surface, (200,200,200), [pipe_pos, pipe_height[1], pipe_widht, 500], 0)   

            if player_pos[1] <= pipe_height[0] or player_pos[1] >= pipe_height[1]:
                if player_pos[0] in list(range(pipe_pos, pipe_pos + pipe_widht)): 
                    print(f"Game Over. Score {score} ")         

            if player_pos[1] >= height:
                player_pos[1] = height
                speed = 0
            elif player_pos[1] <= 0:
                player_pos[1] = 0
                speed = 0
                
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
    app.main()