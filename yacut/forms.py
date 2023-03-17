from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError

from .models import URLMap


class YaCutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле.'),
            Length(1, 1024),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Regexp(
                r'^[a-zA-Z0-9]+$',
                message='Ссылка должна содержать только цифры и латинские буквы.'
            ),
            Length(
                0,
                16,
                message='Длина ссылки не должна превышать 16 символов.'),
            Optional(),
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(f'Имя {field.data} уже занято!')
