#!/bin/bash
# 🏥 סקריפט התקנה למערכת תיקון שאלות בחינה סיעודית
# להפעלה: bash install_mac.sh

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🏥 התקנת מערכת תיקון שאלות בחינה סיעודית                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# בדיקת Python
echo "🔍 בודק Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python3 לא מותקן!"
    echo "   📥 אנא התקיני מ: https://www.python.org/downloads/"
    exit 1
fi

# בדיקת pip
echo "🔍 בודק pip..."
if command -v pip3 &> /dev/null; then
    echo "   ✅ pip3 מותקן"
else
    echo "   ⚠️ מתקין pip..."
    python3 -m ensurepip --upgrade
fi

# התקנת ספריות
echo ""
echo "📦 מתקין ספריות נדרשות..."
pip3 install pandas openpyxl xlsxwriter

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ ההתקנה הושלמה!                         ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  להפעלה:                                                     ║"
echo "║  python3 run_fixer.py                                        ║"
echo "║                                                              ║"
echo "║  או:                                                         ║"
echo "║  python3 nursing_exam_processor.py                           ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
