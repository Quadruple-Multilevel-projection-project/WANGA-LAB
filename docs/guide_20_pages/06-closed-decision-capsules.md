# 6. קפסולות החלטה סגורות כמנוע צמיחה ארגוני

**אשכול 2 · מצב המימוש: PARTIAL — related contracts and a narrow demo exist; package path and common runner are absent**

## מטרה
לתאר יחידת לוגיקה בעלת חוזה קלט/פלט מוגדר, תנאי קבלה וכשל, כדי להשתמש בה בלי להסתמך על prompt עמום בלבד.

## העיקרון המערכתי
קפסולה כוללת מטרה, קלטים, פלטים, invariants, תנאים מקדימים, מצבי שגיאה, provenance ומבחנים. "סגורה" פירושה שגבולותיה מתועדים ונאכפים בתחום מוגדר.

## משמעות עסקית
קפסולות עשויות להפוך ליחידות המאפשרות התאמה ורכישה חוזרת של יכולות. כדי להצדיק מחיר יש להוכיח שימושיות, תאימות ועלות אינטגרציה.

## מצב GitHub שנבדק
קיימים חוזי ארכיטקטורה ודמו Logic Auditor מצומצם. הנתיב 01_logic_packages/task_decomposition/ לא נמצא ב-main.

## מה חסר ומשימות
אין schema קנונית, runner מאומת לכל קפסולה או מדיניות אחידה לגרסאות. יש לממש envelope אחיד, לאכוף schema, להגדיר פעולות אסורות ולבנות שתי קפסולות עם טסטים.

## תנאי קבלה
קלט לא תקין נדחה; פלטים וסטטוסים מוגדרים; המימוש ניתן לשחזור ומגבלותיו מתועדות.

## קישורים
- [Architecture Agent Contract](../../docs/ARCHITECTURE_AGENT_CONTRACT_V1.md)
- [Master Project Instructions](../../docs/MASTER_PROJECT_INSTRUCTIONS_V1.md)
- [First Logic Auditor demo](../../docs/PRODUCTIZATION_AND_FIRST_LOGIC_DEMO_2026-10-09.md)
- [Issue #88: package schema](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/88)

## השתתפות
תרמו קפסולה תחומה עם דוגמאות קלט/פלט, negative cases, מקור ותיעוד.

## מאמרים קשורים
[5](05-introduction-to-logic-economy.md) · [7](07-negative-constraints.md) · [8](08-evidence-validation-and-compliance.md) · [15](15-capsule-tests-and-conformance.md)
