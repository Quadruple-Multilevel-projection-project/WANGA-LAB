# מילות ההגיון — Sentence Extraction Index

מקור האמת לטקסט: Sivan22/otzaria-library, commit `d1106d9a66528dc3e39cf1ea0732782927d9f678`.

## שערים ומצב כיסוי

| שער | קובץ / מיקום מקור | מצב |
|---|---|---|
| א׳ | `integration/gates_1_8_source_registry.json#G01-S01` | SOURCE-LOCATED |
| ב׳ | `integration/gates_1_8_source_registry.json#G02-S01` | SOURCE-LOCATED |
| ג׳ | `integration/gates_1_8_source_registry.json#G03-S01` | SOURCE-LOCATED |
| ד׳ | `integration/gates_1_8_source_registry.json#G04-S01` | SOURCE-LOCATED |
| ה׳ | `integration/gates_1_8_source_registry.json#G05-S01` | SOURCE-LOCATED |
| ו׳ | `integration/gates_1_8_source_registry.json#G06-S01` | SOURCE-LOCATED |
| ז׳ | `integration/gates_1_8_source_registry.json#G07-S01` | SOURCE-LOCATED |
| ח׳ | `integration/gates_1_8_source_registry.json#G08-S01` | SOURCE-LOCATED |
| ט׳ | `שער-ט.md` / `שער-ט-יא-יב.md` | EXTRACTED |
| י׳ | `שער-י.md` | EXTRACTED |
| י״א | `שער-יא.md` | EXTRACTED |
| י״ב | `שער-יב.md` | EXTRACTED |
| י״ג | `../../docs/LOGIC/MILOT_HIGAYON_GATE_13_SENTENCE_REGISTRY.md` | EXTRACTED |
| י״ד | `שער-יד.md` | EXTRACTED |

## גבול הכיסוי

- שערים א׳–ח׳ אותרו ונבדקו מול קובץ המקור הבלתי־משתנה במאגר Otzaria; המרשם הנוכחי מספק מיקומי מקור וקטעי ראיה מדויקים לצורכי הקישור.
- `SOURCE-LOCATED` אינו שקול לחילוץ מלא ברמת משפט. שערים א׳–ח׳ עדיין אינם רשומים כאן כחילוץ משפטים מלא.
- שערים ט׳–י״ד מכילים את רישומי החילוץ הקיימים במאגר.
- קשרים בין שער י״ד לשערים קודמים נשמרים ב-`integration/explicit_links.json` ורק כאשר מצורפת הפניה לראיה.

## רצף העבודה

`שער א׳–ח׳` = מערכת סוגי המשפטים וההיקשים  
`שער ט׳–י״ב` = סבות → מין/סוג/הבדל/סגולה/מקרה → בעצמות/במקרה → קדימות/יחד  
`שער י״ג` = מיפוי שמות, סוגי שמות משותפים והעברה לשונית  
`שער י״ד` = דבור, מלאכה, פילוסופיה, חכמות והנהגה

## כלל בקרה

הציטוטים הם שכבת המקור.  
הסיווגים והתרשימים הם שכבת מבנה.  
תבנית מבנית חדשה חייבת להיות מסומנת כ-NEW ואסור להציגה כמשפט מן המקור.


## רישום קנוני של המקור — שערים א׳–י״ד

המקור המלא נשמר ללא שינוי ב־`milaot-hahigayon/source/milot_hahigayon_d1106d9a.html` לפי commit `d1106d9a66528dc3e39cf1ea0732782927d9f678`. רישום המילים ומועמדי המשפטים נמצא ב־`artifacts/book_sentence_registry.json`. חלוקת משפטים מבוססת פיסוק היא מועמדת בלבד (`CANDIDATE_SENTENCE_SEGMENTATION_NOT_VERIFIED`); היא אינה חילוץ תחבירי מאומת ואינה מוכיחה קשר בין שערים.


## אינטגרציה חיה ותוצרי ביקורת

- רישום מקור/משפטים/מילים לכל 14 השערים: `artifacts/book_sentence_registry.json` — חלוקת המשפטים היא מועמדת ולא תחביר מאומת.
- ניתוח מבני נגזר לשער י״ד: `artifacts/gate14_sentence_structure.json`.
- חפיפת פני־מילה בלבד: `artifacts/gate14_word_occurrence_matrix.json`.
- תפקידי מילים מועמדים עם מיקומי מקור: `artifacts/gate14_word_role_candidates.json`.
- מצב ביקורת עדכני שנוצר ב־CI ונשמר בענף: `artifacts/current_audit_status.json`.
- קוד ה־Wix Dashboard החי: `integration/wix_audit_dashboard_embed.html`.
- קוד WebMCP לקריאה בלבד: `integration/wix_webmcp_readonly_embed.html`.
- דוח סטטי/אינטראקטיבי לשימוש חוזר: `../../docs/milaot-hahigayon-structural-dashboard.html`.

ה־Wix Dashboard מציג `overall_mechanical_status`, `integration_status`, כיסוי מקור, מצב הרישום הישן, ריצת CI אחרונה, 34 מועמדי משפט, 799 טוקנים של שער י״ד, חפיפות מונחים ותפקידי מילים מועמדים. WebMCP נרשם רק כאשר `document.modelContext` או `navigator.modelContext` זמין בדפדפן; כל הכלים המוצגים לקריאה בלבד.
