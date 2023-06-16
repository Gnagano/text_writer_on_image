
from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np

def img_add_msg(img, message, width, line_spacing, letter_spacing, align="center"):
  font_path = "./fonts/NotoSansJPBold700.otf"
  font_size = 70
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

  y_text = 680
  for line in lines:
    line_width = draw.textlength(line, font=font) + letter_spacing * (len(line) - 1)
    if align == 'center':
      x_text = (img.width - line_width) / 2  # 中央揃えにするためのX座標を計算
    else:
      x_text = 50
    # 文字間隔を制御しながら描画
    for char in line:
      draw.text((x_text, y_text), char, font=font, fill=(255, 255, 255, 0))
      x_text += draw.textlength(char, font=font) + letter_spacing
    y_text += draw.textlength("あ", font=font) + line_spacing  # 次の行のY座標を計算

  img = np.array(img)
  return img

img = cv2.imread('./template/template001.png', 1) # カラー画像読み込み
line_spacing = 15 # 行間の設定
letter_spacing = 15 # 文字間の指定
message = '「勃起不全の原因には生活週間病がある！予防や改善方法を紹介」' # 画像に入れる文章
img = img_add_msg(img, message, 900, line_spacing, letter_spacing, 'center') # 画像に文字を入れる関数を実行
 
# 画像を表示させる（何かキーを入力すると終了）
cv2.imwrite('output/output.png', img)