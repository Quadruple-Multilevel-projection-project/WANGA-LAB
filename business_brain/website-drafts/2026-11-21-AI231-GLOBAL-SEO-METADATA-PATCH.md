# AI231 Global Neural Governance — SEO Metadata Patch Draft
Date: 2026-11-21
Status: DRAFT_ONLY / PRODUCTION_BLOCKED — no Wix file was changed or published.

## Scope and provenance
- Site: AI231 Global Neural Governance
- Site ID: `70e8848a-5ab9-459d-905d-1d82d5706e81`
- Site URL: https://headless-eqndpcqanph-beywolf5-1408.wix-site-host.com/
- Read method: Wix headless `files.list/read`, read-only.
- Files: `budget.html`, `roadmap.html`, `technology.html`.
- Snapshot date: 2026-11-21.

## VERIFIED before-state
All three pages contain a charset, viewport, title and stylesheet link, but no `meta name="description"` element.

### `budget.html`
Before:
```html
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>מסגרת פיתוח ועלויות | AI231</title><link rel="stylesheet" href="assets/site.css"></head>
```
Proposed after:
```html
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="מסגרת תכנון ראשונית לעלויות AI231 בחמש שנים: טווחי חבילות, הנחות ורזרבה; המספרים הם אומדני תכנון ודורשים תמחור מחדש והצעות מחיר."><title>מסגרת פיתוח ועלויות | AI231</title><link rel="stylesheet" href="assets/site.css"></head>
```

### `roadmap.html`
Before:
```html
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>מפת פיתוח | AI231</title><link rel="stylesheet" href="assets/site.css"></head>
```
Proposed after:
```html
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="מפת הפיתוח של AI231: מיפוי מקורות, מפרט, אבטיפוס לוגי, ביקורת, ממשל, קואופרטיב סוכנים, מחקר חומרה ופיילוטים מבוקרים עם שערי קבלה."><title>מפת פיתוח | AI231</title><link rel="stylesheet" href="assets/site.css"></head>
```

### `technology.html`
Before:
```html
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>התשתית הטכנולוגית | AI231</title><link rel="stylesheet" href="assets/site.css"></head>
```
Proposed after:
```html
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="סקירת התשתית הטכנולוגית המוצעת של AI231: מנוע לוגי, קומפיילר, ספריית לוגיקה, Auditor, Drift Forensics ומחקר חומרה — עם גבולות טענה ודרישות אימות."><title>התשתית הטכנולוגית | AI231</title><link rel="stylesheet" href="assets/site.css"></head>
```

## Acceptance and rollback
- Acceptance: each page has exactly one non-empty description; existing title, viewport and stylesheet link remain unchanged; description matches the page's actual planning/research scope.
- Not tested: live SERP display, rankings, mobile browser rendering, Lighthouse scores or conversion impact.
- No terminology replacement was made. The legacy processor name in other pages remains subject to source verification.
- Rollback: discard this draft or revert its dedicated repository commit. Production Wix write/publication remains blocked until explicit approval for this exact site, these exact three pages and this metadata-only scope.
