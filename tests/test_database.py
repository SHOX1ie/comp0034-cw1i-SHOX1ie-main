# A test that includes using a context to check the database
from sqlalchemy import func
from src import db
from src.models import Teacher, User


def test_post_teacher_database_update(client, app):
    """
    GIVEN a Flask test client and test app
    AND valid JSON for a new teacher
    WHEN a POST request is made to /teachers
    THEN the database should have one more entry
    """
    teacher_json = {"teacher_id": 61, "time_period": 202425,
                    "qts_status": 'Total', "n_total": 20000}

    # Count the rows in the Teacher table before and after the post
    with app.app_context():
        num_rows_start = db.session.scalar(
            db.select(func.count(Teacher.teacher_id)))

        client.post("/Teachers", json=teacher_json)

        num_rows_end = db.session.scalar(
            db.select(func.count(Teacher.teacher_id)))
    assert num_rows_end - num_rows_start == 1


def test_post_teacher_database_update_again(test_client):
    """
    GIVEN a Flask test client that has an application context
    AND valid JSON for a new teacher
    WHEN a POST request is made to /teachers
    THEN the database should have one more entry
    """
    teacher_json = {"teacher_id": 62, "time_period": 202425,
                    "qts_status": 'Total', "n_total": 21000}

    # Count the rows in the Teacher table before and after the post
    num_rows_start = db.session.scalar(
        db.select(func.count(Teacher.teacher_id)))

    test_client.post("/Teachers", json=teacher_json)

    num_rows_end = db.session.scalar(db.select(func.count(Teacher.teacher_id)))
    assert num_rows_end - num_rows_start == 1


# Test that doesn't make a request to a route
def test_database_after_insert(test_client, random_user_json):
    """
        GIVEN a test_client with an application context
        AND a new user
        WHEN a user is added to the database
        THEN the database User table should have one more entry
        """
    num_rows_start = db.session.scalar(db.select(func.count(User.user_id)))
    user = User(email=random_user_json['email'],
                user_name=random_user_json['user_name'])
    user.set_password(random_user_json['password'])
    db.session.add(user)
    db.session.commit()
    num_rows_end = db.session.scalar(db.select(func.count(User.user_id)))
    assert num_rows_end - num_rows_start == 1
