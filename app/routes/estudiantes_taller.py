from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from ..models import Estudiantes, Taller, EstudianteTaller
from ..extensions import db

estudiantes_taller_bp = Blueprint('estudiantes_taller', __name__)

@estudiantes_taller_bp.route('/', methods=['GET', 'POST'])
@login_required
def gestionar_estudiantes_taller():
    if request.method == 'POST':
        taller_id = request.form['taller_id']
        id_estudiantes = request.form.getlist('id_estudiantes')
        
        for id_estudiante in id_estudiantes:
            nueva_asignacion = EstudianteTaller(
                id_estudiante=id_estudiante,
                taller_id=taller_id
            )
            db.session.add(nueva_asignacion)
        
        db.session.commit()
        flash('Estudiantes asignados correctamente al taller', 'success')
        return redirect(url_for('estudiantes_taller.gestionar_estudiantes_taller'))
    
    estudiantes = Estudiantes.query.all()
    talleres = Taller.query.all()
    cursos = list(set(estudiante.curso for estudiante in estudiantes))
    asignaciones = EstudianteTaller.query.all()

    return render_template('gestionar_estudiantes_taller.html', estudiantes=estudiantes, talleres=talleres, cursos=cursos, asignaciones=asignaciones)

@estudiantes_taller_bp.route('/delete/<int:id_taller_estudiante>', methods=['POST'])
@login_required
def delete_estudiante_taller(id_taller_estudiante):
    asignacion = EstudianteTaller.query.get_or_404(id_taller_estudiante)
    db.session.delete(asignacion)
    db.session.commit()
    flash('Asignación eliminada correctamente', 'success')
    return redirect(url_for('estudiantes_taller.gestionar_estudiantes_taller'))