# 🧠 KVÍZJÁTÉK 🏆
## CLI felületű többféle kérdéstípust vegyesen tartalmazó kvízjáték
### Futtatáshoz szükséges:
#### <li>Python 3.10+</li>
#### <li><code>python.exe Quiz_main.py</code></li>

### Feature-k:
- ✅ Fájlbeolvasás: A kérdések és válaszok fájlból kerülnek beolvasásra.
- ✅ Véletlenszerű sorrend: A kérdések és válaszok sorrendje keverve lesz.
- ✅ Pontozás és eredményösszegzés: A játék végén összegzi az eredményt.
- ✅ Időmérés és ranglista: A játék időre mehet, és az eredményeket elmenti.
- ✅ Segítségek: Felezés (50/50)
- ✅ Kategóriák kibővítése

### Térkép:
/CLI_Quiz
│── quizes/
│   ├── capitals.json
│   ├── cars.json
│   ├── python_learning.json
│   ├── songs_hu.json
│   ├── songs_int.json
│── main.py
│── modules.py
│── classic_quiz.py
│── question_loader.py
│── ascii.py
│── categories.py
│── colors_cli.py
│── highscores.txt - TODO: időtartó ranglista