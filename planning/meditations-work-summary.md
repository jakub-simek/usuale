# Zusammenfassung: Usuale-Richtlinien fuer liturgische Meditationen

Stand: 2026-05-17

Diese Notiz fasst nur noch das Usuale-spezifische Overlay zusammen. Die
allgemeinen Regeln fuer lateinische Meditationen liegen zentral im Submodul:

```text
shared/latin-meditations-guidelines/guidelines/
```

Massgeblich ist die Reihenfolge:

1. zentrale Richtlinien im Submodul
2. Usuale-Overlay in `planning/meditations-guidelines.md`
3. konkrete Quellen und vorhandene Meditationen im Projekt

## Usuale-Spezifikum

Usuale-Meditationen sind traditionelle katholische Meditationen in
kirchlichem Latein, die von einem konkreten Text der traditionellen roemischen
Liturgie ausgehen.

Der gewaehlte liturgische Text bleibt Mittelpunkt. Weitere Texte der Messe
oder des Officiums duerfen den Zusammenhang erhellen, sollen aber nicht das
Thema ersetzen.

## Quellen und Kontext

Vor neuen oder revidierten Meditationen sind zu pruefen:

- der Divinum-Officium-Quellenzeuge in `sources/divinum-officium/`
- die zugehoerige `celebratio` in `data/indexes/celebrations.xml`
- vorhandene Meditationen desselben liturgischen Tages in `data/meditations/`
- der relevante Kontext von Messe und ggf. Officium

Zum liturgischen Kontext gehoeren insbesondere Epistel, Evangelium, Orationen,
Graduale, Alleluia, Offertorium, Communio und passende Officiumstexte.

## Zitation

Im `Textus fundamentalis` wird der primaere liturgische Text voll mit
Bibelstelle und liturgischem Kontext angegeben, z.B.:

```text
(Act 1,1-11; Lectio Missae In Ascensione Domini)
```

Spaetere Zitate aus demselben primaeren Text nennen normalerweise nur noch die
Bibelstelle, z.B. `(Act 1,7)`. Bei Zitaten aus anderen Mess- oder
Officiumstexten bleibt der liturgische Kontext erhalten.

Psalmstellen folgen der Vulgata-Zaehlung der traditionellen roemischen
Liturgie.

## Pflichtquellen im Usuale-Projekt

Jede Meditation soll normalerweise verbinden:

- Schrift und unmittelbaren liturgischen Text
- patristische Resonanzen
- mittelalterliche oder scholastische Vertiefung
- Catechismus Romanus
- Alphonsus Maria de Liguori
- eine organische marianische Komponente

Die allgemeinen Regeln zu Latein, Zitatstil, Quellenverifikation und
Schlusskorrektur stehen im zentralen Submodul.
