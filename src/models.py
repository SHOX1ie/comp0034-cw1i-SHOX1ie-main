from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from src import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String, unique=True,
                                               nullable=False)
    user_name: Mapped[str] = mapped_column(db.String, unique=True,
                                           nullable=False)
    feedback: Mapped[List["Feedback"]] = relationship(back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Feedback(db.Model):
    feedback_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    feedback_time: Mapped[str] = mapped_column(db.String, nullable=False)
    feedback_content: Mapped[str] = mapped_column(db.String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    user: Mapped["User"] = relationship(back_populates="feedback")


class Age_group(db.Model):
    __tablename__ = "age_group"
    age_group_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    time_period: Mapped[int] = mapped_column(db.Integer, nullable=False)
    pct_total_age_u25: Mapped[int] = mapped_column(db.Integer, nullable=False)
    pct_total_age_25andover: Mapped[int] = mapped_column(db.Integer,
                                                         nullable=False)


class Gender(db.Model):
    __tablename__ = "gender"
    gender_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    time_period: Mapped[int] = mapped_column(db.Integer, nullable=False)
    pct_total_sex_m: Mapped[int] = mapped_column(db.Integer, nullable=False)
    pct_total_sex_f: Mapped[int] = mapped_column(db.Integer,
                                                 nullable=False)


class Ethnicity(db.Model):
    __tablename__ = "ethnicity"
    ethnicity_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    time_period: Mapped[int] = mapped_column(db.Integer, nullable=False)
    pct_total_ethnic_asian: Mapped[int] = mapped_column(db.Integer,
                                                        nullable=False)
    pct_total_ethnic_black: Mapped[int] = mapped_column(db.Integer,
                                                        nullable=False)
    pct_total_ethnic_white: Mapped[int] = mapped_column(db.Integer,
                                                        nullable=False)
    pct_total_ethnic_mixed_ethnicity: Mapped[int] = mapped_column(
        db.Integer, nullable=False)
    pct_total_ethnic_other: Mapped[int] = mapped_column(db.Integer,
                                                        nullable=False)
    pct_total_ethnic_unknown: Mapped[int] = mapped_column(db.Integer,
                                                          nullable=False)


class Employment(db.Model):
    __tablename__ = "employment"
    employment_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    time_period: Mapped[int] = mapped_column(db.Integer, nullable=False)
    employment_status: Mapped[str] = mapped_column(db.Text, nullable=False)


class Course_level(db.Model):
    __tablename__ = "course_level"
    course_level_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    time_period: Mapped[int] = mapped_column(db.Integer, nullable=False)
    course_level_recoded: Mapped[str] = mapped_column(db.Text,
                                                      nullable=False)


class Disability(db.Model):
    __tablename__ = "disability_group"
    disability_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    time_period: Mapped[int] = mapped_column(db.Integer, nullable=False)
    pct_total_disability: Mapped[str] = mapped_column(db.Integer,
                                                      nullable=False)
    pct_total_nondisability: Mapped[str] = mapped_column(db.Integer,
                                                         nullable=False)
    pct_total_disability_unknown: Mapped[str] = mapped_column(db.Integer,
                                                              nullable=False)


class Teacher(db.Model):
    __tablename__ = "teacher"
    teacher_id: Mapped[int] = mapped_column(db.Integer,
                                            primary_key=True, nullable=False)
    time_period: Mapped[int] = mapped_column(db.Integer, nullable=False)
    qts_status: Mapped[str] = mapped_column(db.Text, nullable=False)
    n_total: Mapped[int] = mapped_column(db.Integer, nullable=False)
