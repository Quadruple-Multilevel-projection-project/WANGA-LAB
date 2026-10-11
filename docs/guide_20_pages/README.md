# מדריך 20 המאמרים — תזה, פיתוח והשתתפות באקוסיסטם

**מאגר:** WANGA-LAB  
**נתיב:** docs/guide_20_pages/  
**מטרת המדריך:** לחבר כל חלק בתזה למסמכים, ראיות, משימות GitHub, פערי מימוש ותנאי קבלה — כך שמשקיעים יוכלו לעקוב ומהנדסים יוכלו להשתתף.

## מקרא סטטוסים
- **BUILT** — רכיב קיים בנתיב שצוין.
- **SPECIFIED** — חוזה או מפרט קיים, אך לא בהכרח מימוש עובד.
- **PROTOTYPED** — הדגמה מוגבלת קיימת.
- **TESTED** — בדיקות מוגדרות הורצו; חובה לציין מה נבדק.
- **VERIFIED** — ראיות עברו שערים מוגדרים בתחום מפורש.
- **PLANNED** — העבודה טרם בוצעה.
- **HYPOTHETICAL** — תרחיש או טענה עתידית שטרם אומתו.
- **PARTIAL** — קיימים רכיבים סמוכים, לא המנגנון המלא.
- **NOT FOUND IN AUDITED PATH** — הנתיב המדויק לא נמצא ב-main בביקורת מ-2026-10-11; אין בכך הוכחה שאין רכיבים דומים בנתיב אחר.

## אשכול 1 — שינוי השוק
- [1. הקץ לכלכלת הביצוע ועליית הערך של הארכיטקטורה](01-end-of-execution-economy.md)
- [2. עיוורון המיינסטרים והסירוב לבצע אלימינציה](02-mainstream-blind-spots-and-elimination.md)
- [3. מעבר מאי־ודאות ניחושית לשליטה דטרמיניסטית](03-from-guessing-to-deterministic-control.md)
- [4. הארכיטקטורה כעוגן קיומי בעידן של שינוי מואץ](04-architecture-as-stability-anchor.md)

## אשכול 2 — כלכלת הלוגיקה
- [5. מבוא לכלכלת לוגיקה וכריית מנגנונים](05-introduction-to-logic-economy.md)
- [6. קפסולות החלטה סגורות כמנוע צמיחה ארגוני](06-closed-decision-capsules.md)
- [7. מניעת חורים התנהגותיים באמצעות Negative Constraints](07-negative-constraints.md)
- [8. אימות ראיות ובדיקת תאימות בחבילות לוגיקה](08-evidence-validation-and-compliance.md)

## אשכול 3 — ארכיטקטורה ובקרה
- [9. חומת האש הדטרמיניסטית מול דריפט ורעש נוירוני](09-deterministic-firewall-drift.md)
- [10. מנועי קונצנזוס ובדיקות תאימות בין רכיבים](10-consensus-and-compatibility-engines.md)
- [11. מגן ההוצאה לפועל (Execution Shields) והבטחת דטרמיניזם](11-execution-shields.md)
- [12. ניהול מערכות מבוזרות ללא תלות במודלים חיצוניים](12-distributed-systems-without-provider-dependence.md)

## אשכול 4 — מעבדת הפיתוח
- [13. מבנה ה-Repository והנדסת התיקיות ב-GitHub](13-repository-architecture-and-folder-engineering.md)
- [14. מנהל המניפסטים ותצורת המערכת הדטרמיניסטית](14-manifest-registry-and-system-configuration.md)
- [15. כתיבת בדיקות תקינות ומבחני קפסולה](15-capsule-tests-and-conformance.md)
- [16. ניהול גרסאות ויומן החלטות למערכות אינווריאנטיות](16-versioning-and-decision-log.md)

## אשכול 5 — המקצוע והשוק העתידי
- [17. פרופיל מהנדס הלוגיקה החדש מול המפתח הישן](17-the-logic-engineer.md)
- [18. המודל הכלכלי של המטבע האונטולוגי והפרדת התגמולים](18-ontological-token-economic-model.md)
- [19. שקיפות למשקיעים: ממעקב פיתוח ועד לערך מבני](19-investor-transparency-development-tracking.md)
- [20. מפת הדרכים למעבר של האקוסיסטם](20-ecosystem-transition-roadmap.md)

## ממשק תפעולי והשתתפות
- [Active Operational Interface & Ontological Reward Model](ACTIVE_OPERATIONAL_INTERFACE_AND_ONTOLOGICAL_REWARD_MODEL.md)
- [Engineering Contribution, Review & Verification Protocol](ENGINEERING_CONTRIBUTION_AND_REVIEW_PROTOCOL.md)
- [Implementation Gap Register](IMPLEMENTATION_GAP_REGISTER.md)
- [Development Status Registry — JSON](DEVELOPMENT_STATUS_REGISTRY.json)

## Issues פעילים
- [#88 — Canonical Logic Package schema](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/88)
- [#89 — Logic & Filter Workbench](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/89)
- [#90 — Proof-of-Logic and reward ledger](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/90)
- [#91 — Logic Marketplace and Execution Shields](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/91)
- [#92 — Development and contribution tracking](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/92)

## ביקורת נתיבים
הנתיבים 01_logic_packages/, 02_deterministic_filters/ ו-03_intellectual_infrastructure/ לא נמצאו בשורש main בבדיקה מ-2026-10-11. קיימים במאגר רכיבים סמוכים במחקר Logic Mine, אדריכלות, ראיות, בדיקות ו-drift forensics. נדרשת החלטה אם ליצור את מבנה התיקיות החדש או להמשיך עם הנתיבים הקיימים. אין ליצור כפילויות רק כדי להתאים לשמות שבתוכנית.

## כלל שקיפות
כל שינוי סטטוס חייב לקשר לקובץ, PR, test report או evidence record ולהציג מגבלות. GitHub מתעד התקדמות; הוא אינו מבטיח ביקוש, מחיר מטבע או תשואה.
