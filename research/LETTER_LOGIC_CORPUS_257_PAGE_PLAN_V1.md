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


## עדכון מחייב: מבנה פרקטלי, ארבע שכבות המשקולות, והעיבוד המתמטי ההפיך

**סטטוס:** SPECIFIED — תיקון מסגור ותוכנית להמשך. אין כאן שפה נוספת נפרדת. ארבע שכבות המשקולות הן עומק לוגי־מתמטי בתוך המערכת; ההגדרות המדויקות שלהן חייבות להישלף מחומר המחקר ולא להיות מומצאות.

### 1. 257 עמודים הם שלד ניווט, לא תקרת המחקר

257 העמודים הם אינדקס ראשי ראשוני בעשרה כרכים. כל עמוד יכול להתפצל לתת־עמודים, רשומות מקור, רשומות פרשנות, יחסי צירוף, מפרטים מתמטיים, ניסויים ודוגמאות כאשר קיימת הבחנה מחקרית עצמאית. המספר 257 הוא תכנון עריכה, לא גבול הידע.

לכל הרחבה יש לתעד מה התווסף, אילו צמתים היא משנה ואיזה מקור/ניסוי מצדיק אותה. ההתרחבות הפרקטלית היא כרגע עיקרון ארגון; טענה על ממד פרקטלי מתמטי מחייבת מדידות ונוסחה נפרדות.

### 2. כרטיס תכנון נפרד לכל עמוד

כל אחד מ-257 העמודים יקבל:
- מזהה יציב ושם;
- שאלת המחקר המדויקת;
- נושא אב ותתי־נושאים;
- מקורות נדרשים, זמינותם ומצב האימות;
- מונחים, אותיות, פרשנויות, יחסים ומשקולות קשורים;
- הבחנה בין מקור, חילוץ, פרשנות והצעת הנדסה;
- דוגמאות, נגד־דוגמאות ומבחנים;
- קישורים נכנסים ויוצאים;
- פערים ושאלות פתוחות;
- סטטוס והיסטוריית שינויים.

עמוד חסר־מקור יישאר מסומן כחסר; אין למלאו בתוכן כללי רק כדי שייראה שלם.

### 3. לוגיקת האותיות

לכל אות יש לשמור רשומה נפרדת לכל פרשנות שנמצאה בפועל. הרשומה תכלול מקור והקשר מדויקים, נוסח הפרשנות, הבחנה בין מקור לפרשנות החוקר, צורה גרפית כאשר רלוונטית, מיקום/סדר/צירוף, יחסים לאותיות אחרות, פרשנויות מתחרות, מזהה יציב וקישורים.

אין להניח מראש מספר קבוע של פירושים לאות. אין להסיק מתיאור הצורה לבדו שמנגנון חישובי מסוים הוכח.

### 4. העומק הרביעי: ארבע שכבות המשקולות הלוגיות־מתמטיות

מסגרת המחקר של המשתמש קובעת ארבע שכבות משקולות, כאשר לכל פרשנות של אות משויכת משקולת לוגית־מתמטית. יש לתעד את השכבות ואת ההגדרות המקוריות שלהן לפני ניסוח המפרט הסופי.

**הגדרות פתוחות:** בקובץ המקור בן 79 העמודים שנבדק לא נמצאו שמות, נוסחאות או כללי שילוב מלאים של ארבע שכבות המשקולות. לכן אין להמציא להן שמות, ערכים או נוסחאות. יש לאתר את חומר המחקר הנוסף שמגדיר אותן, ולאחר מכן לתעד לכל שכבה:
- הגדרה ותפקיד;
- על איזה אובייקט היא חלה;
- קלט/פלט וכלל חישוב;
- תחום הערכים/יחידות, אם קיימים;
- קשר לשאר השכבות ולפרשנות האות;
- תנאי תחולה, חריגים ואי־ודאות;
- דוגמאות חישוב ונגד־דוגמאות;
- מבחני עקביות ורגישות;
- ראיה ותוצאה בפועל וסטטוס.

יש להבדיל בין ארבע שכבות המשקולות לבין (א) ארבעת תפקידי המשפט המתוארים בקובץ המקור — נושא, נשוא, משתתף פנימי וסוג החיבור הלוגי; (ב) שלוש שכבות המנוע שהוצעו במסמך הארכיטקטורה; ו-(ג) ארבע שכבות התיעוד מקור/חילוץ/פרשנות/הצעת הנדסה. אלו חלוקות שונות ואין למזגן.

### 5. ייצוג מתמטי ומסלול שחזור

יש לתכנן שני מסלולים נפרדים:
- **קידוד:** טקסט מקור → חילוץ מבני → ייצוג לוגי → פרשנויות אות → ארבע שכבות המשקולות → ייצוג מתמטי.
- **פענוח/שחזור:** הייצוג המתמטי → פירוק לפי המפרט → שחזור המבנה הלוגי → שחזור הטקסט או ייצוג נאמן שלו.

אין להניח שהמסלול ההפוך כבר אפשרי. יש להגדיר שני מבחנים שונים:
1. **שחזור טקסט מדויק:** האם `decode(encode(T)) = T`, תוך שימור סדר תווים, ניקוד, סימני פיסוק ומקטעי מקור ככל שהייצוג טוען לשמרם.
2. **שחזור מבני:** האם ניתן לשחזר את יחסי הנושא/נשוא, המשתתפים, מילות הקישור, המשפטים הפנימיים, הסדר והעמימות המתועדת.

אם ייצוג כלשהו מאבד מידע, יש לרשום מה אבד ואיזה שלב איבד אותו. אין לטעון לשחזור מדויק אם נשמר רק מבנה סמנטי כללי.

### 6. מה הקובץ בן 79 העמודים תומך בו — ומה לא

ביקורת הקובץ מתועדת ב-[SOURCE_AUDIT_79_PAGE_LOGIC_EXTRACTION_2026-10-12.md](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/research/SOURCE_AUDIT_79_PAGE_LOGIC_EXTRACTION_2026-10-12.md).

הקובץ תומך בתיעוד של חילוץ לוגיקה ראשונה: שמירת המשפט, הנושא/הסיפור, הנשוא/המסופר, מילות יחס וקישור, שמות משתתפים, יחסים ומשפטים פנימיים. הוא כולל מיפוי יחסים מתוך עץ חיים, ובחלק על מורה נבוכים א׳:ח׳ — יחידות `S-08-001…S-08-028`. באותו חלק נאמר מפורשות שלא מסיקים עדיין לוגיקה שנייה, ורק לאחר סגירת החילוץ ניתן להפעיל את החלק הבא.

הקובץ אינו מגדיר את ארבע שכבות המשקולות, נוסחת קידוד/פענוח הפיכה, מפרט מלא של 231 השערים, כל קואורדינטות ה־3D, נוסחת ממד פרקטלי מלאה או פרוטוקול הניסוי שמאמת את ערכי LFA/CSR/EDI. רכיבים אלה נשארים מפרטים/ניסויים נפרדים.

### 7. מפרטים מתמטיים שיש לנהל בנפרד

לצורך דיוק יש להפריד בין:
- קומבינטוריקה של 231 שערים וסדר האותיות;
- הגדרת כל שער ופונקציית המעבר שלו;
- קואורדינטות X/Y/Z ונתוני צומת;
- הגדרת Macro/Micro/Pico והקשרם לנתונים מדידים;
- נוסחה ונתוני קלט לממד פרקטלי;
- יחס הזהב ומקור סכומי האותיות;
- ארבע שכבות המשקולות וכלל השילוב ביניהן;
- מדדי ביצועים, מערך נתונים, baseline, יומני הרצה ותוצאות.

הוכחה חשבונית שהמספר 231 שווה ל-`22×21/2` אינה מאמתת את מנוע 231. התאמה מספרית ליחס הזהב אינה מאמתת כשלעצמה חוק פרקטלי. כל טענה מתמטית או ניסויית תלווה בהנחות, נוסחה, נתונים ובדיקה חוזרת.

### 8. כלל עדכון פרקטלי

בעת גילוי מקור, פרשנות, יחס או משקולת:
1. ליצור רשומה עם מזהה יציב;
2. לתעד מקור וסטטוס;
3. למצוא עמודים ומפרטים תלויים;
4. לעדכן מפת קשרים והיסטוריית שינויים;
5. ליצור תת־עמוד רק כשיש שאלה עצמאית;
6. לשמור פרשנויות סותרות בנפרד;
7. להוסיף דוגמאות ומבחנים;
8. להשאיר נתון חסר בתור NOT_YET_VERIFIED ולא להשלים אותו בניחוש.

### 9. פרסום לפי שלבי אתרים

- **WANGA-LAB / GitHub:** מקור האמת למפרטים, לסכמות, למקורות, לבדיקות ולהיסטוריית שינויים.
- **Notion:** כרטיסי מחקר, קשרים בין פרקטלים, שאלות פתוחות והחלטות.
- **Wanga Logic Research:** מסמכי הסבר טכניים ומפרטי מנוע, במצב Draft עד ביקורת.
- **Forensic Logic Drift:** פוסט ציבורי שמבדיל בבירור בין מה שהחילוץ מדגים לבין הארכיטקטורה המתוכננת.
- **Hebrew Thesis Insight:** תקציר למשקיעים שמפנה לראיות ומפריד בין מחקר, מפרט, אב־טיפוס ותוצאה מאומתת.
- **Wanga Lab:** דף ניווט מסכם לענפי המחקר ולסטטוסים, בלי שכפול המאמר הטכני כולו.

אין לפרסם מדדי ביצוע מספריים כעובדות ללא מערך נתונים, הגדרות מדדים, קוד/יומני הרצה ותוצאות הניתנות לשחזור.

### 10. סדר העבודה

1. לאמת את מפת המקורות.
2. לשמור ולסיים את חילוץ הלוגיקה הראשונה מכל מקור.
3. לאתר את ההגדרות הקיימות של ארבע שכבות המשקולות.
4. לתעד את כל הפרשנויות של האותיות שנמצאו בפועל ולשייך משקולות לפי ההגדרות המקוריות.
5. להגדיר קידוד, פענוח ושחזור.
6. להגדיר בנפרד שערי 231, גיאומטריה, ממד פרקטלי וכל נוסחה אחרת.
7. לבנות מבחנים חוזרים לפני הצגת ביצועים.
8. לסנכרן את GitHub ואת Notion.
9. להכין טיוטות Wix נפרדות לפי תפקיד האתר, ורק לאחר ביקורת להחליט על פרסום.

**סטטוס:** תוכנית המיפוי עודכנה. ארבע שכבות המשקולות, הנוסחאות המלאות, המנוע ההפיך והביצועים נשארים NOT_YET_VERIFIED עד שיוצגו ההגדרות והראיות.

## תיקון מושגי מחייב: אין כאן שפה נפרדת

לא מפתחים שפה עצמאית חדשה. העומק הרביעי הוא שכבת לוגיקה מתמטית: לכל פרשנות של אות משויכת משקולת לוגית־מתמטית, והיא מתחברת למבנה הרחב של הטקסט. המטרה היא לבדוק אם ניתן לייצג ולפרק את המבנה המתמטי בחזרה לרמה הלוגית והטקסטואלית. את ארבע שכבות המשקולות צריך לשחזר מהמחקר עצמו; אין לשנות את שמותיהן או להמציא נוסחאות ללא מקור.


## רישום פרסום לפי שלבי האתרים

מפת המצב של GitHub, Notion ואתרי Wix — כולל אתר שבו נוצרה טיוטת פוסט לא־מפורסמת ואתרים שלא שונו — נמצאת ב-[LOGIC_CORPUS_PUBLICATION_STAGING_2026-10-12.md](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/LOGIC_CORPUS_PUBLICATION_STAGING_2026-10-12.md). יש להתייחס אליה כמפת מצב עדכנית, לא כהוכחה שכל המסלולים מומשו.

## ארכיטקטורת חמש שכבות קדימה וחמישה שלבי חזור

המודל החדש אוחד למסמך קנוני אחד: [FIVE_FORWARD_FIVE_RETURN_LOGIC_ARCHITECTURE_REVIEW_V1.md](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/FIVE_FORWARD_FIVE_RETURN_LOGIC_ARCHITECTURE_REVIEW_V1.md). הוא מסיר כפילות בין תיאור חמש השכבות לבין תיאור עשר התחנות, ומבחין בין שלוש מערכות מושגיות: חמש שכבות עיבוד + חמישה שלבי חזור; ארבע שכבות משקולות לוגיות־מתמטיות; וארבעת תפקידי המשפט בחילוץ הטקסט. שמות ונוסחאות ארבע שכבות המשקולות עדיין דורשים איתור במקורות.


## מפת ניווט לקורא והקופסאות הלוגיות באתר

פורסם דף היכרות שמדגים ניווט בין תוצרי המחקר באמצעות קופסאות קישור: [מפת השימוש הלוגי באתר](https://beywolf5.wixsite.com/forensic-logic-dri/post/מפת-השימוש-הלוגי-באתר-קופסאות-קישור). בתוכנית ההמשך, כל עמוד לוגי יקבל מפת ניווט מקומית שמקשרת מקור, בעיה, המודל הרלוונטי, בדיקות והשלב הבא. מפת הניווט המרכזית אינה מוכיחה שכל המאמרים הישנים כבר עודכנו.

## Supplementary atomic page definitions — 1,000-record extension (2026-10-12)

The 257-page plan remains the editorial outline. The separate 1,000-record registry defines granular letter/gate/transition dossiers, map/submap definitions, validation cases and formalization obligations. These are not represented as complete or published articles.

- [Extended 1,000-page plan](../docs/EXTENDED_LOGIC_CORPUS_1000_PAGE_BLUEPRINT_V1.md)
- [Machine-readable registry index](./data/LOGIC_CORPUS_1000_PAGE_BLUEPRINT_V1.json)
- [Master map atlas](../docs/LOGIC_CORPUS_MAP_ATLAS_V1.md)
- [Mathematical integrity register](../docs/LOGIC_231_MATHEMATICAL_INTEGRITY_REGISTER_V1.md)

The extension distinguishes 231 unordered pairs, 462 ordered pairs, 1,540 unordered triples and 9,240 ordered triples without repetition. It retains the documented 221/231 textual variant and leaves missing weight formulas and spatial/Lie/E8/Tonnetz mappings unresolved.
