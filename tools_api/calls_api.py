import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

LAST_RUN_FILE = 'last_run_date.txt'

def read_last_run_date():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, 'r') as file:
            return file.read().strip()
    return '19022013'

def write_last_run_date(date_str):
    with open(LAST_RUN_FILE, 'w') as file:
        file.write(date_str)

def check_date_exists(engine, date_str):
    query = text("SELECT EXISTS (SELECT 1 FROM programmes_des_courses WHERE date_programme = :date_programme)")
    with engine.connect() as conn:
        result = conn.execute(query, {'date_programme': date_str}).scalar()
    return result

def call_api():

    # Connexion à la base de données avec SQLAlchemy
    engine = create_engine('postgresql://admin:admin@localhost:5434/bdd_equide')
    session_maked = sessionmaker(bind=engine)
    session = session_maked()

    # Initialiser les DataFrames
    df_programmes = pd.DataFrame()
    df_reunions = pd.DataFrame()
    df_courses = pd.DataFrame()
    df_participations = pd.DataFrame()

    id_course = 0

    # Lire la date de début à partir du fichier ou définir une date par défaut (Date du premier enregistrement 19-02-2013)
    start_date_str = read_last_run_date()
    start_date = datetime.strptime(start_date_str, "%d%m%Y")

    # Vérifier si la date existe déjà
    if check_date_exists(engine, start_date):
        print(f"Les données pour la date {start_date} existent déjà, passage à la date suivante.")
        start_date += timedelta(days=1)
    
    end_date = datetime.now()

    current_date = start_date

    while current_date <= end_date:
        id_programme = current_date.strftime("%d%m%Y")

        # URL avec la date de début
        url = f"https://offline.turfinfo.api.pmu.fr/rest/client/7/programme/{id_programme}"

        # Récupération du Json
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()

            #------------------------------------------------------------------- Construction de la table programme -------------------------------------------------------------------
            # Extraire les informations du programme
            date_programme_timestamp = json_data["programme"]["date"] // 1000
            date_programme = datetime.fromtimestamp(date_programme_timestamp).date()

            # Format personnalisé de la date en français
            date_programme_fr = date_programme.strftime("%Y-%m-%d")

            # Afficher les informations du programme
            df_programmes = pd.concat([df_programmes, pd.DataFrame([{"id_programme": id_programme, "date_programme": date_programme_fr}])], ignore_index=True)
            #------------------------------------------------------------------- Construction de la table programme -------------------------------------------------------------------

            #------------------------------------------------------------------- Construction de la table reunions --------------------------------------------------------------------

            for reunion in json_data["programme"]["reunions"]:
                
                discipline_mere = ', '.join(reunion.get("disciplinesMere", []))
                specialites = reunion.get("specialites", [])

                # Assurez-vous d'avoir suffisamment d'éléments, sinon remplissez avec None
                specialites_padded = specialites + [None] * (4 - len(specialites))

                reunion_data = {
                    # id_reunion est date + numero de la reunion exemple 19022013R1
                    "id_reunion": f"{id_programme}R{reunion.get('numOfficiel')}",
                    "id_programme": id_programme,
                    "num_officiel": reunion.get("numOfficiel"),
                    "nature": reunion.get("nature"),
                    "code_hippodrome": reunion.get("hippodrome", {}).get("code"),
                    "libelle_court_hippodrome": reunion.get("hippodrome", {}).get("libelleCourt"),
                    "libelle_long_hippodrome": reunion.get("hippodrome", {}).get("libelleLong"),
                    "code_pays": reunion["pays"].get("code"),
                    "libelle_pays": reunion["pays"].get("libelle"),
                    "audience": reunion.get("audience"),
                    "statut": reunion.get("statut"),
                    "disciplines_mere": discipline_mere,
                    "specialite_1": specialites_padded[0],
                    "specialite_2": specialites_padded[1],
                    "specialite_3": specialites_padded[2],
                    "specialite_4": specialites_padded[3],
                    "meteo_nebulosite_code": reunion.get("meteo", {}).get("nebulositeCode"),
                    "meteo_nebulosite_Libelle_Court": reunion.get("meteo", {}).get("nebulositeLibelleCourt"),
                    "meteo_nebulosite_Libelle_Long": reunion.get("meteo", {}).get("nebulositeLibelleLong"),
                    "meteo_temperature": reunion.get("meteo", {}).get("temperature"),
                    "meteo_force_vent": reunion.get("meteo", {}).get("forceVent"),
                    "meteo_direction_vent": reunion.get("meteo", {}).get("directionVent")
                }

                df_reunions = pd.concat([df_reunions, pd.DataFrame([reunion_data])], ignore_index=True)
                #------------------------------------------------------------------- Construction de la table reunions --------------------------------------------------------------------




                #------------------------------------------------------------------- Construction de la table courses --------------------------------------------------------------------
                num_reunion = reunion_data['num_officiel']
                url_courses = f"https://offline.turfinfo.api.pmu.fr/rest/client/7/programme/{id_programme}/R{num_reunion}"

                # Récupération du Json
                response_courses = requests.get(url_courses)

                if response_courses.status_code == 200:
                    json_data_courses = response_courses.json()
                

                    for course in json_data_courses["courses"]:
                        id_course += 1
                        heure_depart_timestamp = course.get("heureDepart", 0) // 1000

                        # Gérer les timestamps négatifs
                        if heure_depart_timestamp < 0:
                            heure_depart = None
                        else:
                            heure_depart = datetime.fromtimestamp(heure_depart_timestamp).time()

                        # Convertir dureeCourse de millisecondes à un format lisible
                        duree_course_ms = course.get("dureeCourse", 0)
                        duree_course_minutes, duree_course_seconds = divmod(duree_course_ms // 1000, 60)
                        duree_course_formatted = f"{duree_course_minutes}m {duree_course_seconds}s"

                        # Extraction des incidents
                        incidents_list = course.get("incidents", [])
                        incidents_type = [incident.get("type") for incident in incidents_list] if isinstance(incidents_list, list) else []
                        incidents_participants = [incident.get("numeroParticipants") for incident in incidents_list] if isinstance(incidents_list, list) else []

                        # Conversion des listes en chaînes de caractères
                        incidents_type_str = ' | '.join(incidents_type)
                        incidents_participants_str = ' | '.join([', '.join(map(str, participants)) for participants in incidents_participants])

                        # Gestion des spécialités
                        specialites = reunion.get("specialites", [None, None])  
                        specialite_1 = specialites[0] if len(specialites) > 0 else None
                        specialite_2 = specialites[1] if len(specialites) > 1 else None

                        # Récupération des ordres d'arrivée
                        ordre_arrivee = course.get("ordreArrivee", [])
                        ordre_arrivee_padded = [ordre[0] if isinstance(ordre, list) else ordre for ordre in (ordre_arrivee + [None] * (5 - len(ordre_arrivee)))]

                        # Tronquer les conditions si nécessaire
                        conditions = course.get("conditions", "")
                        if len(conditions) > 3000:
                            conditions = conditions[:3000]

                        course_data = {
                            "id_course":id_course,
                            "id_reunion": reunion_data['id_reunion'],
                            "libelle": course.get("libelle"),
                            "libelle_court": course.get("libelleCourt"),
                            "heure_depart": heure_depart,
                            "parcours": course.get("parcours"),
                            "distance": course.get("distance"),
                            "distance_unit": course.get("distanceUnit"),
                            "corde": course.get("corde"),
                            "discipline": course.get("discipline"),
                            "specialite_1": specialite_1,
                            "specialite_2": specialite_2,
                            "condition_sexe": course.get("conditionSexe"),
                            "conditions": conditions,
                            "statut": course.get("statut"),
                            "categorie_statut": course.get("categorieStatut"),
                            "duree_course": course.get("dureeCourse"),
                            "duree_course_en_minute":duree_course_formatted,
                            "montant_prix": course.get("montantPrix"),
                            "grand_prix_national_trot": course.get("grandPrixNationalTrot"),
                            "nombre_declares_partants": course.get("nombreDeclaresPartants"),
                            "montant_total_offert": course.get("montantTotalOffert"),
                            "premier": ordre_arrivee_padded[0],
                            "montant_offert_1er": course.get("montantOffert1er"),
                            "deuxieme": ordre_arrivee_padded[1],
                            "montant_offert_2eme": course.get("montantOffert2eme"),
                            "troisieme": ordre_arrivee_padded[2],
                            "montant_offert_3eme": course.get("montantOffert3eme"),
                            "quatrieme": ordre_arrivee_padded[3],
                            "montant_offert_4eme": course.get("montantOffert4eme"),
                            "cinquieme": ordre_arrivee_padded[4],
                            "montant_offert_5eme": course.get("montantOffert5eme"),
                            "incidents_type": incidents_type_str,
                            "incidents_participants": incidents_participants_str,
                        }

                        df_courses = pd.concat([df_courses, pd.DataFrame([course_data])], ignore_index=True)
                        #------------------------------------------------------------------- Construction de la table courses --------------------------------------------------------------------


                        #------------------------------------------------------------------- Construction de la table participations -------------------------------------------------------------
                        num_course = course.get("numOrdre")
                        url_participants = f"https://offline.turfinfo.api.pmu.fr/rest/client/7/programme/{id_programme}/R{num_reunion}/C{num_course}/participants"

                        # Récupération du Json
                        response_participants = requests.get(url_participants)

                        if response_participants.status_code == 200:
                            json_data_participants = response_participants.json()

                            for participant in json_data_participants["participants"]:

                                # Convertir dureeCourse de millisecondes à un format lisible
                                temps_obtenu_ms = participant.get("tempsObtenu", 0)
                                temps_obtenu_minutes, temps_obtenu_seconds = divmod(temps_obtenu_ms // 1000, 60)
                                temps_obtenu_formatted = f"{temps_obtenu_minutes}m {temps_obtenu_seconds}s"

                                participation_data = {
                                    "id_course": id_course,
                                    "nom": participant.get("nom"),
                                    "numero_cheval": participant.get("numPmu"),
                                    "age": participant.get("age"),
                                    "sexe": participant.get("sexe"),
                                    "race": participant.get("race"),
                                    "statut_au_depart": participant.get("statut"),
                                    "proprietaire": participant.get("proprietaire"),
                                    "entraineur": participant.get("entraineur"),
                                    "driver": participant.get("driver"),
                                    "driverChange": participant.get("driverChange"),
                                    "code_robe": participant.get("robe", {}).get("code"),
                                    "libelle_court_robe": participant.get("robe", {}).get("libelleCourt"),
                                    "libelle_long_robe": participant.get("robe", {}).get("libelleLong"),
                                    "nombre_courses": participant.get("nombreCourses"),
                                    "nombre_victoires": participant.get("nombreVictoires"),
                                    "nombre_places": participant.get("nombrePlaces"),
                                    "nom_pere": participant.get("nomPere"),
                                    "nom_mere": participant.get("nomMere"),
                                    "place_dans_la_course": participant.get("ordreArrivee"),
                                    "jument_pleine": participant.get("jumentPleine"),
                                    "engagement": participant.get("engagement"),
                                    "supplement": participant.get("supplement"),
                                    "handicap_distance": participant.get("handicapDistance"),
                                    "poids_condition_monte_change": participant.get("poidsConditionMonteChange"),
                                    "temps_obtenu": participant.get("tempsObtenu"),
                                    "temps_obtenu_en_minute": temps_obtenu_formatted,
                                    "reduction_kilometrique": participant.get("reductionKilometrique"),
                                    "allure": participant.get("allure"),
                                }
                                df_participations = pd.concat([df_participations, pd.DataFrame([participation_data])], ignore_index=True)


                        #------------------------------------------------------------------- Construction de la table participations -------------------------------------------------------------
            
            # Sauvegarde des données en base à chaque itération
            df_programmes.to_sql('programmes_des_courses', engine, if_exists='append', index=False)
            df_reunions.to_sql('reunion', engine, if_exists='append', index=False)
            df_courses.to_sql('courses', engine, if_exists='append', index=False)
            df_participations.to_sql('participations_aux_courses', engine, if_exists='append', index=False)

            # Réinitialiser les DataFrames après chaque itération
            df_programmes = pd.DataFrame()
            df_reunions = pd.DataFrame()
            df_courses = pd.DataFrame()
            df_participations = pd.DataFrame()

            # Mettre à jour le fichier avec la date actuelle
            write_last_run_date(current_date.strftime("%d%m%Y"))

        else:
            print(f"Échec de la récupération des données, code de statut : {response.status_code}")

        # Passer à la date suivante
        current_date += timedelta(days=1)

    session.close()
    message = "Remplissage terminé"

    return message