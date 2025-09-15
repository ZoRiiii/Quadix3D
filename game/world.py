from ursina import *
from game.voxel import Voxel

class World:
    def __init__(self, player=None):
        self.boxes = []
        self.player = player
        self.create_platform()
    
    def create_platform(self):
        """Создает стартовую платформу"""
        platform_position = (15, 0, 15)
        for i in range(30):
            for j in range(30):
                box = Voxel(
                    position=(platform_position[0] + j - 15, 
                             platform_position[1], 
                             platform_position[2] + i - 15),
                    texture='grass',
                    world=self,
                    player=self.player 
                )
                self.boxes.append(box)
    
    def get_boxes(self):
        return self.boxes