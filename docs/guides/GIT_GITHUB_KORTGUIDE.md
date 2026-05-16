# Git og GitHub kortguide (for nybegynnere)

Denne guiden er en enkel oppskrift for gruppa.

## Hurtigversjon TLDR (bruk denne hver gang)
- Apne terminal i VS Code: Terminal -> New Terminal.
- Kjor kommandoene under i denne rekkefolgen:
  - git pull
  - git status
  - git add .
  - git commit -m "Kort forklaring av endringen"
  - git push

## 1) For du starter
- Apne prosjektmappen i VS Code.
- Sjekk at du star pa riktig branch:
  - git branch
- Hent siste endringer:
  - git pull

## 2) Nar du har gjort endringer
- Sjekk hva som er endret:
  - git status
- Legg til filer:
  - git add .
- Lag commit med kort melding:
  - git commit -m "Kort forklaring av endringen"
- Push til GitHub:
  - git push

## 3) Enkel arbeidsflyt for gruppa
- Pull alltid for du begynner.
- Commit ofte (sma endringer er best).
- Skriv tydelige commit-meldinger.
- Push nar du er ferdig med en liten del.

## 3.1) Arbeidslogg i prosjektet
- Git commit-loggen er utgangspunktet for arbeidsloggen i gruppa.
- Derfor ma hver commit-melding beskrive hva som faktisk ble gjort.
- Alle i gruppa ma committe fra egen bruker, slik at bidrag blir synlige.

## 4) Hvis du far problemer
- Hvis push feiler fordi andre har pushet:
  - git pull
  - los eventuelle konflikter i filene
  - git add .
  - git commit -m "Los konflikt"
  - git push

## 5) Forslag til commit-meldinger
- "Rettet skrivefeil i oppgaven"
- "La til validering i kunde-funksjon"
- "Oppdaterte README med installasjonssteg"
