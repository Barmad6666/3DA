from ursina import *
import pymongo
app = Ursina() 
block_num = 1
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["3DA_db"]
mycol = mydb["blocks"]
clobbestone=load_texture('pics/brick2_texture.jpg')
grass= load_texture('pics/grass_texture.jpg')
dirt= load_texture("pics/dirt.jpg")
oak_log=load_texture('pics/wood.jpg')
quarts=load_texture('pics/Quarts.png')
oak_plank=load_texture('pics/oak plank.jpg')
brich_log=load_texture('pics/brich log.png')


class Block(Entity):
    def __init__(self, position=(0, 0, 0), texture=grass):
        super().__init__(
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=1.0,
            collider='box'  # Add a collider to the block
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if block_num==1: create_grass_block(self.position + mouse.normal, grass)
                if block_num==2: create_grass_block(self.position + mouse.normal, clobbestone)
                if block_num==3: create_grass_block(self.position + mouse.normal, dirt)
                if block_num==4: create_grass_block(self.position + mouse.normal, oak_log)
                if block_num==5: create_grass_block(self.position + mouse.normal, oak_plank)
                if block_num==6: create_grass_block(self.position + mouse.normal, quarts)
                if block_num==7: create_grass_block(self.position + mouse.normal, brich_log)
            
            if key == 'right mouse down':
                destroy(self)
                mycol.delete_one(self.__dict__)
def create_grass_block(position, bl):
    grass_block = Block(position=position, texture=bl)
    blocks.append(grass_block)
    mycol.insert_one(grass_block.__dict__)
blocks=[]
b=Block((0,0,0), grass)
print(b.__dict__)