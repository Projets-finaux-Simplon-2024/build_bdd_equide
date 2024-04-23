# Imports -------------------------------------------------------------------------------------------------------------------------------------------
from selenium.webdriver.common.by import By
#----------------------------------------------------------------------------------------------------------------------------------------------------


def cut_article(article) :

    # Initialisation des variables
    nom_cheval = race = sexe = couleur = annee_str = naisseur = date_deces = "Non renseigné"
    parent1_name = parent1_race = parent2_name = parent2_race = "Non renseigné"
    lien_cheval = article.find_element(By.CSS_SELECTOR, 'a.strong.text-uppercase').get_attribute('href')

    infos_article = article.text.split('\n')
    for info in infos_article:
        # Extraction des informations de base
        if ',' in info and 'Par' not in info:  # Cette ligne devrait contenir les informations principales
            nom_cheval, race, sexe, couleur, annee_str = [detail.strip() for detail in info.split(',')[:5]]

        # Extraction des informations sur les parents
        elif info.startswith('Par'):
            parent_info = info.split(' et ')
            if len(parent_info) > 0:
                parent1_info = parent_info[0].split(' par ')[0].strip()
                parent1_name = ' '.join(parent1_info.split(' ')[1:-1])
                parent1_race = parent1_info.split(' ')[-1].strip('()')

            if len(parent_info) > 1:
                parent2_info = parent_info[1].split(' par ')[0].strip()
                parent2_name = ' '.join(parent2_info.split(' ')[1:-1])
                parent2_race = parent2_info.split(' ')[-1].strip('()')

        # Extraction de la date de décès et du naisseur
        elif info.startswith("Enregistré(e) mort(e) le"):
            date_deces = info.replace("Enregistré(e) mort(e) le", "").strip()
        elif info.startswith("Naisseur :"):
            naisseur = info.replace("Naisseur :", "").strip()

    return nom_cheval, race, sexe, couleur, annee_str, parent1_name, parent1_race, parent2_name, parent2_race, date_deces, naisseur, lien_cheval