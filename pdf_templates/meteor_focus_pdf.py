#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meteor Focus PDF Generator
===========================
מערכת עיצוב Meteor Focus - סיכומים לימודיים | טבלאות שאלות | חומרי לימוד

Design System Version: 1.0
"""

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, Color
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, KeepTogether, ListFlowable, ListItem, Flowable
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.graphics.shapes import Drawing, Rect, Circle, String
from reportlab.graphics import renderPDF
import os

# =============================================================================
# FONT REGISTRATION
# =============================================================================
FONT_PATH = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(FONT_PATH, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', os.path.join(FONT_PATH, 'DejaVuSans-Bold.ttf')))

# =============================================================================
# BRAND COLORS - צבעי מותג
# =============================================================================
METEOR_BLUE = HexColor('#5A6FD6')       # METEOR שמאל, כותרות ראשיות
METEOR_PURPLE = HexColor('#8C6BBE')     # METEOR ימין, כותרות משנה
METEOR_LIGHT = HexColor('#8F73C8')      # FOCUS, קווי תחתון
METEOR_ICON = HexColor('#5F6FDB')       # קווי מתאר אייקונים
WHITE = HexColor('#FFFFFF')             # רקע

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

# Traffic Light Colors - מערכת רמות
GREEN_BG = HexColor('#E8F5E9')
GREEN_TEXT = HexColor('#2E7D32')
YELLOW_BG = HexColor('#FFF9C4')
YELLOW_TEXT = HexColor('#F57F17')
RED_BG = HexColor('#FFEBEE')
RED_TEXT = HexColor('#C62828')

# Table Colors
ZEBRA_LIGHT = HexColor('#F8F9FF')
HEADER_LAVENDER = HexColor('#E8EAF6')
GRID_LIGHT = HexColor('#E0E0E0')

# Success box
SUCCESS_BG = HexColor('#E8F5E9')
SUCCESS_BORDER = HexColor('#4CAF50')


# =============================================================================
# HEBREW TEXT HELPER
# =============================================================================
def heb(text):
    """Convert Hebrew text for proper RTL display in PDF"""
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def heb_with_english(hebrew_text, english_text=None):
    """Format Hebrew text with optional English in parentheses"""
    if english_text:
        # Keep English LTR within Hebrew RTL context
        combined = f"{hebrew_text} ({english_text})"
        reshaped = arabic_reshaper.reshape(combined)
        return get_display(reshaped)
    return heb(hebrew_text)


# =============================================================================
# CUSTOM FLOWABLES
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
        # Simulate gradient with multiple rectangles
        steps = 20
        for i in range(steps):
            r = self.color1.red + (self.color2.red - self.color1.red) * i / steps
            g = self.color1.green + (self.color2.green - self.color1.green) * i / steps
            b = self.color1.blue + (self.color2.blue - self.color1.blue) * i / steps
            self.canv.setFillColor(Color(r, g, b))
            x = i * self.width / steps
            self.canv.rect(x, 0, self.width / steps + 1, self.height, fill=1, stroke=0)

        if self.text:
            self.canv.setFillColor(self.text_color)
            self.canv.setFont('DejaVuSans-Bold', 14)
            self.canv.drawCentredString(self.width / 2, self.height / 2 - 5, heb(self.text))


class NumberedCircle(Flowable):
    """Purple numbered circle for main headings"""
    def __init__(self, number, size=24):
        Flowable.__init__(self)
        self.number = number
        self.size = size
        self.width = size
        self.height = size

    def draw(self):
        # Draw gradient circle (simulated)
        self.canv.setFillColor(METEOR_BLUE)
        self.canv.circle(self.size/2, self.size/2, self.size/2, fill=1, stroke=0)

        # Inner lighter circle for gradient effect
        self.canv.setFillColor(METEOR_PURPLE)
        self.canv.circle(self.size/2, self.size/2, self.size/2 - 2, fill=1, stroke=0)

        # Number
        self.canv.setFillColor(WHITE)
        self.canv.setFont('DejaVuSans-Bold', 12)
        self.canv.drawCentredString(self.size/2, self.size/2 - 4, str(self.number))


class InfoBox(Flowable):
    """Info box with emoji, title and content"""
    def __init__(self, box_type, title, content, width=None):
        Flowable.__init__(self)
        self.box_type = box_type
        self.title = title
        self.content = content
        self.box_width = width or 170*mm

        # Set colors based on box type
        self.colors = {
            'tip': (BOX_TIP_BG, BOX_TIP_BORDER, '⭐'),           # טיפ
            'note': (BOX_NOTE_BG, BOX_NOTE_BORDER, '💡'),        # שימו לב
            'warning': (BOX_WARN_BG, BOX_WARN_BORDER, '⚠️'),     # אזהרה
            'remember': (BOX_REMEMBER_BG, BOX_REMEMBER_BORDER, '📌'),  # זכרו
            'forbidden': (BOX_FORBID_BG, BOX_FORBID_BORDER, '🚫'),    # אסור
            'success': (SUCCESS_BG, SUCCESS_BORDER, '✔'),        # הצלחה
        }

        bg, border, emoji = self.colors.get(box_type, (BOX_TIP_BG, BOX_TIP_BORDER, ''))
        self.bg_color = bg
        self.border_color = border
        self.emoji = emoji

        # Calculate height based on content
        self.box_height = 50 + len(content) // 50 * 10

    def wrap(self, availWidth, availHeight):
        self.box_width = min(self.box_width, availWidth)
        return (self.box_width, self.box_height)

    def draw(self):
        # Background
        self.canv.setFillColor(self.bg_color)
        self.canv.roundRect(0, 0, self.box_width, self.box_height, 8, fill=1, stroke=0)

        # Left accent bar
        self.canv.setFillColor(self.border_color)
        self.canv.roundRect(self.box_width - 6, 0, 6, self.box_height, 3, fill=1, stroke=0)

        # Border
        self.canv.setStrokeColor(self.border_color)
        self.canv.setLineWidth(1.5)
        self.canv.roundRect(0, 0, self.box_width, self.box_height, 8, fill=0, stroke=1)

        # Title with emoji
        self.canv.setFillColor(HexColor('#333333'))
        self.canv.setFont('DejaVuSans-Bold', 11)
        title_text = f"{self.emoji} {heb(self.title)}"
        self.canv.drawRightString(self.box_width - 15, self.box_height - 20, title_text)

        # Content
        self.canv.setFont('DejaVuSans', 10)
        content_lines = self._wrap_text(heb(self.content), self.box_width - 30)
        y = self.box_height - 38
        for line in content_lines:
            self.canv.drawRightString(self.box_width - 15, y, line)
            y -= 14

    def _wrap_text(self, text, max_width):
        """Simple text wrapping"""
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if len(test_line) * 6 < max_width:  # Approximate character width
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines[:3]  # Limit to 3 lines


# =============================================================================
# PARAGRAPH STYLES
# =============================================================================
def get_styles():
    """Get all paragraph styles for the document"""
    styles = {}

    # Main title - כותרת ראשית
    styles['title'] = ParagraphStyle(
        'Title',
        fontName='DejaVuSans-Bold',
        fontSize=24,
        textColor=METEOR_BLUE,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=30
    )

    # Subtitle - כותרת משנה
    styles['subtitle'] = ParagraphStyle(
        'Subtitle',
        fontName='DejaVuSans',
        fontSize=14,
        textColor=METEOR_PURPLE,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # Section heading - כותרת סעיף
    styles['heading1'] = ParagraphStyle(
        'Heading1',
        fontName='DejaVuSans-Bold',
        fontSize=14,
        textColor=METEOR_BLUE,
        alignment=TA_RIGHT,
        spaceBefore=16,
        spaceAfter=8,
        leading=18
    )

    # Subheading - כותרת משנה
    styles['heading2'] = ParagraphStyle(
        'Heading2',
        fontName='DejaVuSans-Bold',
        fontSize=12,
        textColor=METEOR_PURPLE,
        alignment=TA_RIGHT,
        spaceBefore=12,
        spaceAfter=6,
        leading=16,
        borderWidth=0,
        borderColor=METEOR_LIGHT,
        borderPadding=0
    )

    # Body text - טקסט גוף
    styles['body'] = ParagraphStyle(
        'Body',
        fontName='DejaVuSans',
        fontSize=10,
        textColor=HexColor('#333333'),
        alignment=TA_RIGHT,
        spaceBefore=4,
        spaceAfter=4,
        leading=14
    )

    # Bullet text - טקסט נקודה
    styles['bullet'] = ParagraphStyle(
        'Bullet',
        fontName='DejaVuSans',
        fontSize=10,
        textColor=HexColor('#333333'),
        alignment=TA_RIGHT,
        leftIndent=20,
        bulletIndent=10,
        leading=14
    )

    # Table header
    styles['table_header'] = ParagraphStyle(
        'TableHeader',
        fontName='DejaVuSans-Bold',
        fontSize=10,
        textColor=HexColor('#333333'),
        alignment=TA_RIGHT,
        leading=12
    )

    # Table cell
    styles['table_cell'] = ParagraphStyle(
        'TableCell',
        fontName='DejaVuSans',
        fontSize=9,
        textColor=HexColor('#333333'),
        alignment=TA_RIGHT,
        leading=12
    )

    # Footer
    styles['footer'] = ParagraphStyle(
        'Footer',
        fontName='DejaVuSans',
        fontSize=8,
        textColor=HexColor('#888888'),
        alignment=TA_CENTER
    )

    # TOC - תוכן עניינים
    styles['toc'] = ParagraphStyle(
        'TOC',
        fontName='DejaVuSans',
        fontSize=11,
        textColor=HexColor('#333333'),
        alignment=TA_RIGHT,
        leftIndent=20,
        spaceBefore=4,
        spaceAfter=4
    )

    return styles


# =============================================================================
# TABLE BUILDERS
# =============================================================================
def create_clinical_table(headers, data, col_widths=None):
    """
    Create a clinical summary table with Meteor Focus styling

    Args:
        headers: List of header strings
        data: List of lists containing row data
        col_widths: Optional list of column widths
    """
    styles = get_styles()

    # Prepare headers (RTL)
    formatted_headers = [Paragraph(heb(h), styles['table_header']) for h in headers]

    # Prepare data rows
    formatted_data = [formatted_headers]
    for row in data:
        formatted_row = []
        for cell in row:
            if isinstance(cell, str):
                formatted_row.append(Paragraph(heb(cell), styles['table_cell']))
            else:
                formatted_row.append(cell)
        formatted_data.append(formatted_row)

    # Create table
    if col_widths:
        table = Table(formatted_data, colWidths=col_widths)
    else:
        table = Table(formatted_data)

    # Apply style
    style = TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_LAVENDER),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#333333')),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),

        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),

        # Borders
        ('GRID', (0, 0), (-1, -1), 0.5, GRID_LIGHT),
        ('LINEBELOW', (0, 0), (-1, 0), 2, METEOR_BLUE),

        # Zebra striping
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, ZEBRA_LIGHT]),

        # Alignment
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    table.setStyle(style)
    return table


def create_comparison_table(left_header, right_header, left_items, right_items):
    """
    Create a comparison table with ✅ vs ❌ styling

    Args:
        left_header: Header for left column (correct/recommended)
        right_header: Header for right column (incorrect/not recommended)
        left_items: List of correct items
        right_items: List of incorrect items
    """
    styles = get_styles()

    # Prepare data
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
        # Headers
        ('BACKGROUND', (0, 0), (0, 0), RED_BG),
        ('BACKGROUND', (1, 0), (1, 0), GREEN_BG),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

        # Data
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),

        # Borders
        ('GRID', (0, 0), (-1, -1), 1, GRID_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1.5, GRID_LIGHT),

        # Alignment
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ])

    table.setStyle(style)
    return table


def create_traffic_light_table(headers, data):
    """
    Create a table with traffic light (🟢🟡🔴) indicators

    The last column should contain 'green', 'yellow', or 'red' as values
    """
    styles = get_styles()

    # Process headers
    formatted_headers = [Paragraph(heb(h), styles['table_header']) for h in headers]

    # Process data with traffic light colors
    formatted_data = [formatted_headers]
    for row in data:
        formatted_row = []
        for i, cell in enumerate(row):
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
            subtitle: Optional subtitle (e.g., "סיכום מקיף | שוק | סיעוד פנימי")
            source: Source reference (e.g., "Ignatavicius, Chapter 35")
            landscape_mode: Use landscape orientation
        """
        self.filename = filename
        self.title = title
        self.subtitle = subtitle or ""
        self.source = source or ""
        self.styles = get_styles()
        self.elements = []
        self.page_count = 0

        # Page setup
        if landscape_mode:
            self.pagesize = landscape(A4)
        else:
            self.pagesize = A4

        self.doc = SimpleDocTemplate(
            filename,
            pagesize=self.pagesize,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=25*mm,
            bottomMargin=25*mm
        )

    def add_cover_page(self, toc_items=None):
        """Add a cover page with title and optional table of contents"""
        # Logo placeholder (gradient bar as header)
        self.elements.append(GradientRect(170*mm, 12*mm, METEOR_BLUE, METEOR_PURPLE, "METEOR FOCUS"))
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
        """Add a numbered section heading"""
        # Create heading with number circle
        heading_text = f"<font color='{METEOR_BLUE.hexval()}'><b>{heb(title_hebrew)}</b></font>"
        if title_english:
            heading_text += f" <font size='10' color='{METEOR_PURPLE.hexval()}'><i>({title_english})</i></font>"

        # Number indicator
        number_text = f"<font color='{METEOR_BLUE.hexval()}'><b>⬤ {number}</b></font>  "
        full_heading = number_text + heading_text

        self.elements.append(Spacer(1, 8*mm))
        self.elements.append(Paragraph(full_heading, self.styles['heading1']))

        # Underline
        self.elements.append(Spacer(1, 2))

    def add_subsection(self, title_hebrew, title_english=None):
        """Add a subsection heading"""
        heading_text = heb(title_hebrew)
        if title_english:
            heading_text += f" ({title_english})"

        self.elements.append(Paragraph(
            f"<u>{heb(heading_text)}</u>",
            self.styles['heading2']
        ))

    def add_paragraph(self, text):
        """Add a body paragraph"""
        self.elements.append(Paragraph(heb(text), self.styles['body']))

    def add_bullet_list(self, items, bullet_char="●"):
        """Add a bullet list with purple bullets"""
        for item in items:
            bullet_text = f"<font color='{METEOR_PURPLE.hexval()}'>{bullet_char}</font> {heb(item)}"
            self.elements.append(Paragraph(bullet_text, self.styles['bullet']))

    def add_numbered_steps(self, steps):
        """Add numbered steps with purple circles"""
        circled_numbers = "❶❷❸❹❺❻❼❽❾❿"
        for i, step in enumerate(steps, 1):
            num_char = circled_numbers[i-1] if i <= 10 else str(i)
            step_text = f"<font color='{METEOR_BLUE.hexval()}'><b>{num_char}</b></font> {heb(step)}"
            self.elements.append(Paragraph(step_text, self.styles['bullet']))

    def add_info_box(self, box_type, title, content):
        """
        Add an info box

        Args:
            box_type: 'tip', 'note', 'warning', 'remember', 'forbidden', 'success'
            title: Box title
            content: Box content
        """
        self.elements.append(Spacer(1, 5*mm))
        self.elements.append(InfoBox(box_type, title, content))
        self.elements.append(Spacer(1, 5*mm))

    def add_table(self, headers, data, col_widths=None, table_type='clinical'):
        """
        Add a table

        Args:
            headers: List of header strings
            data: List of lists for row data
            col_widths: Optional column widths
            table_type: 'clinical', 'comparison', or 'traffic'
        """
        self.elements.append(Spacer(1, 5*mm))

        if table_type == 'clinical':
            self.elements.append(create_clinical_table(headers, data, col_widths))
        elif table_type == 'traffic':
            self.elements.append(create_traffic_light_table(headers, data))

        self.elements.append(Spacer(1, 5*mm))

    def add_comparison_table(self, correct_header, incorrect_header, correct_items, incorrect_items):
        """Add a comparison table with ✅ vs ❌"""
        self.elements.append(Spacer(1, 5*mm))
        self.elements.append(create_comparison_table(
            correct_header, incorrect_header,
            correct_items, incorrect_items
        ))
        self.elements.append(Spacer(1, 5*mm))

    def add_gradient_bar(self, text, bar_type='purple'):
        """
        Add a gradient header bar

        Args:
            text: Bar text
            bar_type: 'purple', 'orange', 'green'
        """
        colors_map = {
            'purple': (METEOR_BLUE, METEOR_PURPLE),
            'orange': (HexColor('#FF7043'), HexColor('#FFB74D')),
            'green': (HexColor('#66BB6A'), HexColor('#81C784'))
        }
        color1, color2 = colors_map.get(bar_type, colors_map['purple'])

        self.elements.append(Spacer(1, 5*mm))
        self.elements.append(GradientRect(170*mm, 10*mm, color1, color2, text))
        self.elements.append(Spacer(1, 5*mm))

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

        # Header - Gradient bar placeholder
        canvas.setFillColor(METEOR_BLUE)
        canvas.rect(20*mm, height - 18*mm, width - 40*mm, 8*mm, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont('DejaVuSans-Bold', 10)
        canvas.drawCentredString(width/2, height - 15*mm, "METEOR FOCUS")

        # Footer
        canvas.setFont('DejaVuSans', 8)
        canvas.setFillColor(HexColor('#888888'))

        # Page number
        page_text = heb(f"עמוד {doc.page}")
        canvas.drawCentredString(width/2, 15*mm, page_text)

        # Website
        canvas.drawString(20*mm, 15*mm, "he.meteorfocus.com")

        # Copyright
        canvas.drawRightString(width - 20*mm, 15*mm, "© Meteor Focus")

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
    """
    Quick function to create a summary PDF

    Args:
        filename: Output filename
        title: Document title
        subtitle: Document subtitle
        source: Source reference
        sections: List of section dictionaries with structure:
            {
                'number': 1,
                'title_hebrew': 'הגדרה',
                'title_english': 'Definition',
                'content': [
                    {'type': 'paragraph', 'text': '...'},
                    {'type': 'bullets', 'items': ['...', '...']},
                    {'type': 'info_box', 'box_type': 'tip', 'title': '...', 'content': '...'},
                    {'type': 'table', 'headers': [...], 'data': [...]},
                ]
            }
        toc_items: Optional table of contents items
    """
    pdf = MeteorFocusPDF(filename, title, subtitle, source)

    # Cover page
    if toc_items:
        pdf.add_cover_page(toc_items)

    # Sections
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

    # Success page
    pdf.add_success_page()

    return pdf.build()


if __name__ == "__main__":
    # Test the module
    print("Meteor Focus PDF Generator loaded successfully!")
    print(f"Available box types: tip, note, warning, remember, forbidden, success")
    print(f"Available table types: clinical, comparison, traffic")
