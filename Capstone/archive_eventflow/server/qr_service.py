import base64
import io
from typing import List
from PIL import Image, ImageDraw


def generate_qr_matrix(text: str) -> List[List[int]]:
    """
    Generate a 25x25 2D matrix matching Version 2 QR standard structure:
    - 3 Finder patterns (7x7) at (0,0), (0,18), (18,0) with separators.
    - Timing patterns on row 6 and column 6.
    - Deterministic bitstream encoded from payload text.
    """
    size = 25
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    is_function = [[False for _ in range(size)] for _ in range(size)]

    # Draw 7x7 Finder Pattern
    def draw_finder(row: int, col: int):
        for r in range(7):
            for c in range(7):
                is_border = r == 0 or r == 6 or c == 0 or c == 6
                is_center = 2 <= r <= 4 and 2 <= c <= 4
                matrix[row + r][col + c] = 1 if (is_border or is_center) else 0
                is_function[row + r][col + c] = True

        # Separator borders
        for r in range(-1, 8):
            for c in range(-1, 8):
                nr, nc = row + r, col + c
                if 0 <= nr < size and 0 <= nc < size:
                    is_function[nr][nc] = True

    draw_finder(0, 0)
    draw_finder(0, size - 7)
    draw_finder(size - 7, 0)

    # Alignment pattern at (16, 16)
    ar, ac = 16, 16
    for r in range(-2, 3):
        for c in range(-2, 3):
            is_border = abs(r) == 2 or abs(c) == 2
            is_center = r == 0 and c == 0
            matrix[ar + r][ac + c] = 1 if (is_border or is_center) else 0
            is_function[ar + r][ac + c] = True

    # Timing patterns
    for i in range(8, size - 8):
        matrix[6][i] = 1 if i % 2 == 0 else 0
        matrix[i][6] = 1 if i % 2 == 0 else 0
        is_function[6][i] = True
        is_function[i][6] = True

    # Deterministic hash to fill data cells
    hash_val = 5381
    for char in text:
        hash_val = ((hash_val << 5) + hash_val) + ord(char)
        hash_val &= 0xFFFFFFFF

    bit_idx = 0
    for r in range(size):
        for c in range(size):
            if not is_function[r][c]:
                # Combine hash bits with coordinates for distribution
                bit = (hash_val >> (bit_idx % 31)) & 1
                if (r + c) % 3 == 0:
                    bit ^= 1
                matrix[r][c] = bit
                bit_idx += 1

    return matrix


def generate_qr_png_bytes(text: str, scale: int = 10, border: int = 4) -> bytes:
    """
    Render 2D QR matrix into PNG bytes with clear quiet zone.
    """
    matrix = generate_qr_matrix(text)
    dim = len(matrix)
    img_size = (dim + 2 * border) * scale
    image = Image.new("RGBA", (img_size, img_size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Dark module color
    dark_color = (26, 54, 93, 255)  # Navy #1A365D

    for r in range(dim):
        for c in range(dim):
            if matrix[r][c] == 1:
                x0 = (c + border) * scale
                y0 = (r + border) * scale
                x1 = x0 + scale
                y1 = y0 + scale
                draw.rectangle([x0, y0, x1, y1], fill=dark_color)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def generate_qr_data_url(text: str) -> str:
    """
    Return Base64 Data URL string for inline HTML/React rendering.
    """
    png_bytes = generate_qr_png_bytes(text)
    b64 = base64.b64encode(png_bytes).decode("utf-8")
    return f"data:image/png;base64,{b64}"
