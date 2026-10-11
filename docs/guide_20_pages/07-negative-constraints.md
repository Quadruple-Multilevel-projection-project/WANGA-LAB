# 7. מניעת חורים התנהגותיים באמצעות Negative Constraints

**אשכול 2 · מצב המימוש: PARTIAL — general controls exist; dedicated packaged engine is not established**

## מטרה
להגדיר מה מערכת אינה רשאית לעשות: לדלג על ראיות, להציג השערה כעובדה או לפעול כאשר התשובה היא UNKNOWN.

## העיקרון המערכתי
כל constraint צריך לציין תחום, טריגר, החלטת DENY/DEFER/ESCALATE, reason code, דרישת ראיות וסמכות override. רשימת איסורים אינה מבטיחה כיסוי של כל כשל אפשרי.

## משמעות עסקית
ארגונים עשויים לרכוש מדיניות שניתנת לבדיקה ולביקורת כאשר פעולה בלתי מורשית או החלטה ללא ראיות מסוכנת. יש למדוד כיסוי וחסימות שווא.

## מצב GitHub שנבדק
קיימים guardrails, חוזי מערכת ופרוטוקולי אימות. לא אותר מנוע נפרד בנתיב 01_logic_packages/constraint_enforcement/.

## מה חסר ומשימות
חסרים פורמט machine-readable, פתרון התנגשויות בין כללים, policy tests ובקרת שינויים. יש להגדיר schema, בדיקות deny/defer/escalate, precedence, חריגים ו-mutation tests.

## תנאי קבלה
ראיות UNKNOWN מובילות למסלול מוגדר; התנגשות בין כללים מדווחת ואינה נפתרת בשקט.

## קישורים
- [Master Project Instructions](../../docs/MASTER_PROJECT_INSTRUCTIONS_V1.md)
- [Engineering Guardrails](../../ai-drift-forensics/CODEX_ENGINEERING_GUARDRAILS.md)
- [Verification Protocol](../../ai-drift-forensics/VERIFICATION_PROTOCOL.md)
- [Issue #88: package schema](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/88)

## השתתפות
תרמו כלל איסור, counterexample או בדיקת mutation שמוכיחה שהכלל משפיע.

## מאמרים קשורים
[6](06-closed-decision-capsules.md) · [8](08-evidence-validation-and-compliance.md) · [9](09-deterministic-firewall-drift.md) · [11](11-execution-shields.md) · [15](15-capsule-tests-and-conformance.md)
