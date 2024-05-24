from selenium.webdriver.common.by import By

def cut_article(article):
    # Initialisation des variables
    nom_cheval = race = sexe = couleur = annee_str = naisseur = date_deces = "Non renseigné"
    parent1_name = parent2_name = "Non renseigné"
    lien_cheval = article.find_element(By.CSS_SELECTOR, 'a.strong.text-uppercase').get_attribute('href')

    infos_article = article.text.split('\n')

    for info in infos_article:
        # Extraction des informations de base
        if ',' in info and 'Par' not in info:  # Cette ligne devrait contenir les informations principales
            parts = [detail.strip() for detail in info.split(',') if detail.strip()]
            if len(parts) >= 5:
                nom_cheval, race, sexe, couleur, annee_str = parts[:5]
            else:
                print(f"Données insuffisantes pour déballage complet : {parts}")

        # Extraction des informations sur les parents
        elif info.startswith('Par'):
            # Scinder les informations des parents
            parent_parts = info.replace('Par ', '').split(' et ')
            if len(parent_parts) >= 1:
                # Nettoyer le nom du premier parent pour enlever 'TF'
                parent1_name = parent_parts[0].split(' par ')[0].strip()
                if parent1_name.endswith(" TF"):
                    parent1_name = parent1_name[:-3].strip()

            if len(parent_parts) > 1:
                # Nettoyer le nom du second parent pour enlever 'TF'
                parent2_name = parent_parts[1].split(' par ')[0].strip()
                if parent2_name.endswith(" TF"):
                    parent2_name = parent2_name[:-3].strip()

        # Extraction de la date de décès et du naisseur
        elif "Enregistré(e) mort(e) le" in info:
            date_deces = info.replace("Enregistré(e) mort(e) le", "").strip()
        elif "Naisseur :" in info:
            naisseur = info.replace("Naisseur :", "").strip()

    return nom_cheval, race, sexe, couleur, annee_str, parent1_name, parent2_name, date_deces, naisseur, lien_cheval
