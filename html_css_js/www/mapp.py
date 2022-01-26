OBSTACLE = -10
DESTINATION = -2
UNINITIALIZED = -1

def generate_field(terrain, walkable_fcn, pad=False):
    field = [[UNINITIALIZED if walkable_fcn(j) else OBSTACLE for j in i] for i in terrain]
    if pad:
        pad_field(field)
    return field 
        
def pad_field(field):
    for i in range(len(field)):
        field[i][0] = OBSTACLE
        field[i][-1] = OBSTACLE
    for j in range(len(field[0])):
        field[0][j] = OBSTACLE
        field[-1][j] = OBSTACLE

def load_obstacle_image(img_name, obstacle_colour=0xFFFFFF):
    import pygame
    image = pygame.surfarray.array3d(pygame.image.load(img_name))
    obstacle_colour = (obstacle_colour // 0x10000, obstacle_colour // 0x100 % 0x100, obstacle_colour % 0x100)

    return generate_field(image, lambda x:(x!=obstacle_colour).any(), pad=True) 

def init_map(map_name="map1"):    
    if map_name=="map1":
        MAP = [                       
        [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10], 
        [-10,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, -10], 
        [-10,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, -10], 
        [-10,  -1,  -1,  -1,  -1, -10,  -1,  -1,  -1, -10], 
        [-10,  -1,  -1,  -1,  -1, -10, -10,  -1,  -1, -10], 
        [-10,  -1,  -1, -10, -10, -10,  -1,  -1,  -1, -10], 
        [-10,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, -10], 
        [-10,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, -10], 
        [-10,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, -10], 
        [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10] ]
    elif map_name=="map2":
        print('ffffffffffff')
        MAP=[[1,2,3],[5,6,7]]
    else:
        MAP = load_obstacle_image('E:/Mohammed/Micro Controller/STM/Thesis/Master_Project/w/jps-master/'+map_name+'.png', 0xff0000)

    MAP_WIDTH,MAP_HEIGHT=len(MAP),len(MAP[0])
    return (MAP,MAP_WIDTH,MAP_HEIGHT)