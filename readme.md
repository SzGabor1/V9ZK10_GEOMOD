# Catmull-Rom Görbe és Forgási Felület Generátor

Ez a Python projekt egy **Catmull-Rom spline** alapú görbét generál, amelyet az Y-tengely körül forgatva 3D felületet hoz létre. Az alkalmazás interaktív grafikus felhasználói felülettel rendelkezik, amely lehetővé teszi a görbe és a felület paramétereinek testreszabását. A felület vizualizációja **PyVista** segítségével történik.

## Fő Funkciók

- **Catmull-Rom spline generálás**: Sima, folytonos görbék generálása megadott vezérlőpontok alapján.
- **Forgási felület létrehozása**: A görbét az Y-tengely körül forgatva 3D felületet hoz létre.
- **Matematikai elemzés**: Ívhossz, felszín és térfogat számítása, valamint görbület megjelenítése.
- **Interaktív vizualizáció**: A görbe és a felület megjelenítése PyVista segítségével, színezés görbület alapján.
- **Felhasználói felület**: Egyszerű Tkinter-alapú GUI, amely lehetővé teszi a spline felbontásának és a forgási szögek számának beállítását.

## Követelmények

A projekt futtatásához a következő csomagok szükségesek:

```bash
pip install numpy pyvista tkinter
```

## Használati Útmutató

### 1. Vezérlőpontok Megadása
A vezérlőpontokat a `control_points` változóban adhatod meg a kódban. Példa:

```python
control_points = np.array([
    [0, 0],
    [1, 2],
    [2, 3],
    [3, 5],
    [4, 4],
    [5, 2]
])
```

### 2. Paraméterek Beállítása
Az alkalmazás indítása után a következő paramétereket állíthatod be a grafikus felületen:
- **Spline felbontás (pontok száma)**: A görbe generálásához használt interpolációs pontok száma.
- **Forgási felbontás (szögek száma)**: A forgási felület generálásához használt szögfelbontás.

### 3. Görbe és Felület Generálása
Kattints a **"Generate"** gombra a görbe és a forgási felület generálásához és megjelenítéséhez.

## Matematikai Háttér

### Catmull-Rom spline
A Catmull-Rom spline egy interpolációs görbe, amely a megadott vezérlőpontokon halad át. A görbe folytonos és differenciálható, így ideális interpolációs feladatokhoz.

### Forgási Felület
A görbét az Y-tengely körül forgatva egy 3D felületet hozunk létre. A forgási felület pontjai a következőképpen számíthatók:
- Egy adott szögben a görbe minden pontját elforgatjuk az Y-tengely körül.

### Felszín és Térfogat Számítása
- **Felszín**: A görbe mentén numerikus integrációval számítjuk ki a forgási felület felszínét.
  \[
  A = 2 \pi \int y \, ds
  \]
- **Térfogat**: A forgási felület térfogata szintén numerikus integrációval számítható.
  \[
  V = \pi \int y^2 \, ds
  \]
