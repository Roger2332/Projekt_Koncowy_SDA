# Evently

Evently to aplikacja webowa stworzona przy użyciu Django, która umożliwia użytkownikom tworzenie, komentowanie,
zarządzanie, oraz zapisanie się na wydarzenia. Każdy zarejestrowany użytkownik posiada profil, który pomaga budować
zaangażowaną społeczność oraz rozwijać sieć kontaktów. Projekt zawiera intuicyjny panel administracyjny, który umożliwia
zarządzanie wszystkimi aspektami aplikacji.

![logo_evently](for_README/img_2.png)
***

## Spis treści:

- [**Wymagania**](#wymagania)
- [**Baza Danych**](#baza-danych)
- [**Instrukcja**](#instrukcja)
- [**Testownie**](#testownie)
- [**Ocena**](#ocena)
- [**Zespół prosjektowy**](#zespół-projektowy)

***

## Wymagania:

> 💡 Aktualny spis wymagań możma zobaczyć tu: [Spis wymagań](requirements.txt)

Aby nasza aplikacja działała poprawnie będziesz potrzebować:

- [Django (v. 5.0.6)](https://pypi.org/project/Django/5.0.6/)
- [asgiref (v. 3.8.1)](https://pypi.org/project/asgiref/3.8.1/)
- [colorama (v. 0.4.6)](https://pypi.org/project/colorama/0.4.6/)
- [execnet (v. 2.1.1)](https://pypi.org/project/execnet/2.1.1/)
- [iniconfig (v. 2.0.0)](https://pypi.org/project/iniconfig/2.0.0/)
- [packaging (v. 24.1)](https://pypi.org/project/packaging/24.1/)
- [pluggy (v. 1.5.0)](https://pypi.org/project/pluggy/1.5.0/)
- [pytest (v. 8.2.2)](https://pypi.org/project/pytest/8.2.2/)
- [pytest-django (v. 4.8.0)](https://pypi.org/project/pytest-django/4.8.0/)
- [pytest-xdist (v. 3.6.1)](https://pypi.org/project/pytest-xdist/3.6.1/)
- [python-decouple (v. 3.8)](https://pypi.org/project/python-decouple/3.8/)
- [sqlparse (v. 0.5.0)](https://pypi.org/project/sqlparse/0.5.0/)
- [tzdata (v. 2024.1)](https://pypi.org/project/tzdata/2024.1/)

> ⚠️ Aby łatwo zaintalować aktualny pakiet bibliotek wykonaj polecenie:
> ```sh
>-pip install -r requirements.txt
>```
***

## Baza Danych:

Struktura bazy danych:

![BD_zaleznosci](for_README/img_1.png)

> ⚠️ Tu możesz pobrać naszą testową [Bazę Danych](for_README/test-db.zip)
>
>| **Loginy do testowej Bazy Danych:** | **Hasła:**     |
>|-------------------------------------|----------------|
>| admin                               | *admin*        |
>| User1/ User2/ User3/ User4/ User5   | *Re?7x4B11(6)* |
***

## Instrukcja:

Jesli chcesz uzyc naszą [Bazę Danych do testów](for_README/test-db.zip) to umiesc ją w swoim folderze.

Natomiast jesli chcesz stworzyc swoja wlasna baze danych wpisz polecenia:

```sh
-python manage.py makemigrations
-python manage.py migrate
```

Dalej stwórz administratora:

```sh
python manage.py createsuperuser
```

Wlaczasz projekt, poleceniem:

```sh
python manage.py runserver
```

Nastepnie przechodzisz do panelu administratora wpisujac
http://localhost:8000/admin
w sesji status tworzysz 3 statusy:

1: Inactive

2: Active

3: Rejected

W panelu administratora tworzysz kategorie eventow, jakie wolisz.

Po utworzeniu Serwis Evently zaczyna dzialac!! Wroc na strone http://localhost:8000/ i baw się dobrze 😄

![gif_koniec instalacji](for_README/gif_end.gif)
***

## Testownie:

Nasz projekt jest objęty w 80 procentach testami jednostkowymi przez bibliotekę PyTest.

Na ten moment w projekcie jest 94 testy.

Aby je uruchomić, wpisz polecenie:

```sh
pytest -n 21
```

***

## Ocena

Projekt został bardzo dobrze oceniony co możma zobaczyć
wg. [CodeReview](https://github.com/Roger2332/Projekt_Koncowy_SDA/pull/54#pullrequestreview-2149544766) od Senior Python
Dewelopera [Jerzyego Grynczewskiego
](https://github.com/jgrynczewski).
![Ocena CR](for_README/img.png)
> [*Super projekt! Trzymacie bardzo wysoki poziom jak na pierwszy projekt w Django. Gratuluję 🥇 Tak trzymać
👍*](https://github.com/Roger2332/Projekt_Koncowy_SDA/pull/54#pullrequestreview-2149544766)
***

## Dlaczego opracowaliśmy ten projekt?

Projekt ten powstał w celu potwierdzenia wiedzy po ukończeniu kursu SDAcademy.
***

## Zespół projektowy:

- [Roger Szwaja](https://www.linkedin.com/in/rogerszwaja)
- [Artem Monkiewicz](https://www.linkedin.com/in/artem-monkiewicz)

