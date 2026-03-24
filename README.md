# Ak2gruppe4

Flask-prosjekt for arbeidskrav med GUI/nettvisning mot databasen `varehusdb`.

## AWS databasekobling

Prosjektet er satt opp for å bruke denne RDS-host'en som standard:

`varehusdb.cf6um6awm1jz.eu-north-1.rds.amazonaws.com`

For lokal kjøring anbefales en `.env`-fil i prosjektroten. `.env` er ignorert av Git.

Eksempel:

```env
DB_HOST=varehusdb.cf6um6awm1jz.eu-north-1.rds.amazonaws.com
DB_USER=<aws-bruker>
DB_PASSWORD=<aws-passord>
DB_NAME=varehusdb
```

## Hvordan koble til databasen

1. Gå til `AWS Console` -> `RDS` -> databasen deres.
2. Under `Connectivity & security`, finn tilhørende `Security Group`.
3. I `Inbound rules`, legg til `MySQL/Aurora` på port `3306`.
4. Sett `Source` til deres offentlige IP-adresser som `/32`, ikke `0.0.0.0/0`.
5. Kopier RDS-endepunktet og legg det i `.env` som `DB_HOST`.
6. Legg inn AWS-brukernavn og passord som `DB_USER` og `DB_PASSWORD`.
7. Start appen med `python app.py`.

## Import av databasen til AWS RDS

Hvis databasen ikke er importert ennå:

1. Bruk `db\varehusdb.sql`.
2. Koble til RDS med MySQL Workbench eller `mysql`-klient.
3. Hvis importen feiler fordi databasen allerede finnes, fjern `CREATE DATABASE` og `USE varehusdb;` fra dump-filen før import.
4. Importer filen og verifiser at tabeller som `kunde` finnes.

Eksempel med MySQL-klient:

```powershell
mysql -h varehusdb.cf6um6awm1jz.eu-north-1.rds.amazonaws.com -u <aws-bruker> -p varehusdb < db\varehusdb.sql
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPL-3.0 license](LICENSE)
