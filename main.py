from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController as FPC
from ursina.mesh_importer import *

#create an app

app = Ursina()

textures = {1: load_texture("minecraft_assets/Assets/Textures/Grass_Block.png"), 
          2: load_texture("minecraft_assets/Assets/Textures/Dirt_Block.png"), 
          3: load_texture("minecraft_assets/Assets/Textures/Brick_BLock.png"), 
          4: load_texture("minecraft_assets/Assets/Textures/Stone_Block.png"),
          5: load_texture("minecraft_assets/Assets/Textures/Wood_Block.png"),
          6: load_texture("minecraft_assets/Assets/Textures/carrot side.png")
          }

# create a sky entity
sky_textures = load_texture("minecraft_assets/Assets/Textures/Skybox.png")
# walking sound for the player
walk_sound = Audio("minecraft_assets/Assets/SFX/Punch_sound.wav")

block_pick = 1


class Block(Button):
    def __init__(self, position=(0,0,0), texture= textures[1]):
        super().__init__(parent=scene, 
                         position=position,
                         model= "minecraft_assets/Assets/Models/Block",
                         origin_y = 0.5,
                         texture = texture,
                         color = color.color(0,0,random.uniform(0.9,1)),
                         scale = 0.5)


    def input(self, key):
        if self.hovered:
            if key == "right mouse down":
                walk_sound.play()
                new_block = Block(position=self.position + mouse.normal, texture = textures[block_pick])

            elif key == "left mouse down":
                walk_sound.play()
                destroy(self)

# sky class

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=sky_textures,
            scale = 150,
            double_sided = True
        )
        print(f"Sky entity created with model: {self.model}, texture: {self.texture}")
        print(f"Sky texture loaded: {sky_textures}")


class Tree(Entity):
    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent = scene,
            position=position, # type: ignore
            model = "Assets/Models/Lowpoly_tree_sample.obj",
            texture=sky_textures,
            scale = (1,1,1)
        )
#grid
def generate_trees(num_trees = 10, terrain_size= 30):
    for _ in range(num_trees):
        x = random.randint(0, terrain_size-1)
        y = 0.5
        z =  random.randint(0, terrain_size-1)
        Tree(position = (x,y,z))

generate_trees()

# def generate_terrain():
#     for z in range(40):
#         for x in range(40):
#             height = random.randint(1,5)
#             for y in range(10):
#                 block = Block(position = (x,height, z))

# generate_terrain()


for z in range(40):
    for x in range(40):
        block = Block(position=(x,0,z))


player = FPC(postion=(25,50,25))
player.speed = 5

sky = Sky() 

def update():
    global block_pick
    
    if held_keys["escape"]:
        application.quit()

    for i in range(1,7):
        if held_keys[str(i)]:
            block_pick = i
            block = Text(
              text = str(str(textures[i]).replace("minecraft_assets/Assets/Textures/","")),
                scale = 1,
                
                origin = (0,16),
                background = False,
                color=color.white.tint(0.5),
                )

            destroy(block, delay = 1)
            break

    if held_keys["r"]:
        player.speed = 10
    elif held_keys["r"] == False:
        player.speed = 3

    

app.run()

