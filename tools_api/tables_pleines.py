from sqlalchemy import create_engine, inspect

def tables_pleines():

    # Connexion à la base de données
    engine = create_engine('postgresql://admin:admin@localhost:5434/bdd_equide')

    inspector = inspect(engine)
    tables = ["participations_aux_courses", "courses", "reunion", "programmes_des_courses"]

    with engine.connect() as connection:
        for table_name in tables:
            count_query = f"SELECT COUNT(*) FROM {table_name}"
            result = connection.execute(count_query)
            count = result.fetchone()[0]
            if count > 0:
                return True
    return False
