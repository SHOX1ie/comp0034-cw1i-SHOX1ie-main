# Helper classes and functions for the application
import csv
from pathlib import Path


# Add data to the database if it does not already exist
def add_data(db):
    """Adds data to the database if it does not already exist."""

    # Add import here and not at the top of the file to avoid circular import
    # issues
    from src.models import Age_group, Gender, Ethnicity, Employment, \
        Course_level, Teacher, Disability

    # If there are no age groups in the database, then add them
    first_age = db.session.execute(db.select(Age_group)).first()
    if not first_age:
        print("Start adding age group data to the database")
        df_prepared = Path(__file__).parent.parent.joinpath("data",
                                                            "df_prepared.csv")
        with open(df_prepared, 'r') as file:
            csv_dict_reader = csv.DictReader(file)
            for row in csv_dict_reader:
                a = Age_group(time_period=row['time_period'],
                              pct_total_age_u25=row['pct_total_age_u25'],
                              pct_total_age_25andover=row[
                                  'pct_total_age_25andover'])
                db.session.add(a)
            db.session.commit()

    # If there are no gender groups in the database, then add them
    first_gender = db.session.execute(db.select(Gender)).first()
    if not first_gender:
        print("Start adding gender group data to the database")
        df_prepared = Path(__file__).parent.parent.joinpath("data",
                                                            "df_prepared.csv")
        with open(df_prepared, 'r') as file:
            csv_dict_reader = csv.DictReader(file)
            for row in csv_dict_reader:
                g = Gender(time_period=row['time_period'],
                           pct_total_sex_m=row['pct_total_sex_m'],
                           pct_total_sex_f=row['pct_total_sex_f'])
                db.session.add(g)
            db.session.commit()

    # If there are no ethnicity groups in the database, then add them
    first_ethnicity = db.session.execute(db.select(Ethnicity)).first()
    if not first_ethnicity:
        print("Start adding ethnicity group data to the database")
        df_prepared = Path(__file__).parent.parent.joinpath("data",
                                                            "df_prepared.csv")
        with open(df_prepared, 'r') as file:
            csv_dict_reader = csv.DictReader(file)
            for row in csv_dict_reader:
                e = Ethnicity(time_period=row['time_period'],
                              pct_total_ethnic_asian=row[
                                  'pct_total_ethnic_asian'],
                              pct_total_ethnic_black=row[
                                  'pct_total_ethnic_black'],
                              pct_total_ethnic_white=row[
                                  'pct_total_ethnic_white'],
                              pct_total_ethnic_mixed_ethnicity=row[
                                  'pct_total_ethnic_mixed_ethnicity'],
                              pct_total_ethnic_other=row[
                                  'pct_total_ethnic_other'],
                              pct_total_ethnic_unknown=row[
                                  'pct_total_ethnic_unknown'])
                db.session.add(e)
            db.session.commit()


# If there are no employment groups in the database, then add them
    first_employment = db.session.execute(db.select(Employment)).first()
    if not first_employment:
        print("Start adding employment group data to the database")
        df_prepared = Path(__file__).parent.parent.joinpath("data",
                                                            "df_prepared.csv")
        with open(df_prepared, 'r') as file:
            csv_dict_reader = csv.DictReader(file)
            for row in csv_dict_reader:
                em = Employment(time_period=row['time_period'],
                                employment_status=row['employment_status'])
                db.session.add(em)
            db.session.commit()


# If there are no course_level groups in the database, then add them
    first_course_level = db.session.execute(db.select(Course_level)).first()
    if not first_course_level:
        print("Start adding course_level group data to the database")
        df_prepared = Path(__file__).parent.parent.joinpath("data",
                                                            "df_prepared.csv")
        with open(df_prepared, 'r') as file:
            csv_dict_reader = csv.DictReader(file)
            for row in csv_dict_reader:
                c = Course_level(time_period=row['time_period'],
                                 course_level_recoded=row[
                                     'course_level_recoded'])
                db.session.add(c)
            db.session.commit()


# If there are no disability groups in the database, then add them
    first_disability = db.session.execute(db.select(Disability)).first()
    if not first_disability:
        print("Start adding disability group data to the database")
        df_prepared = Path(__file__).parent.parent.joinpath("data",
                                                            "df_prepared.csv")
        with open(df_prepared, 'r') as file:
            csv_dict_reader = csv.DictReader(file)
            for row in csv_dict_reader:
                d = Disability(time_period=row['time_period'],
                               pct_total_disability=row[
                                   'pct_total_disability'],
                               pct_total_nondisability=row[
                                   'pct_total_nondisability'],
                               pct_total_disability_unknown=row[
                                   'pct_total_disability_unknown'])
                db.session.add(d)
            db.session.commit()


# If there are no teacher groups in the database, then add them
    first_teacher = db.session.execute(db.select(Teacher)).first()
    if not first_teacher:
        print("Start adding teacher group data to the database")
        df_prepared = Path(__file__).parent.parent.joinpath("data",
                                                            "df_prepared.csv")
        with open(df_prepared, 'r') as file:
            csv_dict_reader = csv.DictReader(file)
            for row in csv_dict_reader:
                t = Teacher(time_period=row['time_period'],
                            qts_status=row['qts_status'],
                            n_total=row['n_total'])
                db.session.add(t)
            db.session.commit()
