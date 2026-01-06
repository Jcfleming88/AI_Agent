import colorsys
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

'''
Example tools taken from the LangChain documentation.
'''

@dataclass
class HLS:
    h: float
    l: float
    s: float

@tool
def get_colour_hex(r: float, g: float, b: float) -> str:
    """
    Converts RGB float values (0 to 1) to a hexadecimal color string. Values outside of 0 to 1 are clamped.
    
    Args:
        r: Red component as a float between 0 and 1.
        g: Green component as a float between 0 and 1.
        b: Blue component as a float between 0 and 1.
    Returns:
        A string representing the color in hexadecimal format (e.g., "#rrggbb").
    """
    colour_array = [r, g, b]
    for i in range(3):
        if colour_array[i] < 0:
            colour_array[i] = 0
        elif colour_array[i] > 1:
            colour_array[i] = 1
    
    return '#%02x%02x%02x' % (int(colour_array[0] * 255), int(colour_array[1] * 255), int(colour_array[2] * 255))

@tool
def get_colour_hls(rgb: str) -> HLS:
    """
    Converts a hexadecimal color string to HLS (Hue, Lightness, Saturation) float values.
    
    Args:
        rgb: A string representing the color in hexadecimal format (e.g., "#rrggbb").
    Returns:
        A tuple of three floats representing Hue, Lightness, and Saturation (each between 0 and 1).
    """

    rgb = rgb.lstrip('#')
    r, g, b = tuple(int(rgb[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return HLS(h=h, l=l, s=s)

@tool
def get_random_colour(index: int) -> str:
    """
    Generates a unique and varied colour (in hex format) based on the provided index.
    
    Args:
        index: An integer representing the position in the sequence of colours.
    Returns:
        A string representing the colour in hexadecimal format (e.g., "#rrggbb").
    """
    golden_ratio = (1 + 5**0.5) / 2
    hue = (index * golden_ratio) % 1
    saturation = 0.8
    lightness = 0.6

    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return '#%02x%02x%02x' % (int(r * 255), int(g * 255), int(b * 255))

@tool
def get_opposite_colour(rgb: str) -> str:
    """
    Calculates the opposite colour (also known as a complementary colour) in hex format for a given hexadecimal color string.
    
    Args:
        rgb: A string representing the color in hexadecimal format (e.g., "#rrggbb").
    Returns:
        A string representing the opposite colour in hexadecimal format (e.g., "#rrggbb").
    """
    hls = get_colour_hls.invoke({"rgb": rgb})
    opposite_hue = (hls.h + 0.5) % 1.0
    r, g, b = colorsys.hls_to_rgb(opposite_hue, hls.l, hls.s)
    return get_colour_hex.invoke({"r": r, "g": g, "b": b})