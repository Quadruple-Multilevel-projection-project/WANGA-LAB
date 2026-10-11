# 10. מנועי קונצנזוס ובדיקות תאימות בין רכיבים

**אשכול 3 · מצב המימוש: PLANNED — adjacent architecture artifacts exist; dedicated engine not found**

## מטרה
להגדיר איך מחברים חבילות בלי להניח שהסכמה בין תוצאות פירושה אמת או שתוצאות שונות הן בהכרח סתירה.

## העיקרון המערכתי
בדיקות תאימות בוחנות interfaces, types, pre/postconditions, dependencies, scope ו-evidence. קונצנזוס משמעותי רק כאשר עצמאות המשתתפים ומצבי הכשל ידועים; כמה מודלים מתואמים אינם ראיות עצמאיות.

## משמעות עסקית
יכולת composition יכולה להוריד עלויות שילוב ולהרחיב bundles, אך יש למדוד חיסכון מול baseline של אינטגרציה.

## מצב GitHub שנבדק
קיימים architecture pattern matrix, registry schemas ו-roadmap; לא אותר מנוע קונצנזוס ייעודי או test suite מתאימה.

## מה חסר ומשימות
חסרים compatibility graph, conflict model, כללי הכרעה דטרמיניסטיים ו-fixtures לתאימות ואי-תאימות. יש להגדיר matrix, לייצג conflicts, להוסיף טיפול ב-UNKNOWN ולבדוק correlated-model risk.

## תנאי קבלה
אי-תאימות מזוהה; אין מיזוג אוטומטי של סתירות; הכרעת compatibility מקושרת לגרסה ולראיות.

## קישורים
- [Architecture Pattern Matrix](../../docs/ARCHITECTURE_PATTERN_MATRIX_V1.md)
- [Architecture Discovery Registry Schema](../../docs/ARCHITECTURE_DISCOVERY_REGISTRY.schema.json)
- [Architecture Roadmap](../../ARCHITECTURE_ROADMAP.md)
- [Issue #88: package schema](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/88)

## השתתפות
מהנדסים יכולים להוסיף interface contracts, compatibility cases ובדיקות ל-conflicting constraints.

## מאמרים קשורים
[6](06-closed-decision-capsules.md) · [7](07-negative-constraints.md) · [9](09-deterministic-firewall-drift.md) · [11](11-execution-shields.md) · [14](14-manifest-registry-and-system-configuration.md)
