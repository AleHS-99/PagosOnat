from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bd.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)

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
            n_codigo = CodigoPagoMora(codigo=codigo, descripcion=desc,dias_mora1=d1,dias_mora2=d2,dias_mora3=d3,
                                      porcentaje_mora1=pc_1,porcentaje_mora2=pc_2,porcentaje_mora3=pc_3)
            db.session.add(n_codigo)
            db.session.commit()
        return redirect('/codigo')
    else:
        return render_template('cod_add.html')

def create_all_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_all_tables()
    app.run(debug=True)