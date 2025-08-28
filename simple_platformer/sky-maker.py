# create_sky_sprite.py

# We need the 'Image' tool from the Pillow library
from PIL import Image

print("Starting sky sprite generation...")

# --- 1. Define the 32x32 color data (the same as before) ---
sky_color_top = (40, 60, 120) 
sky_color_bottom = (135, 206, 235)

sky_sprite_data = []
SPRITE_HEIGHT = 32
SPRITE_WIDTH = 32

for y in range(SPRITE_HEIGHT):
    gradient_position = y / (SPRITE_HEIGHT - 1)

    current_r = sky_color_top[0] + (sky_color_bottom[0] - sky_color_top[0]) * gradient_position
    current_g = sky_color_top[1] + (sky_color_bottom[1] - sky_color_top[1]) * gradient_position
    current_b = sky_color_top[2] + (sky_color_bottom[2] - sky_color_top[2]) * gradient_position

    row_color = (int(current_r), int(current_g), int(current_b))
    
    pixel_row = [row_color] * SPRITE_WIDTH
    sky_sprite_data.append(pixel_row)

# --- 2. Create a new, blank image object ---
# We tell Pillow we want an 'RGB' image with a size of 32x32 pixels
image = Image.new('RGB', (SPRITE_WIDTH, SPRITE_HEIGHT))

# --- 3. "Paint" our color data onto the blank image, pixel by pixel ---
for y in range(SPRITE_HEIGHT):
    for x in range(SPRITE_WIDTH):
        # Get the color for this pixel from our data list
        color = sky_sprite_data[y][x]
        # Place the color at the (x, y) coordinate
        image.putpixel((x, y), color)

# --- 4. Save the completed image to a file ---
# The file will be saved inside the 'images' folder so our game can find it.
image.save('images/sky.png')

print("Successfully created 'images/sky.png'!")