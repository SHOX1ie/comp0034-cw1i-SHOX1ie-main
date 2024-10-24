from src.models import User, Feedback, Age_group, Gender, Ethnicity, \
    Employment, Course_level, Teacher, Disability
from src import db, ma


# Flask-Marshmallow Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class.
    Inherits all the attributes from the Event class."""

    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class FeedbackSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class.
    Inherits all the attributes from the Event class."""

    class Meta:
        model = Feedback
        include_fk = True
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class Age_groupSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class.
    Inherits all the attributes from the Event class."""

    class Meta:
        model = Age_group
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class GenderSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class.
    Inherits all the attributes from the Event class."""

    class Meta:
        model = Gender
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class EthnicitySchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class.
    Inherits all the attributes from the Event class."""

    class Meta:
        model = Ethnicity
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class EmploymentSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class.
    Inherits all the attributes from the Event class."""

    class Meta:
        model = Employment
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class Course_levelSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class.
    Inherits all the attributes from the Event class."""

    class Meta:
        model = Course_level
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class DisabilitySchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class.
    Inherits all the attributes from the Event class."""

    class Meta:
        model = Disability
        load_instance = True
        sqla_session = db.session
        include_relationships = True


class TeacherSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class.
    Inherits all the attributes from the Event class."""

    class Meta:
        model = Teacher
        include_fk = True
        load_instance = True
        sqla_session = db.session
        include_relationships = True
