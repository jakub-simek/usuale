# Studies

Dieser Ordner enthält Untersuchungen zu liturgischen Texten und ihren Quellen.
Er ist von `data/translations` getrennt: Übersetzungen liegen dort, Quellenidentifikation,
Kollationen, Kontextberichte und korpusweite Auswertungen liegen hier.

## Struktur

- `celebrations/`: Studien, die einer konkreten Feier zugeordnet sind. Die Gliederung folgt den Divinum-Officium-Basisordnern, z. B. `tempora/pent06-0` für `Tempora/Pent06-0.txt`.
- `corpora/`: übergreifende Untersuchungen zu einem Korpus oder Werkbestand, z. B. zum römischen Brevier vor *Divino afflatu* oder zu allen DO-Lesungen aus einem patristischen Werk.
- `topics/`: thematische Studien, Notizen und Vorarbeiten, die nicht primär an eine einzelne `celebratio` gebunden sind. Sie können über `related_celebrations` lose auf Feiern verweisen.

Jede celebration-bezogene Studie sollte in der YAML-Kopfzeile `celebration`,
`celebration_ref`, `do_sources` und nach Möglichkeit `text_unit` angeben.
