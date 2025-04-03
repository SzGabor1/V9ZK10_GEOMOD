# Naprendszer szimuláció

## Leírás
Ez a program egy 3D-s naprendszer szimulációt valósít meg, amelyben a Nap, a bolygók, a Hold és véletlenszerű meteoritok is megjelennek. A szimuláció OpenGL-t használ a grafikus megjelenítéshez, és a Pygame könyvtárat a felhasználói interakciók kezelésére.

## Funkciók
- **Nap és bolygók**: A Nap és a bolygók forgása és keringése a valósághoz hasonlóan van szimulálva.
- **Hold**: A Hold kering az Föld körül.
- **Meteoritok**: Véletlenszerű meteoritok mozognak a naprendszerben.
- **Kameravezérlés**: A felhasználó szabadon mozoghat a kamerával a szimuláció felfedezéséhez.

## Használati utasítás
1. **Futtatás**:
   - Győződj meg róla, hogy a Python telepítve van a gépeden.
   - Telepítsd a szükséges csomagokat:
     ```bash
     pip install pygame PyOpenGL pillow
     ```
   - Futtasd a programot:
     ```bash
     python main.py
     ```

2. **Kameravezérlés**:
   - **W**: Előre mozgás
   - **S**: Hátra mozgás
   - **A**: Balra mozgás
   - **D**: Jobbra mozgás
   - **Q**: Felfelé mozgás
   - **E**: Lefelé mozgás
   - Egér mozgatása: Kamera forgatása

3. **Kilépés**:
   - Nyomd meg az `ESC` billentyűt a kilépéshez.

## Főbb jellemzők
- **Nap**:
  - A Nap a szimuláció középpontjában helyezkedik el, és fényforrásként működik.
  - Teljesen megvilágított, hogy kiemelkedjen a szimulációban.

- **Bolygók**:
  - Minden bolygó saját textúrával, mérettel és forgási sebességgel rendelkezik.
  - A bolygók a Nap körül keringenek.

- **Hold**:
  - A Hold az Föld körül kering, és saját textúrával rendelkezik.

- **Meteoritok**:
  - Véletlenszerűen generált meteoritok mozognak a naprendszerben.
  - A meteoritok tüzes hatással jelennek meg. (Ezek valójában inkább csillagoknak néznek ki)


## Követelmények
- Python 3.8 vagy újabb
- Telepített csomagok:
  - `pygame`
  - `PyOpenGL`
  - `Pillow`

## Fájlstruktúra
- `main.py` A program fő fájlja, amely tartalmazza a szimuláció logikáját.
- `textures` A bolygók és a Hold textúrái (pl. `sun.jpg`, `earth.jpg`, stb.).

## Továbbfejlesztési lehetőségek
- Több hold hozzáadása más bolygókhoz.
- Felhasználói interfész a szimuláció vezérléséhez.

## Készítette
Ez a program egy oktatási célú projekt, amely a 3D grafika és a fizikai szimuláció alapjait mutatja be Pythonban.