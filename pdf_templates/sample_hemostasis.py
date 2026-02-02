#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hemostasis Summary PDF - מערכת הקרישה
Based on Meteor Focus Design System
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from meteor_focus_pdf import MeteorFocusPDF


def create_hemostasis_summary():
    """Create hemostasis summary PDF"""

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'hemostasis_summary.pdf')

    # Initialize PDF
    pdf = MeteorFocusPDF(
        filename=output_path,
        title="מערכת הקרישה וההמוסטאזיס",
        subtitle="סיכום מקיף | Hemostasis & Coagulation | פיזיולוגיה",
        source="Ignatavicius Medical-Surgical Nursing, 11th Edition"
    )

    # Table of Contents
    toc_items = [
        "מטרת מערכת הקרישה",
        "אבני הבניין של ההמוסטאזיס",
        "שלושת הצירים של ההמוסטאזיס"
    ]
    pdf.add_cover_page(toc_items)

    # ==========================================================================
    # Section 1: Purpose of the Coagulation System
    # ==========================================================================
    pdf.add_section(1, "מטרת מערכת הקרישה", "Purpose of the Coagulation System")

    pdf.add_paragraph(
        "המטרה המרכזית של מערכת ההמוסטאזיס היא לעצור דימום מבלי לעצור את זרימת הדם הכללית. "
        "מדובר במנגנון מבוקר, מקומי ומדויק, שמופעל אך ורק במקום שבו נגרם נזק לכלי דם."
    )

    pdf.add_paragraph(
        "הגוף נדרש לאזן בין שני צרכים מנוגדים: מצד אחד למנוע אובדן דם, "
        "ומצד שני לשמור על פרפוזיה תקינה לכל שאר הרקמות."
    )

    pdf.add_info_box(
        'remember',
        'חשוב לבחינה',
        'המערכת חייבת לייצר קריש יציב רק באתר הפגיעה, תוך מניעה של יצירת קרישים מפושטים שעלולים לחסום זרימת דם תקינה.'
    )

    # ==========================================================================
    # Section 2: Building Blocks of Hemostasis
    # ==========================================================================
    pdf.add_section(2, "אבני הבניין של ההמוסטאזיס", "Building Blocks of Hemostasis")

    # 2.1 Platelets
    pdf.add_subsection("טסיות דם והפקק הטסייתי", "Platelets & Platelet Plug")

    pdf.add_paragraph(
        "הטסיות הן מרכיב מרכזי בשלב הראשוני של ההמוסטאזיס. במצב תקין הן נעות בזרם הדם "
        "כיחידות נפרדות ואינן נצמדות זו לזו."
    )

    pdf.add_paragraph(
        "בעת פגיעה בדופן כלי הדם מתרחש תהליך של הפעלת טסיות, שבמהלכו משתנה המבנה של "
        "ממברנת הטסית והיא נעשית \"דביקה\". כתוצאה מכך הטסיות נצמדות זו לזו בתהליך של "
        "Aggregation ויוצרות פקק טסייתי חצי-מוצק החוסם זמנית את אזור הפגיעה."
    )

    pdf.add_info_box(
        'note',
        'שימו לב',
        'הפקק הטסייתי אינו קריש יציב! הוא זמני, מחזיק שעות ספורות בלבד, ואינו מספק המוסטאזיס מלא. תפקידו העיקרי הוא לייצר חסימה ראשונית ולהפעיל את המשך תהליך הקרישה.'
    )

    # 2.2 Platelet activating substances
    pdf.add_subsection("חומרים מפעילי טסיות", "Platelet Activating Substances")

    pdf.add_paragraph(
        "הפעלת הטסיות וההיצמדות ביניהן מתרחשת בעקבות חשיפה ושחרור של מספר חומרים מרכזיים:"
    )

    pdf.add_bullet_list([
        "ADP - אדנוזין דיפוספט",
        "סידן (Ca++)",
        "Thromboxane A₂ (TXA₂) - תרומבוקסן",
        "קולגן (Collagen)"
    ])

    pdf.add_info_box(
        'tip',
        'טיפ לזכירה',
        'הטסיות עצמן מפרישות חלק מהחומרים הללו לאחר שהופעלו, וכך נוצר מנגנון של הגברה עצמית (Positive Feedback) שמחזק את יצירת הפקק הטסייתי.'
    )

    # 2.3 Clotting factors
    pdf.add_subsection("גורמי הקרישה וסידן", "Clotting Factors & Calcium")

    pdf.add_paragraph(
        "מעבר לשלב הטסייתי, תהליך ההמוסטאזיס תלוי במערכת של גורמי קרישה. "
        "גורמים אלו הם אנזימים המצויים בדם במצב לא פעיל, והם מופעלים בסדרה מדורגת."
    )

    pdf.add_paragraph(
        "כל גורם שמופעל מפעיל את הגורם הבא אחריו, וכך נוצרת שרשרת תגובות רציפה (Cascade)."
    )

    pdf.add_info_box(
        'warning',
        'חשוב לדעת',
        'סידן וטסיות משתתפים כמעט בכל שלב של הקסקדה, והיעדרם פוגע משמעותית ביכולת ליצור קריש יציב.'
    )

    # ==========================================================================
    # Section 3: Three Axes of Hemostasis
    # ==========================================================================
    pdf.add_page_break()
    pdf.add_section(3, "שלושת הצירים של ההמוסטאזיס", "Three Axes of Hemostasis")

    pdf.add_gradient_bar("מפגיעה לקריש יציב", "purple")

    # 3.1 Platelet plug
    pdf.add_subsection("הפקק הטסייתי - ההתחלה המיידית", "Platelet Plug - Immediate Response")

    pdf.add_paragraph(
        "מיד לאחר פגיעה בדופן כלי הדם מתרחשת היצמדות טסיות ויצירת פקק טסייתי זמני. "
        "שלב זה מתרחש במהירות ומהווה את הטריגר להפעלת מנגנון הקרישה האנזימטי."
    )

    # 3.2 Coagulation cascade
    pdf.add_subsection("קסקדת הקרישה - מנגנון מתעצם", "Coagulation Cascade")

    pdf.add_paragraph(
        "קסקדת הקרישה היא מנגנון של שרשרת תגובות שמתחזקת במהירות. "
        "התחלה מינימלית עלולה להוביל לתגובה מתגלגלת רחבה, שקשה לעצור לאחר שהחלה."
    )

    pdf.add_info_box(
        'warning',
        'זהירות',
        'זהו מנגנון יעיל אך גם מסוכן אם אינו מבוקר כראוי!'
    )

    # 3.3 Pathways
    pdf.add_subsection("הנתיבים של הקסקדה", "Cascade Pathways")

    pdf.add_paragraph("הקסקדה מופעלת דרך שני נתיבים:")

    # Comparison table for pathways
    pdf.add_comparison_table(
        correct_header="המסלול החיצוני (Extrinsic)",
        incorrect_header="המסלול הפנימי (Intrinsic)",
        correct_items=[
            "מופעל ע\"י נזק רקמתי",
            "Tissue Factor (TF)",
            "מהיר יותר",
            "Factor VII"
        ],
        incorrect_items=[
            "מופעל ע\"י מגע עם משטח",
            "Contact Activation",
            "איטי יותר",
            "Factors XII, XI, IX, VIII"
        ]
    )

    pdf.add_info_box(
        'remember',
        'חשוב לבחינה',
        'שני המסלולים מתאחדים בהמשך לנתיב משותף (Common Pathway), שבסופו נוצר קריש פיברין יציב המספק המוסטאזיס מלא ומבוקר.'
    )

    # Summary section
    pdf.add_gradient_bar("סיכום נקודות מפתח", "green")

    pdf.add_bullet_list([
        "מטרת ההמוסטאזיס: עצירת דימום מקומית מבלי לפגוע בזרימת הדם הכללית",
        "הפקק הטסייתי הוא זמני בלבד - מחזיק שעות ספורות",
        "חומרים מפעילי טסיות: ADP, סידן, TXA₂, קולגן",
        "גורמי הקרישה מופעלים בשרשרת (קסקדה)",
        "סידן חיוני כמעט בכל שלב של הקסקדה",
        "שני נתיבים: חיצוני (מהיר) ופנימי (איטי) → נתיב משותף → פיברין"
    ])

    # Success page
    pdf.add_page_break()
    pdf.add_success_page()

    # Build PDF
    output_file = pdf.build()
    print(f"PDF created successfully: {output_file}")
    return output_file


if __name__ == "__main__":
    create_hemostasis_summary()
