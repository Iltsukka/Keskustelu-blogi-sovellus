# Tietokannat_ja_web-ohjelmointi
Harjoitustyön repositorio
Projektin aihe on blogisovellus, jossa käyttäjät voivat luoda uuden viestiketjun jostain aiheesta ja sovellus mahdollistaa viestien lisäämisen ketjuun. Sovellukseen tulee tietoturvallisesti pystyä kirjautumaan. Viestejä on mahdollista muokata, poistaa tai piilottaa muilta käyttäjiltä. Vain viestiketjun omistaja voi poistaa ketjun. Sovelluksesta voi myös kirjautua ulos.  


Nykyinen tila:
1. palautus:
Perustoiminnallisuudet ovat hyvällä mallilla ja sovellus kommunikoi tietokannan kanssa. Kirjautuminen ja uloskirjautuminen on mahdollista. Taulujen osalta ajattelin vielä jotenkin laajentaa sovellusta, että saisi ainakin sen viisi taulua käyttöön.  
Virheidenkäsittelyyn, (mm. salasanan minimipituus jne.) en ole vielä kiinnittänyt huomiota ja toteutan sen myöhemmin. Ulkoasun kanssa sama juttu. 

2. palautus:
Sovelluksella on jonkinlainen ulkonäkö ja navigaatiopalkki, jolla siirtyä keskeisimpien toimintojen välillä. Postausten muokkaus- ja poistomahdollisuus on lisätty. Koodi on mielestäni selkeää, vaikkakin tietokantapyynnöt voisi ulkoistaa omaan moduuliin. Tietokantatauluja on edelleen 3, mutta ajattelin vielä lisätä pari taulua yksinkertaisten kyselyjen laatimiseen. Keskeisimmät toiminnot ovat kuitenkin jo hyvällä mallilla.



Käynnistysohjeet:
Kloonaa repositorio koneellesi. Luo .env kansio, jonka sisältö on; DATABASE_URL=<tietokannan-paikallinen-osoite>, SECRET_KEY=<salainen-avain>. Aktivoi virtuaaliympäristö: python3 -m venv venv ja source/venv/bin/activate Asenna tarvittavat riippuvuudet: pip install -r ./requirements.txt. Määritä tietokannan skeema: psql < schema.sql. Käynnistä paikallinen tietokanta: start-pg.sh. Nyt sovellus käynnistyy komennolla 'flask run'.