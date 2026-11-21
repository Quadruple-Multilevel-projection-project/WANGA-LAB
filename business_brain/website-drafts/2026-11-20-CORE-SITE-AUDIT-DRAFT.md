# Wix Core-Site Audit — Draft Remediations
Date: 2026-11-20
Status: DRAFT ONLY — no Wix page was changed or published.

## Verified inventory and coverage
- Wix inventory: 69 connected sites, from two read-only ListWixSites pages (50 + 19; no further page reported).
- Deep inspection this run: 6 priority sites, 71 HTML pages across 73 listed files.
- Remaining sites: 63 not deeply inspected this run; carry forward in the unified queue.
- Method: Wix headless files.list/read; static HTML checks for title, meta description, H1, relative links, image alt attributes and source text.
- Not performed: browser/device testing, Core Web Vitals, live route checks, screen-reader testing, search-ranking analysis or conversion analytics.

## 1. Logic Engine Research Lab
Inventory: 29 files / 28 HTML pages.

### VERIFIED findings
- `cross-site-logic-map.html`, `logic-compositions.html` and `source-audit.html` have titles and H1s but no meta description.
- `index.html` and `source-audit.html` report 53 Wix account sites.
- The connected Wix inventory currently returns 69 sites (50 + 19). The earlier 53 count is consistent with a historical snapshot, not the current inventory.
- `source-audit.html` also records a 16-site focused inventory, 174 unique URLs and 70 article sitemap entries. Those figures describe the earlier audit scope and must not be silently replaced by the 69-site account inventory.

### Proposed reversible draft
1. Label the 53-site metric as “Wix account inventory at the 2026-10-12 audit snapshot: 53 sites”.
2. Add a separate current line: “Connected Wix inventory on 2026-11-20: 69 sites; deep content inspection remains partial.”
3. Keep the 16-site / 174-URL / 70-article figures explicitly scoped to the 2026-10-12 sitemap audit.
4. Add the following meta descriptions:
   - `cross-site-logic-map.html`: “מפת קשרים רב־אתרית של WANGA-LAB: הבחנה בין קישור שנצפה, קשר לוגי מוסק וקומבינציה מוצעת, עם דרישות ראיה ובדיקות לפני אימות.”
   - `logic-compositions.html`: “מקרי הדגמה למנוע הלוגיקה: בדיקת הרשאות והיקף פעולה, השוואת טענה למקור וחישוב, ובחינת שינוי החלטה תחת קריטריון משתנה — באמצעות נתונים סינתטיים ומסומנים.”
   - `source-audit.html`: “מרשם מקורות WANGA-LAB: מלאי sitemap, סטטוס סקירת תוכן, ממצאי איכות והבחנה בין קישור, מקור שנבדק וטענה שאומתה.”

### Acceptance / rollback
- Acceptance: page titles remain unique; descriptions match the actual page content; historical and current inventory counts are separately dated and scoped.
- Rollback: discard the draft or revert the dedicated branch commit. Production write remains BLOCKED pending explicit site/change/publication approval.

Status: BLOCKED for production change; draft prepared.

## 2. AI231 Global Neural Governance
Inventory: 8 files / 7 HTML pages.

### VERIFIED findings
- `budget.html`, `cooperative.html`, `institute.html`, `roadmap.html` and `technology.html` have titles and H1s but no meta description.
- `budget.html` labels the ₪300–450M range as a five-year planning frame and says it requires re-pricing. This is a planning estimate, not evidence of a secured budget or financing.
- `technology.html` and `roadmap.html` use the legacy string “MIOMA-1”. The approved final processor name is not independently verified in the inspected site sources for this run; do not silently replace it.

### Proposed meta descriptions
- `budget.html`: “מסגרת תכנון ראשונית לעלויות AI231 בחמש שנים: טווחי חבילות, הנחות ורזרבה; המספרים הם אומדני תכנון ודורשים תמחור מחדש והצעות מחיר.”
- `cooperative.html`: “מבנה מוצע לקואופרטיב חברות AI: תחומי מומחיות, אחריות, תוצרים, הרשאות, IP ותנאי קבלה — ללא הנחת מספר סוכנים או חברות קבוע.”
- `institute.html`: “תפקיד מוצע למכון לממשל נוירוני עולמי: שירות ציבורי, ממשל אלגוריתמי, זכויות אזרח, ביקורת וגבולות משפטיים.”
- `roadmap.html`: “מפת הפיתוח של AI231: מיפוי מקורות, מפרט, אבטיפוס לוגי, ביקורת, ממשל, קואופרטיב סוכנים, מחקר חומרה ופיילוטים מבוקרים עם שערי קבלה.”
- `technology.html`: “סקירת התשתית הטכנולוגית המוצעת של AI231: מנוע לוגי, קומפיילר, ספריית לוגיקה, Auditor, Drift Forensics ומחקר חומרה — עם גבולות טענה ודרישות אימות.”

### Terminology task
Create a source-verification task for the processor's canonical name before any public terminology replacement. Preserve “MIOMA-1” as historical text until the source owner confirms the exact replacement.

Status: BLOCKED for production change; metadata draft prepared; terminology replacement unresolved.

## 3. AI231 Robotics Collaboration
Inventory: 3 files / 3 HTML pages.

Status: NO_CHANGE_WITH_EVIDENCE.
The inspected pages had titles, descriptions and H1s; no missing image alt or broken static internal target was found in the inspected files. No browser-level responsiveness or accessibility certification is claimed.

## 4. Logical AI Atlas
Inventory: 6 files / 6 HTML pages.

Status: NO_CHANGE_WITH_EVIDENCE.
The single `href="#"` is the header brand link and behaves as a top-of-page anchor pattern; it is not sufficient evidence of a broken link. No change prepared. Browser behavior remains unverified.

## 5. The Logic Economy
Inventory: 26 files / 26 HTML pages.

### VERIFIED findings
- `last-24-hours-logical-developments.html` has no meta description.
- The page labels itself “24 hours” but its content is dated 10 November 2026; this is stale relative to the 20 November inspection date.
- The Wix site context reports the site as Published on a Free plan and lists Wix Blog, Wix Payments and Wix Stores V3. App installation is not evidence of a transaction, cash receipt or revenue.
- Static link inspection found `/post/...` paths not represented as static files. Wix Blog is installed, so these are UNRESOLVED dynamic routes, not confirmed broken links.

### Proposed reversible draft
- Change the page label to “Research note — 10 November 2026” or add a clearly visible historical-date label; do not call it the latest 24-hour update.
- Proposed meta description: “תיעוד היסטורי של נקודות המחקר וההחלטות שגובשו ב־10 בנובמבר 2026 בכלכלת הלוגיקה; המסמך מתאר התפתחות מחקרית ואינו טוען לאימוץ חיצוני.”
- Verify each `/post/...` route through the Wix Blog read API or a live browser before classifying it as broken.

Status: BLOCKED for production change; draft prepared; dynamic routes unresolved.

## 6. AI231 Global
Inventory: 1 file / 1 HTML page.

Status: NO_CHANGE_WITH_EVIDENCE.
The inspected homepage had a title, description and H1; no static internal-link or missing-alt finding was returned. Browser-level checks remain unverified.

## Carry-forward
- 63 of 69 sites remain outside this run's deep-inspection batch.
- P1: inspect the next priority site batch using the same read-only method.
- P1: obtain explicit approval for any specific production Wix change before writing or publishing.
- P1: verify dynamic Wix Blog routes and the canonical processor name from authoritative project sources.
