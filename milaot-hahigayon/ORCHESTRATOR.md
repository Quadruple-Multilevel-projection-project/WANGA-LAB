# מילות ההגיון — Orchestrator

## תפקיד
זהו שער הניתוב הקבוע ל-175 רשומות המונחים של *מילות הגיון*.

## מבנה
- `milaot-hahigayon/terms/001.md` … `175.md` — רשומה אחת לכל מונח.
- `milaot-hahigayon/INDEX.md` — מפתח השערים והמספור.
- קובץ זה — שכבת האורכסטרציה והשליפה.

## כלל שליפה
כאשר נדרש מונח:
1. מזהים את שם המונח.
2. מזהים את מספר הרשומה באמצעות INDEX.
3. שולפים את הרשומה הפרטנית.
4. אם נדרש ציטוט מילולי, בודקים את מקור הטקסט עצמו לפני סימון VERIFIED.
5. אם נדרשת השוואה בין מונחים, שולפים את הרשומות הנוגעות ליחס ולא מאחדים אותן להגדרה אחת.

## סטטוסים
- INDEXED — המונח רשום במאגר.
- SOURCE-CHECKED — המיקום והנוסח נבדקו מול המקור.
- RELATION-CHECKED — היחסים למונחים אחרים נבדקו.
- VERIFIED — קיימת ראיית מקור מספקת.

## כלל אמון
המסמך שסופק בשיחה הוא מפרט הקלט של המאגר. הוא אינו הופך אוטומטית את הציטוטים ל-VERIFIED. אין להשלים או להמציא נוסח מקור.

## שערים
א: 001–004
ב: 005–018
ג: 019–023
ד: 024–036
ה: 037–040
ו: 041–051
ז: 052–063
ח: 064–079
ט: 080–089
י: 090–107
יא: 108–123
יב: 124–132
יג: 133–149
יד: 150–175

## יעד
המאגר נועד להיות ניתן לשליפה בכל שלב של העבודה על מילות ההגיון, בלי לאבד את המספור, השער, המונח או סטטוס האימות.


## Logic Factory map integration
The 175-term retrieval layer is now connected by reference to the central map integration contract and machine-readable registry:
- `docs/LOGIC_FACTORY/MASTER_MAP_INTEGRATION_CONTRACT.md`
- `docs/LOGIC_FACTORY/map_registry.v1.json`

Routing sequence:
1. Resolve the gate and term range from `INDEX.md`.
2. Resolve the term record.
3. Resolve map and app dependencies from the map registry.
4. Require evidence for every relation edge.
5. Route through SERIAL_RETURN, PARALLEL_14_GATE, or COMPARISON without merging their outputs.
6. On any source or relation gap, retain UNRESOLVED / ABSTAIN.

The Logical Map Clock tracks map-change sequence and dependency impact. It does not change source meaning or replace the source index.

## Integration action signature
Timestamp=2026-11-18T00:12:00+02:00
Contract_Start_Time=2026-11-17T20:29:00+02:00
Action_ID=AI231-ORCHESTRATOR-LINK-003
SHA256=fe85f2e5896e590f0ee864680455abb5a1919a715d313b96bee437ef7993bc66
