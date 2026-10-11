# 14. מנהל המניפסטים ותצורת המערכת הדטרמיניסטית

**אשכול 4 · מצב המימוש: PARTIAL — manifests and registries exist; logic-package registry is not established**

## מטרה
להסביר כיצד manifest ו-registry מתעדים רכיבים, גרסאות ותלויות במקום להסתמך על ידע שבעל-פה.

## העיקרון המערכתי
Manifest מצהיר מה נכלל ובאיזה סדר; הוא אינו מוכיח שכל רכיב עובד. השלמת build ואימות דורשים ראיות עצמאיות.

## מצב GitHub שנבדק
קיימים ARCHITECTURE_REGISTRY.json, GLOBAL_ARCHITECTURE_REGISTRY.md ו-docs/ARCHITECTURE_BUILD_MANIFEST.yml. הנתיב 03_intellectual_infrastructure/manifest_registry/ שהוצע לא קיים ב-main.

## מה חסר ומשימות
חסרים CI checks לנתיבים, lifecycle לסכמות, audit של שינויי סטטוס, stale-entry detection ו-registry לתרומות. יש להגדיר owner, לאמת נתיבים, לחבר article/package IDs ולהפיל CI על metadata חסר.

## תנאי קבלה
כל entry פעיל פונה ל-artifact אמיתי או מסומן planned; schema לא תקין נכשל ב-CI.

## קישורים
- [Architecture Registry JSON](../../ARCHITECTURE_REGISTRY.json)
- [Global Architecture Registry](../../GLOBAL_ARCHITECTURE_REGISTRY.md)
- [Architecture Build Manifest](../../docs/ARCHITECTURE_BUILD_MANIFEST.yml)
- [Architecture Discovery Registry Schema](../../docs/ARCHITECTURE_DISCOVERY_REGISTRY.schema.json)
- [Issue #92: status tracking](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/92)

## השתתפות
תרמו schema validation, link checker, registry entries ובדיקות ל-manifest לא תקין.

## מאמרים קשורים
[4](04-architecture-as-stability-anchor.md) · [13](13-repository-architecture-and-folder-engineering.md) · [15](15-capsule-tests-and-conformance.md) · [16](16-versioning-and-decision-log.md)
