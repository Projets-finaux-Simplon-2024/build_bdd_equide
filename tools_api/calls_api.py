import requests
import pandas as pd
from datetime import datetime, timedelta


# Initialiser les DataFrames
df_programmes = pd.DataFrame(columns=["id_programme", "date_programme"])
df_reunions = pd.DataFrame(columns=["id_reunion", "id_programme", "num_officiel", "nature", "code_hippodrome", "libelle_court_hippodrome", "libelle_long_hippodrome", "code_pays", "libelle_pays", "audience", "statut", "disciplines_mere", "specialites", "meteo_nebulosite_code", "meteo_nebulosite_Libelle_Court", "meteo_nebulosite_Libelle_Long", "meteo_temperature", "meteo_force_vent", "meteo_direction_vent"])
df_courses = pd.DataFrame(columns=["id_course", "id_reunion", "num_course", "nom_course", "distance", "allocation"])

# Date du premier enregistrement 19-02-2013
# Nombre d'enregistrements = 4161 (environ 11 ans)
id_programme = 19022013

# Obtenir la date d'aujourd'hui au format JJMMYYYY
# date_fin = datetime.now().strftime("%d%m%Y")

# URL avec la date de début
url = f"https://offline.turfinfo.api.pmu.fr/rest/client/7/programme/{id_programme}"

# Récupération du Json
response = requests.get(url)

if response.status_code == 200:
    json_data = response.json()

    # Extraire les informations du programme
    date_programme_timestamp = json_data["programme"]["date"]//1000
    date_programme = datetime.fromtimestamp(date_programme_timestamp).date()

     # Format personnalisé de la date en français
    date_programme_fr = date_programme.strftime("%d-%m-%Y")

    # Afficher les informations du programme
    print(f"Id du programme : {id_programme} | Date du programme : {date_programme_fr}")

    # Ajouter les informations du programme au DataFrame
    df_programmes = pd.concat([df_programmes, pd.DataFrame([{"id_programme": id_programme, "date_programme": date_programme_fr}])], ignore_index=True)


    # Extraire les informations des réunions
    reunions_data = []
    for reunion in json_data["programme"]["reunions"]:
        # id_reunion est date + numeroe de la reunion exemple 19022013R1
        id_reunion = f"{id_programme}R{reunion.get('numOfficiel')}" 
        reunion_data = {
            "num_officiel": reunion.get("numOfficiel"),
            "nature": reunion.get("nature"),
            "code_hippodrome": reunion["hippodrome"].get("code"),
            "libelle_court_hippodrome": reunion["hippodrome"].get("libelleCourt"),
            "libelle_long_hippodrome": reunion["hippodrome"].get("libelleLong"),
            "code_pays": reunion["pays"].get("code"),
            "libelle_pays": reunion["pays"].get("libelle"),
            "audience": reunion.get("audience"),
            "statut": reunion.get("statut"),
            "disciplines_mere": reunion.get("disciplinesMere"),
            "specialites": reunion.get("specialites"),
            "meteo_nebulosite_code": reunion.get("meteo", {}).get("nebulositeCode"),
            "meteo_nebulosite_Libelle_Court": reunion.get("meteo", {}).get("nebulositeLibelleCourt"),
            "meteo_nebulosite_Libelle_Long": reunion.get("meteo", {}).get("nebulositeLibelleLong"),
            "meteo_temperature": reunion.get("meteo", {}).get("temperature"),
            "meteo_force_vent": reunion.get("meteo", {}).get("forceVent"),
            "meteo_direction_vent": reunion.get("meteo", {}).get("directionVent")
        }
        reunions_data.append(reunion_data)
        df_reunions = pd.concat([df_reunions, pd.DataFrame([reunion_data])], ignore_index=True)


    # Afficher les informations des réunions
    for reunion in reunions_data:
        print("--------------------------------------------------------------------------------------------------------------------->")
        print(f"id_programme : {id_programme} | date_programmation : {date_programme_fr} | num_reunion : {reunion["num_officiel"]}")
        print(f"code_hippodrome : {reunion["code_hippodrome"]} | libelle_court_hippodrome : {reunion["libelle_court_hippodrome"]} | libelle_long_hippodrome : {reunion["libelle_long_hippodrome"]}")
        print(f"audience : {reunion["audience"]} | nature : {reunion["nature"]} | statut : {reunion["statut"]} | disciplines_mere : {reunion["disciplines_mere"]}")
        print(f"specialites : {reunion["specialites"]} | meteo_nebulosite_code : {reunion["meteo_nebulosite_code"]} | meteo_nebulosite_Libelle_Court : {reunion["meteo_nebulosite_Libelle_Court"]}")
        print(f"meteo_nebulosite_Libelle_Long : {reunion["meteo_nebulosite_Libelle_Long"]} | meteo_temperature : {reunion["meteo_temperature"]} | meteo_force_vent : {reunion["meteo_force_vent"]} | meteo_direction_vent : {reunion["meteo_direction_vent"]}")
        print("---------------------------------------------------------------------------------------------------------------------<")

        # URL pour les détails des courses de la réunion
        num_reunion = reunion['num_officiel']
        url_courses = f"https://offline.turfinfo.api.pmu.fr/rest/client/7/programme/{id_programme}/R{num_reunion}"
            
        # Récupérer les données JSON pour les courses
        response_courses = requests.get(url_courses)
        
        if response_courses.status_code == 200:
            courses_data = response_courses.json()
            # Traitez les données des courses ici
            print(f"Détails des courses pour la réunion {num_reunion} : {courses_data}")
        else:
            print(f"Échec de la récupération des données des courses pour la réunion {num_reunion}, code de statut : {response_courses.status_code}")
else:
    print(f"Échec de la récupération des données, code de statut : {response.status_code}")

# Afficher les DataFrames
print(df_programmes.head())
print(df_reunions.head())
