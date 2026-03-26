# Budzeta planotajs

## Programmas nosaukums
Budzeta planotajs

## Merkis
Lietotne palidz ievadit ienakumus un izdevumus, redzet visus ierakstus viena vieta, aprekinat bilanci un saglabat datus CSV faila, lai tie nepazustu pec programmas aizversanas.

## Ka lietot programmu
1. Aktivize savu Python vidi un uzinstale `flask`, ja tas vel nav pieejams.
2. Palaid programmu ar komandu `python app.py`.
3. Atver parluku un dodies uz `http://127.0.0.1:5000/`.
4. Forma ievadi tipu, summu, aprakstu un, ja vajag, datumu.
5. Skaties kopsavilkumu, filtre ierakstus pec tipa vai datuma un dzes nevajadzigos ierakstus.
6. Atver `/bilance`, lai redzetu atsevisku bilances lapu.

## Ekranatteli
Pievieno seit 2-3 ekranattelus:
- sakumlapu ar ievades formu;
- filtru un ierakstu sarakstu;
- bilances lapu.

## Koda apraksts
- `ieladet_datus()` nolasa CSV failu un ielade saglabatos ierakstus atmina.
- `saglabat_datus()` ieraksta visus datus `dati.csv`, lai tie saglabatos starp palaisanas reizem.
- `aprekinat_kopsavilkumu()` saskaita ienakumus, izdevumus un kopejo bilanci.
- `atlasit_ierakstus()` nodrosina filtrus pec tipa un datuma.
- `/pievienot` parbauda ievadi, parvers summu par `float` un saglaba ierakstu.
- `/dzest/<id>` izdzes konkretu ierakstu un atjauno CSV failu.
- `/bilance` paradisa atsevisku parskata lapu.

## Secinajumi
Projekta laika tika izveidota vienkarsa, bet praktiska Flask lietotne ar datu validaciju, bilances aprekinu, CSV glabasanu un ertiem filtriem. To var talak papildinat ar kategorijam, diagrammam vai autorizaciju.
