from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()
window.color = color.hex("#87CEEB")
window.icon = 'resources/logo.png'
window.title = 'Quadix'

Texture.default_path = './resources/'
Audio.default_path = './resources/'

place_sound = Audio('place_block.mp3', autoplay=False)
destroy_sound = Audio('destroy_block.mp3', autoplay=False)

blocks = ['grass', 'stone', 'dirt', 'planks', 'log', 'leaves', 'emerald_ore', 'dern', 'furnace']
current_texture_index = 0

for i in range(9):
    block_idx = i % len(blocks)
    Entity(
        parent=camera.ui,
        model='quad',
        texture=blocks[block_idx],
        scale=(0.05, 0.05),
        x=-0.4 + i * 0.08,
        y=-0.45,
        z=-1,
        texture_scale=(1, 1)
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
player.fly_speed = 2

def update():
    selector.x = -0.4 + current_texture_index * 0.08
    if player.flying:
        if held_keys['w']: player.position += player.forward * player.fly_speed * time.dt
        if held_keys['s']: player.position -= player.forward * player.fly_speed * time.dt
        if held_keys['space']: player.position += player.up * player.fly_speed * time.dt
        if held_keys['shift']: player.position -= player.up * player.fly_speed * time.dt
        if held_keys['a']: player.position -= player.right * player.fly_speed * time.dt
        if held_keys['d']: player.position += player.right * player.fly_speed * time.dt

boxes = []
for i in range(30):
    for j in range(30):
        box = Button(
            color=color.white,
            model='cube',
            position=(j, 0, i),
            texture='grass.png',
            parent=scene,
            origin_y=0.5
        )
        boxes.append(box)

def input(key):
    global current_texture_index
    for box in boxes:
        if box.hovered:
            if key == 'right mouse down':
                new = Button(
                    color=color.white,
                    model='cube',
                    position=box.position + mouse.normal,
                    texture=blocks[current_texture_index],
                    parent=scene,
                    origin_y=0.5
                )
                boxes.append(new)
                place_sound.play()
            if key == 'left mouse down':
                boxes.remove(box)
                destroy(box)
                destroy_sound.play()
    
    if key == 'scroll down': current_texture_index = (current_texture_index + 1) % len(blocks)
    if key == 'scroll up': current_texture_index = (current_texture_index - 1) % len(blocks)
    if key == 'escape': application.quit()
    if key == 'alt': 
        player.flying = not player.flying
        player.gravity = 0 if player.flying else 9.8

app.run()