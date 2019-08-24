import Map
import pygame

block_length = 20
screen_width = 20 * block_length
screen_height = 10 * block_length
screen = pygame.display.set_mode((screen_width, screen_height))


class Camera:
    # Initialisation
    def __init__(self, world, x_y_radii, centre, screen):
        self.x_y_radii = x_y_radii
        self.centre = centre
        self.width = 2*x_y_radii[0] + 1
        self.height = 2*x_y_radii[1] + 1
        self.world = world
        self.init_picture()
        self.screen = screen

    # ---------------- Create array that will be our pixel values

    def init_picture(self):
        pic = [0]*self.height
        for i in range(self.height):
            pic[i] = [0]*self.width
        self.set_picture(pic)

    # -------------- Getters and setters

    def set_picture(self, pic):
        self.picture = pic

    def get_picture(self):
        return self.picture

    # ----------------- Drawing

    def get_screen_coords(self, block_coords, block_length):
        return block_coords[0]*block_length, block_coords[1]*block_length

    def draw(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(self.screen, self.world.get_screen_colour(i, j), (i * block_length, j*block_length, block_length, block_length))
                pygame.display.update()


w = Map.Map(200, 100)
w.full_generation()
cam = Camera(w, (10, 5), (50, 25), screen)
w.draw(5)

        
                
                        
        
                
                             
        
