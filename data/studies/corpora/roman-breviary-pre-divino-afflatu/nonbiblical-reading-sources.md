# Nichtbiblische Lesungen mit Quellenangabe im römischen Brevier vor Divino afflatu

Erstellt am 2026-07-22 aus `sources/divinum-officium/web/www/horas/Latin`.

## Abgrenzung und Methode

- Ausgewertet wurden die römischen Basisordner `Tempora`, `Sancti` und `Commune`.
- Das Sanctorale wurde auf die in `Tabulae/Kalendaria/1906.txt` sichtbare Kalenderstufe eingegrenzt, kumulativ über `1570 → 1888 → 1906`.
- Nicht ausgewertet wurden Ordensfassungen, lokale Anhänge (`aliquibus locis`, `Urbis`) und Votivanhänge.
- Gezählt werden nur Matutin-Lesungen `[Lectio...]`, in denen eine nichtbiblische Quellenzeile `!…` ausdrücklich steht.
- Biblische Quellenzeilen, etwa `!2 Reg 12:1-4` oder `!Marc 8:1-9`, wurden ausgeschlossen; bei Evangelienhomilien wurde die nachfolgende patristische Quellenzeile gezählt.
- `Quellenblöcke` meint eine ausdrücklich genannte Quellenangabe; `Lesungen` zählt den daraus erschlossenen Brevierumfang, also etwa `Lectio7-9` als drei Lesungen.
- Erkennbar spätere DO-Textschichten, besonders Quellen aus Pius XI/Pius XII oder nach 1906 entstandene universale Feste, wurden aus der Hauptstatistik ausgeschlossen und separat protokolliert.
- Die Rubriken-/Versionslogik von Divinum Officium wurde nicht vollständig als Kalenderlauf simuliert. Der Befund ist daher eine quellennahe, aber noch manuell kontrollbedürftige Bestandsaufnahme des 1906-nahen römischen Textbestands.

## Gesamtstatistik

- Quellenblöcke mit expliziter nichtbiblischer Quelle: **532**
- Daraus erschlossene Einzel-Lesungen: **1178**
- Autoren/Autorzeilen nach Normalisierung: **28**
- Autor-Werk-Gruppen nach Normalisierung: **180**
- Detaildaten: `data/studies/corpora/roman-breviary-pre-divino-afflatu/nonbiblical-reading-sources.csv` und `data/studies/corpora/roman-breviary-pre-divino-afflatu/nonbiblical-reading-sources.json`
- Ausgeschlossene Quellenzeilen: `data/studies/corpora/roman-breviary-pre-divino-afflatu/excluded-source-lines.csv`
- Grafiken: `data/studies/corpora/roman-breviary-pre-divino-afflatu/assets/authors.svg` und `data/studies/corpora/roman-breviary-pre-divino-afflatu/assets/works.svg`

### Nach Korpus

| Korpus | Quellenblöcke | Lesungen |
|---|---:|---:|
| Commune | 74 | 158 |
| Sancti | 215 | 452 |
| Tempora | 243 | 568 |

### Ausgeschlossene Quellenzeilen

| Grund | Zahl |
|---|---:|
| Kommemorationsmarker, keine eigentliche Werkquelle | 6 |
| post-1906-Textschicht in DO | 5 |

### Häufigste Autoren

| Autor | Quellenblöcke | Lesungen |
|---|---:|---:|
| Augustinus Hipponensis | 137 | 315 |
| Gregorius Magnus | 84 | 202 |
| Ambrosius Mediolanensis | 69 | 145 |
| Ioannes Chrysostomus | 44 | 104 |
| Hieronymus Stridonensis | 39 | 82 |
| Leo Magnus | 31 | 66 |
| Bernardus Claraevallensis | 23 | 50 |
| Beda Venerabilis | 19 | 44 |
| Hilarius Pictaviensis | 13 | 33 |
| Unklarer Autor | 19 | 23 |
| Maximus Taurinensis | 7 | 15 |
| Cyrillus Alexandrinus | 6 | 15 |
| Cyprianus Carthaginiensis | 5 | 14 |
| Athanasius Alexandrinus | 5 | 11 |
| Basilius Magnus | 4 | 10 |
| Ioannes Damascenus | 6 | 8 |
| Petrus Chrysologus | 2 | 6 |
| Bonaventura | 4 | 6 |
| Thomas Aquinas | 2 | 6 |
| Fulgentius Ruspensis | 3 | 5 |
| Epiphanius Salaminensis | 2 | 5 |
| Sophronius Hierosolymitanus | 2 | 4 |
| Felix IV Papa | 1 | 2 |
| sancti Germáni Epíscopi | 1 | 2 |
| Tarasius Constantinopolitanus | 1 | 2 |
| Irenaeus Lugdunensis | 1 | 1 |
| sancti Lauréntii Justiniáni Epíscopi | 1 | 1 |
| Petrus Canisius | 1 | 1 |

### Häufigste Werke

| Autor und Werk | Quellenblöcke | Lesungen |
|---|---:|---:|
| Gregorius Magnus — Homiliae in Evangelia | 49 | 125 |
| Augustinus Hipponensis — Tractatus in Iohannis Evangelium | 50 | 123 |
| Augustinus Hipponensis — Sermones | 51 | 110 |
| Ambrosius Mediolanensis — Expositio evangelii secundum Lucam | 40 | 89 |
| Leo Magnus — Sermones | 28 | 61 |
| Hieronymus Stridonensis — Commentarii in Matthaeum | 26 | 58 |
| Ioannes Chrysostomus — Homiliae in Matthaeum | 17 | 45 |
| Ioannes Chrysostomus — Sermones | 19 | 43 |
| Bernardus Claraevallensis — Sermones | 18 | 35 |
| Gregorius Magnus — Homiliae | 6 | 17 |
| Augustinus Hipponensis — Sermones de verbis Domini | 7 | 17 |
| Beda Venerabilis — Expositio in Lucam / homiliae de tempore | 7 | 15 |
| Maximus Taurinensis — Sermones | 7 | 15 |
| Gregorius Magnus — Ex eadem Homilía 29 | 5 | 13 |
| Ambrosius Mediolanensis — Sermones | 8 | 12 |
| Basilius Magnus — Sermones | 3 | 9 |
| Gregorius Magnus — Moralia in Iob | 3 | 8 |
| Gregorius Magnus — Sermones | 4 | 8 |
| Ioannes Chrysostomus — Homiliae | 3 | 8 |
| Cyrillus Alexandrinus — Sermones | 3 | 8 |
| Beda Venerabilis — Sermones | 4 | 7 |
| Augustinus Hipponensis — Enarrationes in Psalmos | 3 | 7 |
| Petrus Chrysologus — Sermones | 2 | 6 |
| Ioannes Damascenus — Sermones | 4 | 6 |
| Bernardus Claraevallensis — Sermones super Cantica canticorum | 2 | 6 |
| Augustinus Hipponensis — Liber 2 de Consensu Evang. | 2 | 6 |
| Thomas Aquinas — Sermones | 2 | 6 |
| Athanasius Alexandrinus — Sermones | 2 | 5 |
| Fulgentius Ruspensis — Sermones | 2 | 4 |
| Ambrosius Mediolanensis — Liber 1, post initium | 2 | 4 |
| Augustinus Hipponensis — Cap. 6-7 | 2 | 4 |
| Sophronius Hierosolymitanus — Homilia in Deiparæ Annunt. | 2 | 4 |
| Beda Venerabilis — Homilia in Natali S. Benedicti Ep. | 1 | 3 |
| Hilarius Pictaviensis — Comment. in Matthaeum, can. 10 post medium | 1 | 3 |
| Augustinus Hipponensis — Tract. 81 in Joan., sub med. | 1 | 3 |
| Beda Venerabilis — In Natali S. Benedicti | 1 | 3 |
| Cyprianus Carthaginiensis — Lib. de hab. Virg. n. 3-5 | 1 | 3 |
| Ambrosius Mediolanensis — Prope finem | 1 | 3 |
| Unklarer Autor — In Psalm. 121 | 1 | 3 |
| Beda Venerabilis — Paulo post prædicta | 1 | 3 |

## Vollständige Übersicht nach Autor und Werk

| Autor | Werk | Quellenblöcke | Lesungen | Quellenvarianten | Belege |
|---|---|---:|---:|---|---|
| Ambrosius Mediolanensis | Apologia David | 1 | 1 | Apolog. 1, c. 2 (1x) | `Tempora/Pent06-0.txt:65` |
| Ambrosius Mediolanensis | Cap. 1. | 1 | 2 | Cap. 1. (1x) | `Tempora/Quad3-0.txt:88` |
| Ambrosius Mediolanensis | Cap. 4. circa med. | 1 | 3 | Cap. 4. circa med. (1x) | `Tempora/Quadp2-0.txt:76` |
| Ambrosius Mediolanensis | Epist. 81, alias 7, circa medium | 1 | 1 | Epist. 81, alias 7, circa medium (1x) | `Commune/C10.txt:159` |
| Ambrosius Mediolanensis | Epist. 81, alias 7, post initium | 1 | 1 | Epist. 81, alias 7, post initium (1x) | `Commune/C10.txt:123` |
| Ambrosius Mediolanensis | Expositio evangelii secundum Lucam | 40 | 89 | Expositio in Luc. lib. 3 (2x); Lib. 5. in Lucam. Cap. 6., post init. (1x); Lib. 8. in Lucam. (1x); Lib. 8 in Luc., prope finem (1x); Lib. 8 in Luc., in fine (1x); Ex Lib. 8 in Luc., prope finem (1x); … | `Commune/C3.txt:373`; `Commune/C5.txt:328`; `Commune/C8.txt:230`; `Commune/C8.txt:415`; `Commune/C8.txt:441`; `Sancti/01-01.txt:109`; … |
| Ambrosius Mediolanensis | Lectio iv, Cap. 9 | 1 | 3 | Lectio iv, Cap. 9 (1x) | `Tempora/094-0.txt:51` |
| Ambrosius Mediolanensis | Lectio iv, Liber 3, Cap. 15 | 1 | 1 | Lectio iv, Liber 3, Cap. 15 (1x) | `Tempora/095-0.txt:45` |
| Ambrosius Mediolanensis | Lib. 1, cap. 18 | 1 | 1 | Lib. 1, cap. 18 (1x) | `Commune/C10.txt:195` |
| Ambrosius Mediolanensis | Lib. 1, Cap. 40 | 1 | 3 | Lib. 1, Cap. 40 (1x) | `Tempora/101-0.txt:58` |
| Ambrosius Mediolanensis | Lib. 1. Cap. 28 et 29 | 1 | 3 | Lib. 1. Cap. 28 et 29 (1x) | `Tempora/083-0.txt:47` |
| Ambrosius Mediolanensis | Lib. 1. cap. 41 | 1 | 3 | Lib. 1. cap. 41 (1x) | `Tempora/103-0.txt:48` |
| Ambrosius Mediolanensis | Lib. 1., cap. 41., in medio. | 1 | 1 | Lib. 1., cap. 41., in medio. (1x) | `Sancti/08-13oct.txt:13` |
| Ambrosius Mediolanensis | Lib. 3 post initium. | 1 | 3 | Lib. 3 post initium. (1x) | `Sancti/08-29.txt:75` |
| Ambrosius Mediolanensis | Lib. 4, Cap. 4 | 1 | 1 | Lib. 4, Cap. 4 (1x) | `Tempora/Pent02-3.txt:53` |
| Ambrosius Mediolanensis | Lib. 5 de Fide ad Gratianum, cap. 2, post initium | 1 | 3 | Lib. 5 de Fide ad Gratianum, cap. 2, post initium (1x) | `Tempora/Quad2-3.txt:17` |
| Ambrosius Mediolanensis | Liber 1, cap 2 | 1 | 3 | Liber 1, cap 2 (1x) | `Tempora/Quadp3-0.txt:79` |
| Ambrosius Mediolanensis | Liber 1, post initium | 2 | 4 | Liber 1, post initium (2x) | `Sancti/01-21.txt:63`; `Sancti/01-21.txt:94` |
| Ambrosius Mediolanensis | Liber 2, post initium. | 1 | 1 | Liber 2, post initium. (1x) | `Sancti/11-21.txt:35` |
| Ambrosius Mediolanensis | Post medium | 1 | 3 | Post medium (1x) | `Tempora/Pasc5-0.txt:63` |
| Ambrosius Mediolanensis | Prope finem | 1 | 3 | Prope finem (1x) | `Commune/C7.txt:80` |
| Ambrosius Mediolanensis | Sermones | 8 | 12 | Sermo 21, n. 7 et 8 (1x); Serm. 22 (1x); Lib. 1 de Virg., circa init. (1x); Sermo 22. (1x); Serm. 22. (1x); Lectio v. Serm. 21. (1x); … | `Commune/C2.txt:299`; `Commune/C2p.txt:52`; `Commune/C6.txt:183`; `Sancti/04-22.txt:27`; `Sancti/04-26.txt:28`; `Sancti/07-13.txt:23`; … |
| Athanasius Alexandrinus | In Apologia de fuga sua, ante med. | 1 | 2 | In Apologia de fuga sua, ante med. (1x) | `Sancti/03-18.txt:37` |
| Athanasius Alexandrinus | In Apologia de fuga sua, ante medium | 1 | 1 | In Apologia de fuga sua, ante medium (1x) | `Sancti/05-02.txt:47` |
| Athanasius Alexandrinus | Liber de Virginitate, post initium. | 1 | 3 | Liber de Virginitate, post initium. (1x) | `Tempora/113-0.txt:46` |
| Athanasius Alexandrinus | Sermones | 2 | 5 | De Assumptione? (1x); Orat. 2 contra Ariános, post medium. (1x) | `Sancti/08-15t.txt:124`; `Tempora/Epi6-0.txt:50` |
| Augustinus Hipponensis | ... | 1 | 3 | ... (1x) | `Sancti/08-16bmv.txt:66` |
| Augustinus Hipponensis | Ante medium | 1 | 2 | Ante medium (1x) | `Commune/C1.txt:334` |
| Augustinus Hipponensis | Cap 25, 26 et 27 tomi 3 | 1 | 3 | Cap 25, 26 et 27 tomi 3 (1x) | `Tempora/Quadp1-0.txt:86` |
| Augustinus Hipponensis | Cap. 10, tom. 4; post init. | 1 | 3 | Cap. 10, tom. 4; post init. (1x) | `Tempora/Quad2-0.txt:85` |
| Augustinus Hipponensis | Cap. 6-7 | 2 | 4 | Cap. 6-7 (2x) | `Sancti/06-30.txt:128`; `Sancti/06-30.txt:159` |
| Augustinus Hipponensis | Enarrationes in Psalmos | 3 | 7 | In Psalmum 54 ad 1 versum (1x); In Psalm 63 ad versum 2 (1x); In Psalmum 63 versum 7 (1x) | `Tempora/Quad6-4.txt:116`; `Tempora/Quad6-5.txt:109`; `Tempora/Quad6-6.txt:105` |
| Augustinus Hipponensis | Epist. 13, ante medium | 1 | 1 | Epist. 13, ante medium (1x) | `Commune/C10.txt:171` |
| Augustinus Hipponensis | Inter Opera Augustini, tom. 3 | 1 | 1 | Inter Opera Augustini, tom. 3 (1x) | `Tempora/Pent01-0.txt:193` |
| Augustinus Hipponensis | Lib. 2 de Consensu Evangelist. cap. 20, tom. 4 | 1 | 2 | Lib. 2 de Consensu Evangelist. cap. 20, tom. 4 (1x) | `Tempora/Quadp3-4.txt:20` |
| Augustinus Hipponensis | Lib. 2 quæst. Evang. cap. 40 | 1 | 1 | Lib. 2 quæst. Evang. cap. 40 (1x) | `Tempora/Pent13-0.txt:23` |
| Augustinus Hipponensis | Lib. 2. de consensu Evangelist. Cap. 1. | 1 | 2 | Lib. 2. de consensu Evangelist. Cap. 1. (1x) | `Sancti/09-13bmv.txt:35` |
| Augustinus Hipponensis | Lib. 4. cap. 1. tom. 9. | 1 | 1 | Lib. 4. cap. 1. tom. 9. (1x) | `Tempora/Pasc6-6.txt:79` |
| Augustinus Hipponensis | Lib. de fide et operibus. cap. 15 tom. 4, circa medium | 1 | 3 | Lib. de fide et operibus. cap. 15 tom. 4, circa medium (1x) | `Tempora/Quad1-1.txt:17` |
| Augustinus Hipponensis | Liber 17. cap. 8. sub medio. | 1 | 3 | Liber 17. cap. 8. sub medio. (1x) | `Tempora/Pent08-0.txt:63` |
| Augustinus Hipponensis | Liber 18, cap. 28. | 1 | 3 | Liber 18, cap. 28. (1x) | `Tempora/114-0.txt:42` |
| Augustinus Hipponensis | Liber 18, cap. 45 | 1 | 3 | Liber 18, cap. 45 (1x) | `Tempora/102-0.txt:44` |
| Augustinus Hipponensis | Liber 2 de Consensu Evang. | 2 | 6 | Liber 2 de Consensu Evang. (2x) | `Tempora/Pasc2-3.txt:152`; `Tempora/Pasc2-4.txt:68` |
| Augustinus Hipponensis | Liber 22, cap. 8, circa medium | 1 | 1 | Liber 22, cap. 8, circa medium (1x) | `Sancti/08-03.txt:75` |
| Augustinus Hipponensis | Liber 23 contra Faust. cap. 7-8 | 1 | 1 | Liber 23 contra Faust. cap. 7-8 (1x) | `Tempora/Pasc2-5.txt:62` |
| Augustinus Hipponensis | Liber 50 Homilía 23, tom. 10 | 1 | 1 | Liber 50 Homilía 23, tom. 10 (1x) | `Sancti/07-22.txt:179` |
| Augustinus Hipponensis | Liber Quæst. Evang. in Matth. cap. 11, tom. 4 | 1 | 3 | Liber Quæst. Evang. in Matth. cap. 11, tom. 4 (1x) | `Tempora/Epi5-0.txt:76` |
| Augustinus Hipponensis | Præfátio tom. 4 | 1 | 3 | Præfátio tom. 4 (1x) | `Tempora/Epi3-0.txt:50` |
| Augustinus Hipponensis | Sermones | 51 | 110 | Ex Serm. 256. de Tempore. (3x); Sermo 44 de Sanctis (1x); Serm. 47. de Sanctis. (1x); Lib. 1 de Sermone Domini in monte, cap. 6 (1x); Sermo 252 de Tempore (1x); Serm. 256. de Tempore. (1x); … | `Commune/C2.txt:143`; `Commune/C3.txt:199`; `Commune/C4a.txt:66`; `Commune/C8.txt:195`; `Commune/C8.txt:426`; `Commune/C8.txt:452`; … |
| Augustinus Hipponensis | Sermones de verbis Domini | 7 | 17 | Sermo 10 de verbis Domini (1x); Sermo 44 de Verbis Dómini, circa initium (1x); Sermo 20 de Verbis Domini (1x); Serm. 15. in Evang. Matthǽi de Verbis Dómini, post inítium (1x); Sermo 36 de Verbis Domini, circa medium (1x); Sermo 44 de verbis Domini, circa initium (1x); … | `Sancti/02-24.txt:61`; `Sancti/05-04.txt:43`; `Sancti/07-29.txt:37`; `Tempora/Pent01-0.txt:261`; `Tempora/Pent10-0.txt:84`; `Tempora/Pent15-0.txt:23`; … |
| Augustinus Hipponensis | Tract. 81 in Joan., sub med. | 1 | 3 | Tract. 81 in Joan., sub med. (1x) | `Commune/C2p.txt:120` |
| Augustinus Hipponensis | Tractatus 27. in fine. | 1 | 2 | Tractatus 27. in fine. (1x) | `Sancti/08-17t.txt:21` |
| Augustinus Hipponensis | Tractatus 36 | 1 | 3 | Tractatus 36 (1x) | `Sancti/01-03.txt:49` |
| Augustinus Hipponensis | Tractatus in Iohannis Evangelium | 50 | 123 | Tract. 80 in Joannem (1x); Tract. 6 in Joann., ante med. (1x); Tract. 51 in Joánn., sub med. (1x); Tract. 67 in Joannem (1x); Tract. 11 in Joann., post init. (1x); Tractatus 123 in Joannem, in medio (1x); … | `Commune/C2p.txt:81`; `Sancti/01-13.txt:58`; `Sancti/02-01.txt:41`; `Sancti/05-01.txt:54`; `Sancti/05-03.txt:154`; `Sancti/06-28r.txt:26`; … |
| Basilius Magnus | Lib. Regul. fusius explic. ad interrog. 8 | 1 | 1 | Lib. Regul. fusius explic. ad interrog. 8 (1x) | `Sancti/06-14.txt:43` |
| Basilius Magnus | Sermones | 3 | 9 | Homilia 2 in Psalm. 28 (1x); Homilia in Ps. 33, n. 8 (1x); Homilia 1 de jejúnio, ante med. (1x) | `Sancti/06-27oct.txt:14`; `Tempora/115-0.txt:40`; `Tempora/Quad4-0.txt:71` |
| Beda Venerabilis | Expositio in Lucam / homiliae de tempore | 7 | 15 | Lib. 5. Cap. 77. in Luc. 19 (2x); Lib 4. cap. 49. in Luc. 11. (1x); Lib. 4, Cap. 54, in Luc. 12 (1x); Lib. 4 in Lucam, cap. 12 (1x); Liber 3, cap. 43 in Lucæ 10 (1x); Lib. 4, cap. 48, in cap. 11 Lucæ (1x) | `Commune/C11.txt:223`; `Commune/C5.txt:312`; `Commune/C8.txt:493`; `Commune/C8.txt:519`; `Sancti/06-26.txt:79`; `Tempora/Pent12-0.txt:23`; … |
| Beda Venerabilis | Homilia in Natali S. Benedicti Ep. | 1 | 3 | Homilia in Natali S. Benedicti Ep. (1x) | `Commune/C1.txt:349` |
| Beda Venerabilis | Homiliae | 1 | 2 | Homil. 7 in Quadrag. tom. 7 (1x) | `Tempora/Quad1-2.txt:17` |
| Beda Venerabilis | In Evang. Vos estis sal terra | 1 | 2 | In Evang. Vos estis sal terra (1x) | `Sancti/05-27.txt:47` |
| Beda Venerabilis | In Natali S. Benedicti | 1 | 3 | In Natali S. Benedicti (1x) | `Commune/C4.txt:386` |
| Beda Venerabilis | Lib. 2, cap. 28 in cap. 6 Marci, tom. 4 | 1 | 3 | Lib. 2, cap. 28 in cap. 6 Marci, tom. 4 (1x) | `Tempora/Quadp3-6.txt:20` |
| Beda Venerabilis | Liber 3 Comment. in Marc. cap. 11 | 1 | 3 | Liber 3 Comment. in Marc. cap. 11 (1x) | `Sancti/11-17.txt:39` |
| Beda Venerabilis | Liber 3, cap. 38 in Marcum 9 | 1 | 3 | Liber 3, cap. 38 in Marcum 9 (1x) | `Tempora/093-3.txt:22` |
| Beda Venerabilis | Paulo post prædicta | 1 | 3 | Paulo post prædicta (1x) | `Commune/C8.txt:545` |
| Beda Venerabilis | Sermones | 4 | 7 | Sermo 18 de Sanctis (1x); Ex Sermone 18. de Sanctis. (1x); Sermo 18 de Sanctis. (1x); Ex Sermone 18 de Sanctis (1x) | `Sancti/11-01.txt:194`; `Sancti/11-02oct.txt:17`; `Sancti/11-03oct.txt:16`; `Sancti/11-05oct.txt:15` |
| Bernardus Claraevallensis | Ex Homilía 2 super Missus | 1 | 3 | Ex Homilía 2 super Missus (1x) | `Sancti/12-10bmv.txt:31` |
| Bernardus Claraevallensis | Homilia sancti Bernardíni Senénsis | 1 | 3 | Homilia sancti Bernardíni Senénsis (1x) | `Tempora/Pent03-2.txt:52` |
| Bernardus Claraevallensis | Homiliae | 1 | 3 | Homilia 1 super Missus est, n. 7-8 (1x) | `Tempora/Epi1-0.txt:246` |
| Bernardus Claraevallensis | Sermones | 18 | 35 | Homilia 2 super Missus est (2x); De Verbis Apocalypsis cap. 12, Signum magnum (1x); Serm. in cap. 12 Apoc., ante med. (1x); In Dom. infra Oct. Assumpt. B. Mariæ Virg. (1x); Homil. 2 super Missus est, prope finem (1x); Serm. 1. de Assumpt. B. M. V. (1x); … | `Commune/C10.txt:153`; `Commune/C10.txt:177`; `Commune/C10.txt:183`; `Sancti/03-19.txt:160`; `Sancti/08-19bmv.txt:57`; `Sancti/08-21bmv.txt:52`; … |
| Bernardus Claraevallensis | Sermones super Cantica canticorum | 2 | 6 | Sermo 15 super Cantica, circa medium (1x); Sermo 61 in Cantica Canticorum, nn. 3-5 (1x) | `Tempora/Nat2-0.txt:173`; `Tempora/Pent03-5.txt:35` |
| Bonaventura | Expositio in cap. 9 Lucæ | 1 | 1 | Expositio in cap. 9 Lucæ (1x) | `Sancti/03-28.txt:30` |
| Bonaventura | Legenda S. Francisci cap. 13 | 1 | 3 | Legenda S. Francisci cap. 13 (1x) | `Sancti/09-17.txt:59` |
| Bonaventura | Liber de ligno vitæ, num. 30 | 1 | 1 | Liber de ligno vitæ, num. 30 (1x) | `Tempora/Pent02-5.txt:224` |
| Bonaventura | Liber de ligno Vitæ. | 1 | 1 | Liber de ligno Vitæ. (1x) | `Tempora/Pent02-5o.txt:164` |
| Cyprianus Carthaginiensis | In fine. | 1 | 3 | In fine. (1x) | `Sancti/11-08.txt:18` |
| Cyprianus Carthaginiensis | Lib. 2. Epist. 6. | 1 | 2 | Lib. 2. Epist. 6. (1x) | `Commune/C2p.txt:105` |
| Cyprianus Carthaginiensis | Lib. de hab. Virg. n. 3-5 | 1 | 3 | Lib. de hab. Virg. n. 3-5 (1x) | `Commune/C6.txt:347` |
| Cyprianus Carthaginiensis | Liber 2. Epistola 3. sub init. | 1 | 3 | Liber 2. Epistola 3. sub init. (1x) | `Tempora/Pent02-2.txt:54` |
| Cyprianus Carthaginiensis | Sermones | 1 | 3 | Sermone 3 initio. (1x) | `Tempora/Pasc4-0.txt:71` |
| Cyrillus Alexandrinus | Comm. in Joann. Lib. 12 Cap. 19 | 1 | 1 | Comm. in Joann. Lib. 12 Cap. 19 (1x) | `Tempora/Pent03-4.txt:54` |
| Cyrillus Alexandrinus | Lib. 4. in Joánnem, cap. 17. | 1 | 3 | Lib. 4. in Joánnem, cap. 17. (1x) | `Tempora/Pent02-4o.txt:30` |
| Cyrillus Alexandrinus | Liber 4 in Joánnem, cap. 17 | 1 | 3 | Liber 4 in Joánnem, cap. 17 (1x) | `Tempora/Pent02-4.txt:65` |
| Cyrillus Alexandrinus | Sermones | 3 | 8 | Homilia contra Nestorium. (1x); Catechesis mystagog. 4 (1x); Catechesi mystagog. 4. (1x) | `Sancti/09-15t.txt:27`; `Tempora/Pent02-4.txt:50`; `Tempora/Pent02-4o.txt:15` |
| Epiphanius Salaminensis | Lib. 3. hæresi 78. post medium. | 1 | 3 | Lib. 3. hæresi 78. post medium. (1x) | `Sancti/09-13bmv.txt:11` |
| Epiphanius Salaminensis | Oratio de laudibus S. Maríæ Deiparæ | 1 | 2 | Oratio de laudibus S. Maríæ Deiparæ (1x) | `Sancti/12-15.txt:41` |
| Felix IV Papa | De Consecr. dist. 1. cap. 2 | 1 | 2 | De Consecr. dist. 1. cap. 2 (1x) | `Commune/C8.txt:556` |
| Fulgentius Ruspensis | Ex libro 2. Officiorum ad S. Fulgentium cap. 5. | 1 | 1 | Ex libro 2. Officiorum ad S. Fulgentium cap. 5. (1x) | `Sancti/04-04.txt:36` |
| Fulgentius Ruspensis | Sermones | 2 | 4 | Ex Serm. 5 qui est de Epiphania, sub initium (1x); Sermo 3, de S. Stéphano, circa init. (1x) | `Sancti/01-11.txt:30`; `Sancti/12-26.txt:90` |
| Gregorius Magnus | Ex | 1 | 2 | Ex Homil. 28. habita in Basilica horum Ss. Mártyrum, in die natalis eorum (1x) | `Sancti/05-12.txt:36` |
| Gregorius Magnus | Ex eadem Homilía 29 | 5 | 13 | Ex eadem Homilía 29 (5x) | `Tempora/Pasc5-5.txt:71`; `Tempora/Pasc5-6.txt:74`; `Tempora/Pasc6-1.txt:75`; `Tempora/Pasc6-2.txt:77`; `Tempora/Pasc6-3.txt:69` |
| Gregorius Magnus | Ex eadem Homilía 29. | 1 | 3 | Ex eadem Homilía 29. (1x) | `Tempora/Pasc6-4.txt:81` |
| Gregorius Magnus | Ex Homilía 17 in Lucæ 10 ante med. | 1 | 3 | Ex Homilía 17 in Lucæ 10 ante med. (1x) | `Sancti/03-12.txt:53` |
| Gregorius Magnus | Homiliae | 6 | 17 | Homilia 3, Lib. 1 (1x); Homilia 32 in Evang. (1x); Homilia 13 in Evang. (1x); Homilia 10 in Evang. (1x); Homilia 17. in Evang. (1x); Homilia 26 in Evang., post med. (1x) | `Commune/C1a.txt:30`; `Commune/C2.txt:314`; `Commune/C5.txt:115`; `Sancti/01-06.txt:197`; `Sancti/05-28.txt:36`; `Sancti/12-21.txt:39` |
| Gregorius Magnus | Homiliae in Evangelia | 49 | 125 | Ex Homilía 10 in Evangelia (2x); Homilia 25 in Evangelia (2x); Homilia 29 in Evangelia, post initium (2x); Homilia 30 in Evangelia, post medium (1x); Homilia 17 in Evangelia (1x); Homilia 27. in Evangelia. (1x); … | `Commune/C1.txt:198`; `Commune/C1a.txt:45`; `Commune/C1v.txt:36`; `Commune/C2.txt:178`; `Commune/C3.txt:234`; `Commune/C4.txt:213`; … |
| Gregorius Magnus | Homiliae in Ezechielem | 1 | 1 | Homilia 10, liber 1 in Ezech., ante medium (1x) | `Tempora/Pent11-0.txt:79` |
| Gregorius Magnus | In 1 Reg. 1 | 1 | 1 | In 1 Reg. 1 (1x) | `Commune/C10.txt:165` |
| Gregorius Magnus | In Tractatu de fide, post init. | 1 | 2 | In Tractatu de fide, post init. (1x) | `Tempora/Pent01-0.txt:228` |
| Gregorius Magnus | Lectio iv, Lib. 2, Cap. 1 | 1 | 2 | Lectio iv, Lib. 2, Cap. 1 (1x) | `Tempora/091-0.txt:50` |
| Gregorius Magnus | Lib. 2, Cap. 33. | 1 | 2 | Lib. 2, Cap. 33. (1x) | `Sancti/02-10.txt:23` |
| Gregorius Magnus | Lib. 3 Cap. 31 | 1 | 3 | Lib. 3 Cap. 31 (1x) | `Sancti/04-13.txt:54` |
| Gregorius Magnus | Lib. 4, cap. 5 in I Reg. c. 10 | 1 | 1 | Lib. 4, cap. 5 in I Reg. c. 10 (1x) | `Tempora/Pent03-0o.txt:43` |
| Gregorius Magnus | Lib. 4. Cap. 30. | 1 | 3 | Lib. 4. Cap. 30. (1x) | `Tempora/Epi4-0.txt:54` |
| Gregorius Magnus | Lib. 9. cap. 11., n. 45 | 1 | 1 | Lib. 9. cap. 11., n. 45 (1x) | `Commune/C4a.txt:51` |
| Gregorius Magnus | Liber 1, Homilía 2. | 1 | 1 | Liber 1, Homilía 2. (1x) | `Tempora/111-0.txt:35` |
| Gregorius Magnus | Liber 2 Homiliar. Hom. 38, circa medium | 1 | 3 | Liber 2 Homiliar. Hom. 38, circa medium (1x) | `Sancti/09-18.txt:71` |
| Gregorius Magnus | Liber 3, cap. 31 | 1 | 1 | Liber 3, cap. 31 (1x) | `Sancti/04-13.txt:65` |
| Gregorius Magnus | Liber 4, Cap. 3 et 4 | 1 | 1 | Liber 4, Cap. 3 et 4 (1x) | `Tempora/Pent05-0.txt:64` |
| Gregorius Magnus | Liber 9, Cap. 2. | 1 | 1 | Liber 9, Cap. 2. (1x) | `Tempora/092-0.txt:45` |
| Gregorius Magnus | Moralia in Iob | 3 | 8 | Lib. 10. cap. 16. in cap. 12. Job. (1x); Lib. 27 in Moralium, cap. 27 post medium (1x); Liber 1, cap. 10 in cap. 1 Job (1x) | `Commune/C5.txt:296`; `Commune/C8.txt:467`; `Tempora/084-0.txt:46` |
| Gregorius Magnus | Sermones | 4 | 8 | Oratio in sancta Lumina (1x); Homil. 34 in Evang. ante medium (1x); Sermo 20 de Machabæis (1x); Oratio de Ascensione Domini (1x) | `Sancti/01-13.txt:43`; `Sancti/09-29.txt:41`; `Tempora/105-0.txt:44`; `Tempora/Pasc6-3.txt:54` |
| Hieronymus Stridonensis | Apologia ad Pammachium pro lib. adversus Jovinianum, in fine | 1 | 1 | Apologia ad Pammachium pro lib. adversus Jovinianum, in fine (1x) | `Commune/C10.txt:129` |
| Hieronymus Stridonensis | Cap. 16 | 1 | 3 | Cap. 16 (1x) | `Sancti/02-01.txt:22` |
| Hieronymus Stridonensis | Cap. 17 | 1 | 3 | Cap. 17 (1x) | `Sancti/01-26.txt:20` |
| Hieronymus Stridonensis | Cap. 67 | 1 | 1 | Cap. 67 (1x) | `Sancti/09-16.txt:24` |
| Hieronymus Stridonensis | Cap. 7 | 1 | 2 | Cap. 7 (1x) | `Sancti/10-18.txt:23` |
| Hieronymus Stridonensis | Commentarii in Matthaeum | 26 | 58 | Liber 1 Comment. in cap. 5 Matth. (2x); Lib. 3 Comm. in cap. 18 Matth. (2x); Liber 1 Comment. in cap. 8 Matth. (2x); Lib. 3. in Matth. cap. 19. (1x); Lib. 4. Comment. in cap. 23. Matth. (1x); Liber 1 in Comment. in cap. 2 Matthæi (1x); … | `Commune/C1.txt:233`; `Sancti/01-02.txt:70`; `Sancti/01-05.txt:55`; `Sancti/01-10.txt:46`; `Sancti/05-06.txt:52`; `Sancti/06-29.txt:178`; … |
| Hieronymus Stridonensis | De viris illustribus, cap 8 | 1 | 3 | De viris illustribus, cap 8 (1x) | `Sancti/04-25.txt:25` |
| Hieronymus Stridonensis | Epistulae | 1 | 1 | Epist. 2, tom. 1 (1x) | `Tempora/Pent07-0.txt:62` |
| Hieronymus Stridonensis | Lib. 11 in Isaíæ cap. 38 | 1 | 1 | Lib. 11 in Isaíæ cap. 38 (1x) | `Tempora/Pent11-0.txt:55` |
| Hieronymus Stridonensis | Lib. 13 in cap. 44 | 1 | 1 | Lib. 13 in cap. 44 (1x) | `Commune/C10.txt:141` |
| Hieronymus Stridonensis | Liber 1, n. 26 | 1 | 3 | Liber 1, n. 26 (1x) | `Sancti/05-06.txt:32` |
| Hieronymus Stridonensis | Liber 4. in cap. 11 Isaíæ. | 1 | 2 | Liber 4. in cap. 11 Isaíæ. (1x) | `Tempora/Adv2-0.txt:73` |
| Hieronymus Stridonensis | Liber 7 in Ezechiel. cap. 21. | 1 | 2 | Liber 7 in Ezechiel. cap. 21. (1x) | `Tempora/112-0.txt:40` |
| Hieronymus Stridonensis | Sermones | 1 | 1 | De Assumptione B. M. V. (1x) | `Sancti/12-08.txt:139` |
| Hilarius Pictaviensis | Comm. in Matthæum, cap. 4, n. 10 | 1 | 1 | Comm. in Matthæum, cap. 4, n. 10 (1x) | `Commune/C4a.txt:93` |
| Hilarius Pictaviensis | Comment in Matth. can. 18 | 1 | 3 | Comment in Matth. can. 18 (1x) | `Sancti/05-08.txt:214` |
| Hilarius Pictaviensis | Comment. in Matth. Can 26 | 1 | 1 | Comment. in Matth. Can 26 (1x) | `Commune/C4.txt:370` |
| Hilarius Pictaviensis | Comment. in Matth. can. 1. | 1 | 2 | Comment. in Matth. can. 1. (1x) | `Sancti/09-11bmv.txt:35` |
| Hilarius Pictaviensis | Comment. in Matth. can. 16, post initium | 1 | 2 | Comment. in Matth. can. 16, post initium (1x) | `Sancti/01-18.txt:82` |
| Hilarius Pictaviensis | Comment. in Matth. can. 18, post initium | 1 | 3 | Comment. in Matth. can. 18, post initium (1x) | `Sancti/10-02.txt:165` |
| Hilarius Pictaviensis | Comment. in Matth. can. 23 | 1 | 3 | Comment. in Matth. can. 23 (1x) | `Tempora/Pent22-0.txt:23` |
| Hilarius Pictaviensis | Comment. in Matth. can. 6 | 1 | 3 | Comment. in Matth. can. 6 (1x) | `Tempora/Pent07-0.txt:86` |
| Hilarius Pictaviensis | Comment. in Matth. cap. 25 | 1 | 3 | Comment. in Matth. cap. 25 (1x) | `Sancti/09-19.txt:41` |
| Hilarius Pictaviensis | Comment. in Matth., can. 10 | 1 | 3 | Comment. in Matth., can. 10 (1x) | `Sancti/09-28.txt:34` |
| Hilarius Pictaviensis | Comment. in Matthaei, cap. 1. | 1 | 3 | Comment. in Matthaei, cap. 1. (1x) | `Sancti/09-12bmv.txt:26` |
| Hilarius Pictaviensis | Comment. in Matthaeum, can. 10 post medium | 1 | 3 | Comment. in Matthaeum, can. 10 post medium (1x) | `Commune/C2.txt:339` |
| Hilarius Pictaviensis | Liber 8 de Trinitáte, ante medium | 1 | 3 | Liber 8 de Trinitáte, ante medium (1x) | `Tempora/Pent02-3.txt:68` |
| Ioannes Chrysostomus | Hom. 59 in Joánnem | 1 | 3 | Hom. 59 in Joánnem (1x) | `Sancti/11-14.txt:34` |
| Ioannes Chrysostomus | Hom. 84. | 1 | 1 | Hom. 84. (1x) | `Tempora/Pent02-5o.txt:151` |
| Ioannes Chrysostomus | Hom. 87. in Joann., circa med. | 1 | 2 | Hom. 87. in Joann., circa med. (1x) | `Sancti/01-03.txt:64` |
| Ioannes Chrysostomus | Homiliae | 3 | 8 | Homilia 65. in Joánnem, post med. (1x); Homilia 66. in Joánnem. (1x); Homilia 85, alias 84 in Joánnem, num. 3 (1x) | `Sancti/08-14oct.txt:37`; `Sancti/08-17t.txt:36`; `Tempora/Pent02-6.txt:60` |
| Ioannes Chrysostomus | Homiliae in Matthaeum | 17 | 45 | Homilia 72 in Matthæum (2x); Homilia 4 in Matth. (2x); Homilia 15 in Matthæum, sub medium (1x); Homilia 63 in Matth., sub med. (1x); Ex Hom. 33 in c. 9., Matth. (1x); Ex Hom. 8 in Matth., ante med. (1x); … | `Commune/C4a.txt:109`; `Commune/C6.txt:371`; `Commune/C8.txt:530`; `Sancti/01-04.txt:59`; `Sancti/03-08.txt:34`; `Sancti/04-14.txt:52`; … |
| Ioannes Chrysostomus | In Joann. c. 2 | 1 | 1 | In Joann. c. 2 Homilia 20, circa finem (1x) | `Sancti/08-14.txt:24` |
| Ioannes Chrysostomus | Liber de Virginitate | 1 | 1 | Liber de Virginitate (1x) | `Sancti/06-21.txt:36` |
| Ioannes Chrysostomus | Sermones | 19 | 43 | Apud Metaphrasten (2x); Sermo 1 de Martyribus, tom. 3. (2x); In Orat. de S. Philogonio (1x); Serm. 67. de diversis novi Testamenti locis. (1x); Apud Metaphr. mense Julio (1x); Sermo 32 in morali exhortat (1x); … | `Commune/C11.txt:188`; `Commune/C3.txt:358`; `Commune/C5.txt:80`; `Commune/C7.txt:162`; `Sancti/07-02.txt:86`; `Sancti/07-04oct.txt:25`; … |
| Ioannes Damascenus | Liber 4, Cap. 15 | 1 | 1 | Liber 4, Cap. 15 (1x) | `Sancti/11-21.txt:30` |
| Ioannes Damascenus | Oratio 3 de B.M.V. Nativ. | 1 | 1 | Oratio 3 de B.M.V. Nativ. (1x) | `Tempora/Pasc3-2.txt:66` |
| Ioannes Damascenus | Sermones | 4 | 6 | Oratio 2 de Nativ. B. Mariæ, prope finem (1x); Oratio 2 de Dormit. B. M. V., post init. (1x); Orat. 2 de drom. Deiparæ (1x); Orat. 2 de Dormitione Deiparæ, sub finem (1x) | `Sancti/07-26.txt:24`; `Sancti/08-15t.txt:117`; `Sancti/08-18bmv.txt:70`; `Sancti/08-18bmv.txt:80` |
| Irenaeus Lugdunensis | Lib. 5, c. 19 | 1 | 1 | Lib. 5, c. 19 (1x) | `Commune/C10.txt:135` |
| Leo Magnus | Ex Homil. de Transfiguratione Domini | 1 | 3 | Ex Homil. de Transfiguratione Domini (1x) | `Tempora/Quad2-0.txt:120` |
| Leo Magnus | Homilia de Transfiguratione Domini | 1 | 1 | Homilia de Transfiguratione Domini (1x) | `Tempora/Quad1-6.txt:15` |
| Leo Magnus | Litteræ Encyclicæ Leónis Papæ XIII | 1 | 1 | Litteræ Encyclicæ Leónis Papæ XIII (1x) | `Sancti/07-07.txt:58` |
| Leo Magnus | Sermones | 28 | 61 | Sermo 2 de Ascensione Domini (2x); Sermo 7 de Nativitate Domini (1x); Sermo 2 de Epiphania (1x); Sermo 1 de Epiphania (1x); Sermo 1 de Ss. Apost. Petro et Paulo, ante medium. (1x); Sermo 3 in annivers. assumpt. suæ, post initium (1x); … | `Sancti/01-01.txt:74`; `Sancti/01-06.txt:162`; `Sancti/01-09.txt:29`; `Sancti/01-18.txt:58`; `Sancti/02-22.txt:150`; `Sancti/03-12.txt:44`; … |
| Maximus Taurinensis | Sermones | 7 | 15 | Homilia 78, quæ est 2 de S. Eusebio Vercellensi (1x); Homilía 78, de S. Eusebio 2, circa medio (1x); Homilia 1 de Epiphania (1x); Homilia 3. in Nativ. S. Joannis Bapt. (1x); Homilia 1 de S. Laurentio (1x); Ex Homilía 59, quæ est 2 de S. Eusebio (1x); … | `Commune/C4.txt:178`; `Commune/C4.txt:355`; `Sancti/01-10.txt:31`; `Sancti/07-01t.txt:13`; `Sancti/08-14oct.txt:13`; `Sancti/11-17.txt:26`; … |
| Petrus Canisius | Homilia sancti Petri Canísii Presbýteri | 1 | 1 | Homilia sancti Petri Canísii Presbýteri (1x) | `Tempora/Pent03-3.txt:51` |
| Petrus Chrysologus | Sermones | 2 | 6 | Sermo 32 (1x); Sermo 50 (1x) | `Sancti/03-27.txt:47`; `Tempora/Pent18-0.txt:23` |
| sancti Germáni Epíscopi | In Præsentatione Deiparæ | 1 | 2 | In Præsentatione Deiparæ (1x) | `Sancti/12-08.txt:176` |
| sancti Lauréntii Justiniáni Epíscopi | De triumpháli Christi agóne, cap. 21 | 1 | 1 | De triumpháli Christi agóne, cap. 21 (1x) | `Tempora/Pent03-1.txt:49` |
| Sophronius Hierosolymitanus | Homilia in Deiparæ Annunt. | 2 | 4 | Homilia in Deiparæ Annunt. (2x) | `Sancti/12-09bmv.txt:31`; `Sancti/12-14bmv.txt:38` |
| Tarasius Constantinopolitanus | De Præsentatióne Deiparæ | 1 | 2 | De Præsentatióne Deiparæ (1x) | `Sancti/12-12bmv.txt:30` |
| Thomas Aquinas | Sermones | 2 | 6 | Lectio iv in opusculo 57 (1x); In eodem Opusculo 57. (1x) | `Tempora/Pent01-4.txt:185`; `Tempora/Pent01-5.txt:67` |
| Unklarer Autor | Breve « Neminem fugit » 14 junii 1892 | 1 | 3 | Breve « Neminem fugit » 14 junii 1892 (1x) | `Tempora/Epi1-0.txt:211` |
| Unklarer Autor | Can 27 | 1 | 1 | Can 27 (1x) | `Commune/C4.txt:374` |
| Unklarer Autor | Cap. 16 | 1 | 1 | Cap. 16 (1x) | `Tempora/095-0.txt:55` |
| Unklarer Autor | Cap. 17 post init. | 1 | 1 | Cap. 17 post init. (1x) | `Commune/C5.txt:303` |
| Unklarer Autor | Cap. 2. | 1 | 1 | Cap. 2. (1x) | `Sancti/09-13bmv.txt:48` |
| Unklarer Autor | De Consec. dist. 1., c. 17 | 1 | 1 | De Consec. dist. 1., c. 17 (1x) | `Commune/C8.txt:563` |
| Unklarer Autor | de Homilía Feriæ. | 1 | 1 | de Homilía Feriæ. (1x) | `Tempora/Quad5-5.txt:240` |
| Unklarer Autor | De vite mystica, cap. 3 | 1 | 1 | De vite mystica, cap. 3 (1x) | `Tempora/Pent02-5.txt:234` |
| Unklarer Autor | Ex Bulla dogmatica Pii Papæ noni | 1 | 1 | Ex Bulla dogmatica Pii Papæ noni (1x) | `Sancti/12-12bmv.txt:11` |
| Unklarer Autor | Ex libro 9 Conf. cap. 12. | 1 | 1 | Ex libro 9 Conf. cap. 12. (1x) | `Sancti/05-04.txt:30` |
| Unklarer Autor | In cap. 8 post initium | 1 | 1 | In cap. 8 post initium (1x) | `Commune/C10.txt:189` |
| Unklarer Autor | In Evang. Dominica I post Pascha | 1 | 1 | In Evang. Dominica I post Pascha (1x) | `Tempora/Pent03-3.txt:55` |
| Unklarer Autor | In Psalm. 121 | 1 | 3 | In Psalm. 121 (1x) | `Commune/C8.txt:400` |
| Unklarer Autor | Lib. 1 Moral., cap. 1 | 1 | 1 | Lib. 1 Moral., cap. 1 (1x) | `Tempora/091-0.txt:69` |
| Unklarer Autor | Lib. 2., cap. 28., post medium. | 1 | 1 | Lib. 2., cap. 28., post medium. (1x) | `Sancti/08-13oct.txt:20` |
| Unklarer Autor | Lib. 3 cap. 4 in fine | 1 | 1 | Lib. 3 cap. 4 in fine (1x) | `Commune/C10.txt:147` |
| Unklarer Autor | Medit. 6 | 1 | 1 | Medit. 6 (1x) | `Tempora/Pent03-3.txt:59` |
| Unklarer Autor | Sermones | 2 | 2 | Sermo 5. de eodem Festo, circa medium. (1x); Sermo 2 de Circumcisione (1x) | `Sancti/11-06oct.txt:20`; `Tempora/Nat2-0.txt:229` |

## Hinweise zur Weiterarbeit

- Für eine streng datierte Fassung `1906` müsste als nächster Schritt die DO-Rubrikenlogik beziehungsweise ein konkreter Kalenderlauf ausgewertet werden. Das würde vor allem Temporale-Varianten mit `o`-/`r`-Suffixen und Referenzen `@...` noch sauberer auflösen.
- Die Normalisierung von Werktiteln ist heuristisch. Die CSV bewahrt deshalb immer die originale DO-Quellenzeile (`source`) und die erkannte Autorzeile (`author_line`).
- Für wissenschaftliche Arbeit sollten die normalisierten Werkgruppen gegen Clavis/CPL, PL/CSEL/CCSL oder BHL-nahe Spezialfälle kontrolliert werden.

