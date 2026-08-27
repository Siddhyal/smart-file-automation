from PIL import Image, ImageDraw, ImageFont

SIZE = 512

image = Image.new(
    "RGBA",
    (SIZE, SIZE),
    (25, 25, 35, 255)
)

draw = ImageDraw.Draw(image)

# Main folder
draw.rounded_rectangle(
    (80, 150, 432, 400),
    radius=45,
    fill=(70, 130, 220, 255)
)

# Folder tab
draw.rounded_rectangle(
    (110, 110, 280, 190),
    radius=25,
    fill=(90, 150, 240, 255)
)

# Automation arrows
draw.line(
    (170, 275, 335, 275),
    fill="white",
    width=25
)

draw.polygon(
    [(335, 275), (295, 245), (295, 305)],
    fill="white"
)

draw.line(
    (335, 325, 170, 325),
    fill="white",
    width=25
)

draw.polygon(
    [(170, 325), (210, 295), (210, 355)],
    fill="white"
)

# Save icon
image.save(
    "smart_file_automation.ico",
    format="ICO",
    sizes=[
        (256, 256),
        (128, 128),
        (64, 64),
        (32, 32),
        (16, 16)
    ]
)

print("Icon created successfully!")