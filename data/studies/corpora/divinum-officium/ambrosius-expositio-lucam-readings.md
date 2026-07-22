# Ambrosius: Lukas-Auslegung in den römischen DO-Daten

Suchbereich: `sources/divinum-officium/web/www/horas/Latin/{Tempora,Sancti,Commune}` einschließlich lokaler Unterordner unter `Sancti`. Ausgeschlossen sind Ordens- und monastische Sonderordner (`*OP`, `*Cist`, `*M`) sowie Martyrologium, Psalterium, Regula und Necrologium.

Gezählt ist jeweils ein zusammenhängender Lesungsblock aus Ambrosius, *Expositio evangelii secundum Lucam*. Wenn nur die erste Lektion die Homilie überschreibt, sind die folgenden Fortsetzungslektionen im Feld `Lesungen` mit erfasst.

## Zisterziensische Berücksichtigung

Für den zisterziensischen Abgleich wurden zusätzlich `TemporaCist`, `SanctiCist`, `CommuneCist` und, wo die DO-Daten für die zisterziensisch/monastische 12-Lesungen-Struktur darauf verweisen, auch die entsprechenden `*M`-Dateien berücksichtigt. Die Markierung bezieht sich auf den Textbestand, nicht zwingend auf denselben liturgischen Tag oder dieselbe Lesungseinteilung.

| Markierung | Bedeutung |
|---|---|
| `R+Z` | Der römische Lesungsblock ist im zisterziensischen Bestand direkt oder über `@`-Verweise nachweisbar, oft mit anderer Aufteilung. |
| `R` | In der geprüften zisterziensischen DO-Schicht wurde kein entsprechender Lesungsblock gefunden. |
| `Z` | Nur zisterziensisch nachweisbar; im römischen Bestand nicht gefunden. |

Nach diesem Abgleich sind keine eindeutig `Z`-only Ambrosius-Lukas-Lesungen in den eigentlichen `*Cist`-Dateien hinzugekommen. Zwei römische Basis-Einträge blieben ohne zisterziensischen Nachweis: `Tempora/Adv3-5.txt` und `Sancti/09-20o.txt`. Die übrigen universalen römischen Basis-Einträge sind als `R+Z` zu lesen. Die lokalen/partikularen Zusätze am Ende der Datei bleiben gesondert; für sie wurde in der zisterziensischen Schicht kein sicherer Parallelbefund angesetzt.

Besonders zu beachten:

| Römischer Eintrag | Zisterziensischer Befund | Markierung |
|---|---|---|
| `Tempora/Pent06-0.txt:83` | In `TemporaM/Pent06-0.txt` aus dem römischen Text übernommen und auf `Lectio9-12` verteilt. | `R+Z` |
| `Tempora/Nat1-0.txt:72` | In `TemporaCist/Nat30.txt` als dreiteilige Lesung ausgeschrieben; gleicher Ambrosius-Abschnitt, anderer Tag/Schnitt. | `R+Z` |
| `Sancti/12-25.txt:253` | In `SanctiCist/12-25.txt` als `Lectio11` ausgeschrieben. | `R+Z` |
| `Tempora/Adv3-5.txt:18` | Kein sicherer zisterziensischer Lesungsbefund im geprüften Material. | `R` |
| `Sancti/09-20o.txt:23` | Kein sicherer zisterziensischer Lesungsbefund im geprüften Material. | `R` |

## Universale römische Basisdateien

| Datei | Lesungen | Officium | Evangelium | DO-Werkangabe | Incipit des Ambrosius-Abschnitts |
|---|---:|---|---|---|---|
| [`Commune/C3.txt:367`](../sources/divinum-officium/web/www/horas/Latin/Commune/C3.txt) | `Lectio7 in 2 loco-9 in 2 loco` | Commune Plurimorum Martyrum Pontificum | Luc 6:17-23 | Lib. 5. in Lucam. Cap. 6., post init. | Advérte ómnia diligénter, quómodo et cum Apóstolis ascéndat et descéndat ad turb |
| [`Commune/C5.txt:322`](../sources/divinum-officium/web/www/horas/Latin/Commune/C5.txt) | `Lectio7 in 3 loco-9 in 3 loco` | Commune Confessoris non pontificis | Luc 19:12-26 | Lib. 8. in Lucam. | Bonus ordo, ut vocatúrus gentes, et Judǽos jussúrus intérfici, qui noluérunt reg |
| [`Commune/C8.txt:224`](../sources/divinum-officium/web/www/horas/Latin/Commune/C8.txt) | `Lectio7-9` | Commune Dedicationis Ecclesiae | Luc 19:1-10 | Lib. 8 in Luc., prope finem | Zachǽus, statúra pusíllus, hoc est, nulla nobilitátis ingénitæ dignitáte sublími |
| [`Commune/C8.txt:409`](../sources/divinum-officium/web/www/horas/Latin/Commune/C8.txt) | `Lectio7 in 2 loco-9 in 2 loco` | Commune Dedicationis Ecclesiae | Luc 19:1-10 | Lib. 8 in Luc., in fine | Et conféstim, inquit, vidit, et sequebatur illum, magníficans Dóminum. Áliter en |
| [`Commune/C8.txt:435`](../sources/divinum-officium/web/www/horas/Latin/Commune/C8.txt) | `Lectio7 in 3 loco-9 in 3 loco` | Commune Dedicationis Ecclesiae | Luc 19:1-10 | Ex Lib. 8 in Luc., prope finem | Quæ autem turba, nisi imperitæ confúsio multitúdinis, quæ vérticem nequit vidére |
| [`Sancti/01-01.txt:103`](../sources/divinum-officium/web/www/horas/Latin/Sancti/01-01.txt) | `Lectio7-9` |  | Luc 2:21 | Liber 2 in cap. 2 Lucæ, circa medium | Circumcíditur ítaque Puer. Quis est iste puer, nisi ille, de quo dictum est: Pue |
| [`Sancti/01-11.txt:39`](../sources/divinum-officium/web/www/horas/Latin/Sancti/01-11.txt) | `Lectio7-9` |  | Matt 2:1-12 | Liber 2 in Lucam cap. 2, post init. | Quæ sunt ista veræ fídei múnera? Aurum Regi, thus Deo, myrrha defúncto. Aliud en |
| [`Sancti/02-02.txt:103`](../sources/divinum-officium/web/www/horas/Latin/Sancti/02-02.txt) | `Lectio7-9` |  | Luc 2:22-32 | Liber 2 Comment. in Lucæ cap. 2, post initium | Et ecce homo erat in Jerúsalem, cui nomen Símeon, et homo iste justus et timorát |
| [`Sancti/03-25.txt:108`](../sources/divinum-officium/web/www/horas/Latin/Sancti/03-25.txt) | `Lectio7-9` |  | Luc 1:26-38 | Liber 2 in Lucam | Latent quidem divína mystéria, nec fácile, juxta prophéticum dictum, quisquam hó |
| [`Sancti/06-23.txt:20`](../sources/divinum-officium/web/www/horas/Latin/Sancti/06-23.txt) | `Lectio1-3` | In Vigilia S. Joannis Baptistæ | Luc 1:5-17 | Liber 1 in Lucam | Docet nos Scriptúra divína non solum mores in iis qui prædicábiles sunt, sed éti |
| [`Sancti/06-24.txt:236`](../sources/divinum-officium/web/www/horas/Latin/Sancti/06-24.txt) | `Lectio7-9` | In Nativitate S. Joannis Baptistæ | Luc 1:57-69 | Liber 2 Comm. in Lucæ cap. 1, ante finem | Péperit fílium Elísabeth, et congratulabántur vicíni. Habet Sanctórum edítio læt |
| [`Sancti/06-25oct.txt:23`](../sources/divinum-officium/web/www/horas/Latin/Sancti/06-25oct.txt) | `Lectio7-9` | Die secunda infra Octavam Nativitatis S. Joannis Baptistæ | Luc 1:57-69 | Lib. 2. in Lucam. | Joánnes est, inquit, nomen ejus. Non póterat Elísabeth Dómini ignoráre prænúntiu |
| [`Sancti/06-27oct.txt:23`](../sources/divinum-officium/web/www/horas/Latin/Sancti/06-27oct.txt) | `Lectio7-9` | Quarta die infra Octavam Nativitatis S. Joannis Baptistæ | Luc 1:57-68 | Lib. 2 in Luc. cap. 1 in fine | Et Zacharías pater ejus implétus est Spíritu Sancto, et prophetábat. Vide quam b |
| [`Sancti/07-01t.txt:22`](../sources/divinum-officium/web/www/horas/Latin/Sancti/07-01t.txt) | `Lectio7-9` | In Octava S. Joannis Baptistæ | Luc 1:57-65 | Lib. 2. in Luca3 cap. L, circa finem. | Joannes est, inquit, nomen ejus. Non poterat Elisabeth Domini ignorare prænuntiu |
| [`Sancti/07-02.txt:112`](../sources/divinum-officium/web/www/horas/Latin/Sancti/07-02.txt) | `Lectio7-9` |  | Luc 1:39-47 | Liber 2 Comment. in Lucæ. cap. 1, post initium | Contuéndum est, quia supérior venit ad inferiórem, ut inférior adjuvétur: María |
| [`Sancti/07-23.txt:34`](../sources/divinum-officium/web/www/horas/Latin/Sancti/07-23.txt) | `Lectio7-9` | S. Apollinaris Episcopi et Martyris | Luc 22:24-30 | Liber 10 in Lucæ, cap. 22, post initium. | Regnum Dei non est de hoc mundo. Non ergo æqualitátis hómini ad Deum, sed simili |
| [`Sancti/08-24.txt:40`](../sources/divinum-officium/web/www/horas/Latin/Sancti/08-24.txt) | `Lectio7-9` | S. Bartholomæi Apostoli | Luc 6:12-19 | Lib. 5 Comment. in Luc. cap. 6, post initium | Omnes magni, omnes sublímes montem ascéndunt. Non enim cuicúmque prophéta dicit: |
| [`Sancti/09-20o.txt:23`](../sources/divinum-officium/web/www/horas/Latin/Sancti/09-20o.txt) | `Lectio1_` | In Vigilia S. Matthæi Ap. | Luc 5:27-32 | Liber 5 Comment. in Lucæ Cap. 5 post initium | Sequitur mystica est hæc vocátio publicani, quem sequi jubet, non corporis gress |
| [`Sancti/11-11.txt:102`](../sources/divinum-officium/web/www/horas/Latin/Sancti/11-11.txt) | `Lectio7-8` | S. Martini Episcopi et Confessoris | Luc 11:33-36 | Liber 7 Comment. in Luc. cap. 11, post initium | Quia in superióribus Ecclésiam Synagógæ prǽtulit, hortátur nos ut fidem pótius n |
| [`Sancti/12-25.txt:253`](../sources/divinum-officium/web/www/horas/Latin/Sancti/12-25.txt) | `Lectio8` |  | Luc 2:15-20 | Lib. 2 in cap. 2. Lucæ, circa medium | Vidéte Ecclésiæ surgéntis exórdium: Christus náscitur, et pastóres vigiláre cœpé |
| [`Tempora/Adv3-5.txt:18`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Adv3-5.txt) | `Lectio1-3` | Feria VI Quattuor Temporum in Adventu | Luc 1:39-47 | Lib. 2 in Luc. cap. 1 post init. | Morále est ómnibus, ut qui fidem éxigunt, fidem ástruant. Et ídeo Angelus, cum a |
| [`Tempora/Epi1-0a.txt:75`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Epi1-0a.txt) | `Lectio7-9` | Dominica infra Octavam Epiphaniæ | Luc 2:42-51 | Lib. 2. in cap. 2. Lucæ, in fine | A duodécimo anno, ut légimus, Domínicæ súmitur disputatiónis exórdium. Hic enim |
| [`Tempora/Nat1-0.txt:72`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Nat1-0.txt) | `Lectio7-9` | Dominica Infra Octavam Nativitatis | Luc 2:33-40 | Lib. 2 in cap. 2 Lucæ, prope finem | Vides úberem in omnes grátiam, Dómini generatióne diffúsam, et prophetíam incréd |
| [`Tempora/Nat30.txt:86`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Nat30.txt) | `Lectio7-9` | Diei VI infra Octavam Nativitatis | Luc 2:15-20 | Liber 2 in cap. 2. Lucæ, circa med. | Vides festináre pastóres; nemo enim cum desídia Christum requírit. Vides pastóre |
| [`Tempora/Pasc0-2.txt:25`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Pasc0-2.txt) | `Lectio1-3` | Die III infra octavam Paschæ | Luc 24:36-47 | Liber 10. Comment. in Lucam, cap. 24, ante finem | Mirum, quo modo se natúra corpórea per impenetrábile corpus infúderit invisíbili |
| [`Tempora/Pasc2-6.txt:60`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Pasc2-6.txt) | `Lectio7-9` | De IV die infra Octavam S. Joseph | Luc 3:21-23 | Expositio in Luc. lib. 3 | Néminem movére debet, quod ita scriptum est: Qui putabátur fílius Joseph. Bene e |
| [`Tempora/Pasc3-1.txt:66`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Pasc3-1.txt) | `Lectio7-9` | De VI die infra Octavam S. Joseph | Luc 3:21-23 | Expositio in Luc. lib. 3 | Quod per Salomónem Matthǽus generatiónem derivándum putávit, Lucas vero per Nath |
| [`Tempora/Pasc5-1.txt:15`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Pasc5-1.txt) | `Lectio1-3` | Feria Secunda in Rogationibus | Luc 11:5-13 | Liber 7 in Lucæ cap. 11 | Alius præcépti locus est, ut ómnibus moméntis, non solum diébus, sed étiam nocti |
| [`Tempora/Pasc7-4.txt:25`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Pasc7-4.txt) | `Lectio1-3` | Feria Quinta infra octavam Pentecostes | Luc 9:1-6 | Liber 6 in cap. 9 Lucæ | Qualis débeat esse, qui evangelízat regnum Dei, præcéptis evangélicis designátur |
| [`Tempora/Pasc7-5.txt:24`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Pasc7-5.txt) | `Lectio1-3` | Feria Sexta Quattuor Temporum Pentecostes | Luc 5:17-26 | Liber 5 in cap. 5 Lucæ, post initium | Non otiósa hujus paralýtici, nec angústa medicína est, quando Dóminus et orásse |
| [`Tempora/Pasc7-6.txt:25`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Pasc7-6.txt) | `Lectio1-3` | Sabbato Quattuor Temporum Pentecostes | Luc 4:38-44 | Liber 4 in cap. 4 Lucæ, circa finem | Vide cleméntiam Dómini Salvatóris: nec indignatióne commótus nec scélere offénsu |
| [`Tempora/Pent04-0.txt:83`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Pent04-0.txt) | `Lectio7-9` | Dominica IV Post Pentecosten | Luc 5:1-11 | Liber 4 in Lucæ cap. 5 prope finem libri | Ubi Dóminus multis impartívit varia génera sanitátum, nec témpore, nec loco pótu |
| [`Tempora/Pent06-0.txt:83`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Pent06-0.txt) | `Lectio7-9` | Dominica VI Post Pentecosten | Marc 8:1-9 | Liber 6 in Lucæ cap. 9, post initium | Posteáquam illa, quæ Ecclésiæ typum accépit, a fluxu curáta est sánguinis, poste |
| [`Tempora/Pent16-0.txt:17`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Pent16-0.txt) | `Lectio7-9` | Dominica XVI Post Pentecosten | Luc 14:1-11 | Liber 7 in Lucæ cap. 14 | Curátur hydrópicus, in quo fluxus carnis exúberans ánimæ gravábat offícia, spíri |
| [`Tempora/Quad1-3.txt:9`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Quad1-3.txt) | `Lectio1-3` | Feria Quarta Quattuor Temporum Quadragesimæ | Matt 12:38-50 | Lib. 7 in Lucæ cap. 11 | Judæórum plebe damnáta, Ecclésiæ mystérium evidénter exprímitur, quæ in Ninivíti |
| [`Tempora/Quad2-5.txt:11`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Quad2-5.txt) | `Lectio1-3` | Feria Sexta infra Hebdomadam II in Quadragesima | Matt 21:33-46 | Lib. 9 in cap. 20 Lucæ | Pleríque várias significatiónes de víneæ appellatióne derívant: sed evidénter Is |
| [`Tempora/Quad2-6.txt:11`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Quad2-6.txt) | `Lectio1-3` | Sabbato infra Hebdomadam II in Quadragesima | Luc 15:11-32 | Lib. 8 Comment. in cap. 15 Lucæ, post initium | Vides, quod divínum patrimónium peténtibus datur. Nec putes culpam patris, quod |
| [`Tempora/Quad3-1.txt:11`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Quad3-1.txt) | `Lectio1-3` | Feria Secunda infra Hebdomadam III in Quadragesima | Luc 4:23-30 | Lib. 4 in c. 4 Lucæ, post med. | Non medíocris invídia próditur, quæ cívicæ caritátis oblíta, in acérba ódia caus |
| [`Tempora/Quad4-4.txt:11`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Quad4-4.txt) | `Lectio1-3` | Feria Quinta infra Hebdomadam IV in Quadragesima | Luc 7:11-16 | Lib. 5 Comment. in Lucæ cap. 7, post initium | Et hic locus ad utrámque redúndat grátiam; et ut cito flecti divínam misericórdi |
| [`Tempora/Quad6-0.txt:97`](../sources/divinum-officium/web/www/horas/Latin/Tempora/Quad6-0.txt) | `Lectio7-9` | Dominica in Palmis | Matt 21:1-9 | Liber 9 in Lucam | Pulchre relíctis Judǽis, habitatúrus in afféctibus géntium, templum Dóminus ascé |

## Lokale oder partikulare Zusätze

| Datei | Lesungen | Officium | Evangelium | DO-Werkangabe | Incipit des Ambrosius-Abschnitts |
|---|---:|---|---|---|---|
| [`Sancti/Urbis/08-13octT.txt:33`](../sources/divinum-officium/web/www/horas/Latin/Sancti/Urbis/08-13octT.txt) | `Lectio7-8` | In Octava Transfiguratione Domini Nostri Jesu Christi | Matt 17:1-9 | Lib. 7. in Luc., cap. 9. | Hic est Fílius meus diléctus; hoc est, non Elías fílius, non Móyses fílius, sed |
| [`Sancti/aliquibus locis/Quad2-5-SindonDNJC.txt:162`](../sources/divinum-officium/web/www/horas/Latin/Sancti/aliquibus locis/Quad2-5-SindonDNJC.txt) | `Lectio4-6` | Ss. Sindonis Domini Nostri Jesu Christi |  | In Luc. cap. 23. | Quid sibi vult quod non Apóstoli, sed Joseph et Nicodemus, ut Joánnes dicit, Chr |
| [`Sancti/aliquibus locis/Quadp1-2-OratioDNJC.txt:173`](../sources/divinum-officium/web/www/horas/Latin/Sancti/aliquibus locis/Quadp1-2-OratioDNJC.txt) | `Lectio7-9` | Orationis Domini Nostri Jesu Christi in Monte Oliveti | Luc 22:39-44 | Lib. 10. Commcnt. in Luc. c. 22. | Transfer a me cálicem istum: quasi homo mortem recúsans, quasi Deus senténtiam s |
