# 12. ניהול מערכות מבוזרות ללא תלות במודלים חיצוניים

**אשכול 3 · מצב המימוש: PARTIAL — foundational evidence components exist; provider-independent runtime not demonstrated**

## מטרה
להגדיר עצמאות כיכולת להחליף ספק, runtime או תשתית תוך שמירה על חוזי evidence ו-policy, ולא כהבטחה שאין תלות חיצונית.

## העיקרון המערכתי
Provider independence נובעת מממשקים, adapters, portable formats, גבולות credentials ובדיקות recovery. היא אינה מבטלת תלות ברשת, compute, identity, storage או APIs.

## משמעות עסקית
ניידות עשויה להפחית lock-in וסיכון רציפות. הערך צריך להימדד באמצעות זמן החלפה, התאוששות מהשבתה, ניידות נתונים ועלות מעבר.

## מצב GitHub שנבדק
קיימים רכיבי hash-chain, timestamp ו-anchor ומחקר ארכיטקטורה. הם לא מוכיחים רשת production עמידה לתקלות.

## מה חסר ומשימות
חסרים adapter contract, בדיקות provider-neutral, מפת תלות, degraded mode, retry/idempotency וראיות disaster recovery. יש למפות תלות, להגדיר adapter, לבדוק החלפת ספק ולדמות timeout/credential failure.

## תנאי קבלה
כשל ספק מובחן מכשל לוגיקה; retries מוגבלים ואידמפוטנטיים; דרך ספק חלופי מתועדת ונבדקת.

## קישורים
- [SHA-256 chain](../../src/crypto/sha256_chain.py)
- [RFC3161 timestamp adapter](../../src/crypto/rfc3161_timestamp.py)
- [Bitcoin anchor adapter](../../src/crypto/bitcoin_anchor.py)
- [Global Work Manager V2](../../docs/WANGA_GLOBAL_WORK_MANAGER_V2.md)
- [Issue #89: workbench](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/89)

## השתתפות
תרמו adapters, failure fixtures, recovery runbooks ומדידות portability.

## מאמרים קשורים
[4](04-architecture-as-stability-anchor.md) · [9](09-deterministic-firewall-drift.md) · [11](11-execution-shields.md) · [13](13-repository-architecture-and-folder-engineering.md)
