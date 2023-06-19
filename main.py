
from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np
import os, glob
from config.constant import CONFIG, SPREAD_SHEET_ID, SPREAD_SHEET_WORK_SHEET_ARTICLE_NAME
from types_custom.types import Color, TextPosition
from lib.gspreadsheet.gspreadsheet import get_values_spreadsheet

CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# Initialization
def initialize_output_directory():
  # Delete all .txt files in the ./posts/ folder
  for img_file in glob.glob(os.path.abspath(f"{CURRENT_DIR_PATH}/output/*.png")):
    os.remove(img_file)  

def convert_message_to_lines(draw, font_path, font_size, message, width, letter_spacing):
  # Setup
  font = ImageFont.truetype(font_path, font_size)

  # Lines
  lines = []
  line = ''
  line_width = 0

  # Calculation
  for char in message:
    char_width = draw.textlength(char, font=font)
    if line_width + char_width + letter_spacing <= width:
      line += char
      line_width += char_width + letter_spacing
    else:
      lines.append(line)
      line = char
      line_width = char_width + letter_spacing
  lines.append(line)
  return lines

def img_add_msg (img, message, width, font_family, font_size, line_spacing, letter_spacing, text_position: TextPosition, color: Color, align="center"):  
  font_path = os.path.abspath(f"{CURRENT_DIR_PATH}/fonts/{font_family}")
  img = Image.fromarray(img)
  draw = ImageDraw.Draw(img)

  # 文字列を一文字ずつ描画し、指定のピクセル幅を超えないように制御
  adjustment_value = 0
  font_size_adjusted = font_size
  while True:
    font_size_adjusted += adjustment_value   
    lines = convert_message_to_lines(draw, font_path, font_size_adjusted, message, width, letter_spacing)
    if (len(lines) < 4):
      break
    adjustment_value -= 2

  font = ImageFont.truetype(font_path, font_size_adjusted)
  y_text = text_position["y"]["start"]
  for line in lines:
    line_width = draw.textlength(line, font=font) + letter_spacing * (len(line) - 1)
    if align == 'center':
      x_text = (img.width - line_width) / 2  # 中央揃えにするためのX座標を計算
    else:
      x_text = text_position["x"]["start"]
    # 文字間隔を制御しながら描画
    for char in line:
      draw.text((x_text, y_text), char, font=font, fill=(color["B"], color["G"], color["R"], 0))
      x_text += draw.textlength(char, font=font) + letter_spacing
    y_text += draw.textlength("あ", font=font) + line_spacing  # 次の行のY座標を計算

  img = np.array(img)
  return img

rows = get_values_spreadsheet(SPREAD_SHEET_ID,SPREAD_SHEET_WORK_SHEET_ARTICLE_NAME)
key = "001"
config = CONFIG[key]

# initialize output directory
initialize_output_directory()

for index, row in enumerate(rows):
  # Index
  index_padded = str(index + 1).zfill(3)

  # カラー画像読み込み
  img = cv2.imread(os.path.abspath(f"{CURRENT_DIR_PATH}/template/template{key}.png"), 1)
  
  # Message
  message = row[0]

  # 画像に文字を入れる関数を実行
  img = img_add_msg(
    img, 
    message, 
    config["container"]["width"],
    config["font"]["family"],
    config["font"]["size"],
    config["font"]["line_spacing"],  # 行間の設定
    config["font"]["letter_spacing"],  # 文字間の指定
    config["position"],
    config["font"]["color"],
    config["font"]["text_align"]
  ) 
  # 画像を表示させる（何かキーを入力すると終了）
  cv2.imwrite(f"output/output{index_padded}.png", img)
  