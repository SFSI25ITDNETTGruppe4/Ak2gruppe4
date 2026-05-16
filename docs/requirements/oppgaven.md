## Innledning

Kunden trenger en app (GUI) til databasen de bruker for handel og lager.

## Oppdraget deres

### Programmering og database

Ut ifra den vedlagte databasen skal dere lage en app som kobler seg opp mot databasen. Dere bruker SQL-kode i Python for å kommunisere med databasen, og i en av deloppgavene nedenfor skal det brukes «Stored Procedures».

Appen skal kunne gjøre følgende via Python GUI-grensesnittet (her er det mange valg, for eksempel Tkinter eller customtkinter, begrunn valget i rapporten):

- Databasen må sikres mot SQL-injection i Python-koden, inndata må sjekkes om de er gyldige (validering), og koden må sikres mot utilsiktede stopp.
- Vise en liste over hvilke varer som er på varelageret, inkludert varenummer, navn på varen, antall og pris.
- I tillegg til å vise varelageret i selve Python-programmet skal dere ved bruk av et API vise varelageret i en nettleser.
- Ha funksjonalitet som lister opp alle ordrer som ligger i databasen.
- Kunne velge en spesifikk ordre og vise hva slags varer, antall av hver vare som har blitt solgt, pris pr. vare, pris ganger antall, kunde med navn og adresse, og total pris.
- Generere en faktura (PDF) for den valgte ordren. Her må det også genereres et fakturanummer. Dette fakturanummeret må lagres i databasen, og det er ikke tillatt med to like fakturanummer. Ta med moms.
- Vise alle kunder som er registrert i databasen. OBS! Her skal dere bruke «Stored Procedures».
- Legge til og fjerne kunder fra databasen.

## Hva skal leveres/gjøres?

### Innlevering 1

- En rapport på maks 12-18 sider der dere forklarer hva dere har gjort, hvorfor dere har gjort det sånn, og hva som eventuelt har gått galt underveis. Ta utgangspunkt i rapportmalen.
- Programmet dere har kodet som .py eller .zip hvis det er nødvendig.

### Innlevering 2

- Gruppelogg med gruppe-refleksjon over når dere har jobbet, hvem som har vært med, og hvem som har hatt ansvar for hva.
- Vurderes som godkjent/ikke godkjent.

### Innlevering 3

- Individuell refleksjonsvideo etter at arbeidet er ferdig.
- Vurderes som godkjent/ikke godkjent.

Gjennomføre en presentasjon om arbeidet dere har gjort.

Når: I henhold til hva vi har avtalt i fremdriftsplanen. Presentasjonen skal vare i maks 30 minutter.

### Vurdering

Prosjektet teller på emnekarakteren i henhold til «Arbeidskrav og vurdering» i emnet.

Oppgaven blir karaktersatt ut ifra vurderingskriteriene nedenfor, og dere får en gruppekarakter.
Det er innlevering 1 og presentasjonen som gjelder for karakteren, men innlevering 2 og 3 må være godkjent.

Med følgende unntak:
Hvis det blir stor tvil om en student har bidratt til gruppens gjennomføring/resultat av prosjektet, vil det bli gjennomført en muntlig høring med studenten. Resultatet av den høringen vil da ligge til grunn for karakter for vedkommende på prosjektet.

## Ressurser

Database som skal brukes i oppgaven Download Database som skal brukes i oppgaven 
RapportmalDownload Rapportmal
 Lenker og teori: 

Python og MySQL: 

https://www.mysqltutorial.org/python-mysql/Links to an external site.Links to an external site. 
https://www.mysqltutorial.org/calling-mysql-stored-procedures-python/Links to an external site.Links to an external site. 
https://www.w3schools.com/python/python_mysql_getstarted.aspLinks to an external site.Links to an external site. 
https://pynative.com/python-mysql-database-connection/Links to an external site.Links to an external site. 
 

MySQL "Stored Procedures» 

w3schools.com - sql_stored_proceduresLinks to an external site.Links to an external site. 
mysqltutorial.org - MySQL Stored ProceduresLinks to an external site.Links to an external site. 
mysqltutorial.org - Python MySQL – Call Stored Procedures in PythonLinks to an external site.Links to an external site. 
https://pynative.com/python-mysql-execute-stored-procedure/Links to an external site.Links to an external site. 
https://www.softwaretestinghelp.com/mysql-stored-procedure/Links to an external site.Links to an external site. 

Python og SQL-injection 

https://medium.com/@miguel.amezola/protecting-your-code-from-sql-injection-attacks-when-using-raw-sql-in-python-916466961c97Links to an external site. 
https://realpython.com/prevent-python-sql-injection/#understanding-python-sql-injectionLinks to an external site. 

TKinter GUI i Python 

https://docs.python.org/3/library/tkinter.htmlLinks to an external site.Links to an external site. 
https://docs.python.org/3/library/tk.htmlLinks to an external site.Links to an external site. 
https://realpython.com/python-gui-tkinter/#building-your-first-python-gui-application-with-tkinterLinks to an external site.Links to an external site. 
https://www.tutorialspoint.com/python/python_gui_programming.htmLinks to an external site.Links to an external site. 
https://pythonexamples.org/python-tkinter/Links to an external site. 

customTkinter GUI i Python 

https://customtkinter.tomschimansky.com/Links to an external site.

 

Python og API

FastAPILinks to an external site.     (I forbindelse med API er JSON og HTTP-protokollen aktuelle for de som vi ha litt mer inngående forståelse).

Welcome to Flask — Flask Documentation (3.1.x)Links to an external site.
https://fastapi.tiangolo.com/
https://flask.palletsprojects.com/en/stable/
https://youtu.be/cNlJCQHSmbE?si=5z0ttcuV0RAn8QjC&t=149

En kort sammenligning av de tre mest aktuelle APIene i forbindelse med Python Webutvikling.Links to an external site.

 

Tips for mulig løsning for å legge selv databasen i skya for deling

1. AWS Free TierLinks to an external site.
https://aws.amazon.com/free/?trk=52605843-2998-4d6e-a9f7-390cbf6d2c3d&sc_channel=ps&gad_campaignid=23533256638&gclid=CjwKCAiAncvMBhBEEiwA9GU_foeVHl9JtvO06fT8nMOi2cdDE2uOEQPKa_SH7Q5Wup736Zh9KHtTthoCCuUQAvD_BwE

2. AWS service - Amazon RDS - managed SQL databaseLinks to an external site.
https://aws.amazon.com/rds/
3. Tips til løsning hvis det er problemer med kommunikasjon med databasen (5 kr/mnd ??)Links to an external site.
https://aws.amazon.com/blogs/database/securely-connect-to-an-amazon-rds-or-amazon-ec2-database-instance-remotely-with-your-preferred-gui/

 

GITHUB

GitHub Foundations Part 1 of 2 - Training | Microsoft LearnLinks to an 
external site. 
https://learn.microsoft.com/en-us/training/paths/github-foundations/

GitHub Foundations Part 2 of 2 - Traininghttps://learn.microsoft.com/en-us/training/paths/github-foundations/