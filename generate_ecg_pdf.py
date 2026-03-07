#!/usr/bin/env python3
"""Generate ECG diagram PDF with Hebrew explanations."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import os

# Output path
output = "/home/user/deskapp/ecg-diagram.pdf"

# Page setup
width, height = A4  # 595 x 842 points
c = canvas.Canvas(output, pagesize=A4)

# Helper for Hebrew RTL text
def heb(text):
    return get_display(text)

# Try to register a Unicode font
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
]
font_name = "Helvetica"
bold_font = "Helvetica-Bold"

for fp in font_paths:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont("CustomFont", fp))
            font_name = "CustomFont"
            bold_font = "CustomFont"
            break
        except:
            pass

# Also try bold variant
bold_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]
for fp in bold_paths:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont("CustomFontBold", fp))
            bold_font = "CustomFontBold"
            break
        except:
            pass

# Colors
colors = {
    'p': HexColor('#e74c3c'),
    'pr_seg': HexColor('#f39c12'),
    'pr_int': HexColor('#e67e22'),
    'qrs': HexColor('#2980b9'),
    'j': HexColor('#d35400'),
    'st': HexColor('#27ae60'),
    't': HexColor('#8e44ad'),
    'u': HexColor('#16a085'),
    'qt': HexColor('#c0392b'),
    'wave': HexColor('#1a73e8'),
    'grid_light': HexColor('#fce4e4'),
    'grid_dark': HexColor('#f5c6c6'),
}

# Draw grid background
def draw_grid(c, x, y, w, h):
    c.setStrokeColor(colors['grid_light'])
    c.setLineWidth(0.3)
    for i in range(0, int(w), 5):
        c.line(x + i, y, x + i, y + h)
    for j in range(0, int(h), 5):
        c.line(x, y + j, x + w, y + j)
    c.setStrokeColor(colors['grid_dark'])
    c.setLineWidth(0.6)
    for i in range(0, int(w), 25):
        c.line(x + i, y, x + i, y + h)
    for j in range(0, int(h), 25):
        c.line(x, y + j, x + w, y + j)

# ECG drawing area
ecg_x = 40
ecg_y = 380
ecg_w = 510
ecg_h = 280

# Title
c.setFont(bold_font, 22)
c.setFillColor(HexColor('#2c3e50'))
c.drawCentredString(width / 2, height - 45, "ECG - Components of Normal ECG")
c.setFont(font_name, 14)
c.drawCentredString(width / 2, height - 65, heb("תרשים אלקטרוקרדיוגרמה תקינה"))

# Draw grid
draw_grid(c, ecg_x, ecg_y, ecg_w, ecg_h)

# Draw border
c.setStrokeColor(HexColor('#ccc'))
c.setLineWidth(1)
c.rect(ecg_x, ecg_y, ecg_w, ecg_h)

# ECG waveform
baseline = ecg_y + 120
sx = ecg_x + 20

path = c.beginPath()
points = [
    (sx, baseline),
    (sx + 30, baseline),
    (sx + 45, baseline + 25),
    (sx + 55, baseline + 35),
    (sx + 65, baseline + 25),
    (sx + 80, baseline),
    (sx + 110, baseline),
    (sx + 120, baseline - 12),
    (sx + 135, baseline + 130),
    (sx + 145, baseline + 145),
    (sx + 155, baseline + 130),
    (sx + 170, baseline - 35),
    (sx + 178, baseline - 40),
    (sx + 190, baseline),
    (sx + 230, baseline),
    (sx + 255, baseline + 20),
    (sx + 275, baseline + 45),
    (sx + 295, baseline + 40),
    (sx + 315, baseline + 20),
    (sx + 340, baseline),
    (sx + 360, baseline),
    (sx + 370, baseline + 8),
    (sx + 380, baseline + 12),
    (sx + 390, baseline + 8),
    (sx + 400, baseline),
    (sx + 470, baseline),
]

path.moveTo(points[0][0], points[0][1])
for px, py in points[1:]:
    path.lineTo(px, py)

c.setStrokeColor(colors['wave'])
c.setLineWidth(2.5)
c.setLineCap(1)
c.setLineJoin(1)
c.drawPath(path, fill=0, stroke=1)

# Helper to draw label with line
def label(c, x1, y1, x2, y2, text, color, font_size=10):
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.setDash(2, 2)
    c.line(x1, y1, x2, y2)
    c.setDash()
    c.setFillColor(color)
    c.setFont(bold_font, font_size)
    c.drawCentredString(x2, y2 + 4, text)

def bracket(c, x1, x2, y, text, color, above=True):
    offset = 8 if above else -8
    text_offset = 14 if above else -6
    c.setStrokeColor(color)
    c.setLineWidth(1)
    c.setDash(2, 2)
    c.line(x1, y, x1, y + offset)
    c.line(x2, y, x2, y + offset)
    c.setDash()
    c.setLineWidth(1.2)
    c.line(x1, y + offset, x2, y + offset)
    c.setFillColor(color)
    c.setFont(bold_font, 9)
    c.drawCentredString((x1 + x2) / 2, y + text_offset, heb(text))

# Wave labels
label(c, sx + 55, baseline + 38, sx + 55, baseline + 60, "P", colors['p'], 14)

c.setFillColor(colors['qrs'])
c.setFont(bold_font, 11)
c.drawCentredString(sx + 120, baseline - 22, "Q")

label(c, sx + 145, baseline + 148, sx + 145, baseline + 168, "R", colors['qrs'], 16)

c.setFillColor(colors['qrs'])
c.setFont(bold_font, 11)
c.drawCentredString(sx + 178, baseline - 50, "S")

label(c, sx + 275, baseline + 48, sx + 275, baseline + 70, "T", colors['t'], 14)

label(c, sx + 380, baseline + 15, sx + 380, baseline + 32, "U", colors['u'], 12)

# J point
c.setFillColor(colors['j'])
c.setFont(bold_font, 9)
c.drawString(sx + 192, baseline + 8, heb("נקודת J"))

# Brackets
bracket(c, sx + 80, sx + 110, baseline - 15, "מקטע PR", colors['pr_seg'], above=False)
bracket(c, sx + 30, sx + 120, baseline - 35, "מרווח PR", colors['pr_int'], above=False)
bracket(c, sx + 115, sx + 190, baseline - 55, "קומפלקס QRS", colors['qrs'], above=False)
bracket(c, sx + 192, sx + 230, baseline + 55, "מקטע ST", colors['st'], above=True)
bracket(c, sx + 115, sx + 340, baseline - 75, "מרווח QT", colors['qt'], above=False)

# --- Hebrew explanations table ---
explanations = [
    ("P", "גל P", "דה-פולריזציה פרוזדורית - הפעילות החשמלית של התכווצות הפרוזדורים", colors['p']),
    ("PR seg", "מקטע PR", "זמן מעבר הדחף דרך צומת AV, צרור היס ורשת פורקינייה", colors['pr_seg']),
    ("PR int", "מרווח PR", "מתחילת גל P עד תחילת QRS. כולל דה-פולריזציה ומעבר במערכת ההולכה", colors['pr_int']),
    ("QRS", "קומפלקס QRS", "דה-פולריזציה חדרית - הפעילות החשמלית של התכווצות החדרים", colors['qrs']),
    ("J", "נקודת J", "נקודת המפגש בין סוף קומפלקס QRS לתחילת מקטע ST", colors['j']),
    ("ST", "מקטע ST", "רה-פולריזציה חדרית מוקדמת. שינויים מעידים על אוטם", colors['st']),
    ("T", "גל T", "רה-פולריזציה חדרית - התאוששות חשמלית של החדרים", colors['t']),
    ("U", "גל U", "רה-פולריזציה חדרית מאוחרת - גל קטן שמופיע לעיתים אחרי T", colors['u']),
    ("QT", "מרווח QT", "הזמן הכולל לדה-פולריזציה ורה-פולריזציה חדרית", colors['qt']),
]

table_y = 350
c.setFont(bold_font, 14)
c.setFillColor(HexColor('#2c3e50'))
c.drawCentredString(width / 2, table_y, heb("הסברים - Explanations"))

row_y = table_y - 25
for eng, heb_name, desc, color in explanations:
    # Color dot
    c.setFillColor(color)
    c.circle(ecg_x + 10, row_y + 3, 4, fill=1, stroke=0)

    # English label
    c.setFont(bold_font, 10)
    c.setFillColor(color)
    c.drawString(ecg_x + 20, row_y, eng)

    # Hebrew name (right-aligned from a fixed position)
    c.setFont(bold_font, 10)
    c.setFillColor(HexColor('#2c3e50'))
    c.drawString(ecg_x + 70, row_y, heb(heb_name))

    # Hebrew description
    c.setFont(font_name, 9)
    c.setFillColor(HexColor('#555555'))
    c.drawString(ecg_x + 155, row_y, heb(desc))

    row_y -= 22

# Save
c.save()
print(f"PDF saved to: {output}")
