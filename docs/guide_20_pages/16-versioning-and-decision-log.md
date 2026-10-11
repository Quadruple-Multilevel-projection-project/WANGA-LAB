# 16. ניהול גרסאות ויומן החלטות למערכות אינווריאנטיות

**אשכול 4 · מצב המימוש: PARTIAL — repository history and planning docs exist; package-specific records are planned**

## מטרה
לתעד מה השתנה בלוגיקה, מדוע, מי אישר ומה הראיות להשפעה וליכולת rollback.

## העיקרון המערכתי
Git מתעד עריכות; הוא אינו מסביר בהכרח את ההשפעה הסמנטית. שינוי בלוגיקה צריך סיבה, compatibility statement, test diff ותוכנית rollback. Invariant הוא תחום חוזה ולא ערובה נצחית.

## משמעות עסקית
גרסאות אמינות מאפשרות reuse, תחזוקה, ניהול שינוי אצל לקוחות ותמיכה בשוק. שינוי התנהגות שקט פוגע באמון.

## מצב GitHub שנבדק
קיימים Git history, roadmaps ו-Work Memory protocols. לא אותר יומן semantic versioning סטנדרטי לכל package או contribution-reward event.

## מה חסר ומשימות
חסרים version policy, breaking-change labels, deprecation, per-package changelog, test-diff archive ובעל תחזוקה. יש לקבוע scheme לגרסאות, לקשר release ל-test artifacts ולתעד deprecation/rollback.

## תנאי קבלה
כל גרסה מקושרת ל-commit ולתוצאות בדיקה; שינוי שובר מסומן; היסטוריית סטטוסים נשמרת.

## קישורים
- [ROADMAP](../../ROADMAP.md)
- [Architecture Roadmap](../../ARCHITECTURE_ROADMAP.md)
- [Work Memory Protocol](../../docs/WORK_MEMORY_PROTOCOL_V1.md)
- [Productization and first demo](../../docs/PRODUCTIZATION_AND_FIRST_LOGIC_DEMO_2026-10-09.md)
- [Issue #92: tracking registry](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/92)

## השתתפות
תרמו release rules, changelog records, migration tests או rationale להחלטה אמיתית.

## מאמרים קשורים
[13](13-repository-architecture-and-folder-engineering.md) · [14](14-manifest-registry-and-system-configuration.md) · [15](15-capsule-tests-and-conformance.md) · [18](18-ontological-token-economic-model.md) · [19](19-investor-transparency-development-tracking.md)
