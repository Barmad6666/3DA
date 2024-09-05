from ursina import Entity,Ursina,load_texture,camera,random,mouse,Sky,color,destroy,Vec3,held_keys,application,print_on_screen
from pymongo import MongoClient
app = Ursina() 
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["3DA_db"]
mycol = mydb["blocks"]
clobbestone=load_texture('pics/brick2_texture.png')
grass= load_texture('pics/grass_texture.png')
dirt= load_texture("pics/dirt.png")
oak_log=load_texture('pics/wood.png')
quarts=load_texture('pics/Quarts.png')
oak_plank=load_texture('pics/oak plank.png')
brich_log=load_texture('pics/brich log.png')
class Inventory(Entity):

    def __init__(self,position=(-.8,-.3),texture=grass, ):
        super().__init__(           
            parent = camera.ui ,                            
            model = 'quad'  ,
            scale = (.1,.1),                                           
            origin = (-.5, .5),                                         
            position = position,                                        
            texture = texture   ,                                
            texture_scale = (1,1),  
                                                

            )



Sky()


i1 = Inventory((-.8,-.3),grass)  
i2 = Inventory((-.6,-.3),clobbestone)   
i3 = Inventory((-.4,-.3),dirt)   
i4 = Inventory((-.2,-.3),oak_log)   
i5 = Inventory((-.0,-.3),oak_plank)   
i6 = Inventory((.2,-.3),quarts)   
i7 = Inventory((.4,-.3),brich_log)  

class Block(Entity):
    def __init__(self, position=(0, 0, 0), texture=grass):
        super().__init__(
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=1.0,
            collider='box' 
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if block_num==1: create_grass_block(self.position + mouse.normal, grass, e)
                if block_num==2: create_grass_block(self.position + mouse.normal, clobbestone, e)
                if block_num==3: create_grass_block(self.position + mouse.normal, dirt, e)
                if block_num==4: create_grass_block(self.position + mouse.normal, oak_log, e)
                if block_num==5: create_grass_block(self.position + mouse.normal, oak_plank, e)
                if block_num==6: create_grass_block(self.position + mouse.normal, quarts, e)
                if block_num==7: create_grass_block(self.position + mouse.normal, brich_log, e)
            if key == 'right mouse down':
                block_data = {
                "position": tuple(self.position),
                "texture": self.texture.name
                }
                mycol.delete_one(block_data)            
                destroy(self)

def create_grass_block(position, bl,e):
    grass_block = Block(position=position, texture=bl)
    blocks.append(grass_block)
    if not e:
        bb={
            "position":tuple(grass_block.position),
            "texture":grass_block.texture.name
        }
        mycol.insert_one(bb)
    else:
        return


blocks = []
e=False
for i in mycol.find():
    create_grass_block(i["position"], i["texture"], e)
    if -16<= i["position"][0] <= 16 and i["position"][1]==0 and -16<= i["position"][2] <= 16 :
        e=True
for x in range(-16, 16):
    for z in range(-16, 16):
        create_grass_block((x, 0, z),grass, e)
e=False


chunk_size = 16
chunks = {}



def remove_distant_chunks(player_position, max_distance):
    chunks_to_remove = []
    
    for chunk_position, chunk_blocks in list(chunks.items()):
        chunk_center = Vec3(chunk_position[0] + chunk_size / 2, 0, chunk_position[1] + chunk_size / 2)
        distance = player_position - chunk_center
        
        if distance.length() > max_distance:
            print(f"Removing chunk at {chunk_position}, distance: {distance.length()}")  # Debug output
            chunks_to_remove.append(chunk_position)
    
    for chunk_position in chunks_to_remove:
        chunk_blocks = chunks.pop(chunk_position)
        for block in chunk_blocks:
            block_data = {
                "position": tuple(block.position),
                "texture": block.texture.name
            }
            # Debugging output
            print(f"Deleting block at {block.position} from database.")
            result = mycol.delete_one(block_data)
            print(f"Deleted {result.deleted_count} block(s) from database.")
            destroy(block)

def generate_chunk(position):
    chunk_blocks = []
    for x in range(position[0], position[0] + chunk_size):
        for z in range(position[1], position[1] + chunk_size):
            existing_block = mycol.find_one({"position": (x, 0, z)})
            if existing_block:
                create_grass_block((x, 0, z), load_texture(existing_block["texture"]), e)
            else:
                create_grass_block((x, 0, z), grass, e)
    chunks[position] = chunk_blocks
from ursina.prefabs.first_person_controller import FirstPersonController

player = FirstPersonController()
block_list=[]

ggggg=player.gravity
respawn_threshold = -20  
block_num=1


def update():
    global block_list
    global player
    global block_num

    if held_keys['1']:
        block_num=1
        print_on_screen(text="grass",position=(-.1,-.1),scale=3)
    if held_keys['2']:
        block_num=2 
        print_on_screen(text="cobblestone",position=(-.2,-.1),scale=3)
    if held_keys['3']:
        block_num=3 
        print_on_screen(text="dirt",position=(-.1,-.1),scale=3)
    if held_keys['4']:
        block_num=4 
        print_on_screen(text="oak log",position=(-.2,-.1),scale=3)
    if held_keys['5']:
        block_num=5 
        print_on_screen(text="oak plank",position=(-.1,-.1),scale=3)
    if held_keys['6']:
        block_num=6 
        print_on_screen(text="quarts",position=(-.1,-.1),scale=3)
    if held_keys['7']:
        block_num=7 
        print_on_screen(text="brich log",position=(-.1,-.1),scale=3)
    
    if held_keys["q"]:
        player.gravity=0
        
    if held_keys["e"]:
        player.gravity=ggggg
    # ==================
    if held_keys['escape']:
        application.quit()

    player_position = player.position
    max_distance = 32  
    player_chunk = (int(player_position.x // chunk_size) * chunk_size, int(player_position.z // chunk_size) * chunk_size)
    if player_chunk not in chunks:
        generate_chunk(player_chunk)
    if player_position.y < respawn_threshold:
        player.position = Vec3(random.randint(-16, 16), 10, random.randint(-16, 16))
app.run()