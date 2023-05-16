from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flaskwebgui import FlaskUI
from werkzeug.serving import WSGIRequestHandler
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bd.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.secret_key = 'secret!'
db = SQLAlchemy(app)

def start_flask(**server_kwargs):

    app = server_kwargs.pop("app", None)
    server_kwargs.pop("debug", None)

    try:
        import waitress

        waitress.serve(app, **server_kwargs)
    except:
        app.run(**server_kwargs)

ui = FlaskUI(app=app,
             server=start_flask,
             server_kwargs={
            "app": app,
            "port": 3000,
            "threaded": True,
        },)

#Diseño base de datos
class CodigoSimple(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    porcentaje = db.Column(db.Float, nullable=True)
    fecha_pago = db.Column(db.String(200), nullable=False)

class CodigoPagoSalarial(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    monto_excento = db.Column(db.Float, nullable=False)
    monto_pago1 = db.Column(db.Float, nullable=False)
    porcentaje1 = db.Column(db.Float, nullable=False)
    monto_pago2 = db.Column(db.Float, nullable=False)
    porcentaje2 = db.Column(db.Float, nullable=False)
    monto_pago3 = db.Column(db.Float, nullable=False)
    porcentaje3 = db.Column(db.Float, nullable=False)
    monto_pago4 = db.Column(db.Float, nullable=False)
    porcentaje4 = db.Column(db.Float, nullable=False)
    monto_pago5 = db.Column(db.Float, nullable=False)
    porcentaje5 = db.Column(db.Float, nullable=False)
    monto_pago6 = db.Column(db.Float, nullable=False)
    porcentaje6 = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.String(200), nullable=False)
    
class CodigoPagoMora(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    porcentaje_mora1 = db.Column(db.Float, nullable=False)
    dias_mora1 = db.Column(db.Integer, nullable=False)
    porcentaje_mora2 = db.Column(db.Float)
    dias_mora2 = db.Column(db.Integer)
    porcentaje_mora3 = db.Column(db.Float)
    porcentaje_mora3_2 = db.Column(db.Float)
    dias_mora3 = db.Column(db.Integer)

#Pagina Principal
@app.route('/')
def Home():
    return render_template('index.html')

#Codigo Tributario
@app.route('/codigo')
def cod_base():
    c_simple = db.session.query(CodigoSimple).all()
    c_pagoSalario = db.session.query(CodigoPagoSalarial).all()
    c_pagoMora = db.session.query(CodigoPagoMora).all()
    list = []
    for i in c_simple:
        list.append((i.id,i.codigo,i.descripcion,'simple'))
    for i in c_pagoSalario:
        list.append((i.id,i.codigo,i.descripcion,'salario'))
    for i in c_pagoMora:
        list.append((i.id,i.codigo,i.descripcion,'mora'))
    return render_template('cod_base.html',list=list)

#Codigo Tributario Add
@app.route('/codigo/add', methods=['GET', 'POST'])
def cod_add():
    if request.method =='GET':
        return render_template('cod_add.html')
    elif request.method == 'POST':
        codigo = request.form.get('codigo')
        desc = request.form.get('descripcion')
        tipo = request.form.get('tipo')
        if tipo == 'simple':
            fecha = request.form.get('fecha_pago')
            pc = request.form.get('porcentaje')
            n_codigo = CodigoSimple(codigo=codigo, descripcion=desc, porcentaje=pc, fecha_pago=fecha)
            db.session.add(n_codigo)
            db.session.commit()
        elif tipo == 'pago_salarial':
            fecha = request.form.get('fecha_pago')
            s_excento = request.form.get('salario_excento')
            s_1 = request.form.get('tope1')
            s_2 = request.form.get('tope2')
            s_3 = request.form.get('tope3')
            s_4 = request.form.get('tope4')
            s_5 = request.form.get('tope5')
            s_6 = request.form.get('tope6')
            pc_1 = request.form.get('porcentaje1')
            pc_2 = request.form.get('porcentaje2')
            pc_3 = request.form.get('porcentaje3')
            pc_4 = request.form.get('porcentaje4')
            pc_5 = request.form.get('porcentaje5')
            pc_6 = request.form.get('porcentaje6')
            n_codigo = CodigoPagoSalarial(codigo=codigo, descripcion=desc, fecha_pago=fecha, monto_excento= s_excento, 
                                          monto_pago1=s_1, monto_pago2=s_2,monto_pago3=s_3,monto_pago4=s_4,monto_pago5=s_5,
                                          monto_pago6=s_6,porcentaje1=pc_1,porcentaje2=pc_2,porcentaje3=pc_3,porcentaje4=pc_4,
                                          porcentaje5=pc_5,porcentaje6=pc_6)
            db.session.add(n_codigo)
            db.session.commit()
        else:
            d1 = request.form.get('dias_mora1')
            d2 = request.form.get('dias_mora2')
            d3 = request.form.get('dias_mora3')
            pc_1 = request.form.get('porcentaje_mora1')
            pc_2 = request.form.get('porcentaje_mora2')
            pc_3 = request.form.get('porcentaje_mora3')
            pc_32 = request.form.get('porcentaje_mora4')
            n_codigo = CodigoPagoMora(codigo=codigo, descripcion=desc,dias_mora1=d1,dias_mora2=d2,dias_mora3=d3,
                                      porcentaje_mora1=pc_1,porcentaje_mora2=pc_2,porcentaje_mora3=pc_3,porcentaje_mora3_2=pc_32)
            db.session.add(n_codigo)
            db.session.commit()
        flash('El código ha sido añadido correctamente.')
        return redirect('/codigo')
    else:
        return render_template('cod_add.html')
  
#Codigo Tributario   Delete
@app.route('/codigo/delete/<string:tipo>/<int:id>', methods=['GET', 'POST'])
def delete_cod(tipo,id):
    s=0
    ps = 0
    pm = 0
    if tipo == 'simple':
        s = db.session.query(CodigoSimple).get_or_404(id)
    elif tipo == 'salario':
        ps = db.session.query(CodigoPagoSalarial).get_or_404(id)
    elif tipo == 'mora':
        pm = db.session.query(CodigoPagoMora).get_or_404(id)
    else:
        pass
    if request.method=='GET':
        if not s==0:
            return render_template('cod_delete.html', codigo=s.codigo)
        elif not ps==0:
            return render_template('cod_delete.html', codigo=ps.codigo)
        elif not pm==0:
            return render_template('cod_delete.html', codigo=pm.codigo)
        else:
            return redirect('/codigo')
    elif request.method=='POST':
        if not s==0:
            db.session.delete(s)
            db.session.commit()
            flash('El código ha sido eliminado correctamente.')
        elif not ps==0:
            db.session.delete(ps)
            db.session.commit()
            flash('El código ha sido eliminado correctamente.')
        elif not pm==0:
            db.session.delete(pm)
            db.session.commit()
            flash('El código ha sido eliminado correctamente.')
        return redirect('/codigo')
    else:
        return render_template('cod_delete.html')

#Codigo Tributario Edit
@app.route('/codigo/edit/<string:tipo>/<int:id>/', methods=['GET', 'POST'])
def cod_edit(tipo,id):
    s=0
    ps = 0
    pm = 0
    if tipo == 'simple':
        s = db.session.query(CodigoSimple).get_or_404(id)
    elif tipo == 'salario':
        ps = db.session.query(CodigoPagoSalarial).get_or_404(id)
    elif tipo == 'mora':
        pm = db.session.query(CodigoPagoMora).get_or_404(id)
    else:
        pass
    if request.method=='GET':
        if not s==0:
            return render_template('cod_edit.html', tipo=tipo, obj=s)
        elif not ps==0:
            return render_template('cod_edit.html', tipo=tipo, obj=ps)
        elif not pm==0:
            return render_template('cod_edit.html', tipo=tipo, obj=pm)
        else:
            return redirect('/codigo')
    elif request.method=='POST':
        codigo = request.form.get('codigo')
        desc = request.form.get('descripcion')
        if not s == 0:
            fecha = request.form.get('fecha_pago')
            pc = request.form.get('porcentaje')
            s.codigo=codigo 
            s.descripcion=desc
            s.porcentaje=pc
            s.fecha_pago=fecha
            db.session.commit()
        elif not ps == 0:
            fecha = request.form.get('fecha_pago')
            s_excento = request.form.get('salario_excento')
            s_1 = request.form.get('tope1')
            s_2 = request.form.get('tope2')
            s_3 = request.form.get('tope3')
            s_4 = request.form.get('tope4')
            s_5 = request.form.get('tope5')
            s_6 = request.form.get('tope6')
            pc_1 = request.form.get('porcentaje1')
            pc_2 = request.form.get('porcentaje2')
            pc_3 = request.form.get('porcentaje3')
            pc_4 = request.form.get('porcentaje4')
            pc_5 = request.form.get('porcentaje5')
            pc_6 = request.form.get('porcentaje6')
            ps.codigo=codigo
            ps.descripcion=desc
            ps.fecha_pago=fecha
            ps.monto_excento= s_excento
            ps.monto_pago1=s_1
            ps.monto_pago2=s_2
            ps.monto_pago3=s_3
            ps.monto_pago4=s_4
            ps.monto_pago5=s_5
            ps.monto_pago6=s_6
            ps.porcentaje1=pc_1
            ps.porcentaje2=pc_2
            ps.porcentaje3=pc_3
            ps.porcentaje4=pc_4
            ps.porcentaje5=pc_5
            ps.porcentaje6=pc_6
            db.session.commit()
        else:
            d1 = request.form.get('dias_mora1')
            d2 = request.form.get('dias_mora2')
            d3 = request.form.get('dias_mora3')
            pc_1 = request.form.get('porcentaje_mora1')
            pc_2 = request.form.get('porcentaje_mora2')
            pc_3 = request.form.get('porcentaje_mora3')
            pc_32 = request.form.get('porcentaje_mora4')
            pm.codigo=codigo
            pm.descripcion=desc
            pm.dias_mora1=d1
            pm.dias_mora2=d2
            pm.dias_mora3=d3
            pm.porcentaje_mora1=pc_1
            pm.porcentaje_mora2=pc_2
            pm.porcentaje_mora3=pc_3
            pm.porcentaje_mora3_2=pc_32
            db.session.commit()
        flash('El código ha sido Editado correctamente.')
        return redirect('/codigo')
    else:
        return render_template('cod_edit.html')

#Contrataciones
@app.route('/contrato')
def contrat_base():
    return render_template('contract_base.html')

#Contrataciones Add
@app.route('/contrato/add', methods=['GET', 'POST'])
def contrat_add():
    if request.method=='GET':
        return render_template('contract_add.html')
    elif request.method=='POST':
        pass
    else:
        pass

#Crear Tablas BD
def create_all_tables():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_all_tables()
    app.run()
    #WSGIRequestHandler.protocol_version = "HTTP/1.1"
    #ui.run()
