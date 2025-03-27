from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

class Voxel(Entity):
    def __init__(self, position=(0,0,0), texture='grass'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture=texture,
            origin_y=0.5,
            scale=1.0,
            collider='box'
        )
        # Выделение блока
        self.highlight = Entity(
            parent=self,
            model='cube',
            color=color.rgba(0, 0, 0, 0.3),
            scale=1.01,
            origin_y=0.49, 
            visible=False
        )
    
    def update(self):
        self.highlight.visible = mouse.hovered_entity == self
    
    def input(self, key):
        if key == 'left mouse down' and mouse.hovered_entity == self:
            destroy(self)
            destroy_sound.play()
            if self in boxes:
                boxes.remove(self)
        
        if key == 'right mouse down' and mouse.hovered_entity == self:
            new_pos = self.position + mouse.normal
            Voxel(position=new_pos, texture=blocks[current_texture_index])
            place_sound.play()

# Настройки игрока
player = FirstPersonController(
    height=1.8,
    jump_height=1.25,
    origin_y=-0.5,
    mouse_sensitivity=Vec2(40, 40)
)

# Настройки зума
default_fov = 90
zoom_fov = 30
zooming = False

# Настройки приседания
sneak_amount = 0.4
original_camera_y = player.camera_pivot.y
is_sneaking = False

window.color = color.hex("#87CEEB")
window.title = 'Quadix'
window.exit_button.visible = False

Texture.default_path = './resources/'
Audio.default_path = './resources/'
place_sound = Audio('place_block.mp3', autoplay=False)
destroy_sound = Audio('destroy_block.mp3', autoplay=False)

blocks = ['grass', 'stone', 'dirt', 'planks', 'log', 'leaves', 'emerald_ore', 'dern', 'furnace']
current_texture_index = 0

# Хотбар
for i in range(9):
    Entity(
        parent=camera.ui,
        model='quad',
        texture=blocks[i % len(blocks)],
        scale=(0.05, 0.05),
        x=-0.4 + i * 0.08,
        y=-0.45,
        z=-1
    )

selector = Entity(
    parent=camera.ui,
    model='quad',
    color=color.white,
    scale=(0.055, 0.055),
    x=-0.4 + current_texture_index * 0.08,
    y=-0.45,
    z=-0.9
)

player.flying = False
player.sprint_speed = 8
player.sneak_speed = 2
player.normal_speed = 5
player.fly_speed = 5

# Создаем платформу 
platform_position = (15, 0.5, 15)
boxes = []
for i in range(30):
    for j in range(30):
        box = Voxel(
            position=(platform_position[0] + j - 15, platform_position[1], platform_position[2] + i - 15),
            texture='grass'
        )
        boxes.append(box)

def respawn_player():
    player.position = (platform_position[0], platform_position[1] + 5, platform_position[2])
    player.velocity_y = 0

def update():
    global zooming, is_sneaking
    
    selector.x = -0.4 + current_texture_index * 0.08
    
    # Управление скоростью и приседанием
    if held_keys['control']:
        player.speed = player.sprint_speed
        if is_sneaking:
            is_sneaking = False
            player.camera_pivot.y = original_camera_y
    elif held_keys['shift'] and not player.flying:
        player.speed = player.sneak_speed
        if not is_sneaking:
            is_sneaking = True
            player.camera_pivot.y = original_camera_y - sneak_amount
    else:
        player.speed = player.normal_speed
        if is_sneaking:
            is_sneaking = False
            player.camera_pivot.y = original_camera_y
    
    # Управление зумом
    if held_keys['c']:
        if not zooming:
            zooming = True
            camera.fov = zoom_fov
    else:
        if zooming:
            zooming = False
            camera.fov = default_fov
    
    # Управление полетом
    if player.flying:
        if held_keys['space']:
            player.y += player.fly_speed * time.dt
        if held_keys['shift']:
            player.y -= player.fly_speed * time.dt

def input(key):
    global current_texture_index
    
    if key in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        current_texture_index = int(key) - 1
    
    if key == 'scroll down':
        current_texture_index = (current_texture_index + 1) % len(blocks)
    if key == 'scroll up':
        current_texture_index = (current_texture_index - 1) % len(blocks)
    if key == 'escape':
        application.quit()
    if key == 'v':
        player.flying = not player.flying
        player.gravity = 0 if player.flying else 1.0
        if not player.flying and is_sneaking:
            player.camera_pivot.y = original_camera_y
    if key == 'r':
        respawn_player()

respawn_player()
app.run()