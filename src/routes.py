from flask import current_app as app, request, abort, jsonify, make_response

from src import db
from src.schemas import UserSchema, FeedbackSchema, Age_groupSchema, \
    GenderSchema, EthnicitySchema, EmploymentSchema, Course_levelSchema, \
    TeacherSchema, DisabilitySchema
from src.models import User, Feedback, Age_group, Gender, Ethnicity, \
    Employment, Course_level, Teacher, Disability
from src.helpers import token_required, encode_auth_token

import datetime
from sqlalchemy import exc
from marshmallow.exceptions import ValidationError

# Flask-Marshmallow Schemas
Users_schema = UserSchema(many=True)
User_schema = UserSchema()
Feedbacks_schema = FeedbackSchema(many=True)
Feedback_schema = FeedbackSchema()
Age_groups_schema = Age_groupSchema(many=True)
Age_group_schema = Age_groupSchema()
Genders_schema = GenderSchema(many=True)
Gender_schema = GenderSchema()
Ethnicities_schema = EthnicitySchema(many=True)
Ethnicity_schema = EthnicitySchema()
Employments_schema = EmploymentSchema(many=True)
Employment_schema = EmploymentSchema()
Course_levels_schema = Course_levelSchema(many=True)
Course_level_schema = Course_levelSchema()
Disabilities_schema = DisabilitySchema(many=True)
Disability_schema = DisabilitySchema()
Teachers_schema = TeacherSchema(many=True)
Teacher_schema = TeacherSchema()


# Route for the home page
@app.route('/')
def hello():
    return f"Hello!"


# Routes for User in GET, POST, DELETE and PATCH
@app.get("/Users")
def get_Users():
    """Returns a list of user_id and their details in JSON.

    Returns:
        JSON for all the users, or 500 error if not found
    """
    try:
        # Select all the users using Flask-SQLAlchemy
        all_users = db.session.execute(db.select(User)).scalars()
        # Dump the data using the Marshmallow users schema; '.dump()' returns JSON.
        try:
            result = Users_schema.dump(all_users)
            # If all OK then return the data in the HTTP response
            return result
        except ValidationError as e:
            app.logger.error(f"A Marshmallow ValidationError occurred dumping all users: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(f"An error occurred while fetching users: {str(e)}")
        msg = {'message': "An Internal Server Error occurred."}
        return make_response(msg, 500)


@app.get("/Users/<id>")
def get_User(id):
    """ Returns one user in JSON.

    Returns 404 if the user_id is not found in the database.

    Args:
        id (int): The user_id of the user to be searched for

    Returns:
        JSON for the user if found otherwise 404
    """
    # Try to find the user, if it is ot found, catch the error and return 404
    try:
        user = db.session.execute(
            db.select(User).filter_by(user_id=id)
        ).scalar_one_or_none()
        return User_schema.dump(user)
    except exc.NoResultFound as e:
        # See https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json
        app.logger.error(f'User {id} was not found. Error: {e}')
        abort(404, description="User not found")


@app.post('/Users')
def add_User():
    """ Adds a new user.

    Gets the JSON data from the request body and uses this to deserialise JSON to an object using Marshmallow
   User_schema.loads()

    Returns: 
        JSON message  If there is an error, return 400if the issue is with the validation, 500 if there is a
        database issue, otherwise return message 'user added with user_id= {user.user_id}'
    """
    json_data = request.get_json()
    try:
        user = User_schema.load(json_data)

        try:
            db.session.add(user)
            db.session.commit()
            return {"message": f"User added with user_id= {user.user_id}"}
        except exc.SQLAlchemyError as e:
            app.logger.error(f"An error occurred saving the User: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)

    except ValidationError as e:
        app.logger.error(f"A Marshmallow ValidationError loading the User: {str(e)}")
        msg = {'message': "The User details failed validation."}
        return make_response(msg, 400)


@app.delete('/Users/<id>')
def delete_User(id):
    """ Deletes the user with the given code.

    Args:
        id (int): user_id of the user to delete
    Returns:
        JSON If successful, return success message, other return 500 Internal Server Error
    """
    try:
        user = db.session.execute(
            db.select(User).filter_by(user_id=id)
        ).scalar_one_or_none()
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User deleted with id= {user.user_id}"}
    except exc.SQLAlchemyError as e:
        # Log the exception with the error
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        # Report a 404 error to the user who made the request
        msg_content = f'User {id} not found.'
        msg = {'message': msg_content}
        return make_response(msg, 404)


@app.patch("/Users/<id>")
def User_update(id):
    """Updates changed fields for the specified user.

    Args:
        id (int): user_id of the user to update

    Returns:
        JSON message
            If the user for the code is not found, return 404
            If the JSON contents are not valid, return 500
            If the update is not saved, return 500
            If all OK then return 200
    """
    app.logger.error(f"Started the patch")
    # Find the user in the database
    try:
        existing_user = db.session.execute(
            db.select(User).filter_by(user_id=id)
        ).scalar_one_or_none()
    except exc.SQLAlchemyError as e:
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        msg_content = f'User {id} not found'
        msg = {'message': msg_content}
        return make_response(msg, 404)
    # Get the updated details from the json sent in the HTTP patch request
    user_json = request.get_json()
    app.logger.error(f"user_json: {str(user_json)}")
    # Use Marshmallow to update the existing records with the changes from the json
    try:
        user_update = User_schema.load(user_json, instance=existing_user, partial=True)
    except ValidationError as e:
        app.logger.error(f"A Marshmallow schema validation error occurred: {str(e)}")
        msg = f'Failed Marshmallow schema validation'
        return make_response(msg, 500)
    # Commit the changes to the database
    try:
        db.session.add(user_update)
        db.session.commit()
        # Return json message
        response = {"message": f"User {id} updated."}
        return response
    except exc.SQLAlchemyError as e:
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        msg = f'An Internal Server Error occurred.'
        return make_response(msg, 500)


# Routes for Feedback in GET, POST, DELETE and PATCH
@app.get("/Feedbacks")
def get_Feedbacks():
    """Returns a list of Feedbacks and their details in JSON.

    Returns:
        JSON for all the Feedbacks, or 500 error if not found
    """
    try:
        # Select all the Feedbacks using Flask-SQLAlchemy
        all_Feedback = db.session.execute(db.select(Feedback)).scalars()
        try:
            # Get the data using Marshmallow schema (returns JSON)
            result = Feedbacks_schema.dump(all_Feedback)
            # Return the data
            return result
        except ValidationError as e:
            app.logger.error(f"A Marshmallow ValidationError occurred dumping all Feedbacks: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(f"An error occurred while fetching Feedbacks: {str(e)}")
        msg = {'message': "An Internal Server Error occurred."}
        return make_response(msg, 500)


@app.get("/Feedbacks/<id>")
def get_Feedback(id):
    """ Returns one feedback in JSON.

    Returns 404 if the feedback ID is not found in the database.

    Args:
        id (int): The ID of the feedback to be searched for

    Returns: 
        JSON for the feedback if found otherwise 404
    """
    try:
        feedback = db.session.execute(
            db.select(Feedback).filter_by(feedback_id=id)
        ).scalar_one_or_none()
        return Feedback_schema.dump(feedback)
    except exc.NoResultFound as e:
        # See https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json
        app.logger.error(f'Feedback ID {id} was not found. Error: {e}')
        abort(404, description="Feedback not found")


@app.post('/Feedbacks')
def add_Feedback():
    """ Adds a new feedback.

    Gets the JSON data from the request body and uses this to deserialise JSON to an object using Marshmallow
    feedback_schema.loads()

    Returns: 
        JSON message  If there is an error, return 400 if the issue is with the validation, 500 if there is a
        database issue, otherwise return message 'Feedback added with feedback_id= {feedback.feedback_id}'
    """
    json_data = request.get_json()
    try:
        feedback = Feedback_schema.load(json_data)

        try:
            db.session.add(feedback)
            db.session.commit()
            return {"message": f"Feedback added with feedback_id= {feedback.feedback_id}"}
        except exc.SQLAlchemyError as e:
            app.logger.error(f"An error occurred saving the Feedback: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)

    except ValidationError as e:
        app.logger.error(f"A Marshmallow ValidationError loading the Feedback: {str(e)}")
        msg = {'message': "The Feedback details failed validation."}
        return make_response(msg, 400)


@app.delete('/Feedbacks/<id>')
def delete_Feedback(id):
    """ Deletes the feedback with the given ID.

    Args:
        param id (int): The ID of the feedback to delete
    Returns:
        JSON If successful, return success message, otherwise return 500 Internal Server Error
    """
    try:
        feedback = db.session.execute(
            db.select(Feedback).filter_by(feedback_id=id)
        ).scalar_one_or_none()
        db.session.delete(feedback)
        db.session.commit()
        return {"message": f"Feedback deleted with id= {feedback.feedback_id}"}
    except exc.SQLAlchemyError as e:
        # Log the exception with the error
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        # Report a 404 error to the user who made the request
        msg_content = f'Feedback {id} not found.'
        msg = {'message': msg_content}
        return make_response(msg, 404)


# Routes for Age_group in GET, POST and DELETE
@app.get("/Age_groups")
def get_Age_groups():
    """Returns a list of Age_group codes and their details in JSON.

    Returns:
        JSON for all the Age_groups, or 500 error if not found
    """
    try:
        # Select all the Age_groups using Flask-SQLAlchemy
        all_Age_group = db.session.execute(db.select(Age_group)).scalars()
        # Get the data using Marshmallow schema (returns JSON)
        try:
            result = Age_groups_schema.dump(all_Age_group)
            # Return the data
            return result
        except ValidationError as e:
            app.logger.error(f"A Marshmallow ValidationError occurred dumping all Age_groups: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(f"An error occurred while fetching Age_groups: {str(e)}")
        msg = {'message': "An Internal Server Error occurred."}
        return make_response(msg, 500)


@app.get("/Age_groups/<id>")
def get_Age_group(id):
    """ Returns one Age_group in JSON.

    Returns 404 if the Age_group code is not found in the database.

    Args:
        id (int): The ID of the Age_group to be searched for

    Returns: 
        JSON for the Age_group if found otherwise 404
    """
    try:
        age_group = db.session.execute(
            db.select(Age_group).filter_by(age_group_id=id)
        ).scalar_one_or_none()
        return Age_group_schema.dump(age_group)
    except exc.NoResultFound as e:
        # See https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json
        app.logger.error(f'Age_group ID {id} was not found. Error: {e}')
        abort(404, description="Age_group not found")


@app.post('/Age_groups')
def add_Age_group():
    """ Adds a new Age_group.

    Gets the JSON data from the request body and uses this to deserialize JSON to an object using Marshmallow
    age_group_schema.loads()

    Returns: 
        JSON message  If there is an error, return 400 if the issue is with the validation, 500 if there is a
        database issue, otherwise return message 'Age_group added with age_group_id= {age_group.age_group_id}'
    """
    json_data = request.get_json()
    try:
        age_group = Age_group_schema.load(json_data)

        try:
            db.session.add(age_group)
            db.session.commit()
            return {"message": f"Age_group added with age_group_id= {age_group.age_group_id}"}
        except exc.SQLAlchemyError as e:
            app.logger.error(f"An error occurred saving the Age_group: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)

    except ValidationError as e:
        app.logger.error(f"A Marshmallow ValidationError loading the Age_group: {str(e)}")
        msg = {'message': "The Age_group details failed validation."}
        return make_response(msg, 400)


@app.delete('/Age_groups/<id>')
def delete_Age_group(id):
    """ Deletes the age group with the given id.

    Args:
        param id (int): The id of the age group to delete
    Returns:
        JSON If successful, return success message, otherwise return 404 Not Found
    """
    try:
        age_group = db.session.execute(
            db.select(Age_group).filter_by(age_group_id=id)
        ).scalar_one_or_none()
        db.session.delete(age_group)
        db.session.commit()
        return {"message": f"Age_group deleted with id= {age_group.age_group_id}"}
    except exc.SQLAlchemyError as e:
        # Log the exception with the error
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        # Report a 404 error to the user who made the request
        msg_content = f'Age_group {id} not found.'
        msg = {'message': msg_content}
        return make_response(msg, 404)


# Routes for Gender in GET, POST and DELETE
@app.get("/Genders")
def get_Genders():
    """Returns a list of Gender codes and their details in JSON.

    Returns:
        JSON for all the genders, or 500 error if not found
    """
    try:
        # Select all the genders using Flask-SQLAlchemy
        all_Gender = db.session.execute(db.select(Gender)).scalars()
        try:
            # Get the data using Marshmallow schema (returns JSON)
            result = Genders_schema.dump(all_Gender)
            # Return the data
            return result
        except ValidationError as e:
            app.logger.error(f"A Marshmallow ValidationError occurred dumping all genders: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(f"An error occurred while fetching genders: {str(e)}")
        msg = {'message': "An Internal Server Error occurred."}
        return make_response(msg, 500)


@app.get("/Genders/<id>")
def get_Gender(id):
    """ Returns one gender in JSON.

    Returns 404 if the gender code is not found in the database.

    Args:
        id (int): The id of the gender to be searched for

    Returns: 
        JSON for the gender if found otherwise 404
    """
    try:
        gender = db.session.execute(
            db.select(Gender).filter_by(gender_id=id)
        ).scalar_one_or_none()
        return Gender_schema.dump(gender)
    except exc.NoResultFound as e:
        # See https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json
        app.logger.error(f'Gender id {id} was not found. Error: {e}')
        abort(404, description="Gender not found")


@app.post('/Genders')
def add_Gender():
    """ Adds a new gender.

    Gets the JSON data from the request body and uses this to deserialise JSON to an object using Marshmallow
    gender_schema.loads()

    Returns: 
        JSON message  If there is an error, return 400 if the issue is with the validation, 500 if there is a
        database issue, otherwise return message 'Gender added with gender_id= {gender.gender_id}'
    """
    json_data = request.get_json()
    try:
        gender = Gender_schema.load(json_data)

        try:
            db.session.add(gender)
            db.session.commit()
            return {"message": f"Gender added with gender_id= {gender.gender_id}"}
        except exc.SQLAlchemyError as e:
            app.logger.error(f"An error occurred saving the Gender: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)

    except ValidationError as e:
        app.logger.error(f"A Marshmallow ValidationError loading the Gender: {str(e)}")
        msg = {'message': "The Gender details failed validation."}
        return make_response(msg, 400)


@app.delete('/Genders/<id>')
def delete_Gender(id):
    """ Deletes the gender with the given id.

    Args:
        param id (int): The id of the gender to delete
    Returns:
        JSON If successful, return success message, otherwise return 404 if the gender is not found,
        or 500 Internal Server Error for database errors
    """
    try:
        gender = db.session.execute(
            db.select(Gender).filter_by(gender_id=id)
        ).scalar_one_or_none()
        db.session.delete(gender)
        db.session.commit()
        return {"message": f"Gender deleted with id= {gender.gender_id}"}
    except exc.SQLAlchemyError as e:
        # Log the exception with the error
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        # Report a 404 error to the user who made the request
        msg_content = f'Gender {id} not found.'
        msg = {'message': msg_content}
        return make_response(msg, 404)


# Routes for Ethnicity in GET, POST and DELETE
@app.get("/Ethnicities")
def get_Ethnicities():
    """Returns a list of Ethnicity codes and their details in JSON.

    Returns:
        JSON for all the ethnicities, or 500 error if not found
    """
    try:
        # Select all the ethnicities using Flask-SQLAlchemy
        all_ethnicities = db.session.execute(db.select(Ethnicity)).scalars()
        try:
            # Get the data using Marshmallow schema (returns JSON)
            result = Ethnicities_schema.dump(all_ethnicities)
            # Return the data
            return result
        except ValidationError as e:
            app.logger.error(f"A Marshmallow ValidationError occurred dumping all ethnicities: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(f"An error occurred while fetching ethnicities: {str(e)}")
        msg = {'message': "An Internal Server Error occurred."}
        return make_response(msg, 500)


@app.get("/Ethnicities/<id>")
def get_Ethnicity(id):
    """ Returns one ethnicity in JSON.

    Returns 404 if the ethnicity id is not found in the database.

    Args:
        id (int): The id of the ethnicity to be searched for

    Returns: 
        JSON for the ethnicity if found otherwise 404
    """
    try:
        ethnicity = db.session.execute(
            db.select(Ethnicity).filter_by(ethnicity_id=id)
        ).scalar_one_or_none()
        return Ethnicity_schema.dump(ethnicity)
    except exc.NoResultFound as e:
        # See https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json
        app.logger.error(f'Ethnicity id {id} was not found. Error: {e}')
        abort(404, description="Ethnicity not found")


@app.post('/Ethnicities')
def add_Ethnicity():
    """ Adds a new ethnicity.

    Gets the JSON data from the request body and uses this to deserialize JSON to an object using Marshmallow
    ethnicity_schema.loads()

    Returns:
        JSON message. If there is an error, return 400 if the issue is with the validation, 500 if there is a
        database issue, otherwise return message 'Ethnicity added with ethnicity_id= {ethnicity.ethnicity_id}'
    """
    json_data = request.get_json()
    try:
        ethnicity = Ethnicity_schema.load(json_data)

        try:
            db.session.add(ethnicity)
            db.session.commit()
            return {"message": f"Ethnicity added with ethnicity_id= {ethnicity.ethnicity_id}"}
        except exc.SQLAlchemyError as e:
            app.logger.error(f"An error occurred saving the Ethnicity: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)

    except ValidationError as e:
        app.logger.error(f"A Marshmallow ValidationError loading the ethnicity: {str(e)}")
        msg = {'message': "The Ethnicity details failed validation."}
        return make_response(msg, 400)


@app.delete('/Ethnicities/<id>')
def delete_Ethnicity(id):
    """ Deletes the ethnicity with the given id.

    Args:
        param id (int): The id of the ethnicity to delete
    Returns:
        JSON If successful, return success message, otherwise return 404 if the ethnicity is not found,
        or 500 Internal Server Error for database errors
    """
    try:
        ethnicity = db.session.execute(
            db.select(Ethnicity).filter_by(ethnicity_id=id)
        ).scalar_one_or_none()
        db.session.delete(ethnicity)
        db.session.commit()
        return {"message": f"Ethnicity deleted with id= {ethnicity.ethnicity_id}"}
    except exc.SQLAlchemyError as e:
        # Log the exception with the error
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        # Report a 404 error to the user who made the request
        msg_content = f'Ethnicity {id} not found.'
        msg = {'message': msg_content}
        return make_response(msg, 404)


# Routes for Employment in GET, POST and DELETE
@app.get("/Employments")
def get_Employments():
    """Returns a list of Employment codes and their details in JSON.

    Returns:
        JSON for all the employments, or 500 error if not found
    """
    try:
        # Select all the employments using Flask-SQLAlchemy
        all_employments = db.session.execute(db.select(Employment)).scalars()
        try:
            # Get the data using Marshmallow schema (returns JSON)
            result = Employments_schema.dump(all_employments)
            # Return the data
            return result
        except ValidationError as e:
            app.logger.error(f"A Marshmallow ValidationError occurred dumping all employments: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(f"An error occurred while fetching employments: {str(e)}")
        msg = {'message': "An Internal Server Error occurred."}
        return make_response(msg, 500)


@app.get("/Employments/<id>")
def get_Employment(id):
    """ Returns one employment in JSON.

    Returns 404 if the employment id is not found in the database.

    Args:
        id (int): The id of the employment to be searched for

    Returns: 
        JSON for the employment if found, otherwise 404
    """
    try:
        employment = db.session.execute(
            db.select(Employment).filter_by(employment_id=id)
        ).scalar_one_or_none()
        return Employment_schema.dump(employment)
    except exc.NoResultFound as e:
        # See https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json
        app.logger.error(f'Employment id {id} was not found. Error: {e}')
        abort(404, description="Employment not found")


@app.post('/Employments')
def add_Employment():
    """ Adds a new employment.

    Gets the JSON data from the request body and uses this to deserialize JSON to an object using Marshmallow
    Employment_schema.loads()

    Returns: 
        JSON message. If there is an error, return 400 if the issue is with the validation, 500 if there is a
        database issue, otherwise return message 'Employment added with id= {employment.employment_id}'
    """
    json_data = request.get_json()
    try:
        employment = Employment_schema.load(json_data)

        try:
            db.session.add(employment)
            db.session.commit()
            return {"message": f"Employment added with id= {employment.employment_id}"}
        except exc.SQLAlchemyError as e:
            app.logger.error(f"An error occurred saving the Employment: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)

    except ValidationError as e:
        app.logger.error(f"A Marshmallow ValidationError loading the employment: {str(e)}")
        msg = {'message': "The Employment details failed validation."}
        return make_response(msg, 400)


@app.delete('/Employments/<id>')
def delete_Employment(id):
    """ Deletes the employment with the given id.

    Args:
        param id (int): The id of the employment to delete
    Returns:
        JSON If successful, return success message, otherwise return 404 if employment not found or 500 Internal Server Error
    """
    try:
        employment = db.session.execute(
            db.select(Employment).filter_by(employment_id=id)
        ).scalar_one_or_none()
        db.session.delete(employment)
        db.session.commit()
        return {"message": f"Employment deleted with id= {employment.employment_id}"}
    except exc.SQLAlchemyError as e:
        # Log the exception with the error
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        # Report a 404 error to the user who made the request
        msg_content = f'Employment {id} not found.'
        msg = {'message': msg_content}
        return make_response(msg, 404)


# Routes for Course_level in GET, POST and DELETE
@app.get("/Course_levels")
def get_Course_levels():
    """Returns a list of course levels and their details in JSON.

    Returns:
        JSON for all the course levels, or 500 error if not found
    """
    try:
        # Select all the course levels using Flask-SQLAlchemy
        all_course_levels = db.session.execute(db.select(Course_level)).scalars()
        try:
            # Get the data using Marshmallow schema (returns JSON)
            result = Course_levels_schema.dump(all_course_levels)
            # Return the data
            return result
        except ValidationError as e:
            app.logger.error(f"A Marshmallow ValidationError occurred dumping all course levels: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(f"An error occurred while fetching course levels: {str(e)}")
        msg = {'message': "An Internal Server Error occurred."}
        return make_response(msg, 500)


@app.get("/Course_levels/<id>")
def get_Course_level(id):
    """ Returns one course level in JSON.

    Returns 404 if the course level code is not found in the database.

    Args:
        id (int): The id of the course level to be searched for

    Returns: 
        JSON for the course level if found otherwise 404
    """
    try:
        course_level = db.session.execute(
            db.select(Course_level).filter_by(course_level_id=id)
        ).scalar_one_or_none()
        return Course_level_schema.dump(course_level)
    except exc.NoResultFound as e:
        # See https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json
        app.logger.error(f'Course level code {id} was not found. Error: {e}')
        abort(404, description="Course level not found")


@app.post('/Course_levels')
def add_Course_level():
    """ Adds a new course level.

    Gets the JSON data from the request body and uses this to deserialise JSON to an object using Marshmallow
    course_level_schema.loads()

    Returns: 
        JSON message  If there is an error, return 400 if the issue is with the validation, 500 if there is a
        database issue, otherwise return message 'Course level added with id= {course_level.course_level_id}'
    """
    json_data = request.get_json()
    try:
        course_level = Course_level_schema.load(json_data)

        try:
            db.session.add(course_level)
            db.session.commit()
            return {"message": f"Course level added with id= {course_level.course_level_id}"}
        except exc.SQLAlchemyError as e:
            app.logger.error(f"An error occurred saving the Course level: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)

    except ValidationError as e:
        app.logger.error(f"A Marshmallow ValidationError loading the Course level: {str(e)}")
        msg = {'message': "The Course level details failed validation."}
        return make_response(msg, 400)


@app.delete('/Course_levels/<id>')
def delete_Course_level(id):
    """ Deletes the course level with the given id.

    Args:
        param id (int): The id of the course level to delete
    Returns:
        JSON If successful, return success message, otherwise return 404 if the course level is not found,
        or 500 Internal Server Error for other errors
    """
    try:
        course_level = db.session.execute(
            db.select(Course_level).filter_by(course_level_id=id)
        ).scalar_one_or_none()
        db.session.delete(course_level)
        db.session.commit()
        return {"message": f"Course_level deleted with id= {course_level.course_level_id}"}
    except exc.SQLAlchemyError as e:
        # Log the exception with the error
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        # Report a 404 error to the user who made the request
        msg_content = f'Course_level {id} not found.'
        msg = {'message': msg_content}
        return make_response(msg, 404)


# Routes for Disability in GET, POST and DELETE
@app.get("/Disabilities")
def get_Disabilities():
    """Returns a list of Disability codes and their details in JSON.

    Returns:
        JSON for all the disabilities, or 500 error if not found
    """
    try:
        # Select all the disabilities using Flask-SQLAlchemy
        all_Disability = db.session.execute(db.select(Disability)).scalars()
        try:
            # Get the data using Marshmallow schema (returns JSON)
            result = Disabilities_schema.dump(all_Disability)
            # Return the data
            return result
        except ValidationError as e:
            app.logger.error(f"A Marshmallow ValidationError occurred dumping all disabilities: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(f"An error occurred while fetching disabilities: {str(e)}")
        msg = {'message': "An Internal Server Error occurred."}
        return make_response(msg, 500)


@app.get("/Disabilities/<id>")
def get_Disability(id):
    """ Returns one disability in JSON.

    Returns 404 if the disability id is not found in the database.

    Args:
        id (int): The id of the disability to be searched for

    Returns: 
        JSON for the disability if found otherwise 404
    """
    try:
        disability = db.session.execute(
            db.select(Disability).filter_by(disability_id=id)
        ).scalar_one_or_none()
        return Disability_schema.dump(disability)
    except exc.NoResultFound as e:
        # See https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json
        app.logger.error(f'Disability id {id} was not found. Error: {e}')
        abort(404, description="Disability not found")


@app.post('/Disabilities')
def add_Disability():
    """ Adds a new disability.

    Gets the JSON data from the request body and uses this to deserialise JSON to an object using Marshmallow
    disability_schema.loads()

    Returns: 
        JSON message  If there is an error, return 400 if the issue is with the validation, 500 if there is a
        database issue, otherwise return message 'Disability added with id= {disability.disability_id}'
    """
    json_data = request.get_json()
    try:
        disability = Disability_schema.load(json_data)

        try:
            db.session.add(disability)
            db.session.commit()
            return {"message": f"Disability added with id= {disability.disability_id}"}
        except exc.SQLAlchemyError as e:
            app.logger.error(f"An error occurred saving the Disability: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)

    except ValidationError as e:
        app.logger.error(f"A Marshmallow ValidationError loading the disability: {str(e)}")
        msg = {'message': "The Disability details failed validation."}
        return make_response(msg, 400)


@app.delete('/Disabilities/<id>')
def delete_Disability(id):
    """ Deletes the disability with the given id.

    Args:
        param id (int): The id of the disability to delete
    Returns:
        JSON If successful, return success message, otherwise return 404 if the disability is not found,
        or 500 Internal Server Error for database errors
    """
    try:
        disability = db.session.execute(
            db.select(Disability).filter_by(disability_id=id)
        ).scalar_one_or_none()
        db.session.delete(disability)
        db.session.commit()
        return {"message": f"Disability deleted with id= {disability.disability_id}"}
    except exc.SQLAlchemyError as e:
        # Log the exception with the error
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        # Report a 404 error to the user who made the request
        msg_content = f'Disability {id} not found.'
        msg = {'message': msg_content}
        return make_response(msg, 404)


# Routes for Teacher in GET, POST, DELETE and PATCH
@app.get("/Teachers")
def get_Teachers():
    """Returns a list of Teacher codes and their details in JSON.

    Returns:
        JSON for all the teachers, or 500 error if not found
    """
    try:
        # Select all the teachers using Flask-SQLAlchemy
        all_Teacher = db.session.execute(db.select(Teacher)).scalars()
        try:
            # Get the data using Marshmallow schema (returns JSON)
            result = Teachers_schema.dump(all_Teacher)
            # Return the data
            return result
        except ValidationError as e:
            app.logger.error(f"A Marshmallow ValidationError occurred dumping all teachers: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)
    except exc.SQLAlchemyError as e:
        app.logger.error(f"An error occurred while fetching teachers: {str(e)}")
        msg = {'message': "An Internal Server Error occurred."}
        return make_response(msg, 500)


@app.get("/Teachers/<id>")
def get_Teacher(id):
    """ Returns one teacher in JSON.

    Returns 404 if the teacher id is not found in the database.

    Args:
        id (int): The id of the teacher to be searched for

    Returns: 
        JSON for the teacher if found, otherwise 404
    """
    try:
        teacher = db.session.execute(
            db.select(Teacher).filter_by(teacher_id=id)
        ).scalar_one_or_none()
        return Teacher_schema.dump(teacher)
    except exc.NoResultFound as e:
        # See https://flask.palletsprojects.com/en/2.3.x/errorhandling/#returning-api-errors-as-json
        app.logger.error(f'Teacher with id {id} was not found. Error: {e}')
        abort(404, description="Teacher not found")


@app.post('/Teachers')
def add_Teacher():
    """ Adds a new teacher.

    Gets the JSON data from the request body and uses this to deserialise JSON to an object using Marshmallow
    teacher_schema.loads()

    Returns: 
        JSON message  If there is an error, return 400 if the issue is with the validation, 500 if there is a
        database issue, otherwise return message 'Teacher added with id= {teacher.teacher_id}'
    """
    json_data = request.get_json()
    try:
        teacher = Teacher_schema.load(json_data)

        try:
            db.session.add(teacher)
            db.session.commit()
            return {"message": f"Teacher added with id= {teacher.teacher_id}"}
        except exc.SQLAlchemyError as e:
            app.logger.error(f"An error occurred saving the Teacher: {str(e)}")
            msg = {'message': "An Internal Server Error occurred."}
            return make_response(msg, 500)

    except ValidationError as e:
        app.logger.error(f"A Marshmallow ValidationError loading the teacher: {str(e)}")
        msg = {'message': "The Teacher details failed validation."}
        return make_response(msg, 400)


@app.delete('/Teachers/<id>')
def delete_Teacher(id):
    """ Deletes the teacher with the given id.

    Args:
        id (int): The id of the teacher to delete
    Returns:
        JSON If successful, return success message, otherwise return 500 Internal Server Error
    """
    try:
        teacher = db.session.execute(
            db.select(Teacher).filter_by(teacher_id=id)
        ).scalar_one_or_none()
        db.session.delete(teacher)
        db.session.commit()
        return {"message": f"Teacher deleted with id= {teacher.teacher_id}"}
    except exc.SQLAlchemyError as e:
        # Log the exception with the error
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        # Report a 404 error to the user who made the request
        msg_content = f'Teacher {id} not found.'
        msg = {'message': msg_content}
        return make_response(msg, 404)


@app.patch("/Teachers/<id>")
# Secure routes using the @token_required decorator
@token_required
def Teacher_update(id):
    """Updates changed fields for the specified teacher.

    Args:
        id (int): The id of the teacher to update

    Returns:
        JSON message
            If the teacher with the given id is not found, return 404
            If the JSON contents are not valid, return 500
            If the update is not saved, return 500
            If all OK then return 200
    """
    app.logger.error(f"Started the patch")
    # Find the teacher in the database
    try:
        existing_teacher = db.session.execute(
            db.select(Teacher).filter_by(teacher_id=id)
        ).scalar_one_or_none()
    except exc.SQLAlchemyError as e:
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        msg_content = f'Teacher {id} not found'
        msg = {'message': msg_content}
        return make_response(msg, 404)
    # Get the updated details from the json sent in the HTTP patch request
    teacher_json = request.get_json()
    app.logger.error(f"teacher_json: {str(teacher_json)}")
    # Use Marshmallow to update the existing records with the changes from the json
    try:
        teacher_update = Teacher_schema.load(teacher_json, instance=existing_teacher, partial=True)
    except ValidationError as e:
        app.logger.error(f"A Marshmallow schema validation error occurred: {str(e)}")
        msg = f'Failed Marshmallow schema validation'
        return make_response(msg, 500)
    # Commit the changes to the database
    try:
        db.session.add(teacher_update)
        db.session.commit()
        # Return json message
        response = {"message": f"Teacher {id} updated."}
        return response
    except exc.SQLAlchemyError as e:
        app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
        msg = f'An Internal Server Error occurred.'
        return make_response(msg, 500)


# AUTHENTICATION ROUTES
@app.post("/register")
def register():
    """Register a new user for the REST API

    If successful, return 201 Created.
    If email already exists, return 409 Conflict (resource already exists).
    If any other error occurs, return 500 Server error
    """
    # Get the JSON data from the request
    user_json = request.get_json()
    # Check if user already exists, returns None if the user does not exist
    user = db.session.execute(
        db.select(User).filter_by(email=user_json.get("email"))
    ).scalar_one_or_none()
    if not user:
        try:
            # Create new User object
            user = User(email=user_json.get("email"), user_name=user_json.get("user_name"))
            # Set the hashed password
            user.set_password(password=user_json.get("password"))
            # Add user to the database
            db.session.add(user)
            db.session.commit()
            # Return success message
            response = {
                "message": "Successfully registered.",
            }
            # Log the registered user
            app.logger.info(f"{user.email} registered at {datetime.datetime.now(datetime.UTC)}")
            return make_response(jsonify(response)), 201
        except exc.SQLAlchemyError as e:
            app.logger.error(f"A SQLAlchemy database error occurred: {str(e)}")
            response = {
                "message": "An error occurred. Please try again.",
            }
            return make_response(jsonify(response)), 500
    else:
        response = {
            "message": "User already exists. Please Log in.",
        }
        return make_response(jsonify(response)), 409


@app.post('/login')
def login():
    """Logins in the User and generates a token

    If the email and password are not present in the HTTP request, return 401 error
    If the user is not found in the database, or the password is incorrect, return 401 error
    If the user is logged in and the token is generated, return the token and 201 Success
    """
    auth = request.get_json()

    # Check the email and password are present, if not return a 401 error
    if not auth or not auth.get('email') or not auth.get('password'):
        msg = {'message': 'Missing email or password'}
        return make_response(msg, 401)

    # Find the user in the database
    user = db.session.execute(
        db.select(User).filter_by(email=auth.get("email"))
    ).scalar_one_or_none()

    # If the user is not found, or the password is incorrect, return 401 error
    if not user or not user.check_password(auth.get('password')):
        msg = {'message': 'Incorrect email or password.'}
        return make_response(msg, 401)

    # If all OK then create the token
    token = encode_auth_token(user.user_id)

    # Return the token and the user_id of the logged in user
    return make_response(jsonify({"user_id": user.user_id, "token": token}), 201)
