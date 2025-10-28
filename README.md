# BeautyShop

BeautyShop este o platformă de comerț electronic creată cu Django, unde utilizatorii pot vizualiza produse cosmetice, adăuga în coș, cumpăra produse și gestiona comenzi.

## Funcționalități

* Listarea produselor cu categorii și filtre.
* Pagina detaliată a fiecărui produs.
* Adăugare în coș și wishlist.
* Checkout cu opțiuni de plată (Cash on Delivery sau card).
* Confirmare comenzi și vizualizare ordine.
* Recenzii pentru produse.

## Tehnologii folosite

* Python 3.13
* Django 5.2.7
* Bootstrap pentru interfață
* SQLite (sau altă bază de date, configurabilă)

## Instalare și rulare locală

1. Clonează proiectul:

```bash
git clone https://github.com/SanduAndreea22/Beautyshop.git
```

2. Accesează directorul proiectului:

```bash
cd Beautyshop
```

3. Creează un mediu virtual și activează-l:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate
```

4. Instalează dependențele:

```bash
pip install -r requirements.txt
```

5. Rulează migrările:

```bash
python manage.py migrate
```

6. Creează un superuser (administrator):

```bash
python manage.py createsuperuser
```

7. Rulează serverul:

```bash
python manage.py runserver
```

Accesează aplicația la: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Contribuții

Contribuțiile sunt binevenite! Poți deschide un Pull Request pentru a adăuga funcționalități sau a remedia bug-uri.

## Licență

Acest proiect este open-source și poate fi folosit și modificat liber.
