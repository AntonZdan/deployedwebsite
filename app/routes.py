from flask import request, redirect, url_for, flash, render_template, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from .models import Produktas, Vartotojas, Irasas
from . import db

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        el_pastas = request.form.get('el_pastas')
        slaptazodis = request.form.get('slaptazodis')

        vart = Vartotojas.query.filter_by(el_pastas=el_pastas).first()

        if vart and vart.slaptazodis == slaptazodis:
            login_user(vart)
            return redirect(url_for('main.records'))
        flash('Neteisingi prisijungimo duomenys', 'danger')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/irasai')
@login_required
def records():
    page = request.args.get('page', 1, type=int)

    query = Irasas.query.filter_by(vartotojas_id=current_user.id).order_by(Irasas.data.desc())
    visi_irasai = query.paginate(page=page, per_page=5)

    return render_template('irasai.html', visi_irasai=visi_irasai, datetime=datetime)

@main.route('/produktai')
def produktai():
    page = request.args.get('page', 1, type=int)
    visi_produktai = Produktas.query.order_by(Produktas.pavadinimas).paginate(page=page, per_page=4)
    return render_template('produktai.html', visi_produktai=visi_produktai)

@main.route('/new-record')
@login_required
def new_record():
    ir = Irasas(suma=123, pajamos=True, vartotojas_id=current_user.id)
    db.session.add(ir)
    db.session.commit()
    flash('Irasas sukurtas (demo forma)', 'success')
    return redirect(url_for('main.records'))

# Route for testing
@main.route("/uzpildyti-produktus")
def uzpildyti_produktus():
    pavadinimai = ["Obuolys", "Bananas", "Vanduo", "Sūris", "Duona", "Pomidoras", "Agurkas", "Pienas",
                   "Mėsa", "Kava", "Arbata", "Sviestas", "Jogurtas", "Apelsinas", "Ryžiai", "Makaronai",
                   "Saldainiai", "Druska", "Cukrus", "Šokoladas", "Kiaušiniai", "Faršas", "Limonadas",
                   "Džiūvėsiai", "Čipsai", "Kukurūzai", "Tortas", "Majonezas", "Ketchupas", "Aliejus"]
    for i, p in enumerate(pavadinimai):
        produktas = Produktas(pavadinimas=p, kaina=round(1.0 + i * 0.5, 2))
        db.session.add(produktas)
    db.session.commit()
    return "Produktai pridėti"
