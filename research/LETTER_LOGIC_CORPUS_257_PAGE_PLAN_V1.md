# תוכנית אב: מאגר הלוגיקה — תוכנית ל-257 עמודים ב-Wix

**סטטוס:** SPECIFIED — תוכנית תוכן; לא 257 מאמרים שכבר נכתבו או אומתו.  
**מטרה:** להסביר באופן מסודר את הלוגיקה הנחקרת: מקורותיה, פרשנויות, יחסים, צירופים, משקולות, גבולות, והאפשרות לתרגם מבנים נבחרים למודולי לוגיקה עבור AI.  
**גבול:** המאגר הוא שכבת מחקר, הסבר והדגמה. הוא אינו המוצר המסחרי עצמו ואינו חושף את מימוש ה-IP המוגן של Rational Logic.

## מבנה מאקרו

יעד העבודה הוא **257 עמודים** בעשרה כרכים, בתוך הטווח המבוקש 180–300. היעד יותאם לאחר ביקורת מקורות. מספר הפרשנויות לכל אות לא נקבע מראש: הוא ייגזר רק מהמקורות שיימצאו ויתועדו.

### כרך 0: Governance and method — 12 עמודים
**תחום:** Purpose and limits; definitions; three branches; source/extraction/interpretation/engineering distinction; evidence statuses; provenance; citations; competing readings; page template; publication workflow.

### כרך 1: Logic as a structured object — 18 עמודים
**תחום:** Logic beyond dictionaries; propositions; subject/predicate; relations; sequence; composition; cause/effect; distinction; scope; states/transitions; convergence; explicit/inferred rules; meaning versus structure; reusable logic; evaluation criteria.

### כרך 2: Rambam / Maimonides and Millot ha-Higayon — 28 עמודים
**תחום:** Source and edition register; term definitions; classifications; examples; sentence decomposition; subject/predicate; judgment; affirmation/negation; quantification and modality only where the source supports them; argument structure; source-faithful templates; counterexamples; machine-readable extraction; review.

### כרך 3: Philosophical logic: place and relations — 28 עמודים
**תחום:** Place; container/contained; position/location; relation/property; identity; difference; analogy; whole/part; boundary; center/periphery; temporal order; cause; dependence; possibility/actuality; movement; continuity; unity/multiplicity; convergence; ambiguity; context; relation graphs; limits.

### כרך 4: Letter logic: interpretations, form, relations, and composition — 60 עמודים
**תחום:** Method for tracking multiple readings; lexical/symbolic/graphic/positional/relational readings; 44 planned letter dossiers (two per Hebrew letter: source-attested readings and proposed graphic/relational readings); final forms; groups; repetition; order; combinations; module specification.

### כרך 5: Ari / Arizal and the source corpus — 36 עמודים
**תחום:** Corpus inventory and edition policy; source dossier for Olam HaNekudim; terminology of Nekudim/circles/straightness; source relations, sequence, boundaries, pressure/breakage/repair only after exact-source audit; page maps for cited references 31, 37, 38, 39, 41–42; variants; cross-references; explicit versus derived relations; research boundaries.

### כרך 6: Weights, confidence, and combinations — 22 עמודים
**תחום:** Meaning of a weight; separate source confidence, interpretation stability, extraction confidence, task relevance, context fit, evidence, contradictions, uncertainty; scales; normalization; combination rules; sensitivity; non-fabricated precision; examples for Aleph/Lamed/Mem; machine-readable schema.

### כרך 7: Translation into AI logic and engineering — 24 עמודים
**תחום:** Source-to-record pipeline; canonical logic-unit schema; provenance; multiple interpretations; relation graphs; operations; transitions; weights; constraints; composition; conflict handling; tests; deterministic versus model-assisted checks; interfaces; failure/abstention; versioning; drift; traceability; WANGA/Rational Logic interface proposal.

### כרך 8: Demonstrations and tests — 17 עמודים
**תחום:** Source-grounded sentence decomposition; relation mapping; multiple letter readings; source/inference distinction; bounded Aleph/Lamed/Mem hypotheses; composition; weight sensitivity; contradiction; ambiguity preservation; source traceability; fixtures; negative/adversarial tests; human review; reproducibility and results.

### כרך 9: Investor-facing explanation and commercial boundary — 12 עמודים
**תחום:** Definition of logic asset; research corpus versus product; package anatomy; base logic/configuration/execution; illustrative catalogue entries; customer evaluation; unverified commercial assumptions; claim boundaries; investor summary.

## עקרונות המחקר שאסור להפר

1. **ארבע שכבות נפרדות:** מקור מפורש → חילוץ מבני → פרשנות/הסקה → הצעת הנדסה. אסור למזג ביניהן.
2. **שלושה ענפים נפרדים לפני אינטגרציה:** (א) רמב״ם/מילות ההיגיון, (ב) פילוסופיה של מקום ויחסים, (ג) לוגיקת האותיות. קורפוס האריז״ל הוא מקור מרכזי לחקירה, אך אינו שם חלופי ללוגיקת האותיות או למוצר.
3. **אין לקבוע פירוש יחיד לאות:** כל פירוש יקבל מזהה, מקור, הקשר, סטטוס, יחסים ופירושים חלופיים.
4. **צורת אות אינה מנגנון מוכח:** תיאור גרפי ותפקיד חישובי מוצע חייבים להופיע בשדות נפרדים.
5. **אין משקל ללא הגדרה:** כל משקל חייב להסביר מה הוא מודד, למה ניתן הערך, מה רמת אי-הוודאות, ואיך התוצאה משתנה כשמשנים אותו.
6. **אין VERIFIED ללא ראיה:** build מוצלח, ניסוח משכנע או פרשנות מעניינת אינם אימות.
7. **לא כל מקור מכיל בהכרח מבנה לוגי בר-חילוץ:** יש להראות מבנה רציף ולא לכפות לוגיקה על טקסט.
8. **NOT FOUND IN SEARCH ≠ DOES NOT EXIST.**

## תבנית חובה לכל עמוד

- **שאלת העמוד:** בעיה ממוקדת.
- **מקור:** שם החיבור, מחבר/מסורת כפי שהמקור מציגם, מהדורה, עמוד/סעיף, ציטוט נחוץ וקישור.
- **הנאמר במקור:** ניסוח נאמן ללא הרחבה סמויה.
- **חילוץ:** מונחים, נושא/פעולה/מושא, יחסים, סדר, תנאים, הבחנות, צירופים, מעבר ותוצאה.
- **פרשנויות חלופיות:** כל אחת נשמרת בנפרד ומקושרת למקור שלה.
- **הסקה ישירה:** מה נובע מן המקור ומה לא מוכרע.
- **הצעת הנדסה:** פעולה, כלל, מצב, מעבר, אילוץ או ממשק אפשריים — מסומנים כהשערה עד בדיקה.
- **משקולות:** שדות נפרדים למקור, פרשנות, חילוץ, רלוונטיות, התאמה להקשר, ראיות, סתירות ואי-ודאות.
- **דוגמה ונגד-דוגמה:** תנאי התאמה ותנאי כישלון.
- **בדיקה:** קריטריון קבלה, תוצאה צפויה, תוצאה בפועל וראיה.
- **קישורים:** מקור אחד לפחות, מושג/אות/יחידת לוגיקה, ומבחן או עמוד המשך.
- **סטטוס:** SOURCE / EXTRACTED / INFERRED / HYPOTHESIS / SPECIFIED / PROTOTYPED / TESTED / VERIFIED / NOT_YET_VERIFIED.

## כיצד ייבנה מודל המשקולות

אין להתחיל מציון משוקלל אחד. תחילה יש להפריד בין:
- חוזק האסמכתה במקור;
- יציבות הפרשנות;
- ביטחון בחילוץ המבני;
- רלוונטיות למשימה;
- התאמה להקשר;
- ראיות בדיקה;
- סתירות ונגד-דוגמאות;
- אי-ודאות ומידע חסר.

רק אחרי איסוף דוגמאות ניתן להחליט אם כל ממד הוא סולם סדרי, מספרי או קטגוריאלי, ואם וכיצד משלבים ממדים. כל ערך מספרי הוא SPECIFIED בלבד עד שנבדק.

## גרף האתר וקישורים

- **דף שער:** מהו המאגר, מה הוא אינו, ואיך לקרוא סטטוסים.
- **דפי כרכים:** ניווט לעשרת תחומי המחקר.
- **דפי מקור:** ביבליוגרפיה, מהדורה, מיקום, ציטוטים וחילוצים מקושרים.
- **דפי אות:** פרשנויות, צורה, צירופים, משקולות, מקורות ומבחנים.
- **דפי מושג:** מקום, יחס, גבול, צירוף, סיבה, תוצאה ומשקל.
- **דפי יחידת לוגיקה:** משימה, קלט, פלט, תנאים, גבולות, מבחנים וגרסה.
- **דפי הדגמה:** מקור → חילוץ → השערה → מבחן → תוצאה.
- **דף למשקיעים:** הסבר קצר עם קישורים לראיות ולהדגמות, בלי טענות לא מאומתות.

כל עמוד יכלול לפחות שלושה קישורים פנימיים בעלי ערך. אין ליצור קישורים מלאכותיים רק כדי להגיע למספר.

## סדר עבודה

1. **מיפוי מקורות:** לאסוף את מה שנגיש ב-GitHub, Notion, Wix והעלאות קיימות; לסמן מה נקרא בפועל, מה רק מוזכר ומה חסר.
2. **ביקורת מקורות:** אימות מול הטקסט המקורי של הפניות לעמודים 31, 37, 38, 39, 41–42 בנושא נקודים/עיגולים/יושר.
3. **חילוץ נפרד:** רמב״ם/מילות ההיגיון; פילוסופיה של מקום ויחסים; קורפוס האריז״ל; לוגיקת האותיות.
4. **אינדקס האותיות:** לתעד את מספר הפרשנויות שנמצאו בפועל, ולא להמציא מספר מראש.
5. **מפרט משקולות:** להגדיר רק אחרי שיש דוגמאות ממשיות וניתן להסביר כל ממד.
6. **הדגמות AI:** לבחור 3–5 משימות תחומות; להגדיר מבחני הצלחה וכישלון מראש; לשמור תוצאות וכשלים.
7. **ביקורת אנושית:** אין לפרסם מאמר לפני סקירת המקורות והסטטוס שלו.
8. **עדכון דף המשקיעים:** לתאר במדויק את שלושת ענפי המחקר ואת המעבר ממקור למבנה, מהשערה לבדיקה, וממחקר למוצר.
9. **פרסום מדורג:** דפי יסוד והדגמה ראשונה תחילה; הרחבת האתר לאחר מכן.

## עדכון דף המשקיעים — עקרונות ניסוח

יש להסביר שהמחקר מנסה להפוך מבנים לוגיים לאובייקטים שניתן לתעד, להשוות, להרכיב, להגדיר להם גבולות, לבחון אותם ולתרגם חלק מהם ללוגיקה מוכוונת-משימה עבור AI. יש להבחין בין:
- מחקר ומיפוי מקורות;
- מפרט פורמלי;
- אב-טיפוס;
- תוצאות בדיקה;
- אימות עצמאי;
- מוצר ושימוש מסחרי.

אין להציג את הלוגיקה של האותיות כיכולת AI מוכחת לפני שיש מפרט, מערך בדיקות ותוצאות. אין להציג פרשנות קבלית כמנגנון פיזיקלי או חישובי מוכח.

## מקורות שכבר אותרו

- [WANGA-LAB — Logic Mine Research Tracks](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/research/LOGIC_MINE_RESEARCH_TRACKS.md) — מגדיר את מכרה הלוגיקה כהשערת מחקר מבוססת ראיות.
- [WANGA-LAB — Productization and First Logic Demo](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/PRODUCTIZATION_AND_FIRST_LOGIC_DEMO_2026-10-09.md) — מפריד בין אב-טיפוס לבין יכולת מאומתת.
- [WANGA-LAB — Rational Logic Integration Position](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/RATIONAL_LOGIC_INTEGRATION_POSITION_V1.md) — מציג מיקום ארכיטקטוני מוצע ולא מנוע שהושלם.
- Notion: “סיכום חילוץ — מאמרות, סיבות, צירופים וגילוי — 2026-10-02” — יחסים, צירוף, התכנסות, מרכז וגילוי; הרשומה מסומנת unverified.
- Notion: “BUNDLE 01 — שער א׳ — Sentence Analysis” — מתעד 17 משפטים משער א׳ ומפריד בין מקור לתבניות נגזרות.
- Wix [Forensic Logic Drift](https://beywolf5.wixsite.com/forensic-logic-dri) — אתר מפורסם עם Wix Blog, מועמד לאירוח המאגר.
- Wix [Hebrew Thesis Insight](https://beywolf5.wixsite.com/hebrew-thesis-insigh) — אתר משקיעים מפורסם, מועמד לעדכון לאחר אימות הניסוח.

## מצב עבודה
- **SPECIFIED:** תוכנית ל-257 עמודים, עשרה כרכים, תבנית עמוד, גרף קישורים וסדר עבודה.
- **NOT_YET_VERIFIED:** שלמות המקורות, כל פרשנויות האותיות, שיטת המשקולות, איכות המיפוי וערך מסחרי.
- **PLANNED / NOT BUILT YET:** 257 המאמרים המלאים. אין לטעון שהם כבר נכתבו או פורסמו.
