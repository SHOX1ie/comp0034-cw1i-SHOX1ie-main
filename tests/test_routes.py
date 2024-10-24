# Test User GET, POST and DELETE Routes
def test_get_Users_status_code(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /Users
    THEN the status code should be 200
    """
    response = client.get("/Users")
    assert response.status_code == 200


def test_post_User(client):
    """
    GIVEN a Flask test client
    AND valid JSON for a new user group
    WHEN a POST request is made to /Users
    THEN the response status_code should be 200
    """
    # JSON to create a new user group
    user_json = {
        "user_id": 61,
        "email": "asdk",
        "password_hash": "asdf",
        "user_name": "asfjg"
    }
    # pass the JSON in the HTTP POST request
    response = client.post(
        "/Users",
        json=user_json,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_User(client, new_users):
    """
    GIVEN an existing user in JSON format
    AND a Flask test client
    WHEN a DELETE request is made to /Users/<code>
    THEN the response status code should be 200
    AND the response content should include the message 'User {code}
    deleted.'
    """
    # Get the code from the JSON which is returned in the new_users
    # fixture
    code = new_users['user_id']
    response = client.delete(f"/Users/{code}")
    assert response.status_code == 200
    assert response.json['message'] == f'User deleted with id= {code}'


# Test Feedback GET, POST and DELETE Routes
def test_get_Feedbacks_status_code(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /Feedbacks
    THEN the status code should be 200
    """
    response = client.get("/Feedbacks")
    assert response.status_code == 200


def test_post_Feedback(client):
    """
    GIVEN a Flask test client
    AND valid JSON for a new feedback group
    WHEN a POST request is made to /Feedbacks
    THEN the response status_code should be 200
    """
    # JSON to create a new feedback group
    feedback_json = {
        "feedback_id": 61,
        "feedback_time": "2021-12-01T14:30:00Z",
        "feedback_content": "This is my feedback.",
        "user_id": 30
    }
    # pass the JSON in the HTTP POST request
    response = client.post(
        "/Feedbacks",
        json=feedback_json,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_Feedback(client, new_feedback):
    """
    GIVEN an existing feedback group in JSON format
    AND a Flask test client
    WHEN a DELETE request is made to /Feedbacks/<code>
    THEN the response status code should be 200
    AND the response content should include the message
    'Feedback {code} deleted.'
    """
    # Get the Feedback ID from the JSON which is returned in the new_feedback
    # fixture
    code = new_feedback['feedback_id']
    response = client.delete(f"/Feedbacks/{code}")
    assert response.status_code == 200
    assert response.json['message'] == f'Feedback deleted with id= {code}'


# Test Age_group GET, POST and DELETE Routes
def test_get_Age_groups_status_code(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /Age_groups
    THEN the status code should be 200
    """
    response = client.get("/Age_groups")
    assert response.status_code == 200


def test_get_Age_groups_json(client):
    """
    GIVEN a Flask test client
    AND the database contains data of the Age_group
    WHEN a request is made to /Age_groups
    THEN the response should contain json
    AND a JSON object for age should be in the json
    """
    age = {'age_group_id': 1, 'time_period': 201718, 'pct_total_age_u25': 81,
           'pct_total_age_25andover': 80}
    response = client.get("/Age_groups")
    assert response.headers["Content-Type"] == "application/json"
    assert age in response.json


def test_post_Age_group(client):
    """
    GIVEN a Flask test client
    AND valid JSON for a new age group
    WHEN a POST request is made to /Age_groups
    THEN the response status_code should be 200
    """
    # JSON to create a new age group
    age_group_json = {
        "age_group_id": 61,
        "time_period": 202425,
        "pct_total_age_u25": 20,
        "pct_total_age_25andover": 30
    }
    # pass the JSON in the HTTP POST request
    response = client.post(
        "/Age_groups",
        json=age_group_json,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_Age_group(client, new_age_group):
    """
    GIVEN an existing age group in JSON format
    AND a Flask test client
    WHEN a DELETE request is made to /Age_groups/<code>
    THEN the response status code should be 200
    AND the response content should include the message
    'Age_group {code} deleted.'
    """
    # Get the age group ID from the JSON which is returned in the new_age_group
    # fixture
    code = new_age_group['age_group_id']
    response = client.delete(f"/Age_groups/{code}")
    assert response.status_code == 200
    assert response.json['message'] == f'Age_group deleted with id= {code}'


# Test Gender GET, POST and DELETE Routes
def test_get_Genders_status_code(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /Genders
    THEN the status code should be 200
    """
    response = client.get("/Genders")
    assert response.status_code == 200


def test_get_Genders_json(client):
    """
    GIVEN a Flask test client
    AND the database contains data of the Gender
    WHEN a request is made to /Genders
    THEN the response should contain json
    AND a JSON object for gender should be in the json
    """
    gender = {'gender_id': 2, 'time_period': 201718, 'pct_total_sex_m': 92,
              'pct_total_sex_f': 96}
    response = client.get("/Genders")
    assert response.headers["Content-Type"] == "application/json"
    assert gender in response.json


def test_post_Gender(client):
    """
    GIVEN a Flask test client
    AND valid JSON for a new gender
    WHEN a POST request is made to /Genders
    THEN the response status_code should be 200
    """
    # JSON to create a new gender
    gender_json = {
        "gender_id": 61,
        "time_period": 202425,
        "pct_total_sex_m": 20,
        "pct_total_sex_f": 30
    }
    # pass the JSON in the HTTP POST request
    response = client.post(
        "/Genders",
        json=gender_json,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_Gender(client, new_gender):
    """
    GIVEN an existing gender in JSON format
    AND a Flask test client
    WHEN a DELETE request is made to /Genders/<code>
    THEN the response status code should be 200
    AND the response content should include the message 'Gender {code}
    deleted.'
    """
    # Get the code from the JSON which is returned in the new_gender
    # fixture
    code = new_gender['gender_id']
    response = client.delete(f"/Genders/{code}")
    assert response.status_code == 200
    assert response.json['message'] == f'Gender deleted with id= {code}'


# Test Ethnicity GET, POST and DELETE Routes
def test_get_Ethnicities_status_code(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /Ethnicities
    THEN the status code should be 200
    """
    response = client.get("/Ethnicities")
    assert response.status_code == 200


def test_get_Ethnicities_json(client):
    """
    GIVEN a Flask test client
    AND the database contains data of the Ethnicity
    WHEN a request is made to /Ethnicities
    THEN the response should contain json
    AND a JSON object for ethnicity should be in the json
    """
    ethnicity = {'ethnicity_id': 1, 'time_period': 201718,
                 'pct_total_ethnic_asian': 78,
                 'pct_total_ethnic_black': 81,
                 'pct_total_ethnic_white': 81,
                 'pct_total_ethnic_mixed_ethnicity': 82,
                 'pct_total_ethnic_other': 79,
                 'pct_total_ethnic_unknown': 78}
    response = client.get("/Ethnicities")
    assert response.headers["Content-Type"] == "application/json"
    assert ethnicity in response.json


def test_post_Ethnicity(client):
    """
    GIVEN a Flask test client
    AND valid JSON for a new ethnicity
    WHEN a POST request is made to /Ethnicities
    THEN the response status_code should be 200
    """
    # JSON to create a new ethnicity
    ethnicity_json = {'ethnicity_id': 61, 'time_period': 201718,
                      'pct_total_ethnic_asian': 78,
                      'pct_total_ethnic_black': 81,
                      'pct_total_ethnic_white': 81,
                      'pct_total_ethnic_mixed_ethnicity': 82,
                      'pct_total_ethnic_other': 79,
                      'pct_total_ethnic_unknown': 78}
    # pass the JSON in the HTTP POST request
    response = client.post(
        "/Ethnicities",
        json=ethnicity_json,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_Ethnicity(client, new_ethnicity):
    """
    GIVEN an existing ethnicity in JSON format
    AND a Flask test client
    WHEN a DELETE request is made to /Ethnicities/<code>
    THEN the response status code should be 200
    AND the response content should include the message 'Ethnicity {code}
    deleted.'
    """
    # Get the code from the JSON which is returned in the new_ethnicity
    # fixture
    code = new_ethnicity['ethnicity_id']
    response = client.delete(f"/Ethnicities/{code}")
    assert response.status_code == 200
    assert response.json['message'] == f'Ethnicity deleted with id= {code}'


# Test Employment GET, POST and DELETE Routes
def test_get_Employments_status_code(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /Employments
    THEN the status code should be 200
    """
    response = client.get("/Employments")
    assert response.status_code == 200


def test_get_Employments_json(client):
    """
    GIVEN a Flask test client
    AND the database contains data of the Employment
    WHEN a request is made to /Employments
    THEN the response should contain json
    AND a JSON object for employment should be in the json
    """
    employment = {'employment_id': 1, 'time_period': 201718,
                  'employment_status': 'Teaching in a state-funded school'}
    response = client.get("/Employments")
    assert response.headers["Content-Type"] == "application/json"
    assert employment in response.json


def test_post_Employment(client):
    """
    GIVEN a Flask test client
    AND valid JSON for a new employment
    WHEN a POST request is made to /Employments
    THEN the response status_code should be 200
    """
    # JSON to create a new employment
    employment_json = {
        "employment_id": 61,
        "time_period": 202425,
        "employment_status": 'Teaching in a state-funded school'
    }
    # pass the JSON in the HTTP POST request
    response = client.post(
        "/Employments",
        json=employment_json,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_Employment(client, new_employment):
    """
    GIVEN an existing employment in JSON format
    AND a Flask test client
    WHEN a DELETE request is made to /Employments/<code>
    THEN the response status code should be 200
    AND the response content should include the message 'Employment {code}
    deleted.'
    """
    # Get the code from the JSON which is returned in the new_employment
    # fixture
    code = new_employment['employment_id']
    response = client.delete(f"/Employments/{code}")
    assert response.status_code == 200
    assert response.json['message'] == f'Employment deleted with id= {code}'


# Test Course_level GET, POST and DELETE Routes
def test_get_Course_levels_status_code(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /Course_levels
    THEN the status code should be 200
    """
    response = client.get("/Course_levels")
    assert response.status_code == 200


def test_get_Course_levels_json(client):
    """
    GIVEN a Flask test client
    AND the database contains data of the Course_level
    WHEN a request is made to /Course_levels
    THEN the response should contain json
    AND a JSON object for course_level should be in the json
    """
    course_level = {'course_level_id': 1, 'time_period': 201718,
                    'course_level_recoded': 'Postgraduate'}
    response = client.get("/Course_levels")
    assert response.headers["Content-Type"] == "application/json"
    assert course_level in response.json


def test_post_Course_level(client):
    """
    GIVEN a Flask test client
    AND valid JSON for a new course level
    WHEN a POST request is made to /Course_levels
    THEN the response status_code should be 200
    """
    # JSON to create a new course level
    course_level_json = {
        "course_level_id": 61,
        "time_period": 202425,
        "course_level_recoded": 'Undergraduate'
    }
    # pass the JSON in the HTTP POST request
    response = client.post(
        "/Course_levels",
        json=course_level_json,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_Course_level(client, new_course_level):
    """
    GIVEN an existing course_level in JSON format
    AND a Flask test client
    WHEN a DELETE request is made to /Course_levels/<code>
    THEN the response status code should be 200
    AND the response content should include the message 'Course_level {code}
    deleted.'
    """
    # Get the code from the JSON which is returned in the new_course_level
    # fixture
    code = new_course_level['course_level_id']
    response = client.delete(f"/Course_levels/{code}")
    assert response.status_code == 200
    assert response.json['message'] == f'Course_level deleted with id= {code}'


# Test Disability GET, POST and DELETE Routes
def test_get_Disabilities_status_code(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /Disabilities
    THEN the status code should be 200
    """
    response = client.get("/Disabilities")
    assert response.status_code == 200


def test_get_Disabilities_json(client):
    """
    GIVEN a Flask test client
    AND the database contains data of the Disability
    WHEN a request is made to /Disabilities
    THEN the response should contain json
    AND a JSON object for disability should be in the json
    """
    disability = {'disability_id': 1, 'time_period': 201718,
                  'pct_total_disability': 77,
                  'pct_total_nondisability': 81,
                  'pct_total_disability_unknown': 93}
    response = client.get("/Disabilities")
    assert response.headers["Content-Type"] == "application/json"
    assert disability in response.json


def test_post_Disability(client):
    """
    GIVEN a Flask test client
    AND valid JSON for a new disability
    WHEN a POST request is made to /Disabilities
    THEN the response status_code should be 200
    """
    # JSON to create a new disability
    disability_json = {
        "disability_id": 61,
        "time_period": 202425,
        "pct_total_disability": 10,
        "pct_total_nondisability": 20,
        "pct_total_disability_unknown": 30
    }
    # pass the JSON in the HTTP POST request
    response = client.post(
        "/Disabilities",
        json=disability_json,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_Disability(client, new_disability):
    """
    GIVEN an existing disability in JSON format
    AND a Flask test client
    WHEN a DELETE request is made to /Disabilities/<code>
    THEN the response status code should be 200
    AND the response content should include the message 'Disability {code}
    deleted.'
    """
    # Get the code from the JSON which is returned in the new_disability
    # fixture
    code = new_disability['disability_id']
    response = client.delete(f"/Disabilities/{code}")
    assert response.status_code == 200
    assert response.json['message'] == f'Disability deleted with id= {code}'


# Test Teacher GET, POST and DELETE Routes
def test_get_Teachers_status_code(client):
    """
    GIVEN a Flask test client
    WHEN a GET request is made to /Teachers
    THEN the status code should be 200
    """
    response = client.get("/Teachers")
    assert response.status_code == 200


def test_get_Teachers_json(client):
    """
    GIVEN a Flask test client
    AND the database contains data of the Teacher
    WHEN a request is made to /Teachers
    THEN the response should contain json
    AND a JSON object for teacher should be in the json
    """
    teacher = {'teacher_id': 1, 'time_period': 201718,
               'qts_status': 'Awarded QTS',
               'n_total': 20503}
    response = client.get("/Teachers")
    assert response.headers["Content-Type"] == "application/json"
    assert teacher in response.json


def test_get_specified_teacher(client):
    """
    GIVEN a Flask test client
    AND the 5th entry is teacher_id,4,
    WHEN a request is made to /Teachers/teacher_id
    THEN the response json should match that for 4
    AND the response status_code should be 200
    """
    teacher_json = {'teacher_id': 4, 'time_period': 201718,
                    'qts_status': 'Total',
                    'n_total': 26794}
    response = client.get("/Teachers/4")
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == 200
    assert response.json == teacher_json


def test_post_Teacher(client):
    """
    GIVEN a Flask test client
    AND valid JSON for a new teacher
    WHEN a POST request is made to /Teachers
    THEN the response status_code should be 200
    """
    # JSON to create a new teacher
    teacher_json = {
        "teacher_id": 61,
        "time_period": 202425,
        "qts_status": 'Total',
        "n_total": 20200
    }
    # pass the JSON in the HTTP POST request
    response = client.post(
        "/Teachers",
        json=teacher_json,
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_Teacher(client, new_teacher):
    """
    GIVEN an existing teacher in JSON format
    AND a Flask test client
    WHEN a DELETE request is made to /Teachers/<code>
    THEN the response status code should be 200
    AND the response content should include the message 'Teacher {code}
    deleted.'
    """
    # Get the code from the JSON which is returned in the new_teacher
    # fixture
    code = new_teacher['teacher_id']
    response = client.delete(f"/Teachers/{code}")
    assert response.status_code == 200
    assert response.json['message'] == f'Teacher deleted with id= {code}'
