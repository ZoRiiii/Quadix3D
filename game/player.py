from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from game.voxel import blocks

"""
    Я даже близко не врубаюсь как сделать инвентарь... нормальным.
"""

class Player:
    def __init__(self):
        self.player = FirstPersonController(
            height=1.8,
            jump_height=1.25,
            mouse_sensitivity=Vec2(40, 40)
        )
        self.player.camera_pivot.y = 1.7

        self.default_fov = 90
        self.zoom_fov = 30
        self.zooming = False

        self.sneak_amount = 0.2
        self.original_camera_y = self.player.camera_pivot.y
        self.is_sneaking = False

        self.player.flying = False
        self.player.sprint_speed = 10
        self.player.sneak_speed = 2
        self.player.normal_speed = 5
        self.player.fly_speed = 5

        self.respawn()

        current_texture_index = 0

        """
            STOOPID INVENTORY
        """

        self.current_texture_index = 0

        self.hotbar_slots = []
        for i in range(9):
            self.slot = Entity(
                parent=camera.ui,
                model='quad',
                texture=blocks[i % len(blocks)],
                scale=(0.05, 0.05),
                x=-0.4 + i * 0.08,
                y=-0.45,
                z=-1
            )
            self.slot.block_index = i % len(blocks)
            self.hotbar_slots.append(self.slot)

        self.selector = Entity(
            parent=camera.ui,
            model='quad',
            color=color.white,
            scale=(0.055, 0.055),
            x=-0.4 + current_texture_index * 0.08,
            y=-0.45,
            z=-0.9
        )

        self.inventory_bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.color(0, 0, 0.1, 0.8),
            scale=(0.5, 0.6),
            position=(0, 0, -0.5),
            visible=False
        )

        self.inventory_bg.enabled = False

        self.inventory_slots = []
        for i, block in enumerate(blocks):
            self.row = i // 5
            self.col = i % 5
            self.x = -0.2 + self.col * 0.1
            self.y = 0.2 - self.row * 0.1
            
            self.slot = Button(
                parent=self.inventory_bg,
                model='quad',
                texture=block,
                scale=(0.09 , 0.075),
                position=(self.x, self.y, -0.1),
                color=color.white,
                origin=(0, 0)  
            )
            self.slot.block_index = i
            self.inventory_slots.append(self.slot)

    def respawn(self):
        # Center of platform MF
        # DO NOT SAY ANYTHING ABOUT MAGIC NUMBERS, IDIOT
        self.player.position = (15, 2, 15)
        self.player.velocity_y = 0

    def control(self):
        # Control 
        if held_keys['control']:
            self.player.speed = self.player.sprint_speed

            if self.is_sneaking:
                self.is_sneaking = False
                self.player.camera_pivot.y = self.original_camera_y

        # Shift
        elif held_keys['shift'] and not self.player.flying:
            self.player.speed = self.player.sneak_speed

            if not self.is_sneaking:
                self.is_sneaking = True
                self.player.camera_pivot.y = self.original_camera_y - self.sneak_amount

        else:
            self.player.speed = self.player.normal_speed

            if self.is_sneaking:
                self.is_sneaking = False
                self.player.camera_pivot.y = self.original_camera_y

        # C (Zoom)
        if held_keys['c']:
            if not self.zooming:
                self.zooming = True
                self.camera.fov = self.zoom_fov
        else:
            if self.zooming:
                self.zooming = False
                self.camera.fov = self.default_fov

        if self.player.flying:
            if held_keys['space']:
                self.player.y += self.player.fly_speed * time.dt
            if held_keys['shift']:
                self.player.y -= self.player.fly_speed * time.dt

    def ursina_control(self, key):
        # Переключение полёта
        if key == 'v':
            self.player.flying = not self.player.flying
            self.player.gravity = 0 if self.player.flying else 1.0

            if not self.player.flying and self.is_sneaking:
                self.player.camera_pivot.y = self.original_camera_y

        # Респавн
        elif key == 'r':
            self.respawn()

        # Инвентарь
        elif key == 'e':
            self.toggle_inventory()

        # Выбор хотбара через цифры
        elif key in ['1','2','3','4','5','6','7','8','9']:
            self.current_texture_index = int(key) - 1

        # Скролл (только если инвентарь закрыт)
        elif key == 'scroll down' and not self.inventory_bg.visible:
            self.current_texture_index = (self.current_texture_index + 1) % 9

        elif key == 'scroll up' and not self.inventory_bg.visible:
            self.current_texture_index = (self.current_texture_index - 1) % 9

        # Закрыть инвентарь на Esc
        elif key == 'escape':
            if self.inventory_bg.visible:
                self.toggle_inventory()

        # Клик по слоту инвентаря
        elif key == 'left mouse down' and self.inventory_bg.visible:
            self.select_block_from_inventory()

            
    def toggle_inventory(self):
        self.inventory_bg.visible = not self.inventory_bg.visible
        self.inventory_bg.enabled = self.inventory_bg.visible 
        mouse.locked = not self.inventory_bg.visible
        self.player.enabled = not self.inventory_bg.visible

        for slot in self.inventory_slots:
            slot.enabled = self.inventory_bg.visible

    def select_block_from_inventory(self):
        if mouse.hovered_entity in self.inventory_slots:
            self.clicked_block_index = mouse.hovered_entity.block_index
            self.hotbar_slots[self.current_texture_index].texture = blocks[self.clicked_block_index]
            self.hotbar_slots[self.current_texture_index].block_index = self.clicked_block_index
            texture_index = self.hotbar_slots[self.current_texture_index].block_index

    def update(self):
        self.selector.x = -0.4 + self.current_texture_index * 0.08

    def get_position(self):
        return self.player.position
    
    def get_speed(self):
        return self.player.speed
    
    def get_fly_status(self):
        return self.player.flying
    
    def get_y_pivot(self):
        return self.player.camera_pivot.y
    
    def get_inventory(self):
        return self.inventory_bg
    
    def set_texture_index(self, index):
        self.current_texture_index = index

        global texture_index
        texture_index = index

    def get_texture_index(self):
        return self.current_texture_index