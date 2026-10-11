# 11. מגן ההוצאה לפועל (Execution Shields) והבטחת דטרמיניזם

**אשכול 3 · מצב המימוש: PLANNED / NOT VERIFIED as a deployed component**

## מטרה
להציג שכבת policy enforcement לפני פעולה בעולם החיצוני: המודל מציע פעולה, שכבה נפרדת בודקת הרשאה, ראיות, טווח וסיכון.

## העיקרון המערכתי
Shield מקבל פעולה מוצעת והקשר ומחזיר ALLOW, DENY או DEFER עם reason code, policy version וקישורי evidence. הוא אינו מחליף מדיניות בשקט ולא קובע אמת ללא בסיס ראייתי.

## משמעות עסקית
רכיב כזה עשוי להימכר כשירות אינטגרציה או הגנה בזמן ריצה. האיכות תלויה בגבולות אבטחה, latency, fail-safe behavior, rollback ואחריות תפעולית.

## מצב GitHub שנבדק
קיימות בקרות orchestration ו-evidence כלליות, אך הנתיב 02_deterministic_filters/execution_shields/ לא נמצא ב-main. לא אומת רכיב Execution Shield פעיל לייצור.

## מה חסר ומשימות
חסרים API contract, threat model, policy registry, sandbox, permission model, audit log, harness ובדיקות ביצועים. יש להגדיר envelope, לסווג פעולות מוגנות, לממש סימולציה ולבדוק prompt injection, retries והרשאות.

## תנאי קבלה
אין side effect חיצוני לפני verdict; מדיניות או ראיה חסרה מטופלת ב-fail-closed/defer מתועד; ההחלטות ניתנות לביקורת.

## קישורים
- [Global Work Manager V2](../../docs/WANGA_GLOBAL_WORK_MANAGER_V2.md)
- [Master Project Instructions](../../docs/MASTER_PROJECT_INSTRUCTIONS_V1.md)
- [Verification Protocol](../../ai-drift-forensics/VERIFICATION_PROTOCOL.md)
- [Issue #89: workbench](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/89)
- [Issue #91: marketplace and shields](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/91)

## השתתפות
תרמו threat scenarios, adapters, policy tests, audit schemas ודוגמאות sandbox.

## מאמרים קשורים
[3](03-from-guessing-to-deterministic-control.md) · [7](07-negative-constraints.md) · [8](08-evidence-validation-and-compliance.md) · [9](09-deterministic-firewall-drift.md) · [10](10-consensus-and-compatibility-engines.md) · [12](12-distributed-systems-without-provider-dependence.md)
