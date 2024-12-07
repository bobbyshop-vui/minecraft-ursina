from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# Khởi tạo Ursina engine
app = Ursina()

# Thiết lập bầu trời
sky = Entity(model='plane', texture='sky', scale=100, rotation_x=90)

# Khối block đơn giản
class Block(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture='white_cube',
            color=color.hsv(0, 0, random.uniform(0.9, 1)),
            highlight_color=color.lime,
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
            elif key == 'right mouse down':
                Block(position=self.position + mouse.normal)

# Tạo thế giới vô hạn
def generate_world(x_start, z_start, size=8):
    for z in range(size):
        for x in range(size):
            Block(position=(x + x_start, 0, z + z_start))

# Lưu vị trí đã tạo khối để theo dõi
created_chunks = set()

# Tạo chunk đầu tiên
generate_world(0, 0)

# Lưu vị trí bắt đầu
start_position = Vec3(0, 1, 0)  # Đặt vị trí bắt đầu cao hơn một chút để tránh rơi
player = FirstPersonController(position=start_position)

# Cập nhật game
def update():
    if held_keys['escape']:
        application.quit()  # Thoát game khi nhấn ESC

    # Kiểm tra vị trí của nhân vật và tải thêm khối
    player_chunk_x = int(player.x // 50) * 50
    player_chunk_z = int(player.z // 50) * 50

    if (player_chunk_x, player_chunk_z) not in created_chunks:
        created_chunks.add((player_chunk_x, player_chunk_z))
        generate_world(player_chunk_x, player_chunk_z)

    # Kiểm tra nếu nhân vật rơi ra khỏi thế giới
    if player.y < -10:  # Nếu nhân vật rơi xuống dưới y = -10
        player.position = start_position  # Đưa nhân vật trở lại vị trí bắt đầu

# Chạy game
app.run()
