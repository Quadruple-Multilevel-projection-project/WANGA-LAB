# מילות ההגיון — Sentence Extraction Index

מקור האמת לטקסט: Sivan22/otzaria-library, commit `d1106d9a66528dc3e39cf1ea0732782927d9f678`.

## שערים שכבר חולצו

| שער | קובץ | מצב |
|---|---|---|
| ט׳ | `שער-ט.md` / `שער-ט-יא-יב.md` | EXTRACTED |
| י׳ | `שער-י.md` | EXTRACTED |
| י״א | `שער-יא.md` | EXTRACTED |
| י״ב | `שער-יב.md` | EXTRACTED |
| י״ג | `../../docs/LOGIC/MILOT_HIGAYON_GATE_13_SENTENCE_REGISTRY.md` | EXTRACTED |
| י״ד | `שער-יד.md` | EXTRACTED |

## רצף העבודה

`שער א׳–ח׳` = מערכת סוגי המשפטים וההיקשים  
`שער ט׳–י״ב` = סבות → מין/סוג/הבדל/סגולה/מקרה → בעצמות/במקרה → קדימות/יחד  
`שער י״ג` = מיפוי שמות, סוגי שמות משותפים והעברה לשונית  
`שער י״ד` = דבור, מלאכה, פילוסופיה, חכמות והנהגה

## כלל בקרה

הציטוטים הם שכבת המקור.  
הסיווגים והתרשימים הם שכבת מבנה.  
תבנית מבנית חדשה חייבת להיות מסומנת כ-NEW ואסור להציגה כמשפט מן המקור.


## Map and factory integration
This extraction index is consumed by the central map registry:
- `docs/LOGIC_FACTORY/MASTER_MAP_INTEGRATION_CONTRACT.md`
- `docs/LOGIC_FACTORY/map_registry.v1.json`

Gate extraction status remains independent of map rendering:
- שער ט׳–י״ד: EXTRACTED as recorded above.
- שער א׳–ח׳: extraction/source evidence remains incomplete; do not upgrade by inference.
- Chapter maps are a separate mapping dimension. A chapter number is not automatically identical to a gate number.
- Every cross-map edge must carry a source/evidence reference and relation status.

## Integration action signature
Timestamp=2026-11-18T00:12:30+02:00
Contract_Start_Time=2026-11-17T20:29:00+02:00
Action_ID=AI231-SENTENCE-INDEX-LINK-004
SHA256=e6207429f3e68e515274c305ceb060b237739e39792df7871764bdc4b665bc5a
