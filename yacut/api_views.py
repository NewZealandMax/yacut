import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id(URLMap)
    short = data['custom_id']
    if len(short) > 16 or not re.match(r'^[a-zA-Z0-9]+$', short):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    obj = URLMap.query.filter_by(short=short).first()
    if obj:
        raise InvalidAPIUsage(f'Имя "{short}" уже занято.')
    obj = URLMap()
    obj.from_dict(data)
    db.session.add(obj)
    db.session.commit()
    return jsonify(obj.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    obj = URLMap.query.filter_by(short=short_id).first()
    if obj:
        return jsonify({'url': obj.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
