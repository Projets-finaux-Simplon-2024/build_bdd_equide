# API de la base de données équidé
## :heavy_plus_sign: Présentation
Cette application a pour but de créer, agréger et peupler une base de données afin d'étudier des données équidés et plus particulièrement de la race trotteur français. La problématique de départ et d'essayer de déterminer les couples les plus optimaux afin d'obtenir des poulains tendant a avoir les qualités que l'ont recherche, pour la compétition ou pour l'élevage. Cette base de données est une esquisse et est incomplète.

## :heavy_plus_sign: Sources
### Sources du scraping
La source du scraping est le site de l'IFCE et notamment leur moteur de recherche. L'IFCE est une référence pour les éleveurs de chevaux. Il permet aux éleveurs de construire un annuaire et de déclarer les chevaux comme on le ferait pour les chiens avec la SCC. Cette base de données est aussi utilisée par les vétérinaires ce qui en fait une base de données relativement sourcée. Les données affichées sur le site sont soumises à autorisation des propriétaires.

[:link:https://infochevaux.ifce.fr/fr/info-chevaux](https://infochevaux.ifce.fr/fr/info-chevaux?utm_source=Effiweb&utm_medium=Menu%20SIRE%20Demarches&utm_campaign=SIRE%20%E2%80%93%20Infochevaux)

### Sources des appels API
La source des données utilisé pour faire les appels API concerne les résultats de course PMU (Pari Mutuel Urbain) trouvé sur le site [developpez.net](https://www.developpez.net/forums/blogs/1191628-voroltinquo/b10558/windev-exploiter-resultat-api/) qui a déjà fait l'objet d'une étude. Cependant il n'est pas possible d'en vérifier la fiabilité.

> [!NOTE]
> ## Documentation reconstitué de l'API PMU
> ### **Endpoint jour**
> - endpoint qui affiche l'ensemble des réunions de la journée 
> - Exemple : https://offline.turfinfo.api.pmu.fr/rest/client/5/programme/01032013
>
> ### **Endpoint réunion**
> - endpoint qui affiche le programme des courses de la réunion avec pour numéro 1 (R1) du jour 01032013
> - Exemple : https://offline.turfinfo.api.pmu.fr/rest/client/5/programme/01032013/R1
>
> ### **Endpoint courses**
> - endpoint qui affiche le détail de la course 1 (C1) de la réunion 1 (R1) du jour 01032013
> - Exemple : https://offline.turfinfo.api.pmu.fr/rest/client/5/programme/01032013/R1/C1
>
> ### **Endpoint participations**
> - endpoint qui affiche le détails des participants à la course C1 de R1 du 01032013
> - Exemple : https://offline.turfinfo.api.pmu.fr/rest/client/7/programme/01032013/R1/C1/participants
>
> En faisant varier des éléments de l'url on réussi a reconstitué la base de données
> `https://offline.turfinfo.api.pmu.fr/rest/client/7/programme[jour]/[reunbion]/[course]/participants`


### Autres sources à exploiter
Pour vérifier la fiabilité des résultats aux courses du PMU on pourrais croiser avec une autre source incontournable des éleveurs de chevaux de la race trotteur francais : [:link:www.letrot.com](https://www.letrot.com/)


## :heavy_plus_sign: Installlation
### Prérequis
Pour faire fonctionner le programme il est nécéssaire d'avoir Python et [:link:Docker](https://docs.docker.com/desktop/).

> [!IMPORTANT]
> La version actuelle de Python pour l'application est la [:link:version 3.9.13](https://www.python.org/downloads/release/python-3913/). Le fonctionnement dans d'autres versions n'est pas garanti !

### Récupération de l'application **SANS** Git :surfer:
Pour récupérer l'application sans Git il faut télécharger le zip

![Capture d'écran 2024-07-30 172651](https://github.com/user-attachments/assets/3c6d65c4-b747-4d28-b2cd-cbfe88b2f79b)

Puis de le décompresser ou vous le souhaitez !


### Récupération de l'application **AVEC** Git :octocat:

1. Installer [:link:Git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)
2. Ouvrir un terminal et se mettre à l'endroit où on veux installer le projet.
3. Effectuer la commande ```git clone https://github.com/Projets-finaux-Simplon-2024/build_bdd_equide.git```

### Démarrage de l'application
Si vous avez windows vous pouvez simplement utiliser le .bat(avec terminal) ou le .exe(sans terminal).

![Capture d'écran 2024-07-30 172740](https://github.com/user-attachments/assets/38082fe4-8c23-460b-b48f-9803fddf43dd)

> [!IMPORTANT]
> Sous linux vous devrez effectuer les commandes suivantes dans le répertoire du projet
> 
> - ```python -m venv envScraping``` : Création de l'environnement python
> - ```source envScraping/bin/activate``` : Activation de l'environnement virtuel
> - ```pip install -r requirements.txt``` : Installation des dépendances
> - ```python equidia_toolkit.py``` : Lancement de l'application

> [!CAUTION]
> Chromedriver peut poser problème au démarrage de l'application même s'il est embarqué et peut nécessiter le changement de la variable CHROME_DRIVER dans tools_scraping/con_ifce.py vers un autre chromedriver.exe.

## :heavy_plus_sign: Utilisation de l'application
L'application a été construite de façon a créer un cheminement pour la création puis l'agrégation des données dans la base de données.

**Etape 1 : Récupération de la liste des chevaux**

*Scraping du site de l'IFCE afin d'obtenir une liste de chevaux trotteur français avec les liens IFCE correspondants dans des tables en csv*

![Capture d'écran 2024-07-30 175801](https://github.com/user-attachments/assets/16b52011-31e6-43b4-bdd6-23b5192cb111)

> [!NOTE]
> Cette page permet de
> - vérifier le temps de scraping qui peut être assez long
> - séléctionner une ou plusieurs années a scraper
> - d'utiliser les tags pour séléctionner plusieurs années
> - ouvrir le dossier résultats dans le projet qui est le dossier ou sont sauvegarder les csv par défaut

**Etape 2 : Création d'un container postgres**

**Etape 3 : Implémentation des tables**

**Etape 4 : Remplissage de la BDD avec des fichiers plats**

**Etape 5 : Remplissage de la BDD avec une API**

## :heavy_plus_sign: Annexes
### Librairies
:computer:**Système**
flask
webview

:floppy_disk:**Traitement**
sélénium
beautifoulsoup

:mag_right:**Tests**
jupyter
