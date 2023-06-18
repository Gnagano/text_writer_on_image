from typing import TypedDict

class Color(TypedDict):
  R: int
  G: int
  B: int

class TextPositionAxie(TypedDict):
  start: str

class TextPosition(TypedDict):
  x: TextPositionAxie
  y: TextPositionAxie

