::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCuDJEmW+0g1PCRRXRGLOG6GBKAV5OzE7e6DnUgMQes7fbPS2buAM9wa6UrqZs5g1XJfjsoAQRlRZBO5fAp5/zoMv2eKVw==
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSzk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCuDJEmW+0g1PCRRXRGLOG6GBKAV5OzE7e6DnUgMQes7fbP+y6GHJOkS1XHrepom324UndMJbA==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off

:: Vérifier si l'environnement virtuel existe
if not exist "envScraping" (
    echo Création de l'environnement virtuel...
    python -m venv envScraping
)

:: Activer l'environnement virtuel
call envScraping\Scripts\activate

:: Installer les dépendances
pip install -r requirements.txt

:: Lancer l'application Tkinter
python equidia_toolkit.py

:: Désactiver l'environnement virtuel
deactivate

echo Fin de l'exécution du script.
pause