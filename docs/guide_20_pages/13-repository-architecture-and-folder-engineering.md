# 13. מבנה ה-Repository והנדסת התיקיות ב-GitHub

**אשכול 4 · מצב המימוש: BUILT for repository registries; proposed package folder layout requires a decision**

## מטרה
להדריך מהנדס חיצוני במבנה WANGA-LAB בפועל בלי לבלבל בין תיקיות מוצעות לבין נתיבים שקיימים.

## העיקרון המערכתי
שם תיקייה הוא בחירת ניווט, לא ראיה ליכולת. מקור האמת הוא תוכן קבצים, היסטוריה, בדיקות, workflows ותוצאות אימות. שינוי ארכיטקטוני מוצע באמצעות branch ו-PR.

## מצב GitHub שנבדק
קיימים README, registries, roadmaps, research, tests, schemas, scripts ו-artifacts. המאגר שנבדק הוא WANGA-LAB. שלושת הנתיבים שהוצעו בשורש — 01_logic_packages/, 02_deterministic_filters/, 03_intellectual_infrastructure/ — לא נמצאו ב-main בבדיקה מ-2026-10-11.

## מה חסר
צריך להחליט אם ליצור את שלושת שורשי התיקיות החדשים או לרשום יכולות קיימות ב-registry בלי להכפיל ארכיטקטורה. חסר גם onboarding ממוקד למפתחי חבילות.

## משימות ותנאי קבלה
לקשר מסמכים קנוניים, לבחור namespace לחבילות, להוסיף contributor guide ולוודא שכל הקישורים מצביעים לנתיבים קיימים. אחרי merge, כל קישור צריך להיפתח, ונתיב לא מסומן כקיים ללא audit.

## קישורים
- [Repository README](../../README.md)
- [Machine-readable architecture registry](../../ARCHITECTURE_REGISTRY.json)
- [Global Architecture Registry](../../GLOBAL_ARCHITECTURE_REGISTRY.md)
- [Wix ↔ WANGA architecture registry](../../docs/WIX_ARCHITECTURE_REGISTRY.md)
- [Issue #92: development tracking](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/92)

## השתתפות
קראו את המסמכים הקנוניים ופתחו issue ממוקד לפני הוספת תיקייה חדשה או registry כפול.

## מאמרים קשורים
[14](14-manifest-registry-and-system-configuration.md) · [15](15-capsule-tests-and-conformance.md) · [16](16-versioning-and-decision-log.md) · [19](19-investor-transparency-development-tracking.md)
