from http import HTTPStatus

from flask import redirect, render_template

from . import app, db
from .forms import YaCutForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def yacut():
    form = YaCutForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id(URLMap)
        obj = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(obj)
        db.session.commit()
        return render_template('index.html', obj=obj, form=form), HTTPStatus.OK
    return render_template('index.html', form=form)


@app.route('/<short>')
def source(short):
    obj = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(obj.original)
