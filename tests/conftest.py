import os
import string
import secrets
from pathlib import Path

import pytest
from faker import Faker
from sqlalchemy import exists
from src import create_app, db
from src.models import User, Feedback, Age_group, Gender, Ethnicity, \
    Employment, Course_level, Teacher, Disability

from src.schemas import UserSchema, FeedbackSchema, Age_groupSchema, \
    GenderSchema, EthnicitySchema, EmploymentSchema, Course_levelSchema, \
    TeacherSchema, DisabilitySchema


@pytest.fixture(scope='session')
def app():
    """Fixture that creates a test app.

    The app is created with test config parameters that include a temporary
    database. The app is created once for
    each test module.

    Returns:
        app A Flask app with a test config

    """
    # See https://flask.palletsprojects.com/en/2.3.x/tutorial/tests/#id2
    # Create a temporary testing database
    db_path = Path(__file__).parent.parent.joinpath('data',
                                                    'src_testdb.sqlite')
    test_cfg = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(db_path),
        # "SQLALCHEMY_ECHO": True
    }
    app = create_app(test_config=test_cfg)

    yield app

    # clean up / reset resources
    # Delete the test database (if adding data to your database takes a long
    # time you may prefer not to delete the
    # database)
    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


# This is an alternative to the client fixtures above, do not add this as well
# as the client fixture but use it as a replacement!
@pytest.fixture(scope='module')
def test_client(app):
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!


# Conftest fixture for User DELETE route test
@pytest.fixture(scope='function')
def new_users(app):
    """Create a new user and add to the database.

    Adds a new user to the database and also returns the JSON for a new
    user.
    """
    new_user_json = {
        "user_id": 61,
        "email": "asdk",
        "password_hash": "asdf",
        "user_name": "asfjg"
    }

    with app.app_context():
        User_schema = UserSchema()
        new_user = User_schema.load(new_user_json)
        db.session.add(new_user)
        db.session.commit()

    yield new_user_json

    # Remove the user from the database at the end of the test if it still
    # exists
    with app.app_context():
        user_exists = db.session.query(
            exists().where(User.user_id == 61)).scalar()
        if user_exists:
            db.session.delete(new_user)
            db.session.commit()


# Conftest fixture for Feedback DELETE route test
@pytest.fixture(scope='function')
def new_feedback(app):
    """Create a new feedback and add to the database.

    Adds a new feedback to the database and also returns the JSON for a new
    feedback.
    """
    new_feedback_json = {
        "feedback_id": 61,
        "feedback_time": "2021-12-01T14:30:00Z",
        "feedback_content": "This is my feedback.",
        "user_id": 30
    }

    with app.app_context():
        Feedback_schema = FeedbackSchema()
        new_feedback = Feedback_schema.load(new_feedback_json)
        db.session.add(new_feedback)
        db.session.commit()

    yield new_feedback_json

    # Remove the feedback from the database at the end of the test if it still
    # exists
    with app.app_context():
        feedback_exists = db.session.query(
            exists().where(Feedback.feedback_id == 61)).scalar()
        if feedback_exists:
            db.session.delete(new_feedback)
            db.session.commit()


# Conftest fixture for Age_group DELETE route test
@pytest.fixture(scope='function')
def new_age_group(app):
    """Create a new age_group and add to the database.

    Adds a new age_group to the database and also returns the JSON for a new
    age_group.
    """
    new_age_group_json = {'age_group_id': 61, 'time_period': 202425,
                          'pct_total_age_u25': 20,
                          'pct_total_age_25andover': 80}

    with app.app_context():
        Age_group_schema = Age_groupSchema()
        new_age_group = Age_group_schema.load(new_age_group_json)
        db.session.add(new_age_group)
        db.session.commit()

    yield new_age_group_json

    # Remove the age_group from the database at the end of the test if it still
    # exists
    with app.app_context():
        age_group_exists = db.session.query(
            exists().where(Age_group.age_group_id == 61)).scalar()
        if age_group_exists:
            db.session.delete(new_age_group)
            db.session.commit()


# Conftest fixture for Gender DELETE route test
@pytest.fixture(scope='function')
def new_gender(app):
    """Create a new gender and add to the database.

    Adds a new gender to the database and also returns the JSON for a new
    gender.
    """
    new_gender_json = {'gender_id': 61, 'time_period': 202425,
                       'pct_total_sex_m': 73, 'pct_total_sex_f': 82}

    with app.app_context():
        Gender_schema = GenderSchema()
        new_gender = Gender_schema.load(new_gender_json)
        db.session.add(new_gender)
        db.session.commit()

    yield new_gender_json

    # Remove the gender from the database at the end of the test if it still
    # exists
    with app.app_context():
        gender_exists = db.session.query(exists().where
                                         (Gender.gender_id == 61)).scalar()
        if gender_exists:
            db.session.delete(new_gender)
            db.session.commit()


# Conftest fixture for Ethnicity DELETE route test
@pytest.fixture(scope='function')
def new_ethnicity(app):
    """Create a new ethnicity and add to the database.

    Adds a new ethnicity to the database and also returns the JSON for a new
    ethnicity.
    """
    new_ethnicity_json = {'ethnicity_id': 61, 'time_period': 202425,
                          'pct_total_ethnic_asian': 73,
                          'pct_total_ethnic_black': 82,
                          'pct_total_ethnic_white': 20,
                          'pct_total_ethnic_mixed_ethnicity': 20,
                          'pct_total_ethnic_other': 10,
                          'pct_total_ethnic_unknown': 20}

    with app.app_context():
        Ethnicity_schema = EthnicitySchema()
        new_ethnicity = Ethnicity_schema.load(new_ethnicity_json)
        db.session.add(new_ethnicity)
        db.session.commit()

    yield new_ethnicity_json

    # Remove the ethnicity from the database at the end of the test if it still
    # exists
    with app.app_context():
        ethnicity_exists = db.session.query(
            exists().where(Ethnicity.ethnicity_id == 61)).scalar()
        if ethnicity_exists:
            db.session.delete(new_ethnicity)
            db.session.commit()


# Conftest fixture for Employment DELETE route test
@pytest.fixture(scope='function')
def new_employment(app):
    """Create a new employment and add to the database.

    Adds a new employment to the database and also returns the JSON for a new
    employment.
    """
    new_employment_json = {'employment_id': 61, 'time_period': 202425,
                           'employment_status': 'Teaching'}

    with app.app_context():
        Employment_schema = EmploymentSchema()
        new_employment = Employment_schema.load(new_employment_json)
        db.session.add(new_employment)
        db.session.commit()

    yield new_employment_json

    # Remove the employment from the database at the end of the test if it
    # still exists
    with app.app_context():
        employment_exists = db.session.query(
            exists().where(Employment.employment_id == 61)).scalar()
        if employment_exists:
            db.session.delete(new_employment)
            db.session.commit()


# Conftest fixture for Course_level DELETE route test
@pytest.fixture(scope='function')
def new_course_level(app):
    """Create a new course_level and add to the database.

    Adds a new course_level to the database and also returns the JSON for a new
    course_level.
    """
    new_course_level_json = {'course_level_id': 61, 'time_period': 202425,
                             'course_level_recoded': 'Undergraduate'}

    with app.app_context():
        Course_level_schema = Course_levelSchema()
        new_course_level = Course_level_schema.load(new_course_level_json)
        db.session.add(new_course_level)
        db.session.commit()

    yield new_course_level_json

    # Remove the course_level from the database at the end of the test if it
    # still exists
    with app.app_context():
        course_level_exists = db.session.query(
            exists().where(Course_level.course_level_id == 61)).scalar()
        if course_level_exists:
            db.session.delete(new_course_level)
            db.session.commit()


# Conftest fixture for Disability DELETE route test
@pytest.fixture(scope='function')
def new_disability(app):
    """Create a new disability and add to the database.

    Adds a new disability to the database and also returns the JSON for a new
    disability.
    """
    new_disability_json = {'disability_id': 61, 'time_period': 202425,
                           'pct_total_disability': 10,
                           'pct_total_nondisability': 20,
                           'pct_total_disability_unknown': 30}

    with app.app_context():
        Disability_schema = DisabilitySchema()
        new_disability = Disability_schema.load(new_disability_json)
        db.session.add(new_disability)
        db.session.commit()

    yield new_disability_json

    # Remove the disability from the database at the end of the test if it
    # still exists
    with app.app_context():
        disability_exists = db.session.query(
            exists().where(Disability.disability_id == 61)).scalar()
        if disability_exists:
            db.session.delete(new_disability)
            db.session.commit()


# Conftest fixture for Teacher DELETE route test
@pytest.fixture(scope='function')
def new_teacher(app):
    """Create a new teacher and add to the database.

    Adds a new teacher to the database and also returns the JSON for a new
    teacher.
    """
    new_teacher_json = {'teacher_id': 61, 'time_period': 202425,
                        'qts_status': 'Total',
                        'n_total': 20000}

    with app.app_context():
        Teacher_schema = TeacherSchema()
        new_teacher = Teacher_schema.load(new_teacher_json)
        db.session.add(new_teacher)
        db.session.commit()

    yield new_teacher_json

    # Remove the teacher from the database at the end of the test if it still
    # exists
    with app.app_context():
        teacher_exists = db.session.query(
            exists().where(Teacher.teacher_id == 61)).scalar()
        if teacher_exists:
            db.session.delete(new_teacher)
            db.session.commit()


# Conftest fixture for User test routes
@pytest.fixture(scope='session')
def new_user(app):
    """Create a new user and add to the database.

    Adds a new User to the database and also returns the JSON for a new user.

    The scope is session as we need the user to be there throughout for
    testing the logged in functions.

    """
    user_json = {'email': 'tester@mytesting.com',
                 'password': 'PlainTextPassword',
                 'user_name': 'test_user'}

    with app.app_context():
        user = User(email=user_json['email'], user_name=user_json['user_name'])
        user.set_password(user_json['password'])
        db.session.add(user)
        db.session.commit()

    yield user_json

    # Remove the user from the database at the end of the test if it still
    # exists
    with app.app_context():
        user_exists = db.session.query(
            exists().where(User.email == user_json['email'])).scalar()
        if user_exists:
            db.session.delete(user)
            db.session.commit()


@pytest.fixture(scope='function')
def random_user_json():
    """Generates a random email and password for testing and returns as JSON.
    """
    dummy = Faker()
    dummy_email = dummy.email()
    dummy_user_name = dummy.user_name()
    # Generate an eight-character alphanumeric password
    alphabet = string.ascii_letters + string.digits
    dummy_password = ''.join(secrets.choice(alphabet) for i in range(8))
    return {'email': dummy_email,
            'password': dummy_password,
            'user_name': dummy_user_name}


@pytest.fixture(scope="function")
def login(client, new_user, app):
    """Returns login response"""
    # Login
    # If login fails then the fixture fails. It may be possible to 'mock'
    # this instead if you want to investigate it.
    response = client.post('/login', json=new_user,
                           content_type="application/json")
    # Get returned json data from the login function
    data = response.json
    yield data
