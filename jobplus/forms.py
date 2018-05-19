from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, TextAreaField
from wtforms.validators import Length, Email, EqualTo, Required
from jobplus.models import db, User, CompanyDetail

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6,24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')
    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
class RegisterForm(FlaskForm):
    name = StringField('???', validators=[Required(), Length(3, 24)])
    email = StringField('??', validators=[Required(), Email()])
    password = PasswordField('??', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('????', validators=[Required(), EqualTo('password')])
    submit = SubmitField('??')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('??????')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('??????')

    def create_user(self):
        user = User(name=self.name.data,
                    email=self.email.data,
                    password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user


class UserProfileForm(FlaskForm):
    real_name = StringField('??')
    email = StringField('??', validators=[Required(), Email()])
    password = PasswordField('??(???????)')
    phone = StringField('???')
    work_years = IntegerField('????')
    resume_url = StringField('????')
    submit = SubmitField('??')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('?????????')

    def updated_profile(self, user):
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.resume_url = self.resume_url.data
        db.session.add(user)
        db.session.commit()


class CompanyProfileForm(FlaskForm):
    name = StringField('????')
    email = StringField('??', validators=[Required(), Email()])
    password = PasswordField('??(???????)')
    slug = StringField('Slug', validators=[Required(), Length(3, 24)])
    location = StringField('??', validators=[Length(0, 64)])
    site = StringField('????', validators=[Length(0, 64)])
    logo = StringField('Logo')
    description = StringField('?????', validators=[Length(0, 100)])
    about = TextAreaField('????', validators=[Length(0, 1024)])
    submit = SubmitField('??')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('?????????')

    def updated_profile(self, user):
        user.name = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.company_detail:
            company_detail = user.company_detail
        else:
            company_detail = CompanyDetail()
            company_detail.user_id = user.id
        self.populate_obj(company_detail)
        db.session.add(user)
        db.session.add(company_detail)
        db.session.commit()
