############################################################################# 
#
# VFRAME
# MIT License
# Copyright (c) 2020 Adam Harvey and VFRAME
# https://vframe.io 
#
#############################################################################

from dataclasses import dataclass
import colorsys
import random
import logging


@dataclass
class Color:
  r: float
  g: float
  b: float
  a: float=1.0

  
  def __post_init__(self):
    self.log = logging.getLogger('vframe')
    self.r = max(0.0, min(self.r, 1.0))
    self.g = max(0.0, min(self.g, 1.0))
    self.b = max(0.0, min(self.b, 1.0))
    self.a = max(0.0, min(self.a, 1.0))

  
  def to_rgb_int(self):
    """RGB normalized values
    :returns tuple of int RGB values in (255, 255, 255) scale
    """
    rgb_int = (int(255 * self.r), int(255 * self.g), int(255 * self.b))
    return rgb_int


  def to_bgr_int(self):
    """BGR normalized values
    :returns tuple of int RGB values in (255, 255, 255) scale
    """
    bgr_int = (int(255 * self.b), int(255 * self.g), int(255 * self.r))
    return bgr_int
  
  
  def to_rgb_norm(self):
    """RGB normalized values
    :returns tuple of normalized RGB values
    """
    rgb_norm = (self.r, self.g, self.b)
    return rgb_norm
  
  
  def to_rgba_int(self):
    """RGBA int values
    :returns tuple of RGBA int values using (255, 255, 255, 100) scale
    """
    rgb_int = (int(255 * self.r), int(255 * self.g), int(255 * self.b), int(255 * self.a))
    return rgb_int
  
  
  def to_rgba_norm(self):
    """RGBA normalized values
    :returns tuple of RGBA normalized float values
    """
    rgba_norm = (self.r, self.g, self.b, self.a)
    return rgba_norm
  
  
  def to_hsv_int(self):
    """Color to HSV
    :returns tuple of int HSV values in (360, 100, 100) scale
    """
    h, s, v = colorsys.rgb_to_hsv(self.r, self.g, self.b)
    hsv_int = (int(360 * h), int(100 * s), int(100 * v))
    return hsv_int

  
  def to_hsv_norm(self):
    """Color to HSV
    :returns tuple of normalized HSVA float values
    """
    hsv_norm = colorsys.rgb_to_hsv(self.r, self.g, self.b)
    return hsv_norm
  
  
  def to_hsva_int(self):
    """Color to HSV
    :returns tuple of int HSVA values in (360, 100, 100, 100) scale
    """
    h, s, v, a = self.to_hsva_norm()
    hsva_int = (int(360 * h), int(100 * s), int(100 * v), int(100 * a))
    return hsva_int

  
  def to_hsva_norm(self):
    """Color to HSV
    :returns tuple of normalized HSVA float values
    """
    h, s, v = colorsys.rgb_to_hsv(self.r, self.g, self.b)
    a = self.a
    hsva_norm = (h, s, v, a)
    return hsva_norm

  
  def to_rgb_hex_str(self, separator="0x"):
    """Color to RGB HEX string
    :param separator: the prefix string separator
    """
    r, g, b = self.to_rgb_int()
    return f"{separator}{r:02x}{g:02x}{b:02x}"

  def to_rgb_hex_int(self, separator="0x"):
    """Color to RGB HEX string
    :param separator: the prefix string separator
    """
    r, g, b = self.to_rgb_int()
    rgb_hex_str = f"{separator}{r:02x}{g:02x}{b:02x}"
    return int(rgb_hex_str, 16)
  
  
  def to_rgba_hex(self, separator="0x"):
    """Color to RGB HEX string
    :param separator: the prefix string separator
    """
    r, g, b, a = self.to_rgba_int()
    rgb_hex_str = f"{separator}{r:02x}{g:02x}{b:02x}{a:02x}"
    return rgba_hex_str

  
  def get_fg_color(self):
    """Gets black or white foreground color depending on self brightness
    """
    val = 1 - (0.299 * self.r + 0.587 * self.g + 0.114 * self.b)
    if (val < 0.5):
      b = 0  # bright colors - black font
    else:
      b = 255  # dark colors - white font    

    return self.__class__.from_rgb_int((b,b,b))


  def get_brightness(self):
    return (0.299 * self.r + 0.587 * self.g + 0.114 * self.b)


  def max_norm(self):
    """Normalize values to maximum
    """
    v = 1.0 - max(self.rgb_norm)
    r,g,b = (self.r + v, self.g + v, self.b + v)
    return self.__class__(r, g, b, self.a)


  def min_norm(self):
    """Normalize values to minimum
    """
    v = min(self.rgb_norm)
    r,g,b = (self.r - v, self.g - v, self.b - v)
    return self.__class__((r, g, b, self.a))


  @classmethod
  def random(cls, r_range=None, g_range=None, b_range=None):
    """Color from random RGB values
    """
    r = random.uniform(*r_range) if r_range else random.uniform(0.0, 1.0)
    g = random.uniform(*g_range) if g_range else random.uniform(0.0, 1.0)
    b = random.uniform(*b_range) if b_range else random.uniform(0.0, 1.0)
    return cls(r, g, b)

  
  # def jitter(self, fac=0.1):
  #   """Jitter RGB values by percentage
  #   """
  #   fac = np.clip(fac, 0.0, 1.0)
  #   r,g,b = [random.uniform(x - fac, x + fac) for x in (self.r, self.g, self.b)]
  #   return self.__class__.from_rgb_norm((r,g,b))

  
  @classmethod
  def from_rgb_int(cls, rgb_int):
    """Color from int RGB tuple
    """
    r, g, b = rgb_int
    rgb_norm = (r / 255, g / 255, b / 255)
    return cls(*rgb_norm)

  
  @classmethod
  def from_rgb_norm(cls, rgb_norm):
    """Color from normalized RGBA tuple
    """
    return cls(*rgb_norm)

  
  @classmethod
  def from_rgba_int(cls, rgba_int):
    """Color from RGBA using (255, 255, 255, 100) scale
    """
    r, g, b, a = rgba_int
    rgba_norm = (r / 255, g / 255, b / 255, a / 100)
    return cls(*rgba_norm)

  
  @classmethod
  def from_rgba_norm(cls, rgba_norm):
    """Color from normalized RGBA tuple 
    """
    return cls(*rgba_norm)

  
  @classmethod
  def from_hsv_int(cls, hsv_int):
    """Color from int HSV tuple
    """
    h, s, v = hsv_int
    rgb_norm = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
    return cls(*rgb_norm)

  
  @classmethod
  def from_hsv_norm(cls, hsv_norm):
    """Color from normalized HSV tuple
    """
    rgb_norm = colorsys.hsv_to_rgb(*hsv_norm)
    return cls(*rgb_norm)

  
  @classmethod
  def from_hsva_int(cls, hsva_int):
    """Color from int HSVA tuple
    :param hsv_int:  tuple using (360, 100, 100, 100) scale
    """
    h, s, v, a = hsva_int
    hsv_norm = (h / 360, s / 100, v / 100, a / 100)
    rgb_norm = colorsys.hsv_to_rgb(*hsv_norm)
    return cls(*rgb_norm)

  
  @classmethod
  def from_hsva_norm(cls, hsva_norm):
    """Color from normalized HSVA
    :param hsva_norm: tuple using (1.0, 1.0, 1.0, 1.0) scale
    """
    rgb_norm = colorsys.hsv_to_rgb(*hsva_norm)
    return cls(*rgb_norm)

  
  @classmethod
  def from_rgb_hex_str(cls, rgb_hex):
    """Color from hexidecimal RGB str using (eg "0xFFFFFF")
    """
    rgb_hex = rgb_hex.replace('0x', '').replace('#', '')
    r,g,b = tuple(int(rgb_hex[i:i+2], 16) for i in (0, 2, 4))
    return cls.from_rgb_int((r, g, b))

  @classmethod
  def from_rgb_hex_int(cls, rgb_hex):
    """Color from hexidecimal RGB int using (eg 0xFFFFFF)
    """
    r,g,b = rgb_hex >> 16, rgb_hex >> 8 & 0xFF, rgb_hex & 0xFF
    return cls.from_rgb_int((r, g, b))


  @property
  def rgb_int(self):
    return self.to_rgb_int()

  @property
  def bgr_int(self):
    return self.to_rgb_int()[::-1]

  @property
  def rgba_int(self):
    return self.to_rgba_int()

  @property
  def rgba_norm(self):
    return self.to_rgba_norm()

  @property
  def bgr_norm(self):
    return self.to_rgb_norm()[::-1]

  @property
  def rgb_norm(self):
    return self.to_rgb_norm()

  @property
  def hsv_int(self):
    return self.to_hsv_int()

  @property
  def hsv_norm(self):
    return self.to_hsv_norm()

  @property
  def rgb_hex(self):
    return self.to_rgb_hex()

  @property
  def rgba_hex(self):
    return self.rgba_hex()



# ---------------------------------------------------------------------------
#
# Colors
#
# ---------------------------------------------------------------------------

# primary
RED = Color.from_rgb_int((255, 0, 0))
GREEN = Color.from_rgb_int((0, 255, 0))
BLUE = Color.from_rgb_int((0, 0, 255))
YELLOW = Color.from_rgb_int((255, 255, 0))

ORANGE = Color.from_rgb_int((255, 255, 127))
FUSCHIA = Color.from_rgb_int((255, 0, 127))
PINK = Color.from_rgb_int((255, 0, 255))
PURPLE = Color.from_rgb_int((127, 0, 255))
LAVENDER = Color.from_rgb_int((127, 127, 255))
CYAN = Color.from_rgb_int((0, 255, 255))

# grayscale
BLACK = Color.from_rgb_int((0, 0, 0))
WHITE = Color.from_rgb_int((255, 255, 255))
GRAY = Color.from_rgb_int((127, 127, 127))
LIGHT_GRAY = Color.from_rgb_int((170, 170, 170))
DARK_GRAY = Color.from_rgb_int((85, 85, 85))