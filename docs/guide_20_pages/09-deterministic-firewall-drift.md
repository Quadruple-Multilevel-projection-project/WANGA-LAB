# 9. חומת האש הדטרמיניסטית מול דריפט ורעש נוירוני

**אשכול 3 · מצב המימוש: PARTIAL — forensic research and synthetic fixture exist; production real-time firewall is not established**

## מטרה
להבחין בין זיהוי סחיפה במנגנון נצפה לבין הבטחה לזהות כל הזיה או לעצור כל פעולה בזמן אמת.

## העיקרון המערכתי
מגדירים baseline, criterion נצפה, חלון מדידה וסף; משווים, משמרים evidence, מסווגים שינוי ומחליטים אם לאפשר, לחסום או להסלים. Output anomaly ו-criterion drift הם סוגים שונים.

## משמעות עסקית
שירות בקרה עשוי לסמן שינוי ולאסוף evidence לניתוח. טענת real-time protection דורשת latency benchmarks, coverage tests, failure analysis ואבטחת אינטגרציה.

## מצב GitHub שנבדק
קיימים פרוטוקול drift ו-fixture סינתטי ל-criterion drift. הנתיב 02_deterministic_filters/drift_detection/ לא נמצא; מסנן live אוניברסלי לא הוכח.

## מה חסר ומשימות
חסרים streaming adapter בייצור, מדדי latency, benchmark לחסימות שווא, integration security ו-incident playbook. יש להרחיב fixtures לסוגי drift, למדוד latency ולבדוק fail-safe behavior.

## תנאי קבלה
המקרה ניתן לשחזור; סוג drift מפורש; אי-ודאות נשמרת; אין טענת real-time בלי benchmark.

## קישורים
- [Verification Protocol](../../ai-drift-forensics/VERIFICATION_PROTOCOL.md)
- [Drift case](../../ai-drift-forensics/cases/CASE-2026-MODEL-DRIFT-001.md)
- [Synthetic verified fixture](../../artifacts/drift-known-risk-001/README.md)
- [Issue #89: workbench](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/89)

## השתתפות
תרמו fixture, מדד drift, adapter או benchmark שניתן להריץ מחדש.

## מאמרים קשורים
[3](03-from-guessing-to-deterministic-control.md) · [8](08-evidence-validation-and-compliance.md) · [10](10-consensus-and-compatibility-engines.md) · [11](11-execution-shields.md) · [12](12-distributed-systems-without-provider-dependence.md)
