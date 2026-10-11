# 15. כתיבת בדיקות תקינות ומבחני קפסולה

**אשכול 4 · מצב המימוש: PARTIAL — test infrastructure exists; canonical logic-capsule conformance remains planned**

## מטרה
להראות איך חבילת לוגיקה מקבלת expected outputs, negative cases, reproducibility ו-test evidence.

## העיקרון המערכתי
בדיקות צריכות לאתגר גבולות ולא רק happy path. בדיקה דטרמיניסטית מוכיחה התנהגות עבור fixture וגרסה מסוימים, לא נכונות אוניברסלית לכל הקשר.

## משמעות עסקית
בדיקות תאימות יוצרות אמון ומפחיתות עלויות שילוב. ההצעה חייבת לפרט coverage, סיכון לפספוסים, scope וגרסה.

## מצב GitHub שנבדק
קיימים tests ל-integrity, replay ו-architecture. Harness לתאימות packages ב-01_logic_packages/ לא נמצא.

## מה חסר ומשימות
חסרים test-vector format, package runner, adversarial dataset, coverage metrics ו-release report שניתן לשחזור. יש ליצור חבילת דוגמה, לכתוב valid/invalid inputs, להוסיף מקרי גבול וסתירה, להריץ בסביבה נקייה ולפרסם תוצאות.

## תנאי קבלה
CI רץ בכל שינוי package; תוצאה מקושרת ל-commit ולגרסה; בדיקה כושלת מונעת קידום סטטוס.

## קישורים
- [Hash-chain tests](../../tests/test_hash_chain.py)
- [Known-risk replay tests](../../tests/test_known_risk_replay.py)
- [Architecture discovery tests](../../tests/test_architecture_discovery.py)
- [Python project config](../../pyproject.toml)
- [Issue #88: schema and conformance](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/88)

## השתתפות
הוסיפו edge case, expected output, regression test או שחזור עצמאי.

## מאמרים קשורים
[6](06-closed-decision-capsules.md) · [7](07-negative-constraints.md) · [8](08-evidence-validation-and-compliance.md) · [10](10-consensus-and-compatibility-engines.md) · [14](14-manifest-registry-and-system-configuration.md)
