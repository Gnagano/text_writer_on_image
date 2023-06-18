
from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np
import os
from config.constant import CONFIG
from types_custom.types import Color, TextPosition


def img_add_msg (img, message, width, font_family,font_size, line_spacing, letter_spacing, text_position: TextPosition, color: Color, align="center"):  
  font_path = os.path.abspath(f"./fonts/{font_family}")
  font_size = font_size
  font = ImageFont.truetype(font_path, font_size)
  img = Image.fromarray(img)
  draw = ImageDraw.Draw(img)

  # 文字列を一文字ずつ描画し、指定のピクセル幅を超えないように制御
  lines = []
  line = ''
  line_width = 0
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

key = "001"
config = CONFIG[key]

img = cv2.imread(os.path.abspath(f"./template/template{key}.png"), 1) # カラー画像読み込み
message = '「勃起不全の原因には生活週間病がある！予防や改善方法を紹介」' # 画像に入れる文章

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
cv2.imwrite(f"output/output{key}.png", img)