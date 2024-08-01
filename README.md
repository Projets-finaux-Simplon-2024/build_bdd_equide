![icons8-cheval-bizarre-96](https://github.com/user-attachments/assets/36ed1b98-ba07-4721-b91d-3ca9cae42c08)

# Agrégateur pour la bdd équidé
---
---
## :heavy_plus_sign: Présentation
Cette application a pour but de créer, agréger et peupler une base de données afin d'étudier des données équidés et plus particulièrement de la race trotteur français. La problématique de départ et d'essayer de déterminer les couples les plus optimaux afin d'obtenir des poulains tendant a avoir les qualités que l'ont recherche, pour la compétition ou pour l'élevage. Cette base de données est une esquisse et est incomplète. La bdd créer avec ce programme est pré configuré pour fonctionner avec son [:link:API équidé](https://github.com/Projets-finaux-Simplon-2024/api_equide).

---
## :heavy_plus_sign: Sources
### Sources du scraping
La source du scraping est le site de l'IFCE et notamment leur moteur de recherche. L'IFCE est une référence pour les éleveurs de chevaux. Il permet aux éleveurs de construire un annuaire et de déclarer les chevaux comme on le ferait pour les chiens avec la SCC. Cette base de données est aussi utilisée par les vétérinaires ce qui en fait une base de données relativement sourcée. Les données affichées sur le site sont soumises à autorisation des propriétaires.

[:link:https://infochevaux.ifce.fr/fr/info-chevaux](https://infochevaux.ifce.fr/fr/info-chevaux?utm_source=Effiweb&utm_medium=Menu%20SIRE%20Demarches&utm_campaign=SIRE%20%E2%80%93%20Infochevaux)

### Sources des appels API
La source des données utilisé pour faire les appels API concerne les résultats de course PMU (Pari Mutuel Urbain) trouvé sur le site [:link:developpez.net](https://www.developpez.net/forums/blogs/1191628-voroltinquo/b10558/windev-exploiter-resultat-api/) qui a déjà fait l'objet d'une étude. Cependant il n'est pas possible d'en vérifier la fiabilité.

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

---
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

---
## :heavy_plus_sign: Utilisation de l'application
L'application a été construite de façon a créer un cheminement pour la création puis l'agrégation des données dans la base de données.

### **Etape 1 : Récupération de la liste des chevaux**

*Scraping du site de l'IFCE afin d'obtenir une liste de chevaux trotteur français avec les liens IFCE correspondants dans des tables en csv*

![Capture d'écran 2024-07-30 175801](https://github.com/user-attachments/assets/16b52011-31e6-43b4-bdd6-23b5192cb111)

> [!NOTE]
> Cette page permet de
> - vérifier le temps de scraping qui peut être assez long
> - séléctionner une ou plusieurs années a scraper
> - d'utiliser les tags pour séléctionner plusieurs années
> - ouvrir le dossier résultats dans le projet qui est le dossier ou sont sauvegarder les csv par défaut

### **Etape 2 : Création d'un container postgres**

*Permet de créer un container*

![Capture d'écran 2024-07-30 175817](https://github.com/user-attachments/assets/56d158b3-e523-482c-97e2-0715bfed1816)

> [!NOTE]
> Créer un container postgres via une image postgres pull avec Docker.
> Le container est pré réglé pour être utilisé en local avec l'api tel que
> ```
> nom du container : container_equide
> POSTGRES_USER = admin 
> POSTGRES_PASSWORD = admin 
> POSTGRES_DB = bdd_equide 
> mappage des ports : 5434:5432
> ```
> On en déduit la chaîne de connexion local pour Dbeaver : ```jdbc:postgresql://localhost:5434/bdd_equide```

> [!WARNING]
> Pour une connexion entre deux containers, si on veut utiliser l'image de l'[:link:API équidé](https://github.com/Projets-finaux-Simplon-2024/api_equide) plutôt que le code. Il faut reconstruire la chaîne de connexion.
> 1. faire ```docker inspect container_equide```
> 2. récupérer la valeur de IPAddress dans le json
> 3. on récupére le port de postgres par défaut soit 5432 et **NON** le port qui a été remapper précédemment
> 4. on récupére les identifiants de la base de données ainsi que son nom
> 5. Résultat : ```postgresql://admin:admin@172.17.0.2:5432/bdd_equide``` cete chaîne de connexion et la chaîne de connexion à mettre à la création du container de l'[:link:API équidé](https://github.com/Projets-finaux-Simplon-2024/api_equide)

### **Etape 3 : Implémentation des tables**

*Permet d'implémenter les tables dans la bdd avec les contraintes*

![Capture d'écran 2024-07-30 175949](https://github.com/user-attachments/assets/c13b6311-336b-45fc-bf2e-8cd8eadca5c2)

> [!NOTE]
> Le bouton est préréglé pour implémenter les tables dans la bdd précédemment créer.
> Voir le [:link:schéma de la bdd à jour](#schéma-de-la-bdd-à-jour)

### **Etape 4 : Remplissage de la BDD avec des fichiers plats**

*Permet de remplir la table chevaux_trotteur_francais avec les csv du dossier resultats*

![Capture d'écran 2024-07-30 180007](https://github.com/user-attachments/assets/22a42ff1-f03f-4fcb-abb6-40cd482e18d3)


### **Etape 5 : Remplissage de la BDD avec une API**

*Permet de remplir les tables résultats PMU avec les appels API*

![Capture d'écran 2024-07-30 180022](https://github.com/user-attachments/assets/18718d24-352f-405e-bd7a-758988648314)

> [!NOTE]
> Les tables remplis sont remplis avec les endpoints de l'api PMU tel que :
> - **programme des courses avec le endpoint jour** : permet de construire une table avec un id issu de la date. Nécéssaire pour l'identification de la date d'une course.
> - **reunion avec le endpoint reunion** : permet de construire une table qui liste les reunions et associe un id reunion issu de l'id date de la table précédente.
> - **courses avec le endpoint courses** : permet de récupérer toute les courses par id de reunion. 
> - **participations avec le endpoint participation** : permet de récupérer toute les participations par id de course.
>
> (Une journée peut avoir plusieurs réunion, une réunion peut avoir plusieurs courses, une course a plusieurs participants.)
>
> Le **bouton purge** permet de vider ces tables en suivant les contraintes de relation puis en réinitialisant les id auto incrémenté (NE PAS EN ABUSER, si nécéssaire reconstruire la bdd)
---

### **Message d'erreur : Container éteint**

*Renvoi une page d'erreur si le container est éteint*

![Capture d'écran 2024-07-30 180053](https://github.com/user-attachments/assets/0122fff9-bccd-4a76-ba79-1f83f45f1e37)

### **Message d'erreur : Le container n'est pas créer**

*Renvoi une page d'erreur si le container n'est pas créer ou n'est pas trouver avec les préréglages*

![Capture d'écran 2024-07-30 175844](https://github.com/user-attachments/assets/5af0a7ee-9f6c-4e19-a12f-78d2cb3cfc3a)

---
## :heavy_plus_sign: Annexes
### Librairies
:computer:**Système**
- **Flask** : Framework web léger permettant de créer des applications web et des API.
- **Webview** : Librairie permettant d'intégrer des composants d'interface utilisateur web dans des applications de bureau.

:floppy_disk:**Traitement(scraping)**
- **Selenium** : Outil pour l'automatisation des navigateurs web, utilisé pour tester des applications web ou extraire des données.
- **BeautifulSoup** : Librairie pour le parsing et l'extraction de données de fichiers HTML et XML.

:microscope:**Exploration**
- **Jupyter** : Interface interactive pour l'exécution de code Python, utilisée pour le prototypage, les tests et la documentation.

### Schéma de la bdd à jour
![Diagram equide](https://github.com/user-attachments/assets/5f1cfdfa-f856-4a7c-9436-9052a32b7c72)
