# Vstupní úloha pro Python víkend

## Úkol
Úkolem bylo nalézt navazující letecká spojení z daného seznamu letů.

## Omezení
* Nutno nalézt minimálně dvě na sebe navazující spojení
* V nalezené "cestě" není možno opakovat spojení A->B víc než jednou
	* A->B->A je v pořádku
	* A->B->A->B není v pořádku, spojení A->B je zde vícekrát
* Ne všechny lety dovolují požadovaný počet zavazadel
* Na přestup mezi lety je vždy třeba 1-4 hodiny

## Řešení
Zadání jsem vyřešil pomocí vhodně rozvržených datových struktur a pomocí algoritmu hledání do šířky.
Řešení je realizováno pomocí Pythonu 3.5.2
