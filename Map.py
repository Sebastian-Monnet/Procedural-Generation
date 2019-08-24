import pygame
import random

class Map:
    def __init__(self, map_width, map_height):
        # Initialise our map_width x map_height array with zeroes
        self.map = [0]*map_height
        for i in range(map_height):
            self.map[i] = [0]*map_width

        # Set some values
        self.map_width = map_width
        self.map_height = map_height
        self.surface_height_map = [0] * map_width
# Basic methods

    def set_block(self, x, y, value):
        # Sets the block at (x,y) to value
            self.map[y][x] = value

    def get_block_value(self, x, y):
        # Takes x,y coordinates and returns the value of the block at those coordinates
        return self.map[y][x]

    def is_empty(self, x, y):
        # Tells us if the block at (x,y) is empty
        if self.get_block_value(x, y) == 0:
            return True

    def get_neighbouring_coords(self, x, y):
        output = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (not i == j == 0) and 0 <= x+i < self.map_width and 0 <= y+j < self.map_height:
                    output.append((x+i, y+j))
        return output
    
    def get_surface_height(self, x):
        return self.surface_height_map[x]

    def set_surface_height(self, x, height):
        self.surface_height_map[x] = height
    

# Cave generation automaton

    def get_new_value(self, x, y, scope):
        # If a full block has at most death_limit neighbours, return 0, and if an empty block has at least birth_limit
        # neighbours, return 1
        birth_limit = 4
        death_limit = 4
        neighbours = 8 - self.count_empty_neighbours(x, y, scope)
        
        if neighbours <= death_limit and not self.is_empty(x, y):
            return 0
        elif neighbours >= birth_limit:
            return 1
        else:
            return self.get_block_value(x, y)

    '''def executeAutomaton(self, scope):
        newMap = Map(self.map_width,self.map_height)
        for i in range(self.map_width):
            for j in range(self.map_height):
                if (i,j) in scope:
                    newMap.set_block(i,j,self.get_new_value(i,j,scope))
                else:
                    newValue = self.get_block_value(i,j)
                    newMap.set_block(i,j,newValue)
        self.map = newMap.map'''

# Randomisation

    def randomise_block(self, x, y, p):
        # Fills block with probability p, and makes it empty otherwise
        if random.random() < p:
            self.set_block(x, y, 1)
        else:
            self.set_block(x, y, 0)

    '''def randomise_all(self,p):
        #randomises all blocks
        for i in range(self.map_width):
            for j in range(self.map_height):
                self.randomise_block(i,j,p)'''

    '''def gradRandomise(self):
        #randomises a block with a higher probability of filling it if it is lower down
        for i in range(self.map_width):
            for j in range(self.map_height):
                self.randomise_block(i,j,2*j/self.map_height)'''
# Surface generation

    def set_column_height(self,x, height):
        for j in range(0, self.map_height - height):
            self.set_block(x, j, 0)
        for j in range(self.map_height - height, self.map_height):
            self.set_block(x, j, 1)

    def set_all_columns(self, column_height):
        for i in range(self.map_width):
            self.set_column_height(i, column_height)
            
    def generate_noise_map(self, chunk_width, amplitude):
        noise_map = [0] * self.map_width
        for chunk_index in range(int(self.map_width/chunk_width)):
            noise = (2*random.random()-1) * amplitude
            for i in range(chunk_index*chunk_width, (chunk_index+1)*chunk_width):
                noise_map[i] = int(round(noise))
        noise = (2*random.random()-1)*amplitude
        for i in range(int(self.map_width/chunk_width)*chunk_width, self.map_width):
            noise_map[i] = noise
            
        return noise_map

    def add_noise_to_map(self, chunk_width, amplitude):
        noise_map = self.generate_noise_map(chunk_width, amplitude)
        for i in range(self.map_width):
            self.set_column_height(i, self.get_column_height(i)+int(noise_map[i]))

    def get_column_height(self, x):
        surface_reached = False
        j = 0
        while not surface_reached:
            if self.get_block_value(x, j) == 0:
                j += 1
            else:
                surface_reached = True
        return self.map_height - j
    
    def get_mean_column_height(self, list_of_columns):
        tot = 0
        for col in list_of_columns:
            tot += self.get_column_height(col)
        return tot / len(list_of_columns)
    
    def get_nearby_columns(self, x, r):
        output = []
        for i in range(x-r, x+r+1):
            if 0 <= i < self.map_width:
                output.append(i)
        return output

    def get_smoothed_height(self, x, r):
        cols = self.get_nearby_columns(x,r)
        return int(self.get_mean_column_height(cols))

    def smooth_surface(self, r):
        new_heights = [0] * self.map_width
        for i in range(self.map_width):
            new_heights[i] = self.get_smoothed_height(i, r)
        for i in range(self.map_width):
            self.set_column_height(i, new_heights[i])

    def add_dirt_to_column(self, x):
        height = self.get_column_height(x)
        for j in range(self.map_height - height-4, self.map_height - height):
            self.set_block(x, j, 2)
        self.set_block(x, self.map_height - height - 5, 3)
        
    def add_dirt_to_map(self):
        for i in range(self.map_width):
            self.add_dirt_to_column(i)

# Cave generation
    def get_random_block(self):
        while True:
            i = random.randint(0, self.map_width-1)
            j = random.randint(0, self.map_height-1)
            if not self.is_empty(i, j):
                return i, j
            
    def get_random_end_point(self, start_point, box_length):
        while True:
            x_disp = random.randint(-box_length,box_length)
            y_disp = random.randint(-box_length, box_length)
            end_point = (start_point[0] + x_disp, start_point[1] + y_disp)
            if end_point[0] in range(0,self.map_width) and end_point[1] in range(0, self.map_height) and end_point != \
                    start_point:
                return end_point

    def get_random_cave_skeleton(self, segment_count):
        start_point = self.get_random_block()
        i = 0
        vertices = []
        while i < segment_count:
            box_length = random.randint(5, 15)
            new_point = self.get_random_end_point(start_point, box_length)
            vertices.append(new_point)
            start_point = new_point
            i += 1
        return vertices
    
    def get_blocks_on_segment(self, start_point, end_point):
        blocks_on_segment = []
        disp = (end_point[0] - start_point[0], end_point[1]-start_point[1])
        disp_magnitude = (disp[0]**2 + disp[1]**2)**0.5
        unit_disp = (disp[0]/disp_magnitude, disp[1]/disp_magnitude)
        for i in range(int(disp_magnitude)+1):
            point = (int(round(start_point[0]+unit_disp[0]*i)), int(round(start_point[1] + unit_disp[1]*i)))
            if point not in blocks_on_segment:
                blocks_on_segment.append(point)
        return blocks_on_segment
    
    def get_blocks_on_skeleton(self, cave_skeleton):
        blocks = []
        for i in range(len(cave_skeleton)-1):
            for block in self.get_blocks_on_segment(cave_skeleton[i], cave_skeleton[i+1]):
                if block not in blocks:
                    blocks.append(block)
        return blocks

    def grow_set(self, blocks):
        new_blocks = []
        for block in blocks:
            for neighbour in self.get_neighbouring_coords(block[0], block[1]):
                if neighbour not in blocks:
                    new_blocks.append(neighbour)
        blocks = blocks + new_blocks
        return blocks

    def get_random_cave(self, segment_count, caveWidth):
        skeleton = self.get_random_cave_skeleton(segment_count)
        blocks = self.get_blocks_on_skeleton(skeleton)
        for i in range(caveWidth):
            blocks = self.grow_set(blocks)
            new_blocks = []
        for i in range(2):
            for block in blocks:
                if self.count_neighbours_in_cave(block,blocks) >= 4:
                    new_blocks.append(block)
        return new_blocks
    
    def count_neighbours_in_cave(self, block, cave):
        count = 0
        for i in range(block[0] - 1, block[0]+2):
            for j in range(block[1]-1, block[1]+2):
                if (not (i == block[0] and j == block[1])) and (i, j) in cave:
                    count += 1
        return count
    
    def count_empty_neighbours(self, x, y, scope):
        # Counts the number of empty spaces around (x,y), in the set of blocks in scope
        count = 0
        for (i, j) in self.get_neighbouring_coords(x, y):
            if self.is_empty(i, j) and (i, j) in scope:
                count += 1
        return count

    def get_smoothed_value(self, coords, scope):
        neighbours = 8 - self.count_empty_neighbours(coords[0], coords[1], scope)
        if neighbours > 4:
            return 1
        else:
            return 0

    '''def smoothScope(self,scope):
        newMap = Map(self.map_width,self.map_height)
        for i in range(self.map_width):
            for j in range(self.map_height):
                if (i,j) in scope:
                    newMap.set_block(i,j,self.get_smoothed_value((i,j),scope))
                else:
                    newValue = self.get_block_value(i,j)
                    newMap.set_block(i,j,newValue)
        self.map = newMap.map'''
        

# Main generation functions

    def generate_surface(self):
        self.set_all_columns(int(self.map_height/2))
        for i in range(5):
            self.add_noise_to_map(2**(4-i), 2**(4-i))
        self.smooth_surface(30)
        for i in range(self.map_width):
            self.set_surface_height(i, self.get_column_height(i))
        self.add_dirt_to_map()
            
    def generate_caves(self):
        for i in range(int(self.map_width/40)):
            cave = self.get_random_cave(random.randint(3, 15), random.randint(1, 2))
            for block in cave:
                self.set_block(block[0], block[1], 0)

    def full_generation(self):
        self.generate_surface()
        self.generate_caves()

# Draw the map

    def get_screen_coords(self, x, y, block_length):
        return x*block_length, y*block_length
    
    def get_screen_colour(self, x, y):
        val = self.get_block_value(x, y)
        if val == 0:
            if y > self.map_height - self.get_surface_height(x):
                return 130, 130, 130  # rock in cave
            elif self.map_height - self.get_surface_height(x) - 5 < y <= self.map_height - self.get_surface_height(x):
                return 150, 100, 0  # dirt in cave
            else:
                return 115, 233, 255  # sky
        elif val == 1:
            return 50, 50, 50  # rock
        elif val == 2:
            added_brightness = 2 * (self.map_height - self.get_surface_height(x) - y)  # takes values 0 to 4 inc
            return 100 + added_brightness, 70 + added_brightness, 0  # dirt
        elif val == 3:
            return 42, 208, 0  # grass
        
    def draw(self, block_length):
        screen_width = block_length * self.map_width
        screen_height = block_length * self.map_height
        screen = pygame.display.set_mode((screen_width, screen_height))
        for i in range(self.map_width):
            for j in range(self.map_height):
                pygame.draw.rect(screen, self.get_screen_colour(i, j), (i * block_length, j*block_length, block_length, block_length))
                pygame.display.update()

    
        
        




    
