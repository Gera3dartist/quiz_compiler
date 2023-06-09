from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from src.constants import FONT_PATH, FONT_SIZE


def get_build_directory() -> Path:
    """
    Returns build directory creates directory if not exists
    """

    build_dir = Path(__file__).parent.parent / 'build'
    if not build_dir.exists():
        build_dir.mkdir()
    return build_dir

def get_image_directory(subfolder: str = None) -> Path:
    """
    Returns image directory creates directory if not exists
    """
    if subfolder is None:
        image_dir = get_build_directory() / 'images' 
    else:
        image_dir = get_build_directory() / 'images' / subfolder
    if not image_dir.exists():
        image_dir.mkdir()
    return image_dir


def get_image_path(name: str, subfolder: str = None) -> Path:
    """
    Returns image path 
    """
    
    return get_image_directory(subfolder) / name


def get_font_directory() -> Path:
    """
    Returns build directory creates directory if not exists
    """

    font_dir = Path(__file__).parent.parent / 'fonts'
    if not font_dir.exists():
        raise ValueError("Fonts directory does not exist")
    return font_dir

def generate_random_name() -> str:
    """
    Generates random name for the image
    """
    import uuid
    return str(uuid.uuid4())


def create_image_from_multiline_text(
        state_name: str,
        text: str, 
        font_size=FONT_SIZE, 
        padding=10, 
        font_path=None,  
        image_name: str = None) -> Path:
    # Set the font
    if font_path is None:
        font_path = get_font_directory() / FONT_PATH
    font = ImageFont.truetype(str(font_path), font_size)

    # Calculate the size of the text
    lines = text.split('\n')
    line_height = font.getsize('hg')[1]
    width = max(font.getsize(line)[0] for line in lines) + 2 * padding
    height = len(lines) * line_height + 2 * padding

    # Create the image
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    # Draw the text
    y = padding
    for line in lines:
        draw.text((padding, y), line, fill='black', font=font)
        y += line_height
    image_path = get_image_path(image_name or generate_random_name(), subfolder=state_name)
    image.save(image_path)
    return image_path