# תיעוד מודל ניהול פרויקטי תשתיות

## סקירת המודל

מימוש זה יוצר מודל אופטימיזציה לניהול מספר פרויקטי תשתית במקביל תוך טיפול בהחלטות בחירת ספקים ותזמון. המודל מבוסס על הניסוח המתמטי המתואר בקובץ Model 1.docx.

## המודל המתמטי

### אינדקסים וקבוצות

- **פרויקטים (j)**: שלושה פרויקטי תשתית שיש להשלים
- **פעילויות (i)**: 23 פעילויות לכל פרויקט עם יחסי קדימות
- **חומרי גלם (k)**: ארבעה סוגים של חומרי גלם הנדרשים לפרויקטים
- **ספקים (s)**: ארבעה ספקים עם קיבולות וזמני אספקה שונים
- **הזמנות (o)**: חמש הזמנות פוטנציאליות שניתן לבצע

### משתני החלטה

- **ST[i][j]**: זמן התחלה של פעילות i בפרויקט j
- **FT[i][j]**: זמן סיום של פעילות i בפרויקט j
- **OT[o][k][s][j]**: זמן הזמנה עבור הזמנה o של חומר גלם k מספק s לפרויקט j
- **x[o][k][s][j]**: כמות חומר גלם k שהוזמנה בהזמנה o מספק s לפרויקט j
- **S[o][k][s][j]**: משתנה בינארי המציין אם הזמנה o של חומר גלם k מספק s משמשת לפרויקט j
- **q[k][s][j]**: כמות כוללת של חומר גלם k מספק s לפרויקט j
- **TD[j]**: עיכוב בזמן של פרויקט j ביחס לתאריך היעד שלו
- **CT[j]**: זמן השלמת פרויקט j
- **Cmax**: זמן השלמה מקסימלי בין כל הפרויקטים

### פונקציית מטרה

פונקציית המטרה ממזערת את עלויות הקנס הכוללות עקב עיכובים בפרויקט:

```
min ∑(Penalty[j] * TD[j]) לכל j
```

### אילוצים עיקריים

#### אילוצי השלמת פרויקט וזמן מקסימלי
1. **אילוץ 1: השלמת פרויקט**: CT[j] = FT[הפעילות האחרונה][j] לכל j
2. **אילוץ 2: זמן השלמה מקסימלי**: Cmax ≥ CT[j] לכל j

#### אילוצי קיבולת ספקים וכמויות
3. **אילוץ 3: קיבולת ספקים**: ∑ q[k][s][j] ≤ Capacity[k][s] לכל k, s
4. **אילוץ 4: מיפוי כמויות**: ∑ x[o][k][s][j] = q[k][s][j] לכל k, s, j
5. **אילוץ 5: סיפוק ביקוש**: ∑ q[k][s][j] ≥ Quantity[k][j] לכל k, j

#### אילוצי הקצאת הזמנות
6. **אילוץ 6: הקצאת הזמנה (Big-M)**: x[o][k][s][j] ≤ M * S[o][k][s][j] לכל o, k, s, j
7. **אילוץ 7: אילוץ הזמנה אפס**: S[o][k][s][j] ≤ x[o][k][s][j] לכל o, k, s, j (לוודא שהזמנות עם כמות 0 מקבלות S=0)

#### אילוצי משך פעילות וקדימות
8. **אילוץ 8: משך פעילות**: FT[i][j] = ST[i][j] + Duration[i][j] לכל i, j
9. **אילוץ 9: יחסי קדימות**: ST[b][j] ≥ FT[a][j] לכל (a,b) ב-Pred, לכל j

#### אילוצי עיכוב זמן
10. **אילוץ 10: חישוב עיכוב**: TD[j] ≥ CT[j] - Target[j] לכל j
11. **אילוץ 11: עיכוב לא שלילי**: TD[j] ≥ 0 לכל j

#### אילוצי הגעת חומרים
12. **אילוץ 12: הגעת חומרים**: ST[i][j] ≥ OT[o][k][s][j] + Delivery_Time[k][s][j] - M * (1 - S[o][k][s][j]) לכל i, j, k, s, o

#### אילוצים נוספים (13-24)
13. **אילוץ 13: התחלת פעילות לא שלילית**: ST[i][j] ≥ 0 לכל i, j
14. **אילוץ 14: סיום פעילות לא שלילי**: FT[i][j] ≥ 0 לכל i, j
15. **אילוץ 15: זמן הזמנה לא שלילי**: OT[o][k][s][j] ≥ 0 לכל o, k, s, j
16. **אילוץ 16: כמות חומר לא שלילית**: x[o][k][s][j] ≥ 0 לכל o, k, s, j
17. **אילוץ 17: כמות כוללת לא שלילית**: q[k][s][j] ≥ 0 לכל k, s, j
18. **אילוץ 18: משתנה בינארי S**: S[o][k][s][j] ∈ {0,1} לכל o, k, s, j
19. **אילוץ 19: הזמנות רק מספקים בעלי קיבולת**: אם Capacity[k][s] = 0, אז q[k][s][j] = 0 לכל j
20. **אילוץ 20: תאימות לוח זמנים**: FT[i][j] ≤ ST[i+1][j] (לפעילויות ברצף)
21. **אילוץ 21: השלמת פרויקט במועד**: CT[j] ≤ Target[j] + TD[j] לכל j
22. **אילוץ 22: אספקת חומרים בהזמנות**: ∑ x[o][k][s][j] ≤ Capacity[k][s] לכל o, k, s, j
23. **אילוץ 23: התאמת זמן הזמנה לפרויקט**: OT[o][k][s][j] ≤ M * S[o][k][s][j] לכל o, k, s, j
24. **אילוץ 24: מגבלת הזמנות מקסימלית לספק**: ∑ S[o][k][s][j] ≤ NUM_order לכל k, s, j

## נתוני קלט

### פרויקטים ופעילויות

- שלושה פרויקטי תשתית במקביל
- כל פרויקט כולל 23 פעילויות עם יחסי קדימות
- לפעילויות משכי זמן שונים עבור כל פרויקט

### חומרי גלם וספקים

- ארבעה סוגי חומרי גלם נדרשים לפרויקטים
- ארבעה ספקים עם קיבולות שונות לכל חומר
- לספקים זמני אספקה ועלויות שונות

### תאריכי יעד וקנסות

- לכל פרויקט תאריך יעד להשלמה
- קנסות מוטלים עבור כל יום של עיכוב מעבר לתאריך היעד

## מימוש

המימוש מורכב מהקבצים הבאים:

1. **model_data.py**: מכיל את המחלקה `ModelData` עם כל פרמטרי הקלט
2. **model1.py**: מיישם את מודל האופטימיזציה באמצעות ספריית Python-MIP
3. **utils.py**: מכיל פונקציות עזר ליצירת ויזואליזציות
4. **main.py**: סקריפט ראשי שמריץ את המודל ומייצר דוחות וויזואליזציות

## הרצת המודל

להרצת המודל, הפעל את הפקודה הבאה:

```bash
python main.py
```

הסקריפט יבצע:
1. טעינת נתוני המודל
2. יצירה ופתרון של מודל האופטימיזציה
3. יצירת דוחות מפורטים
4. יצירת ויזואליזציות של התוצאות

## פלט וויזואליזציות

המודל מייצר את הפלטים הבאים:

### דוחות

1. **דוח השלמת פרויקט**: מציג תאריכי יעד, זמני השלמה בפועל, עיכובים וקנסות לכל פרויקט
2. **דוח לוח זמנים לפעילויות**: מציג את זמני ההתחלה והסיום לכל פעילות בכל פרויקט
3. **דוח הקצאת ספקים**: מציג כיצד חומרים מוקצים מספקים לפרויקטים
4. **דוח דרישות משאבים**: מציג את הכמויות הנדרשות והמוקצות של חומרים לכל פרויקט

### ויזואליזציות

1. **תרשים גאנט**: ייצוג חזותי של לוח הזמנים לפרויקט, המציג מתי כל פעילות מתחילה ומסתיימת
2. **תרשים שימוש במשאבים**: מפת חום המציגה את השימוש בחומרי גלם לפי פרויקט
3. **תרשים עיכובי פרויקט**: השוואה בין תאריכי יעד לזמני השלמה בפועל, יחד עם עיכובים וקנסות
4. **תרשים הקצאת ספקים**: מציג כיצד חומרי גלם מוקצים מספקים לפרויקטים
5. **תרשים נתיב קריטי**: מדגיש את הפעילויות הקריטיות בכל פרויקט

## פרשנות התוצאות

### ביצועי פרויקט

המודל יספק מידע על האם פרויקטים הושלמו בזמן או מעוכבים. אם פרויקט מעוכב, יוצגו משך העיכוב ועלות הקנס הנלווית.

### הקצאת משאבים

המודל יראה כיצד חומרי גלם מוקצים מספקים לפרויקטים. מידע זה יכול לסייע בהבנה אילו ספקים נמצאים בשימוש ועבור אילו חומרים.

### אופטימיזציה של לוח זמנים

תרשים גאנט וניתוח הנתיב הקריטי יכולים לסייע בזיהוי צווארי בקבוק והזדמנויות לשיפור לוח הזמנים.

## מגבלות והנחות המודל

1. המודל מניח משכי זמן דטרמיניסטיים לפעילויות וזמני אספקה
2. המודל אינו מתחשב באיזון משאבים או מגבלות כוח אדם
3. המודל מניח שכל החומרים חייבים להיות מוזמנים ומסופקים לפני תחילת הפעילויות
4. המודל אינו מתחשב באספקות חלקיות של חומרים

## שיפורים עתידיים

1. **משכי זמן סטוכסטיים**: הוספת אי-ודאות במשכי פעילות וזמני אספקת חומרים
2. **איזון משאבים**: הוספת אילוצים להגבלת מספר הפעילויות המקבילות
3. **אספקות חלקיות**: מתן אפשרות לאספקת חומרים במשלוחים חלקיים
4. **אופטימיזציה מחדש דינמית**: יישום מסגרת לעדכון המודל תוך כדי התקדמות הפרויקטים

## סיכום

מימוש זה מספק פתרון מקיף לניהול מספר פרויקטי תשתית עם בחירת ספקים. הוא מסייע במזעור עלויות קנס עקב עיכובים תוך התחשבות בקיבולות ספקים, דרישות חומרים ויחסי קדימות בין פעילויות.

המודל שימושי במיוחד למנהלי פרויקטים הצריכים לתאם מספר פרויקטים בו-זמנית ולקבל החלטות לגבי בחירת ספקים ותזמון.
