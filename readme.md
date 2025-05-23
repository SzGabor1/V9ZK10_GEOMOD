# Catmull-Rom Görbe és Forgási Felület Generátor

Ez a Python projekt egy **Catmull-Rom spline** alapú görbét generál, amit az **Y-tengely körül forgatva** egy 3D felületté alakít. Az alkalmazás **MVC (Model-View-Controller)** architektúrát használ, és interaktív GUI-val rendelkezik. A felületet **PyVista** segítségével vizualizálja.

## 🔧 Fő Funkciók

- **MVC felépítés**
  - `model.py`: Matematikai számítások, spline és felületgenerálás.
  - `view.py`: Tkinter alapú GUI és PyVista 3D vizualizáció.
  - `controller.py`: Az adatáramlás kezelése a Model és View között.

- **Spline generálás**
  - Catmull-Rom görbék vezérlőpontok alapján.

- **3D forgási felület**
  - A spline Y-tengely körüli forgatásával.

- **Matematikai számítások**
  - Ívhossz, felszín, térfogat, görbület és normálvektorok.

- **Interaktív GUI**
  - Paraméterek állítása: pontszám (spline felbontás) és szögfelbontás (forgatás).

- **Vizualizáció**
  - A generált felület színezése görbületi értékek alapján.
  - Normálvektorok megjelenítése a görbén.

## 📂 Fájlstruktúra

```
.gitignore
controller.py
main.py
model.py
readme.md
view.py
__pycache__/
```

### Fájlok leírása

- **`main.py`**: A program belépési pontja. Inicializálja az MVC komponenseket és elindítja a Tkinter GUI-t.
- **`model.py`**: A spline és a forgási felület matematikai modelljét tartalmazza.
- **`view.py`**: A felhasználói felületet és a PyVista alapú 3D vizualizációt kezeli.
- **`controller.py`**: Összeköti a modellt és a nézetet, valamint kezeli a felhasználói interakciókat.

## 🖥️ Használat

1. **Követelmények telepítése**:
   Telepítsd a szükséges csomagokat a következő paranccsal:
   ```bash
   pip install numpy pyvista
   ```

2. **A program futtatása**:
   Futtasd a `main.py` fájlt:
   ```bash
   python main.py
   ```

3. **Interaktív GUI**:
   - Állítsd be a spline felbontását (pontok száma) és a forgási felbontást (szögek száma).
   - Kattints a "Generate" gombra a 3D felület generálásához és megjelenítéséhez.

## 📊 Matematikai Számítások

- **Ívhossz**: A spline teljes hosszának kiszámítása.
- **Felszín**: A forgási felület teljes felszínének kiszámítása.
- **Térfogat**: A forgási felület által bezárt térfogat kiszámítása.
- **Görbület**: A spline görbületi értékeinek meghatározása.
- **Normálvektorok**: A spline mentén számított normálvektorok.

## 📚 Függőségek

- **Python 3.10+**
- **Könyvtárak**:
  - `numpy`: Matematikai számításokhoz.
  - `pyvista`: 3D vizualizációhoz.
  - `tkinter`: GUI létrehozásához.

## 🛠️ Fejlesztési Lehetőségek

- További spline típusok támogatása.
- Egyéni vezérlőpontok interaktív megadása.
- További vizualizációs lehetőségek, például árnyékolás és textúrázás.

## 📜 Licenc

Ez a projekt szabadon használható és módosítható a [MIT Licenc](https://opensource.org/licenses/MIT) feltételei szerint.