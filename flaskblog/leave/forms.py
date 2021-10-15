from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, SelectMultipleField, FieldList,FormField
from wtforms.validators import DataRequired,Email




class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')




class UploadDoc(FlaskForm):
    document = FileField('Update document', validators=[FileAllowed(['xlsx', 'xls', 'csv', 'tsv', 'docx', 'doc'])])
    timeZone = SelectField('TimeZone', validators=[DataRequired()])
    upload = SubmitField('Update')
    submit = SubmitField('Submit')



class LeaveappliedDate(FlaskForm):
        date = StringField('Leave Start Date',
                               validators=[DataRequired()])
        enddate = StringField('Leave End Date',
                               validators=[DataRequired()])
        leavetype = RadioField('', choices=[('Half Day Leave','Half Day Leave'),('Full Day Leave','Full Day Leave')])
        submit=SubmitField("Apply Leave")