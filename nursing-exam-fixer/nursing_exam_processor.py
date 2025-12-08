#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏥 מערכת תיקון שאלות בחינה סיעודית
גרסה: 1.0.0
תאריך: דצמבר 2025

מבוסס על PROMPT מקיף לתיקון שאלות בחינה סיעודית בעברית
"""

import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
import re
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

# =============================================
# הגדרות צבעים לפי חטיבה
# =============================================
COLORS = {
    'חוזרים ונהלים': {'header': 'B4C6E7', 'row': 'DAEEF3'},
    'סיעוד האישה': {'header': 'F8CBAD', 'row': 'FDE9D9'},
    'סיעוד המבוגר': {'header': 'B4C6E7', 'row': 'DAEEF3'},
    'סיעוד הנפש': {'header': 'E2BFDC', 'row': 'F2DCDB'},
    'פדיאטריה': {'header': 'C6EFCE', 'row': 'EBF1DE'},
    'פרמקולוגיה': {'header': 'FFF2CC', 'row': 'FFFDE7'},
    'רפואת חירום': {'header': 'B4C6E7', 'row': 'DAEEF3'}
}

# סדר החטיבות למיון
HATIVA_ORDER = [
    'חוזרים ונהלים',
    'סיעוד האישה',
    'סיעוד המבוגר',
    'סיעוד הנפש',
    'פדיאטריה',
    'פרמקולוגיה',
    'רפואת חירום'
]

# מקורות רשמיים
OFFICIAL_SOURCES = {
    'סיעוד הנפש': 'Psychiatric Mental Health Nursing',
    'סיעוד האישה': "Olds' Maternal-Newborn Nursing 12th",
    'סיעוד המבוגר': 'Ignatavicius 11th + Kozier',
    'פדיאטריה': "Wong's Nursing Care 12th",
    'פרמקולוגיה': 'Nursing Drug Handbook 2025-2026',
}

# מונחים מוכרים שלא לתרגם
NO_TRANSLATE_TERMS = [
    'HIV', 'CT', 'MRI', 'ECG', 'DNA', 'RNA', 'ICU', 'ER', 'BP', 'HR',
    'GFR', 'BUN', 'ABG', 'CBC', 'WBC', 'RBC', 'Hb', 'Hct', 'PT', 'PTT',
    'INR', 'BNP', 'CRP', 'ESR', 'HbA1c', 'TSH', 'T3', 'T4', 'PSA',
    'DTaP', 'MMRV', 'IPV', 'Hib', 'PCV', 'IV', 'IM', 'SC', 'PO',
    'PRN', 'BID', 'TID', 'QID', 'STAT', 'NPO', 'CVP', 'PICC', 'TPN'
]

# תרגומים רפואיים נפוצים
MEDICAL_TRANSLATIONS = {
    # תרופות
    'Morphine': 'מורפין',
    'Insulin': 'אינסולין',
    'Heparin': 'הפרין',
    'Digoxin': 'דיגוקסין',
    'Warfarin': 'וורפרין',
    'Furosemide': 'פורוסמיד',
    'Metformin': 'מטפורמין',
    'Omeprazole': 'אומפרזול',
    'Amoxicillin': 'אמוקסיצילין',
    'Paracetamol': 'פרצטמול',
    'Acetaminophen': 'אצטמינופן',
    'Aspirin': 'אספירין',
    'Diazepam': 'דיאזפאם',
    'Lorazepam': 'לוראזפאם',
    'Haloperidol': 'הלופרידול',
    'Risperidone': 'ריספרידון',
    'Lithium': 'ליתיום',
    'Metoprolol': 'מטופרולול',
    'Atenolol': 'אטנולול',
    'Amlodipine': 'אמלודיפין',
    'Lisinopril': 'ליסינופריל',
    'Enalapril': 'אנלפריל',
    'Losartan': 'לוסרטן',
    'Hydrochlorothiazide': 'הידרוכלורותיאזיד',
    'Spironolactone': 'ספירונולקטון',
    'Prednisone': 'פרדניזון',
    'Dexamethasone': 'דקסמתזון',
    'Epinephrine': 'אפינפרין',
    'Adrenaline': 'אדרנלין',
    'Norepinephrine': 'נוראפינפרין',
    'Dopamine': 'דופמין',
    'Dobutamine': 'דובוטמין',
    'Atropine': 'אטרופין',
    'Adenosine': 'אדנוזין',
    'Amiodarone': 'אמיודרון',
    'Lidocaine': 'לידוקאין',
    'Nitroglycerin': 'ניטרוגליצרין',
    'Clopidogrel': 'קלופידוגרל',
    'Enoxaparin': 'אנוקספרין',
    'Alteplase': 'אלטפלאז',

    # אבחנות
    'Diabetes': 'סוכרת',
    'Hypertension': 'יתר לחץ דם',
    'Pneumonia': 'דלקת ריאות',
    'Pancreatitis': 'דלקת לבלב',
    'Cirrhosis': 'שחמת כבד',
    'Glaucoma': 'גלאוקומה',
    'Anemia': 'אנמיה',
    'Sepsis': 'ספסיס',
    'Stroke': 'שבץ מוחי',
    'Myocardial Infarction': 'אוטם שריר הלב',
    'Heart Failure': 'אי ספיקת לב',
    'Renal Failure': 'אי ספיקת כליות',
    'Respiratory Failure': 'אי ספיקה נשימתית',
    'Pulmonary Embolism': 'תסחיף ריאתי',
    'Deep Vein Thrombosis': 'פקקת ורידים עמוקים',
    'Atrial Fibrillation': 'פרפור פרוזדורים',
    'Hypothyroidism': 'תת פעילות בלוטת התריס',
    'Hyperthyroidism': 'יתר פעילות בלוטת התריס',
    'Osteoporosis': 'אוסטאופורוזיס',
    'Arthritis': 'דלקת מפרקים',

    # מצבים
    'Hyponatremia': 'היפונתרמיה',
    'Hypernatremia': 'היפרנתרמיה',
    'Hypokalemia': 'היפוקלמיה',
    'Hyperkalemia': 'היפרקלמיה',
    'Hypoglycemia': 'היפוגליקמיה',
    'Hyperglycemia': 'היפרגליקמיה',
    'Hypocalcemia': 'היפוקלצמיה',
    'Hypercalcemia': 'היפרקלצמיה',
    'Hypomagnesemia': 'היפומגנזמיה',
    'Hypermagnesemia': 'היפרמגנזמיה',
    'Acidosis': 'חמצת',
    'Alkalosis': 'בססת',
    'Hypoxia': 'היפוקסיה',
    'Hypoxemia': 'היפוקסמיה',
    'Tachycardia': 'טכיקרדיה',
    'Bradycardia': 'ברדיקרדיה',
    'Tachypnea': 'טכיפניאה',
    'Bradypnea': 'ברדיפניאה',
    'Dyspnea': 'קוצר נשימה',
    'Edema': 'בצקת',
    'Cyanosis': 'כיחלון',
    'Jaundice': 'צהבת',
    'Ascites': 'מיימת',
}

# Regex patterns לזיהוי בעיות
ISSUE_PATTERNS = {
    'missing_question_mark': r'^(?!.*\?$).+$',
    'double_spaces': r'\s{2,}',
    'space_before_punctuation': r'\s+[?!,.:;]',
    'colon_question': r':\s*\?',
    'student_notes': r'(אני חושב|לא זוכר|משהו כזה|כנראה|\.\.\.|\?{2,})',
    'ends_with_colon': r':$',
}


class NursingExamProcessor:
    """
    מעבד שאלות בחינה סיעודית
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.output_path = None
        self.df_dict = {}  # Dictionary of DataFrames per sheet
        self.changes_log = []
        self.stats = {
            'questions_fixed': 0,
            'distractors_added': 0,
            'linguistic_fixes': 0,
            'hativa_transfers': 0,
        }

    def load_file(self) -> Dict:
        """טוען את קובץ ה-Excel ומנתח אותו"""
        print("=" * 70)
        print("📊 טעינת וניתוח קובץ Excel")
        print("=" * 70)
        print(f"📁 קובץ: {self.file_path}")
        print()

        xl = pd.ExcelFile(self.file_path)

        results = {
            'sheets': {},
            'total_questions': 0,
        }

        for sheet_name in xl.sheet_names:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            self.df_dict[sheet_name] = df

            sheet_info = {
                'rows': len(df),
                'columns': list(df.columns),
                'by_hativa': {},
            }

            # חלוקה לפי חטיבה
            if 'חטיבה' in df.columns:
                sheet_info['by_hativa'] = df['חטיבה'].value_counts().to_dict()

            results['sheets'][sheet_name] = sheet_info
            results['total_questions'] += len(df)

            # הדפסת מידע
            print(f"📋 גיליון: '{sheet_name}'")
            print(f"   • שורות: {len(df)}")
            print(f"   • עמודות: {df.columns.tolist()}")

            if sheet_info['by_hativa']:
                print(f"   • חלוקה לפי חטיבה:")
                for hativa, count in sheet_info['by_hativa'].items():
                    print(f"      - {hativa}: {count} שאלות")
            print()

        print(f"📊 סה\"כ שאלות בקובץ: {results['total_questions']}")
        print("=" * 70)

        return results

    def identify_issues(self, df: pd.DataFrame) -> List[Dict]:
        """מזהה בעיות בשאלות"""
        issues = []

        for idx, row in df.iterrows():
            row_issues = []

            # בדיקת שאלה
            question = str(row.get('שאלה', '')) if pd.notna(row.get('שאלה')) else ''

            # 1. שאלה ללא סימן שאלה
            if question and not question.strip().endswith('?'):
                row_issues.append('🔤 חסר סימן שאלה')

            # 2. הערות נבחנים
            if re.search(ISSUE_PATTERNS['student_notes'], question, re.IGNORECASE):
                row_issues.append('🟠 הערות נבחנים')

            # 3. מסיחים חסרים
            answer_cols = ['א', 'ב', 'ג', 'ד']
            existing_answers = 0
            for col in answer_cols:
                if col in df.columns:
                    val = row.get(col)
                    if pd.notna(val) and str(val).strip():
                        existing_answers += 1

            missing = 4 - existing_answers
            if missing > 0:
                row_issues.append(f'⚠️ חסרים {missing} מסיחים')

            # 4. כפילות במסיחים
            answers = []
            for col in answer_cols:
                if col in df.columns and pd.notna(row.get(col)):
                    answers.append(str(row[col]).strip().lower())

            if len(answers) != len(set(answers)):
                row_issues.append('🔴 כפילות במסיחים')

            # 5. שאלה קצרה מדי
            if len(question) < 15 and question:
                row_issues.append('🟠 שאלה קצרה מדי')

            # 6. נגמר בנקודתיים
            if question.strip().endswith(':'):
                row_issues.append('🔤 נגמר בנקודתיים במקום סימן שאלה')

            if row_issues:
                issues.append({
                    'row': idx + 2,  # +2 כי Excel מתחיל מ-1 + שורת כותרת
                    'question': question[:60] + '...' if len(question) > 60 else question,
                    'issues': row_issues,
                    'category': self._categorize_issues(row_issues)
                })

        return issues

    def _categorize_issues(self, issues: List[str]) -> str:
        """מסווג את חומרת הבעיות"""
        issues_text = ' '.join(issues)
        if '🔴' in issues_text:
            return '🔴 אדום'
        elif '⚠️' in issues_text or '🟠' in issues_text:
            return '🟠 כתום'
        elif '🔤' in issues_text:
            return '🔤 לשוני'
        return '🟢 תקין'

    def fix_punctuation(self, text: str) -> Tuple[str, List[str]]:
        """מתקן בעיות פיסוק"""
        if pd.isna(text) or not text:
            return text, []

        original = str(text)
        text = str(text)
        fixes = []

        # הסרת רווחים כפולים
        new_text = re.sub(r'\s+', ' ', text)
        if new_text != text:
            fixes.append('רווחים כפולים')
            text = new_text

        # הסרת רווח לפני סימן פיסוק
        new_text = re.sub(r'\s+([?!,.:;])', r'\1', text)
        if new_text != text:
            fixes.append('רווח לפני פיסוק')
            text = new_text

        # תיקון :? ל-?
        new_text = re.sub(r':\s*\?', '?', text)
        if new_text != text:
            fixes.append(':? → ?')
            text = new_text

        # הוספת סימן שאלה אם חסר
        question_words = ['מה', 'מי', 'איך', 'למה', 'מדוע', 'האם', 'כמה', 'מתי',
                         'איפה', 'לאן', 'באיזה', 'איזה', 'על מה', 'מהו', 'מהי',
                         'מהם', 'מהן', 'לאיזה', 'לאיזו', 'באיזו']

        text_stripped = text.strip()
        if text_stripped and not text_stripped.endswith('?'):
            # בדיקה אם נגמר בנקודתיים
            if text_stripped.endswith(':'):
                text = text_stripped[:-1] + '?'
                fixes.append(': → ?')
            else:
                # בדיקה אם מתחיל במילת שאלה
                for word in question_words:
                    if text_stripped.startswith(word):
                        text = text_stripped + '?'
                        fixes.append('הוסף ?')
                        break

        return text.strip(), fixes

    def fix_answer_format(self, answer: str, is_drug: bool = False) -> str:
        """מתקן פורמט תשובה"""
        if pd.isna(answer) or not answer:
            return answer

        answer = str(answer).strip()

        # בדיקה אם צריך תרגום
        for eng, heb in MEDICAL_TRANSLATIONS.items():
            # רק אם המונח מופיע בלי תרגום
            pattern = rf'\b{re.escape(eng)}\b(?!\s*\([^)]*\))'
            if re.search(pattern, answer, re.IGNORECASE):
                # לא מתרגמים מונחים מוכרים
                if eng.upper() not in [t.upper() for t in NO_TRANSLATE_TERMS]:
                    answer = re.sub(pattern, f'{eng} ({heb})', answer, flags=re.IGNORECASE)

        return answer

    def calculate_quality_score(self, row: pd.Series) -> Tuple[int, List[str]]:
        """מחשב ציון איכות לשאלה"""
        score = 100
        issues = []

        question = str(row.get('שאלה', '')) if pd.notna(row.get('שאלה')) else ''

        # -20: חסר סימן שאלה
        if question and not question.strip().endswith('?'):
            score -= 20
            issues.append('חסר ?')

        # -15 לכל מסיח חסר
        answer_cols = ['א', 'ב', 'ג', 'ד']
        for col in answer_cols:
            if col not in row.index or pd.isna(row.get(col)) or not str(row.get(col, '')).strip():
                score -= 15
                issues.append(f'חסר {col}')

        # -10: שאלה קצרה מדי
        if len(question) < 20:
            score -= 10
            issues.append('שאלה קצרה')

        # -10: חסר חטיבה
        if 'חטיבה' in row.index and (pd.isna(row.get('חטיבה')) or not row.get('חטיבה')):
            score -= 10
            issues.append('חסר חטיבה')

        # -5: הערות נבחנים
        if re.search(ISSUE_PATTERNS['student_notes'], question, re.IGNORECASE):
            score -= 15
            issues.append('הערות נבחנים')

        # -10: כפילות במסיחים
        answers = []
        for col in answer_cols:
            if col in row.index and pd.notna(row.get(col)):
                answers.append(str(row[col]).lower().strip())
        if len(answers) != len(set(answers)):
            score -= 10
            issues.append('כפילות')

        return max(0, score), issues

    def process_sheet(self, sheet_name: str, fix_punctuation: bool = True,
                     fix_answers: bool = True, interactive: bool = True) -> pd.DataFrame:
        """מעבד גיליון שלם"""
        if sheet_name not in self.df_dict:
            raise ValueError(f"גיליון לא נמצא: {sheet_name}")

        df = self.df_dict[sheet_name].copy()

        print(f"\n{'='*70}")
        print(f"📋 מעבד גיליון: {sheet_name}")
        print(f"{'='*70}")

        # זיהוי בעיות
        issues = self.identify_issues(df)

        if issues:
            print(f"\n⚠️ נמצאו {len(issues)} שאלות עם בעיות:\n")

            # קיבוץ לפי קטגוריה
            by_category = {}
            for issue in issues:
                cat = issue['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(issue)

            for cat, cat_issues in sorted(by_category.items()):
                print(f"  {cat}: {len(cat_issues)} שאלות")

            print("\n" + "-"*70)
            print("פירוט (20 ראשונות):")
            print("-"*70)

            for issue in issues[:20]:
                print(f"  שורה {issue['row']}: {', '.join(issue['issues'])}")
                print(f"    \"{issue['question']}\"")
                print()

        # תיקון פיסוק
        if fix_punctuation and 'שאלה' in df.columns:
            print("\n🔤 מתקן פיסוק...")
            punctuation_fixes = 0

            for idx, row in df.iterrows():
                original = row.get('שאלה', '')
                fixed, fixes = self.fix_punctuation(original)

                if fixes:
                    df.at[idx, 'שאלה'] = fixed
                    punctuation_fixes += 1
                    self.changes_log.append({
                        'sheet': sheet_name,
                        'row': idx + 2,
                        'field': 'שאלה',
                        'type': 'punctuation',
                        'old': original,
                        'new': fixed,
                        'fixes': fixes
                    })

            self.stats['linguistic_fixes'] += punctuation_fixes
            print(f"   ✅ תוקנו {punctuation_fixes} שאלות")

        # תיקון תשובות
        if fix_answers:
            print("\n📝 מתקן פורמט תשובות...")
            answer_cols = ['א', 'ב', 'ג', 'ד']
            answer_fixes = 0

            for idx, row in df.iterrows():
                for col in answer_cols:
                    if col in df.columns:
                        original = row.get(col, '')
                        if pd.notna(original) and original:
                            fixed = self.fix_answer_format(str(original))
                            if fixed != str(original):
                                df.at[idx, col] = fixed
                                answer_fixes += 1

            print(f"   ✅ תוקנו {answer_fixes} תשובות")

        # חישוב ציוני איכות
        print("\n📊 מחשב ציוני איכות...")
        scores = []
        all_issues = []

        for idx, row in df.iterrows():
            score, issues_list = self.calculate_quality_score(row)
            scores.append(score)
            all_issues.append(', '.join(issues_list) if issues_list else '✅')

        df['ציון איכות'] = scores
        df['בעיות'] = all_issues

        avg_score = sum(scores) / len(scores) if scores else 0
        perfect = sum(1 for s in scores if s == 100)
        critical = sum(1 for s in scores if s < 50)

        print(f"   • ממוצע: {avg_score:.1f}/100")
        print(f"   • שאלות מושלמות (100): {perfect}")
        print(f"   • שאלות קריטיות (<50): {critical}")

        self.df_dict[sheet_name] = df
        return df

    def sort_by_hativa(self, df: pd.DataFrame) -> pd.DataFrame:
        """ממיין לפי חטיבה"""
        if 'חטיבה' not in df.columns:
            return df

        # יצירת עמודת סדר
        df['_hativa_order'] = df['חטיבה'].apply(
            lambda x: HATIVA_ORDER.index(x) if x in HATIVA_ORDER else 999
        )

        # ספירת מסיחים
        answer_cols = ['א', 'ב', 'ג', 'ד']
        existing_cols = [c for c in answer_cols if c in df.columns]
        if existing_cols:
            df['_num_answers'] = df[existing_cols].notna().sum(axis=1)
        else:
            df['_num_answers'] = 0

        # מיון
        df = df.sort_values(
            by=['_hativa_order', '_num_answers'],
            ascending=[True, False]
        )

        # מספור מחדש
        if 'מספר' in df.columns:
            df['מספר'] = range(1, len(df) + 1)

        # הסרת עמודות עזר
        df = df.drop(columns=['_hativa_order', '_num_answers'], errors='ignore')

        return df.reset_index(drop=True)

    def format_excel(self, output_path: str):
        """מעצב את קובץ ה-Excel"""
        print(f"\n🎨 מעצב את הקובץ...")

        wb = openpyxl.load_workbook(output_path)

        # סגנונות
        header_font = Font(bold=True, color='FFFFFF')
        header_fill = PatternFill(start_color='000000', end_color='000000', fill_type='solid')
        center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
        right_align = Alignment(horizontal='right', vertical='center', wrap_text=True)
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]

            # עיצוב כותרות
            for cell in ws[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = center_align
                cell.border = thin_border

            # עיצוב שורות נתונים
            for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
                # קבלת החטיבה מהשורה
                hativa = None
                for idx, cell in enumerate(row):
                    col_letter = openpyxl.utils.get_column_letter(cell.column)
                    # מחפש את עמודת החטיבה
                    header_cell = ws[f'{col_letter}1']
                    if header_cell.value == 'חטיבה':
                        hativa = cell.value
                        break

                # צבע רקע לפי חטיבה
                if hativa and hativa in COLORS:
                    fill_color = COLORS[hativa]['row']
                    fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type='solid')
                else:
                    fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')

                for cell in row:
                    cell.fill = fill
                    cell.border = thin_border
                    cell.alignment = right_align

            # כיוון RTL
            ws.sheet_view.rightToLeft = True

            # רוחב עמודות
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if cell.value:
                            max_length = max(max_length, len(str(cell.value)))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column].width = adjusted_width

        wb.save(output_path)
        print(f"   ✅ עיצוב הושלם")

    def save(self, output_path: str = None):
        """שומר את הקובץ המעודכן"""
        if output_path is None:
            base, ext = os.path.splitext(self.file_path)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"{base}_מתוקן_{timestamp}{ext}"

        self.output_path = output_path

        print(f"\n💾 שומר לקובץ: {output_path}")

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in self.df_dict.items():
                # מיון לפני שמירה
                df = self.sort_by_hativa(df)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        # עיצוב
        self.format_excel(output_path)

        print(f"   ✅ הקובץ נשמר בהצלחה!")

        return output_path

    def generate_report(self) -> str:
        """מייצר דוח סיכום"""
        report = []
        report.append("=" * 70)
        report.append("📊 דוח סיכום")
        report.append("=" * 70)
        report.append("")
        report.append("### תיקונים שבוצעו:")
        report.append(f"- ✅ תיקוני פיסוק ולשון: {self.stats['linguistic_fixes']}")
        report.append(f"- ✅ מסיחים שנוספו: {self.stats['distractors_added']}")
        report.append(f"- ✅ העברות חטיבה: {self.stats['hativa_transfers']}")
        report.append("")

        report.append("### מצב הקובץ:")
        for sheet_name, df in self.df_dict.items():
            report.append(f"- {sheet_name}: {len(df)} שאלות")
            if 'ציון איכות' in df.columns:
                avg = df['ציון איכות'].mean()
                report.append(f"  • ציון איכות ממוצע: {avg:.1f}/100")

        report.append("")
        report.append(f"📁 קובץ פלט: {self.output_path}")
        report.append("=" * 70)

        return '\n'.join(report)


def display_questions_for_approval(df: pd.DataFrame, start: int = 0, count: int = 10):
    """מציג שאלות לאישור"""
    print("\n" + "="*70)
    print("📋 שאלות לאישור:")
    print("="*70 + "\n")

    end = min(start + count, len(df))

    for idx in range(start, end):
        row = df.iloc[idx]
        row_num = idx + 2  # +2 for Excel row number

        print(f"┌{'─'*68}┐")
        print(f"│ #{row_num} │ {row.get('חטיבה', 'לא מוגדר'):<20} │ ציון: {row.get('ציון איכות', '?')}")
        print(f"├{'─'*68}┤")
        print(f"│ שאלה: {str(row.get('שאלה', ''))[:60]}")
        print(f"├{'─'*68}┤")
        print(f"│ א. {str(row.get('א', ''))[:50]}")
        print(f"│ ב. {str(row.get('ב', ''))[:50]}")
        print(f"│ ג. {str(row.get('ג', ''))[:50]}")
        print(f"│ ד. {str(row.get('ד', ''))[:50]}")

        if row.get('בעיות') and row.get('בעיות') != '✅':
            print(f"├{'─'*68}┤")
            print(f"│ ⚠️ בעיות: {row.get('בעיות', '')}")

        print(f"└{'─'*68}┘\n")

    print(f"מציג {start+1}-{end} מתוך {len(df)} שאלות")


def interactive_menu():
    """תפריט אינטראקטיבי"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║          🏥 מערכת תיקון שאלות בחינה סיעודית                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  1. טען קובץ Excel                                               ║
║  2. הצג סיכום קובץ                                               ║
║  3. עבד גיליון (תיקון פיסוק + תשובות)                            ║
║  4. הצג שאלות לאישור                                             ║
║  5. שמור קובץ מתוקן                                              ║
║  6. צא                                                           ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")


def main():
    """פונקציה ראשית"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     🏥 מערכת תיקון שאלות בחינה סיעודית - גרסה 1.0           ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # בקשת נתיב קובץ
    while True:
        file_path = input("\n📁 הזן נתיב לקובץ Excel (או 'יציאה' לצאת): ").strip()

        if file_path.lower() in ['יציאה', 'exit', 'quit', 'q']:
            print("👋 להתראות!")
            return

        # הסרת גרשיים אם יש
        file_path = file_path.strip('"\'')

        if not os.path.exists(file_path):
            print(f"❌ קובץ לא נמצא: {file_path}")
            continue

        if not file_path.endswith(('.xlsx', '.xls')):
            print("❌ הקובץ חייב להיות בפורמט Excel (.xlsx או .xls)")
            continue

        break

    # יצירת מעבד
    processor = NursingExamProcessor(file_path)

    # טעינת הקובץ
    results = processor.load_file()

    # תפריט אינטראקטיבי
    while True:
        print("\n" + "─"*50)
        print("📌 מה תרצה לעשות?")
        print("─"*50)
        print("1. עבד את כל הגיליונות (תיקון פיסוק + תשובות)")
        print("2. עבד גיליון ספציפי")
        print("3. הצג שאלות מגיליון")
        print("4. שמור קובץ מתוקן")
        print("5. הצג דוח סיכום")
        print("6. יציאה")
        print("─"*50)

        choice = input("בחר אפשרות (1-6): ").strip()

        if choice == '1':
            # עיבוד כל הגיליונות
            for sheet_name in processor.df_dict.keys():
                processor.process_sheet(sheet_name)
            print("\n✅ כל הגיליונות עובדו!")

        elif choice == '2':
            # עיבוד גיליון ספציפי
            print("\nגיליונות זמינים:")
            for i, name in enumerate(processor.df_dict.keys(), 1):
                print(f"  {i}. {name}")

            sheet_choice = input("בחר מספר גיליון: ").strip()
            try:
                sheet_idx = int(sheet_choice) - 1
                sheet_name = list(processor.df_dict.keys())[sheet_idx]
                processor.process_sheet(sheet_name)
            except (ValueError, IndexError):
                print("❌ בחירה לא תקינה")

        elif choice == '3':
            # הצגת שאלות
            print("\nגיליונות זמינים:")
            for i, name in enumerate(processor.df_dict.keys(), 1):
                print(f"  {i}. {name}")

            sheet_choice = input("בחר מספר גיליון: ").strip()
            try:
                sheet_idx = int(sheet_choice) - 1
                sheet_name = list(processor.df_dict.keys())[sheet_idx]
                df = processor.df_dict[sheet_name]

                start = int(input("מאיזו שורה להתחיל (ברירת מחדל: 0): ").strip() or "0")
                count = int(input("כמה שאלות להציג (ברירת מחדל: 10): ").strip() or "10")

                display_questions_for_approval(df, start, count)
            except (ValueError, IndexError):
                print("❌ בחירה לא תקינה")

        elif choice == '4':
            # שמירה
            output = input("נתיב לקובץ פלט (Enter לברירת מחדל): ").strip()
            output = output.strip('"\'') if output else None
            saved_path = processor.save(output)
            print(f"\n✅ הקובץ נשמר: {saved_path}")

        elif choice == '5':
            # דוח סיכום
            print(processor.generate_report())

        elif choice == '6':
            # יציאה
            save_confirm = input("\n💾 לשמור לפני יציאה? (כן/לא): ").strip()
            if save_confirm.lower() in ['כן', 'yes', 'y', 'כ']:
                processor.save()
            print("\n👋 להתראות!")
            break

        else:
            print("❌ בחירה לא תקינה. נסה שוב.")


if __name__ == "__main__":
    main()
