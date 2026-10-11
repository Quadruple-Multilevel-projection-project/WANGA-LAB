# 3. מעבר מאי־ודאות ניחושית לשליטה דטרמיניסטית

**אשכול 1 · מצב המימוש: PARTIAL — scoped evidence/control components exist; universal control is not implemented**

## מטרה
להסביר את ההבדל בין ניבוי המודל או הספק הבא לבין בניית שכבת בקרה שמגדירה תנאי קלט, גבולות פעולה וראיות נדרשות.

## העיקרון המערכתי
אין צורך לנבא כל שדרוג כדי לקבוע חוזה פעולה, לבדוק מקור או לעצור פעולה שחורגת ממדיניות. דטרמיניזם מתייחס להכרעה חוזרת בתחום נתון; הוא אינו מבטיח שכל בעיית AI ניתנת להכרעה מלאה.

## משמעות עסקית
אפשר להציע בדיקות, הגבלות, אימות והתאמה. הערך תלוי בצמצום תקלות מדידות בלי ליצור חסימות שווא או עלות הפעלה מופרזת.

## מצב GitHub שנבדק
קיימים פרוטוקולי ראיות, בדיקות hash, replay סינתטי ומפרטי חוזי סוכן. לא קיים מסנן אוניברסלי מאומת לכל פלט נוירוני.

## מה חסר ומשימות
נדרשים תחום אחריות לכל מסנן, מצבי ALLOW/DENY/DEFER, טיפול ב-UNKNOWN ומדדי false-positive/negative. יש לכתוב חוזה קלט/פלט, לבנות מקרי תקין וחריג, להיכשל באופן בטוח כשחסרה ראיה ולמדוד מול baseline.

## תנאי קבלה
אותם קלטים וגרסה מפיקים תוצאה עקבית בתחום הבדיקה; כל החלטה מקושרת לכללים ולראיות.

## קישורים
- [Architecture Agent Contract](../../docs/ARCHITECTURE_AGENT_CONTRACT_V1.md)
- [Architecture Pattern Matrix](../../docs/ARCHITECTURE_PATTERN_MATRIX_V1.md)
- [Verification Protocol](../../ai-drift-forensics/VERIFICATION_PROTOCOL.md)
- [Synthetic verified fixture](../../artifacts/drift-known-risk-001/README.md)
- [Issue #89: active workbench](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/89)

## השתתפות
מהנדסים יכולים לתרום rule set, מקרי קצה, בדיקות דטרמיניסטיות או ביקורת חוזה API.

## מאמרים קשורים
[4](04-architecture-as-stability-anchor.md) · [7](07-negative-constraints.md) · [8](08-evidence-validation-and-compliance.md) · [9](09-deterministic-firewall-drift.md) · [11](11-execution-shields.md)
