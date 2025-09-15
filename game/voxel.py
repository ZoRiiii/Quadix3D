from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

blocks = ['grass', 'stone', 'dirt', 'planks', 'log', 'leaves', 'emerald_ore', 'dern', 'furnace', 'cooper_ore', 'aluminum_ore', 'gold_ore', 'iron_ore']

class Voxel(Entity):
    def __init__(self, position=(0,0,0), texture='grass', world=None, player=None):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture=texture,
            origin_y=0.5,
            scale=1.0,
            collider='box'
        )
        
        self.world = world
        self.player = player
        self.texture_name = texture
        
        self.highlight = Entity(
            parent=self,
            model='cube',
            color=color.rgba(0, 0, 0, 0.25),
            scale=1.001,
            origin_y=0.49995,
            visible=False
        )
    
    def update(self):
        if mouse.hovered_entity == self and isinstance(mouse.hovered_entity, Voxel):
            self.highlight.visible = True
        else:
            self.highlight.visible = False
    
    def input(self, key):
        if self.player and self.player.inventory_bg.visible:
            return

        if key == 'left mouse down' and mouse.hovered_entity == self:
            if self.world and hasattr(self.world, 'boxes') and self in self.world.boxes:
                self.world.boxes.remove(self)
            destroy(self)

        if key == 'right mouse down' and mouse.hovered_entity == self:
            if self.player and self.world:
                new_pos = self.position + mouse.normal
                current_texture = blocks[self.player.get_texture_index()]
                new_block = Voxel(
                    position=new_pos,
                    texture=current_texture,
                    world=self.world,
                    player=self.player
                )
                self.world.boxes.append(new_block)