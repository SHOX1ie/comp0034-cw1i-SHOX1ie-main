# Authentication tests
def test_register_success(client, random_user_json):
    """
    GIVEN a valid format email and password for a user not already registered
    WHEN an account is created
    THEN the status code should be 201
    """
    user_register = client.post('/register', json=random_user_json,
                                content_type="application/json")
    assert user_register.status_code == 201


def test_login_success(client, new_user):
    """
    GIVEN a valid format email and password for a user already registered
    WHEN /login is called
    THEN the status code should be 201
    """
    user_register = client.post('/login', json=new_user,
                                content_type="application/json")
    assert user_register.status_code == 201


def test_user_not_logged_in_cannot_edit_teacher(client, new_user, new_teacher):
    """
    GIVEN a registered user that is not logged in
    AND a route that is protected by login
    AND a new teacher that can be edited
    WHEN a PATCH request to /Teachers/<code> is made
    THEN the HTTP response status code should be 401 with message
    'Authentication token missing
    """
    new_teacher_time = {'time_period': 201718}
    code = new_teacher['teacher_id']
    response = client.patch(f"/Teachers/{code}", json=new_teacher_time)
    assert response.status_code == 401


def test_user_logged_in_user_can_edit_teacher(app, client, new_user,
                                              login, new_teacher):
    """
    GIVEN a registered user that is successfully logged in
    AND a route that is protected by login
    AND a new teacher that can be edited
    WHEN a PATCH request to /Teachers/<code> is made
    THEN the HTTP status code should be 200
    AND the response content should include the message 'Teacher <code>
    updated'
    """
    # pass the token in the headers of the HTTP request
    token = login['token']
    headers = {
        'content-type': "application/json",
        'Authorization': token
    }
    new_teacher_time = {'time_period': 201819}
    code = new_teacher['teacher_id']
    response = client.patch(f"/Teachers/{code}", json=new_teacher_time,
                            headers=headers)
    assert response.json == {"message": f"Teacher {code} updated."}
    assert response.status_code == 200
