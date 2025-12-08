#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏥 סקריפט הרצה מהירה - תיקון שאלות בחינה סיעודית

שימוש:
    python3 run_fixer.py /path/to/your/file.xlsx

או פשוט:
    python3 run_fixer.py
    (ואז גררי את הקובץ לטרמינל)
"""

import sys
import os
from nursing_exam_processor import NursingExamProcessor, display_questions_for_approval


def quick_process(file_path: str):
    """עיבוד מהיר של קובץ"""

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     🏥 תיקון מהיר - שאלות בחינה סיעודית                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # בדיקת קובץ
    file_path = file_path.strip().strip('"\'')

    if not os.path.exists(file_path):
        print(f"❌ קובץ לא נמצא: {file_path}")
        return

    if not file_path.endswith(('.xlsx', '.xls')):
        print("❌ הקובץ חייב להיות בפורמט Excel (.xlsx או .xls)")
        return

    print(f"📁 קובץ: {file_path}")
    print()

    # יצירת מעבד
    processor = NursingExamProcessor(file_path)

    # טעינה
    results = processor.load_file()

    # שאלה למשתמש
    print("\n" + "─"*50)
    confirm = input("🔄 להמשיך בעיבוד אוטומטי? (Enter להמשיך, 'לא' לביטול): ").strip()

    if confirm.lower() in ['לא', 'no', 'n']:
        print("❌ בוטל")
        return

    # עיבוד כל הגיליונות
    print("\n🔄 מעבד את כל הגיליונות...")

    for sheet_name in processor.df_dict.keys():
        processor.process_sheet(sheet_name, interactive=False)

    # הצגת כמה שאלות לדוגמה
    print("\n" + "═"*70)
    print("📋 דוגמאות לשאלות מעובדות:")
    print("═"*70)

    first_sheet = list(processor.df_dict.keys())[0]
    display_questions_for_approval(processor.df_dict[first_sheet], 0, 5)

    # שאלה לשמירה
    print("\n" + "─"*50)
    save_confirm = input("💾 לשמור את הקובץ המתוקן? (Enter לשמור, 'לא' לביטול): ").strip()

    if save_confirm.lower() in ['לא', 'no', 'n']:
        print("❌ לא נשמר")
        return

    # שמירה
    output_path = processor.save()

    # דוח סיכום
    print("\n" + processor.generate_report())

    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                      ✅ הושלם בהצלחה!                        ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  📁 קובץ מתוקן נשמר ב:                                       ║
    ║  {output_path[:56]:<56} ║
    ╚══════════════════════════════════════════════════════════════╝
    """)


def main():
    """פונקציה ראשית"""

    if len(sys.argv) > 1:
        # קובץ מועבר כארגומנט
        file_path = sys.argv[1]
    else:
        # בקשת קובץ מהמשתמש
        print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     🏥 תיקון מהיר - שאלות בחינה סיעודית                      ║
    ╚══════════════════════════════════════════════════════════════╝
        """)
        print("💡 טיפ: גררי את קובץ ה-Excel לחלון הטרמינל")
        print()
        file_path = input("📁 הזיני נתיב לקובץ Excel: ").strip()

    if not file_path:
        print("❌ לא הוזן נתיב")
        return

    quick_process(file_path)


if __name__ == "__main__":
    main()
