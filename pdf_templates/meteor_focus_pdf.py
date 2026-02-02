#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meteor Focus PDF Generator - Enhanced Version
==============================================
מערכת עיצוב Meteor Focus - סיכומים לימודיים | טבלאות שאלות | חומרי לימוד

Design System Version: 2.0
Featuring: Advanced Flowables, Heebo fonts, gradient effects, RTL Hebrew support
"""

import os
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, KeepTogether, ListFlowable, ListItem, Flowable,
    BaseDocTemplate, Frame, PageTemplate
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.graphics.shapes import Drawing, Rect, Circle, String
from reportlab.graphics import renderPDF

# =============================================================================
# FONT REGISTRATION
# =============================================================================
# Try Heebo first (better Hebrew), fall back to DejaVu
FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
DEJAVU_PATH = '/usr/share/fonts/truetype/dejavu/'
NOTO_PATH = '/usr/share/fonts/truetype/noto/'

# Register fonts with fallbacks
try:
    pdfmetrics.registerFont(TTFont('Heebo', os.path.join(FONTS_DIR, 'Heebo-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('Heebo-Bold', os.path.join(FONTS_DIR, 'Heebo-Bold.ttf')))
    MAIN_FONT = 'Heebo'
    MAIN_FONT_BOLD = 'Heebo-Bold'
except:
    pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(DEJAVU_PATH, 'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', os.path.join(DEJAVU_PATH, 'DejaVuSans-Bold.ttf')))
    MAIN_FONT = 'DejaVuSans'
    MAIN_FONT_BOLD = 'DejaVuSans-Bold'

# Register emoji font
try:
    pdfmetrics.registerFont(TTFont('NotoEmoji', os.path.join(NOTO_PATH, 'NotoColorEmoji.ttf')))
    EMOJI_FONT = 'NotoEmoji'
except:
    EMOJI_FONT = MAIN_FONT

# =============================================================================
# BRAND COLORS - Enhanced Palette
# =============================================================================
# Primary Brand Colors
METEOR_BLUE = HexColor('#5A6FD6')       # Primary blue
METEOR_PURPLE = HexColor('#8C6BBE')     # Secondary purple
METEOR_LIGHT = HexColor('#8F73C8')      # Accent light purple
FOCUS_PURPLE = HexColor('#9575CD')      # Focus purple (lighter)
METEOR_ICON = HexColor('#5F6FDB')       # Icon color
WHITE = white

# Text Colors
DARK_TEXT = HexColor('#2C2C40')         # Primary text
MED_TEXT = HexColor('#444466')          # Body text
LIGHT_TEXT = HexColor('#888899')        # Subtle text

# UI Colors
LAVENDER = HexColor('#E8EAF6')          # Light lavender for backgrounds
SUBTLE_LINE = HexColor('#DDDDEE')       # Subtle borders

# Info Box Colors - צבעי תיבות מידע
BOX_TIP_BG = HexColor('#FFF9E6')        # ⭐ טיפ - רקע
BOX_TIP_BORDER = HexColor('#FFD700')    # ⭐ טיפ - מסגרת
BOX_NOTE_BG = HexColor('#FFF0F5')       # 💡 שימו לב - רקע
BOX_NOTE_BORDER = HexColor('#FFB6C1')   # 💡 שימו לב - מסגרת
BOX_WARN_BG = HexColor('#FFFDE7')       # ⚠️ אזהרה - רקע
BOX_WARN_BORDER = HexColor('#FFA726')   # ⚠️ אזהרה - מסגרת
BOX_REMEMBER_BG = HexColor('#E3F2FD')   # 📌 זכרו - רקע
BOX_REMEMBER_BORDER = HexColor('#5A6FD6')  # 📌 זכרו - מסגרת
BOX_FORBID_BG = HexColor('#FFEBEE')     # 🚫 אסור - רקע
BOX_FORBID_BORDER = HexColor('#E53935') # 🚫 אסור - מסגרת

# Traffic Light Colors
GREEN_BG = HexColor('#E8F5E9')
GREEN_TEXT = HexColor('#2E7D32')
YELLOW_BG = HexColor('#FFF9C4')
YELLOW_TEXT = HexColor('#F57F17')
RED_BG = HexColor('#FFEBEE')
RED_TEXT = HexColor('#C62828')

# Table Colors
ZEBRA_LIGHT = HexColor('#FAFAFD')
HEADER_LAVENDER = HexColor('#E8EAF6')
GRID_LIGHT = HexColor('#E0E0E0')

# Success
SUCCESS_BG = HexColor('#E8F5E9')
SUCCESS_BORDER = HexColor('#4CAF50')

# Page dimensions
WIDTH, HEIGHT = A4
ML, MR, MT, MB = 20*mm, 20*mm, 25*mm, 25*mm
CW = WIDTH - ML - MR  # Content width


# =============================================================================
# RTL HEBREW HELPERS
# =============================================================================
def heb(text):
    """Convert Hebrew text for proper RTL display in PDF"""
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# Alias for backward compatibility and matching advanced script
bidi = heb


def heb_with_english(hebrew_text, english_text=None):
    """Format Hebrew text with optional English in parentheses"""
    if english_text:
        combined = f"{hebrew_text} ({english_text})"
        reshaped = arabic_reshaper.reshape(combined)
        return get_display(reshaped)
    return heb(hebrew_text)


# =============================================================================
# CUSTOM FLOWABLES - Enhanced
# =============================================================================
class GradientRect(Flowable):
    """Gradient rectangle for headers"""
    def __init__(self, width, height, color1, color2, text="", text_color=WHITE):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color1 = color1
        self.color2 = color2
        self.text = text
        self.text_color = text_color

    def draw(self):
        steps = 30
        for i in range(steps):
            r = self.color1.red + (self.color2.red - self.color1.red) * i / steps
            g = self.color1.green + (self.color2.green - self.color1.green) * i / steps
            b = self.color1.blue + (self.color2.blue - self.color1.blue) * i / steps
            self.canv.setFillColor(Color(r, g, b))
            x = i * self.width / steps
            self.canv.rect(x, 0, self.width / steps + 1, self.height, fill=1, stroke=0)

        if self.text:
            self.canv.setFillColor(self.text_color)
            self.canv.setFont(MAIN_FONT_BOLD, 14)
            self.canv.drawCentredString(self.width / 2, self.height / 2 - 5, heb(self.text))


class NumberedCircleHeader(Flowable):
    """Section header with gradient circle, number, title, and optional English subtitle"""
    def __init__(self, number, text, en_text="", width=None):
        Flowable.__init__(self)
        self.number = str(number)
        self.text = text
        self.en_text = en_text
        self.flowable_width = width or CW
        self.height = 16*mm if en_text else 14*mm
        self.width = self.flowable_width

    def draw(self):
        c = self.canv
        r = 5.5*mm
        cx = self.flowable_width - r - 1*mm
        cy = self.height / 2 + (1.5*mm if self.en_text else 0)

        # Gradient circle effect
        c.saveState()
        c.setFillColor(METEOR_BLUE)
        c.circle(cx, cy, r, fill=1, stroke=0)
        c.setFillColor(METEOR_PURPLE)
        c.setFillAlpha(0.5)
        c.circle(cx - 1, cy - 1, r * 0.85, fill=1, stroke=0)
        c.restoreState()

        # Number in circle
        c.saveState()
        c.setFillColor(WHITE)
        c.setFont(MAIN_FONT_BOLD, 15)
        nw = pdfmetrics.stringWidth(self.number, MAIN_FONT_BOLD, 15)
        c.drawString(cx - nw/2, cy - 5, self.number)
        c.restoreState()

        # Title
        display = bidi(self.text)
        c.saveState()
        c.setFont(MAIN_FONT_BOLD, 17)
        c.setFillColor(DARK_TEXT)
        c.setStrokeColor(DARK_TEXT)
        c.setLineWidth(0.3)
        tw = pdfmetrics.stringWidth(display, MAIN_FONT_BOLD, 17)
        tx = cx - r - 4*mm - tw
        ty = cy - 5.5 + (2 if self.en_text else 0)
        t = c.beginText(tx, ty)
        t.setTextRenderMode(2)  # Fill and stroke
        t.textLine(display)
        c.drawText(t)
        c.restoreState()

        # English subtitle
        if self.en_text:
            c.saveState()
            c.setFont(MAIN_FONT, 10)
            c.setFillColor(FOCUS_PURPLE)
            ew = pdfmetrics.stringWidth(self.en_text, MAIN_FONT, 10)
            c.drawString(cx - r - 4*mm - ew, ty - 14, self.en_text)
            c.restoreState()


class SubsectionHeader(Flowable):
    """Subsection header with lavender circle, number, and title"""
    def __init__(self, number, text, en_text="", width=None):
        Flowable.__init__(self)
        self.number = str(number)
        self.text = text
        self.en_text = en_text
        self.flowable_width = width or CW
        self.height = 13*mm if en_text else 10*mm
        self.width = self.flowable_width

    def draw(self):
        c = self.canv
        r = 4*mm
        cx = self.flowable_width - r - 1*mm
        cy = self.height / 2 + (1*mm if self.en_text else 0)

        # Lavender circle
        c.saveState()
        c.setFillColor(LAVENDER)
        c.circle(cx, cy, r, fill=1, stroke=0)
        c.restoreState()

        # Number
        c.saveState()
        c.setFillColor(METEOR_BLUE)
        c.setFont(MAIN_FONT_BOLD, 11)
        nw = pdfmetrics.stringWidth(self.number, MAIN_FONT_BOLD, 11)
        c.drawString(cx - nw/2, cy - 4, self.number)
        c.restoreState()

        # Title
        display = bidi(self.text)
        c.saveState()
        c.setFont(MAIN_FONT_BOLD, 13)
        c.setFillColor(METEOR_PURPLE)
        tw = pdfmetrics.stringWidth(display, MAIN_FONT_BOLD, 13)
        tx = cx - r - 3*mm - tw
        ty = cy - 4.5 + (1.5 if self.en_text else 0)
        c.drawString(tx, ty, display)
        c.restoreState()

        # English subtitle
        if self.en_text:
            c.saveState()
            c.setFont(MAIN_FONT, 8.5)
            c.setFillColor(LIGHT_TEXT)
            ew = pdfmetrics.stringWidth(self.en_text, MAIN_FONT, 8.5)
            c.drawString(cx - r - 3*mm - ew, ty - 12, self.en_text)
            c.restoreState()


class FadeLine(Flowable):
    """Decorative fade line separator"""
    def __init__(self, width=None):
        Flowable.__init__(self)
        self.width = width or CW
        self.height = 3*mm

    def draw(self):
        c = self.canv
        steps = 40
        sw = self.width / steps
        mid = steps // 2
        for i in range(steps):
            alpha = 1.0 - abs(i - mid) / mid
            c.setStrokeColor(LAVENDER)
            c.setStrokeAlpha(alpha)
            c.setLineWidth(0.8)
            c.line(i*sw, self.height/2, (i+1)*sw, self.height/2)


class NumberedCircle(Flowable):
    """Simple purple numbered circle"""
    def __init__(self, number, size=24):
        Flowable.__init__(self)
        self.number = number
        self.size = size
        self.width = size
        self.height = size

    def draw(self):
        self.canv.setFillColor(METEOR_BLUE)
        self.canv.circle(self.size/2, self.size/2, self.size/2, fill=1, stroke=0)

        self.canv.setFillColor(METEOR_PURPLE)
        self.canv.circle(self.size/2, self.size/2, self.size/2 - 2, fill=1, stroke=0)

        self.canv.setFillColor(WHITE)
        self.canv.setFont(MAIN_FONT_BOLD, 12)
        self.canv.drawCentredString(self.size/2, self.size/2 - 4, str(self.number))


class InfoBox(Flowable):
    """Enhanced info box with right border accent, emoji, title, content"""
    def __init__(self, box_type, title, content, width=None):
        Flowable.__init__(self)
        self.box_type = box_type
        self.title = title
        self.content = content
        self.box_width = width or CW

        # Color mappings
        self.colors = {
            'tip': (BOX_TIP_BG, BOX_TIP_BORDER, '⭐'),
            'note': (BOX_NOTE_BG, BOX_NOTE_BORDER, '💡'),
            'warning': (BOX_WARN_BG, BOX_WARN_BORDER, '⚠️'),
            'remember': (BOX_REMEMBER_BG, BOX_REMEMBER_BORDER, '📌'),
            'forbidden': (BOX_FORBID_BG, BOX_FORBID_BORDER, '🚫'),
            'success': (SUCCESS_BG, SUCCESS_BORDER, '✔'),
        }

        bg, border, emoji = self.colors.get(box_type, (BOX_TIP_BG, BOX_TIP_BORDER, ''))
        self.bg_color = bg
        self.border_color = border
        self.emoji = emoji

        # Calculate height dynamically based on content
        self._calculate_height()

    def _calculate_height(self):
        """Calculate box height based on content"""
        style = ParagraphStyle('tmp', fontName=MAIN_FONT, fontSize=10, leading=14.5,
                               alignment=TA_RIGHT, wordWrap='CJK')
        full = bidi(f"{self.title}: {self.content}") if self.content else bidi(self.title)
        p = Paragraph(full, style)
        w, h = p.wrap(self.box_width - 18*mm, 500)
        self.content_height = h
        self.box_height = max(h + 10*mm, 14*mm)
        self.height = self.box_height

    def wrap(self, availWidth, availHeight):
        self.box_width = min(self.box_width, availWidth)
        self._calculate_height()
        return (self.box_width, self.box_height)

    def draw(self):
        c = self.canv

        # Background
        c.saveState()
        c.setFillColor(self.bg_color)
        c.roundRect(0, 0, self.box_width, self.box_height, 6, fill=1, stroke=0)
        c.restoreState()

        # Right border accent
        c.saveState()
        c.setFillColor(self.border_color)
        c.roundRect(self.box_width - 4*mm, 0, 4*mm, self.box_height, 6, fill=1, stroke=0)
        # Square off the left edge of the accent
        c.rect(self.box_width - 4*mm, 2, 2*mm, self.box_height - 4, fill=1, stroke=0)
        c.restoreState()

        # Border stroke
        c.saveState()
        c.setStrokeColor(self.border_color)
        c.setLineWidth(1)
        c.roundRect(0, 0, self.box_width, self.box_height, 6, fill=0, stroke=1)
        c.restoreState()

        # Emoji
        c.saveState()
        c.setFont(MAIN_FONT, 13)
        c.drawString(self.box_width - 3.5*mm - 8, self.box_height - 5.5*mm, self.emoji)
        c.restoreState()

        # Text content
        full = bidi(f"{self.title}: {self.content}") if self.content else bidi(self.title)
        style = ParagraphStyle('info_inner', fontName=MAIN_FONT, fontSize=10, leading=14.5,
                               alignment=TA_RIGHT, textColor=DARK_TEXT, wordWrap='CJK')
        p = Paragraph(full, style)
        pw, ph = p.wrap(self.box_width - 18*mm, 500)
        p.drawOn(c, 4*mm, self.box_height - 5*mm - ph)


class FlowStep(Flowable):
    """Flow diagram step box for process flows"""
    def __init__(self, emoji, title, desc, width=None):
        Flowable.__init__(self)
        self.emoji = emoji
        self.title_text = title
        self.desc_text = desc
        self.box_width = (width or CW) * 0.82
        self.height = 14*mm
        self.width = CW

    def draw(self):
        c = self.canv
        x_off = (CW - self.box_width) / 2

        # Box outline
        c.saveState()
        c.setStrokeColor(LAVENDER)
        c.setLineWidth(1.5)
        c.setFillColor(WHITE)
        c.roundRect(x_off, 0, self.box_width, self.height, 7, fill=1, stroke=1)
        c.restoreState()

        # Title
        title_d = bidi(self.title_text)
        c.saveState()
        c.setFont(MAIN_FONT_BOLD, 11)
        c.setFillColor(METEOR_BLUE)
        c.setStrokeColor(METEOR_BLUE)
        c.setLineWidth(0.2)
        tw = pdfmetrics.stringWidth(title_d, MAIN_FONT_BOLD, 11)
        tx = x_off + self.box_width / 2 + tw / 2
        ty = self.height - 5*mm
        t = c.beginText(tx, ty)
        t.setTextRenderMode(2)
        t.textLine(title_d)
        c.drawText(t)
        c.restoreState()

        # Emoji
        c.saveState()
        c.setFont(MAIN_FONT, 10)
        c.drawString(tx + 3, ty, self.emoji)
        c.restoreState()

        # Description
        desc_d = bidi(self.desc_text)
        c.saveState()
        c.setFont(MAIN_FONT, 9)
        c.setFillColor(MED_TEXT)
        dw = pdfmetrics.stringWidth(desc_d, MAIN_FONT, 9)
        c.drawString(x_off + self.box_width / 2 + dw / 2, 2.5*mm, desc_d)
        c.restoreState()


class FlowArrow(Flowable):
    """Arrow connector for flow diagrams"""
    def __init__(self):
        Flowable.__init__(self)
        self.width = CW
        self.height = 5*mm

    def draw(self):
        c = self.canv
        cx = CW / 2

        c.saveState()
        c.setFillColor(METEOR_PURPLE)
        c.setFillAlpha(0.7)
        # Arrow shaft
        c.rect(cx - 1.5, 1*mm, 3, 3*mm, fill=1, stroke=0)
        # Arrow head
        p = c.beginPath()
        p.moveTo(cx-4, 1.5*mm)
        p.lineTo(cx, 0)
        p.lineTo(cx+4, 1.5*mm)
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        c.restoreState()


# =============================================================================
# PARAGRAPH STYLES
# =============================================================================
def get_styles():
    """Get all paragraph styles for the document"""
    styles = {}

    # Main title
    styles['title'] = ParagraphStyle(
        'Title',
        fontName=MAIN_FONT_BOLD,
        fontSize=24,
        textColor=METEOR_BLUE,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=30
    )

    # Subtitle
    styles['subtitle'] = ParagraphStyle(
        'Subtitle',
        fontName=MAIN_FONT,
        fontSize=14,
        textColor=METEOR_PURPLE,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # Section heading
    styles['heading1'] = ParagraphStyle(
        'Heading1',
        fontName=MAIN_FONT_BOLD,
        fontSize=14,
        textColor=METEOR_BLUE,
        alignment=TA_RIGHT,
        spaceBefore=16,
        spaceAfter=8,
        leading=18
    )

    # Subheading
    styles['heading2'] = ParagraphStyle(
        'Heading2',
        fontName=MAIN_FONT_BOLD,
        fontSize=12,
        textColor=METEOR_PURPLE,
        alignment=TA_RIGHT,
        spaceBefore=12,
        spaceAfter=6,
        leading=16
    )

    # Sub-subheading
    styles['heading3'] = ParagraphStyle(
        'Heading3',
        fontName=MAIN_FONT_BOLD,
        fontSize=11.5,
        textColor=METEOR_BLUE,
        alignment=TA_RIGHT,
        spaceBefore=4*mm,
        spaceAfter=2*mm,
        leading=16
    )

    # Body text
    styles['body'] = ParagraphStyle(
        'Body',
        fontName=MAIN_FONT,
        fontSize=10.5,
        textColor=MED_TEXT,
        alignment=TA_RIGHT,
        spaceBefore=1*mm,
        spaceAfter=3.5*mm,
        leading=16.5,
        wordWrap='CJK'
    )

    # Emphasized body
    styles['body_em'] = ParagraphStyle(
        'BodyEm',
        parent=styles['body'],
        textColor=DARK_TEXT
    )

    # Bullet text
    styles['bullet'] = ParagraphStyle(
        'Bullet',
        fontName=MAIN_FONT,
        fontSize=10,
        textColor=MED_TEXT,
        alignment=TA_RIGHT,
        rightIndent=6*mm,
        spaceAfter=1.5*mm,
        leading=15,
        wordWrap='CJK'
    )

    # Table header
    styles['table_header'] = ParagraphStyle(
        'TableHeader',
        fontName=MAIN_FONT_BOLD,
        fontSize=9.5,
        textColor=DARK_TEXT,
        alignment=TA_RIGHT,
        leading=13,
        wordWrap='CJK'
    )

    # Table cell
    styles['table_cell'] = ParagraphStyle(
        'TableCell',
        fontName=MAIN_FONT,
        fontSize=9,
        textColor=MED_TEXT,
        alignment=TA_RIGHT,
        leading=13,
        wordWrap='CJK'
    )

    # Table cell centered
    styles['table_cell_c'] = ParagraphStyle(
        'TableCellC',
        fontName=MAIN_FONT,
        fontSize=9,
        textColor=MED_TEXT,
        alignment=TA_CENTER,
        leading=13,
        wordWrap='CJK'
    )

    # Info text
    styles['info_text'] = ParagraphStyle(
        'InfoText',
        fontName=MAIN_FONT,
        fontSize=10,
        textColor=DARK_TEXT,
        alignment=TA_RIGHT,
        leading=14.5,
        wordWrap='CJK'
    )

    # Footer
    styles['footer'] = ParagraphStyle(
        'Footer',
        fontName=MAIN_FONT,
        fontSize=8,
        textColor=LIGHT_TEXT,
        alignment=TA_CENTER
    )

    # TOC
    styles['toc'] = ParagraphStyle(
        'TOC',
        fontName=MAIN_FONT,
        fontSize=11,
        textColor=MED_TEXT,
        alignment=TA_RIGHT,
        leftIndent=20,
        spaceBefore=4,
        spaceAfter=4
    )

    # Cover page styles
    styles['c_brand'] = ParagraphStyle(
        'CoverBrand',
        fontName=MAIN_FONT_BOLD,
        fontSize=14,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=2*mm,
        leading=18
    )

    styles['c_label'] = ParagraphStyle(
        'CoverLabel',
        fontName=MAIN_FONT,
        fontSize=16,
        textColor=HexColor('#FFFFFFDD'),
        alignment=TA_CENTER,
        leading=22
    )

    styles['c_title'] = ParagraphStyle(
        'CoverTitle',
        fontName=MAIN_FONT_BOLD,
        fontSize=36,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=46
    )

    styles['c_sub'] = ParagraphStyle(
        'CoverSub',
        fontName=MAIN_FONT,
        fontSize=18,
        textColor=HexColor('#FFFFFFE6'),
        alignment=TA_CENTER,
        leading=24
    )

    styles['c_topics'] = ParagraphStyle(
        'CoverTopics',
        fontName=MAIN_FONT,
        fontSize=11,
        textColor=HexColor('#FFFFFFCC'),
        alignment=TA_CENTER,
        leading=19
    )

    return styles


# =============================================================================
# TABLE BUILDERS
# =============================================================================
def create_clinical_table(headers, data, col_widths=None):
    """Create a clinical summary table with Meteor Focus styling"""
    styles = get_styles()

    formatted_headers = [Paragraph(heb(h), styles['table_header']) for h in headers]

    formatted_data = [formatted_headers]
    for row in data:
        formatted_row = []
        for cell in row:
            if isinstance(cell, str):
                formatted_row.append(Paragraph(heb(cell), styles['table_cell']))
            else:
                formatted_row.append(cell)
        formatted_data.append(formatted_row)

    if col_widths:
        table = Table(formatted_data, colWidths=col_widths, repeatRows=1)
    else:
        n = len(headers)
        table = Table(formatted_data, colWidths=[CW/n]*n, repeatRows=1)

    cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), LAVENDER),
        ('TEXTCOLOR', (0, 0), (-1, 0), DARK_TEXT),
        ('FONTNAME', (0, 0), (-1, -1), MAIN_FONT),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, METEOR_BLUE),
        ('LINEBELOW', (0, 1), (-1, -2), 0.5, HexColor('#EDEDF3')),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]

    # Zebra striping
    for i in range(1, len(formatted_data)):
        if i % 2 == 0:
            cmds.append(('BACKGROUND', (0, i), (-1, i), ZEBRA_LIGHT))

    table.setStyle(TableStyle(cmds))
    return table


def create_comparison_table(left_header, right_header, left_items, right_items):
    """Create a comparison table with ✅ vs ❌ styling"""
    styles = get_styles()

    data = [[
        Paragraph(f"<font color='#C62828'>❌ {heb(right_header)}</font>", styles['table_header']),
        Paragraph(f"<font color='#2E7D32'>✅ {heb(left_header)}</font>", styles['table_header'])
    ]]

    max_items = max(len(left_items), len(right_items))
    for i in range(max_items):
        left = left_items[i] if i < len(left_items) else ""
        right = right_items[i] if i < len(right_items) else ""
        data.append([
            Paragraph(heb(right), styles['table_cell']),
            Paragraph(heb(left), styles['table_cell'])
        ])

    table = Table(data, colWidths=[85*mm, 85*mm])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), RED_BG),
        ('BACKGROUND', (1, 0), (1, 0), GREEN_BG),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, GRID_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1.5, GRID_LIGHT),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ])

    table.setStyle(style)
    return table


def create_traffic_light_table(headers, data):
    """Create a table with traffic light indicators"""
    styles = get_styles()

    formatted_headers = [Paragraph(heb(h), styles['table_header']) for h in headers]

    formatted_data = [formatted_headers]
    for row in data:
        formatted_row = []
        for cell in row:
            if cell in ['green', 'ירוק', '🟢']:
                formatted_row.append(Paragraph(f"<font color='#2E7D32'>🟢 {heb('תקין')}</font>", styles['table_cell']))
            elif cell in ['yellow', 'צהוב', '🟡']:
                formatted_row.append(Paragraph(f"<font color='#F57F17'>🟡 {heb('זהירות')}</font>", styles['table_cell']))
            elif cell in ['red', 'אדום', '🔴']:
                formatted_row.append(Paragraph(f"<font color='#C62828'>🔴 {heb('מסוכן')}</font>", styles['table_cell']))
            else:
                formatted_row.append(Paragraph(heb(str(cell)), styles['table_cell']))
        formatted_data.append(formatted_row)

    table = Table(formatted_data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_LAVENDER),
        ('GRID', (0, 0), (-1, -1), 0.5, GRID_LIGHT),
        ('LINEBELOW', (0, 0), (-1, 0), 2, METEOR_BLUE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, ZEBRA_LIGHT]),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ])

    table.setStyle(style)
    return table


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def body(text):
    """Create a body paragraph"""
    styles = get_styles()
    return Paragraph(bidi(text), styles['body'])


def body_bold(text):
    """Create an emphasized body paragraph"""
    styles = get_styles()
    return Paragraph(bidi(text), styles['body_em'])


def bullet_item(text):
    """Create a bullet item with purple bullet"""
    styles = get_styles()
    display = bidi(text)
    styled = f'{display} <font name="{MAIN_FONT}" color="#8C6BBE" size="14">∙</font>'
    return Paragraph(styled, styles['bullet'])


def sp(h=3):
    """Create a spacer"""
    return Spacer(1, h*mm)


def fade_sep():
    """Create a fade line separator"""
    return FadeLine()


def make_table(headers, rows, col_widths=None):
    """Create a branded table (alias for create_clinical_table)"""
    return create_clinical_table(headers, rows, col_widths)


# =============================================================================
# DOCUMENT BUILDER
# =============================================================================
class MeteorFocusPDF:
    """Main PDF document builder for Meteor Focus design system"""

    def __init__(self, filename, title, subtitle=None, source=None, landscape_mode=False):
        """
        Initialize the PDF document

        Args:
            filename: Output PDF filename
            title: Main document title
            subtitle: Optional subtitle
            source: Source reference
            landscape_mode: Use landscape orientation
        """
        self.filename = filename
        self.title = title
        self.subtitle = subtitle or ""
        self.source = source or ""
        self.styles = get_styles()
        self.elements = []
        self.page_count = 0
        self._section_counter = 0
        self._subsection_counter = 0

        # Page setup
        if landscape_mode:
            self.pagesize = landscape(A4)
            self.width, self.height = self.pagesize
        else:
            self.pagesize = A4
            self.width, self.height = WIDTH, HEIGHT

        self.doc = SimpleDocTemplate(
            filename,
            pagesize=self.pagesize,
            rightMargin=MR,
            leftMargin=ML,
            topMargin=MT,
            bottomMargin=MB
        )

    def add_cover_page(self, toc_items=None, with_gradient=True):
        """Add a cover page with title and optional table of contents"""
        if with_gradient:
            # Gradient header bar
            self.elements.append(GradientRect(CW, 12*mm, METEOR_BLUE, METEOR_PURPLE, "METEOR FOCUS"))
            self.elements.append(Spacer(1, 20*mm))

        # Main title
        self.elements.append(Paragraph(heb(self.title), self.styles['title']))

        # Subtitle
        if self.subtitle:
            self.elements.append(Paragraph(heb(self.subtitle), self.styles['subtitle']))

        self.elements.append(Spacer(1, 15*mm))

        # Table of contents
        if toc_items:
            toc_data = [[Paragraph(heb("תוכן עניינים"), self.styles['heading2'])]]
            for i, item in enumerate(toc_items, 1):
                toc_data.append([Paragraph(f"{heb(item)} .{i}", self.styles['toc'])])

            toc_table = Table(toc_data, colWidths=[150*mm])
            toc_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1, METEOR_LIGHT),
                ('BACKGROUND', (0, 0), (-1, 0), HEADER_LAVENDER),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 15),
                ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ]))
            self.elements.append(toc_table)

        self.elements.append(PageBreak())

    def add_section(self, number, title_hebrew, title_english=None):
        """Add a numbered section heading with the new circular design"""
        self._section_counter = number
        self._subsection_counter = 0
        self.elements.append(Spacer(1, 5*mm))
        self.elements.append(NumberedCircleHeader(number, title_hebrew, title_english or ""))
        self.elements.append(Spacer(1, 3*mm))

    def add_subsection(self, title_hebrew, title_english=None, numbered=False):
        """Add a subsection heading"""
        if numbered:
            self._subsection_counter += 1
            num_str = f"{self._section_counter}.{self._subsection_counter}"
            self.elements.append(SubsectionHeader(num_str, title_hebrew, title_english or ""))
        else:
            heading_text = heb(title_hebrew)
            if title_english:
                heading_text += f" ({title_english})"
            self.elements.append(Paragraph(
                f"<u>{heb(heading_text)}</u>",
                self.styles['heading2']
            ))

    def add_sub_subsection(self, title_hebrew, title_english=None):
        """Add a sub-subsection heading"""
        heading_text = heb(title_hebrew)
        if title_english:
            heading_text += f" ({title_english})"
        self.elements.append(Paragraph(heading_text, self.styles['heading3']))

    def add_paragraph(self, text, emphasized=False):
        """Add a body paragraph"""
        style = self.styles['body_em'] if emphasized else self.styles['body']
        self.elements.append(Paragraph(heb(text), style))

    def add_bullet_list(self, items, bullet_char="∙"):
        """Add a bullet list with purple bullets"""
        for item in items:
            display = heb(item)
            styled = f'{display} <font name="{MAIN_FONT}" color="#8C6BBE" size="14">{bullet_char}</font>'
            self.elements.append(Paragraph(styled, self.styles['bullet']))

    def add_numbered_steps(self, steps):
        """Add numbered steps with purple circles"""
        circled_numbers = "❶❷❸❹❺❻❼❽❾❿"
        for i, step in enumerate(steps, 1):
            num_char = circled_numbers[i-1] if i <= 10 else str(i)
            step_text = f"<font color='{METEOR_BLUE.hexval()}'><b>{num_char}</b></font> {heb(step)}"
            self.elements.append(Paragraph(step_text, self.styles['bullet']))

    def add_info_box(self, box_type, title, content):
        """Add an info box"""
        self.elements.append(Spacer(1, 3*mm))
        self.elements.append(InfoBox(box_type, title, content))
        self.elements.append(Spacer(1, 3*mm))

    def add_flow_step(self, emoji, title, description):
        """Add a flow diagram step"""
        self.elements.append(FlowStep(emoji, title, description))

    def add_flow_arrow(self):
        """Add a flow arrow connector"""
        self.elements.append(FlowArrow())

    def add_table(self, headers, data, col_widths=None, table_type='clinical'):
        """Add a table"""
        self.elements.append(Spacer(1, 3*mm))

        if table_type == 'clinical':
            self.elements.append(create_clinical_table(headers, data, col_widths))
        elif table_type == 'traffic':
            self.elements.append(create_traffic_light_table(headers, data))

        self.elements.append(Spacer(1, 3*mm))

    def add_comparison_table(self, correct_header, incorrect_header, correct_items, incorrect_items):
        """Add a comparison table with ✅ vs ❌"""
        self.elements.append(Spacer(1, 3*mm))
        self.elements.append(create_comparison_table(
            correct_header, incorrect_header,
            correct_items, incorrect_items
        ))
        self.elements.append(Spacer(1, 3*mm))

    def add_gradient_bar(self, text, bar_type='purple'):
        """Add a gradient header bar"""
        colors_map = {
            'purple': (METEOR_BLUE, METEOR_PURPLE),
            'orange': (HexColor('#FF7043'), HexColor('#FFB74D')),
            'green': (HexColor('#66BB6A'), HexColor('#81C784'))
        }
        color1, color2 = colors_map.get(bar_type, colors_map['purple'])

        self.elements.append(Spacer(1, 3*mm))
        self.elements.append(GradientRect(CW, 10*mm, color1, color2, text))
        self.elements.append(Spacer(1, 3*mm))

    def add_fade_line(self):
        """Add a decorative fade line separator"""
        self.elements.append(FadeLine())

    def add_spacer(self, height_mm=5):
        """Add vertical space"""
        self.elements.append(Spacer(1, height_mm*mm))

    def add_page_break(self):
        """Add a page break"""
        self.elements.append(PageBreak())

    def add_success_page(self, message="בהצלחה בלימודים!"):
        """Add a success/closing page"""
        self.elements.append(Spacer(1, 30*mm))
        self.elements.append(InfoBox('success', message, ""))

        if self.source:
            self.elements.append(Spacer(1, 10*mm))
            source_text = f"מקור: {self.source} | © Meteor Focus | meteorfocus@gmail.com | he.meteorfocus.com"
            self.elements.append(Paragraph(heb(source_text), self.styles['footer']))

    def _header_footer(self, canvas, doc):
        """Draw header and footer on each page"""
        canvas.saveState()
        width, height = self.pagesize

        # Top gradient line
        steps = 60
        sw = width / steps
        for i in range(steps):
            t = i / (steps - 1)
            r = METEOR_BLUE.red + (FOCUS_PURPLE.red - METEOR_BLUE.red) * t
            g = METEOR_BLUE.green + (FOCUS_PURPLE.green - METEOR_BLUE.green) * t
            b = METEOR_BLUE.blue + (FOCUS_PURPLE.blue - METEOR_BLUE.blue) * t
            canvas.setStrokeColor(Color(r, g, b))
            canvas.setLineWidth(2.5)
            canvas.line(i*sw, height - 10*mm, (i+1)*sw, height - 10*mm)

        # Header text
        canvas.setFont(MAIN_FONT, 8)
        canvas.setFillColor(FOCUS_PURPLE)
        canvas.drawString(ML, height - 8*mm, "METEOR FOCUS")

        if self.title:
            hr = bidi(self.title[:40])
            hw = pdfmetrics.stringWidth(hr, MAIN_FONT, 8)
            canvas.drawString(width - MR - hw, height - 8*mm, hr)

        # Footer line
        canvas.setStrokeColor(SUBTLE_LINE)
        canvas.setLineWidth(0.4)
        canvas.line(ML, 16*mm, width - MR, 16*mm)

        # Footer text
        canvas.setFont(MAIN_FONT, 7)
        canvas.setFillColor(LIGHT_TEXT)
        canvas.drawString(ML, 12*mm, "he.meteorfocus.com")

        # Page number
        pn = str(doc.page)
        pnw = pdfmetrics.stringWidth(pn, MAIN_FONT, 7)
        canvas.drawString((width - pnw)/2, 12*mm, pn)

        # Copyright
        canvas.drawRightString(width - MR, 12*mm, "© Meteor Focus")

        canvas.restoreState()

    def build(self):
        """Build and save the PDF"""
        self.doc.build(
            self.elements,
            onFirstPage=self._header_footer,
            onLaterPages=self._header_footer
        )
        return self.filename


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================
def create_summary_pdf(filename, title, subtitle, source, sections, toc_items=None):
    """Quick function to create a summary PDF"""
    pdf = MeteorFocusPDF(filename, title, subtitle, source)

    if toc_items:
        pdf.add_cover_page(toc_items)

    for section in sections:
        pdf.add_section(
            section.get('number', 1),
            section.get('title_hebrew', ''),
            section.get('title_english')
        )

        for content in section.get('content', []):
            content_type = content.get('type')

            if content_type == 'paragraph':
                pdf.add_paragraph(content.get('text', ''))

            elif content_type == 'bullets':
                pdf.add_bullet_list(content.get('items', []))

            elif content_type == 'steps':
                pdf.add_numbered_steps(content.get('items', []))

            elif content_type == 'info_box':
                pdf.add_info_box(
                    content.get('box_type', 'tip'),
                    content.get('title', ''),
                    content.get('content', '')
                )

            elif content_type == 'table':
                pdf.add_table(
                    content.get('headers', []),
                    content.get('data', []),
                    content.get('col_widths'),
                    content.get('table_type', 'clinical')
                )

            elif content_type == 'comparison':
                pdf.add_comparison_table(
                    content.get('correct_header', ''),
                    content.get('incorrect_header', ''),
                    content.get('correct_items', []),
                    content.get('incorrect_items', [])
                )

            elif content_type == 'subsection':
                pdf.add_subsection(
                    content.get('title_hebrew', ''),
                    content.get('title_english')
                )

            elif content_type == 'gradient_bar':
                pdf.add_gradient_bar(
                    content.get('text', ''),
                    content.get('bar_type', 'purple')
                )

            elif content_type == 'flow_step':
                pdf.add_flow_step(
                    content.get('emoji', ''),
                    content.get('title', ''),
                    content.get('description', '')
                )

            elif content_type == 'flow_arrow':
                pdf.add_flow_arrow()

            elif content_type == 'fade_line':
                pdf.add_fade_line()

    pdf.add_success_page()
    return pdf.build()


if __name__ == "__main__":
    print("Meteor Focus PDF Generator v2.0 loaded successfully!")
    print(f"Using font: {MAIN_FONT}")
    print(f"Available box types: tip, note, warning, remember, forbidden, success")
    print(f"Available table types: clinical, comparison, traffic")
    print(f"New features: NumberedCircleHeader, SubsectionHeader, FadeLine, FlowStep, FlowArrow")
