# מפת תיקון ועקיבות: FOL, סדר שני, לוגיקה פרקטלית ו-WANGA

**תאריך:** 2026-10-18  
**סטטוס:** DOCUMENTATION / TRACEABILITY MAP — אינו אישור שכל הארכיטקטורה מומשה או אומתה.

## כלל בסיס

הסיכום הוא מסגרת מחקרית משולבת. יש להפריד בין: (1) הגדרה פורמלית; (2) קוד קיים; (3) מפרט/חוזה; (4) מיפוי מחקרי; (5) השערה או עמדה אונטולוגית; (6) תוצאת בדיקה.  
**SPECIFIED ≠ TESTED ≠ VERIFIED.** קישור בין מסמכים או פרסום ב-Wix אינם הוכחה לתקפות סמנטית או לשילוב runtime.

## 1. הרעיון המרכזי — הצעה אינה אישור

מודל יכול להציע טענה או פעולה. המערכת אמורה לייצג את ההצעה, לבדוק מבנה, גזירה וכללים, לבחון מקורות/ראיות לפי הצורך, ואז לאשר, לדחות או לעצור. אין להסיק מכך שהמערכת מונעת את כל ההזיות או מבטיחה בטיחות כללית.

**GitHub:** [README](../README.md) · [Five-Gate Handoff](../AI-AGENT-NOTICE.md) · [LNL Model Builder](../logic_model_builder_v1/README.md)  
**Wix:** [Logic Wiki](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki.html) · [Evidence Status](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-evidence-status.html)

## 2. חלק א׳ — לוגיקה מסדר ראשון (FOL)

ההגדרה הכללית בסיכום נכונה ברמת המבוא: עצמים בתחום דיון, שמות/קבועים, משתנים, נשואים, יחסים, פונקציות, כמתים וקשרים לוגיים — בהתאם לשפה ולסמנטיקה שהוגדרו.

**תיקונים:** `Agent(A)`, `Agent(B)`, `DependsOn(A,B)` הן דוגמאות סכמטיות. קיום תלות אינו מוכיח זמינות של B ואינו מתיר פעולה של A; דרושים נשוא מתאים, כלל, תחום/טיפוסים ותנאי קדם. קוד קיים אינו מוכיח מימוש מלא של FOL: `logic_engine_v1` הוא kernel סמלי מוגבל, ויש לבדוק את הממשק והתכונות בפועל.

**GitHub:** [Logic Wiki catalog](../logic_wiki/data/articles.json) · [Logic kernel](../logic_engine_v1/logic_kernel.py) · [LNL Builder](../logic_model_builder_v1/README.md)  
**Wix:** [Logic Wiki catalog](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki.html)

**סטטוס:** ההגדרה הכללית מבוססת; מידת הכיסוי של FOL במנוע דורשת בדיקות של תחביר, סמנטיקה, טיפוסים וכללי היסק.

## 3. חלק ב׳ — סדר שני לעומת מטא־בדיקה

סדר שני מאפשר, לפי הפורמליזם והסמנטיקה, לכמת על תכונות, נשואים, יחסים או קבוצות. בדיקת כללים/קוד אינה הופכת אוטומטית ללוגיקה מסדר שני.

**תיקונים:** `∀P ...` הוא סכמטי בלבד עד שמוגדרים שפה, טיפוס P, תחום כימות וסמנטיקה. יש להפריד בין (א) Second-Order Logic פורמלית, (ב) meta-logic/rule validation, (ג) שכבת ארכיטקטורה שמפקחת על כללים. מסמך המחקר מתאר first-order ו-second-order גם כקטגוריות ארכיטקטוניות מוצעות, לא כטענה שהן מממשות בהכרח את ההגדרות הקלאסיות. במקורות שנבדקו לא אותר מפרט מלא של שפת סדר שני או מנוע כימות מסדר שני.

**GitHub:** [articles.json](../logic_wiki/data/articles.json) · [Forensic Logic & Drift Lab forecast](../research/FORENSIC_LOGIC_DRIFT_LAB_FORECAST.md) · [Logic Fractal Program](../research/LOGIC_FRACTAL_PROGRAM_V1.md)  
**Wix:** [Logic Wiki](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki.html) · [Fractal Research](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-fractal-research.html)

## 4. חלק ג׳ — חמשת השערים

הסדר המתועד ב-[AI-AGENT-NOTICE](../AI-AGENT-NOTICE.md) הוא:
1. L1 — First-Order Structural Logic
2. L2 — Derivation Logic
3. L3 — Relation / Rule Validation
4. Evidence / Provenance Filter
5. Deterministic Output Filter

**תיקון מרכזי:** אלה שערי בקרה במסמך handoff, לא חמש לוגיקות פורמליות נפרדות. עצם קיום ההוראה אינו מוכיח שכל שער נאכף אוטומטית בכל מסלול runtime. יש להוכיח זאת באמצעות trace, בדיקות ותוצאות replay.

- **L1:** מבנה מקור, טיפוסים ויחסים — [AI-AGENT-NOTICE](../AI-AGENT-NOTICE.md), [kernel](../logic_engine_v1/logic_kernel.py).
- **L2:** הנחות + כלל מוגדר + יישום תקף — [kernel](../logic_engine_v1/logic_kernel.py), [LNL Builder](../logic_model_builder_v1/README.md).
- **L3:** תנאי היחס/כלל; אין להניח טרנזיטיביות, סימטריה, זהות או סיבתיות בלי הגדרה — [AI-AGENT-NOTICE](../AI-AGENT-NOTICE.md).
- **Evidence:** SOURCE → EXTRACTED → FORMALIZED → DERIVED → MAPPED → TESTED → VERIFIED — [README](../README.md).
- **Output:** בדיקה דטרמיניסטית של פלט אינה מוכיחה אמת סמנטית או בטיחות חיצונית.

**Wix:** [Evidence Status](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-evidence-status.html) · [Logic Wiki](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki.html)

## 5. NEURAL_PROPOSAL ≠ FORMAL_COMMIT

זהו כלל בקרה ארכיטקטוני, לא משפט מתמטי. כדי לממשו דרושים מצבים מפורשים, תנאי מעבר, סיבות דחייה, מקור/ראיה ורישום. אין להציגו כמנגנון אוטומטי מאומת בלי מסלול ביצוע ובדיקת replay.

**GitHub:** [LNL Model Builder](../logic_model_builder_v1/README.md) · [Logic kernel](../logic_engine_v1/logic_kernel.py) · [AI-AGENT-NOTICE](../AI-AGENT-NOTICE.md)  
**Wix:** [Evidence Status](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-evidence-status.html) · [Fractal Logic](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-fractal-logic.html)

## 6. חלק ד׳ — לוגיקה פרקטלית

בפרויקט, “לוגיקה פרקטלית” היא תוכנית מחקרית של הרכבה רקורסיבית של מבנים תוך שמירת טיפוסים, אילוצים, מקורות והיסטוריית הורים. דמיון עצמי לבדו אינו תקפות לוגית.

הסקאלות המתועדות: L0 יחידת מקור; L1 fragment מטופס; L2 הרכבה לפי חוזה; L3 מועמד מודל שנבדק מול דוגמאות נגדיות, holdout ו-MIRROR review.

**תיקונים:** הרכבה רקורסיבית אינה מבטיחה שימור של כל תכונה; צריך לציין אינווריאנטים, תנאי עצירה וחסמי חישוב. קשרי Logic Wiki הם `EDITORIAL_RELATION_CANDIDATE`, לא entailment. ה-composer הקיים מאמת שדות, הפניות וטיפוסים ושומר lineage/hash, אך אינו מוכיח אמת סמנטית. חוזי ההרכבה עדיין דורשים benchmark סמנטי.

**GitHub:** [Architecture V2](./LOGIC_WIKI_FRACTAL_ARCHITECTURE_V2.md) · [Logic Fractal Program](../research/LOGIC_FRACTAL_PROGRAM_V1.md) · [Recursive contracts](../logic_fractal/data/recursive_composition_contracts_v1.json) · [Composition rules](../logic_fractal/data/composition_rules.json) · [Fragment composer](../logic_fractal/fragment_composer.py) · [Taxonomy](../logic_wiki/data/fractal_taxonomy.json) · [Readiness gate](../logic_wiki/data/readiness_gate.json) · [Benchmark plan](../logic_fractal/data/semantic_benchmark_plan_v1.json)  
**Wix:** [Fractal Research](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-fractal-research.html) · [Fractal Logic](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-fractal-logic.html) · [Typed Fragment](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-typed-fragment.html)

**מצבים שנמצאו בקבצים:** readiness gate = `CONFIGURED_NOT_EMPIRICALLY_VALIDATED`; benchmark plan = `SPECIFIED_NOT_POPULATED`; recursive contracts = `CANDIDATE_CONTRACTS_NEED_SEMANTIC_BENCHMARK`.

## 7. חלק ה׳ — פורנזיקה ושימור היסטוריה

המחזור Baseline → Observation → Detection → Evidence → Reconstruction → Causal Analysis → Attribution → Risk → Intervention → Verification הוא תהליך מוצע. זיהוי סטייה או שחזור רצף אינם מוכיחים סיבתיות. יש להפריד בין זיהוי, שחזור, מתאם, השערת סיבה וייחוס סיבתי הנתמך בראיות.

**GitHub:** [README](../README.md) · [Daily Integration Map](./DAILY_INTEGRATION_MAP_2026-10-13.md) · [Logic kernel](../logic_engine_v1/logic_kernel.py) · [Benchmark plan](../logic_fractal/data/semantic_benchmark_plan_v1.json) · [Wix sync manifest](../logic_wiki/data/wix_sync_manifest.json)  
**Wix:** [Evidence Status](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-evidence-status.html) · [Research Status](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-research-status.html)

## 8. חלק ו׳ — גבולות הייצוג, אין־סוף ואור אין־סוף

הטענה שאין לייצג אין־סוף/אור אין־סוף כעצם רגיל נשמרת כעמדה אונטולוגית/פרשנית של המסגרת. אין להציג אותה כמסקנה של FOL או כמשפט שהוכח במנוע WANGA. אפשר להבחין בין טענה במטא־שפה על גבולות הייצוג לבין אובייקט בתוך תחום הדיון, אך ההבחנה אינה פותרת לבדה את השאלה הפילוסופית.

**GitHub:** [Logic Mine research tracks](../research/LOGIC_MINE_RESEARCH_TRACKS.md) · [Daily Integration Map](./DAILY_INTEGRATION_MAP_2026-10-13.md) · [Logic Wiki catalog](../logic_wiki/data/articles.json)  
**Wix:** [Research Archive](https://beywolf5.wixsite.com/institute-for-global/research-archive) · [Technology Code](https://beywolf5.wixsite.com/global-algorithmic-g/technology-code)

**פער מקור:** בחיפוש המצומצם לא אותר דף Wix ייעודי או מסמך GitHub שמבסס את הטענה הספציפית על אין־סוף/אור אין־סוף. הקישורים לעיל הם שערי ארכיון, לא אסמכתה ישירה. נדרש קטע מקור מדויק כדי להציג את הטענה כמקור-מקושרת.

## 9. חלק ז׳ — המודל המאוחד

יש להציג את שבע הרמות כתפקידי ארכיטקטורה, לא כשבע מערכות פורמליות מוכחות:
1. ייצוג מבני;
2. גזירה;
3. בדיקת יחסים וכללים;
4. ארגון רב־רמתי/פרקטלי;
5. ראיות ו-provenance;
6. מכונת מצבים ובקרת פעולה;
7. למידה מהיסטוריית כשלים.

**תיקון:** רמה 2 אינה לוגיקה מסדר שני בהכרח; רמה 4 אינה פורמליזם של “לוגיקה פרקטלית” רק מכוח שמה. יש להגדיר ממשקים, כללים ומבחנים.

**GitHub:** [Architecture V2](./LOGIC_WIKI_FRACTAL_ARCHITECTURE_V2.md) · [Daily Integration Map](./DAILY_INTEGRATION_MAP_2026-10-13.md) · [LNL Builder](../logic_model_builder_v1/README.md) · [Algorithmic-seed traceability map](./LOGIC_ARCHITECTURE_CORRECTION_AND_TRACEABILITY_V1.md)  
**Wix:** [Fractal Research](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-fractal-research.html) · [Logic Wiki](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki.html)

## 10. מונחים ופערים שעדיין פתוחים

- **NIR/TNRL:** חיפוש ממוקד במאגר לא החזיר מקור. אין להרחיב את ראשי התיבות או לייחס להם מנגנון עד לאיתור מקור.
- **חמשת השערים ב-runtime:** קיימת הוראת handoff; נדרש trace/test שמראה אכיפה בפועל.
- **מימוש סדר שני:** לא אותר מפרט תחביר/סמנטיקה ומנוע כימות מסדר שני.
- **אימות fractal סמנטי:** benchmark לא מאוכלס וה-readiness gate לא אומת אמפירית.
- **אין־סוף/אור אין־סוף:** לא נמצא קישור ישיר למקור הספציפי.
- **Wix:** manifest מציין `PUBLISHED_READ_BACK_PARTIAL`; פרסום/ניווט אינם מוכיחים שכל התוכן נקרא חזרה או תואם סמנטית למקור.

## 11. מפת קישורים קצרה לפי חלק

| חלק | GitHub עיקרי | Wix עיקרי | גבול הראיה |
|---|---|---|---|
| רעיון מרכזי / הצעה-אישור | [README](../README.md), [Agent Notice](../AI-AGENT-NOTICE.md) | [Logic Wiki](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki.html), [Evidence Status](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-evidence-status.html) | מדיניות, לא הבטחה למניעת כל טעות |
| א׳ FOL | [articles.json](../logic_wiki/data/articles.json), [kernel](../logic_engine_v1/logic_kernel.py) | [Logic Wiki](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki.html) | קטלוג וקוד סמלי מוגבל |
| ב׳ סדר שני | [articles.json](../logic_wiki/data/articles.json), [forecast](../research/FORENSIC_LOGIC_DRIFT_LAB_FORECAST.md) | [Logic Wiki](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki.html), [Fractal Research](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-fractal-research.html) | לא הוכח מנוע כימות מסדר שני |
| ג׳ חמשת השערים | [Agent Notice](../AI-AGENT-NOTICE.md), [LNL Builder](../logic_model_builder_v1/README.md) | [Evidence Status](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-evidence-status.html) | אכיפת runtime דורשת בדיקה |
| ד׳ fractal | [Architecture V2](./LOGIC_WIKI_FRACTAL_ARCHITECTURE_V2.md), [contracts](../logic_fractal/data/recursive_composition_contracts_v1.json), [composer](../logic_fractal/fragment_composer.py) | [Fractal Research](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-fractal-research.html), [Fractal Logic](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-fractal-logic.html), [Typed Fragment](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-typed-fragment.html) | מועמדים/חוזים, לא אמת סמנטית מוכחת |
| ה׳ פורנזיקה | [README](../README.md), [Integration Map](./DAILY_INTEGRATION_MAP_2026-10-13.md) | [Evidence Status](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-evidence-status.html), [Research Status](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-research-status.html) | סיבתיות דורשת ראיות |
| ו׳ אין־סוף | [Logic Mine tracks](../research/LOGIC_MINE_RESEARCH_TRACKS.md) | [Research Archive](https://beywolf5.wixsite.com/institute-for-global/research-archive), [Technology Code](https://beywolf5.wixsite.com/global-algorithmic-g/technology-code) | ארכיון בלבד, מקור ישיר לא אותר |
| ז׳ מודל מאוחד | [Architecture V2](./LOGIC_WIKI_FRACTAL_ARCHITECTURE_V2.md), [Integration Map](./DAILY_INTEGRATION_MAP_2026-10-13.md), [LNL Builder](../logic_model_builder_v1/README.md) | [Fractal Research](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-fractal-research.html), [Logic Wiki](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki.html) | מפת תפקידים, לא שכבות פורמליות מאומתות |

## 12. מפת קשרים בין המסמכים

```text
SOURCE CORPUS
   ↓
Logic Wiki catalog + provenance
   ↓
FOL primitives / typed claims
   ↓
Logic kernel / LNL compiler
   ↓
Derivation + relation/rule checks
   ↓
Evidence / provenance + output filter
   ↓
Typed fragments (L1)
   ↓
Recursive composition contracts (L2)
   ↓
Candidate model (L3) → benchmark / counterexamples / MIRROR
   ↓
Readiness gate (not empirically validated)
   ↓
Wix publication + read-back
   ↓
Drift forensics / replay / receipts
```

זוהי מפת קשרים תיעודית/מחקרית; היא אינה מוכיחה שכל חץ הוא קריאת פונקציה בזמן ריצה. `wix_sync_manifest.json` מציין `PUBLISHED_READ_BACK_PARTIAL`; `semantic_benchmark_plan_v1.json` מציין `SPECIFIED_NOT_POPULATED`.

## מקורות קנוניים שנבדקו

[README](../README.md) · [AI-AGENT-NOTICE](../AI-AGENT-NOTICE.md) · [NEXT-MODEL-HANDOFF-KRAKEN](./NEXT-MODEL-HANDOFF-KRAKEN.md) · [Architecture V2](./LOGIC_WIKI_FRACTAL_ARCHITECTURE_V2.md) · [Daily Integration Map](./DAILY_INTEGRATION_MAP_2026-10-13.md) · [Logic Fractal Program](../research/LOGIC_FRACTAL_PROGRAM_V1.md) · [Logic kernel](../logic_engine_v1/logic_kernel.py) · [LNL Builder](../logic_model_builder_v1/README.md) · [Fragment composer](../logic_fractal/fragment_composer.py) · [Recursive contracts](../logic_fractal/data/recursive_composition_contracts_v1.json) · [Readiness gate](../logic_wiki/data/readiness_gate.json) · [Benchmark plan](../logic_fractal/data/semantic_benchmark_plan_v1.json) · [Wix manifest](../logic_wiki/data/wix_sync_manifest.json)

## מצב לאחר המיפוי

**DOCUMENTED:** קישורים והגבולות הראייתיים הוצמדו לכל חלק.  
**FOUND:** הוראת חמשת השערים, kernel סמלי מוגבל, LNL builder, composer, חוזי fractal וקובצי readiness/benchmark.  
**NOT_YET_VERIFIED:** אכיפה מלאה של השערים ב-runtime; סדר שני פורמלי; תוקף סמנטי מלא של fractal model; read-back מלא ב-Wix; מקור ישיר לטענת אין־סוף/אור אין־סוף ול-NIR/TNRL.  
**NEXT JUSTIFIED STEP:** להגדיר/לאמת trace שמקשר הצעה → מבנה → גזירה → בדיקת כלל → ראיות → פלט, ולהוסיף בדיקות replay שמוכיחות אילו שערים נאכפים בפועל.
