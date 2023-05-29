from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flaskwebgui import FlaskUI
from werkzeug.serving import WSGIRequestHandler
import os
from datetime import datetime

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

class ContratoPersona(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(250),nullable=False)
    ci = db.Column(db.String(11),nullable=False)
    nit = db.Column(db.String(50),nullable=False)
    codigos = db.Column(db.String(1800),nullable=False)
    salario = db.Column(db.Float)
    fecha_inicio = db.Column(db.String(100))
    lugar = db.Column(db.String(250))
    
class ContratoDueno(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(250),nullable=False)
    ci = db.Column(db.String(11),nullable=False)
    nit = db.Column(db.String(50),nullable=False)
    codigos = db.Column(db.String(1800),nullable=False)
    fecha_inicio = db.Column(db.String(100))
    lugar = db.Column(db.String(250))
    cant_trabajadores = db.Column(db.Integer)

class ImpFijo(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    codigo = db.Column(db.String(50),nullable=False)
    imp = db.Column(db.Float)
    nit = db.Column(db.String(50))

class PagoPersona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    persona_nit = db.Column(db.String(50))
    codigo = db.Column(db.String(50))
    importe = db.Column(db.Float)
    fecha = db.Column(db.String(50))
    estado = db.Column(db.Boolean, default=False)

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
    a = ContratoDueno.query.all()
    b = ContratoPersona.query.all()
    lista = []
    for i in a:
        lista.append(('Dueño de Negocio',i.nombre,i.apellidos,i.lugar,i.nit,i.id))
    for i in b:
        lista.append(('Persona Contratada',i.nombre,i.apellidos,i.lugar,i.nit,i.id))
    return render_template('contract_base.html',lista=lista)

#Contrataciones Add
@app.route('/contrato/add', methods=['GET', 'POST'])
def contrat_add():
    cs = CodigoSimple.query.all()
    cps = CodigoPagoSalarial.query.all()
    cpm = CodigoPagoMora.query.all()
    cdno = ContratoDueno.query.all()
    lugares = []
    for i in cdno:
        lugares.append(i.lugar)
    lista = []
    for i in cs:
        lista.append((i.codigo,i.descripcion))
    for i in cps:
        lista.append((i.codigo,i.descripcion))
    for i in cpm:
        lista.append((i.codigo,i.descripcion))
        
    if request.method=='GET':
        return render_template('contract_add.html',lista=lista,negocio=lugares)
    elif request.method=='POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        ci = request.form.get('ci')
        nit = request.form.get('nit')
        cod = request.form.getlist('codigos[]')
        separator = ','
        my_string = separator.join(cod)
        tipo = request.form.get('tipo_C')
        if tipo=='Persona':
            salario = request.form.get('salario')
            lugar = request.form.get('lugar')
            fecha = request.form.get('date')
            n_contrato = ContratoPersona(nombre=nombre, apellidos=apellidos,ci=ci,nit=nit,codigos=my_string,salario=salario,lugar=lugar,
                                         fecha_inicio=fecha)
            db.session.add(n_contrato)
            db.session.commit()
            flash('El contrato ha sido registrado correctamente.')
            return redirect('/contrato')
        else:
            lugar_2 = request.form.get('lugar_2')
            date1 = request.form.get('date1')
            cant = request.form.get('cant')
            n_contrato = ContratoDueno(nombre=nombre, apellidos=apellidos,ci=ci,nit=nit,codigos=my_string,cant_trabajadores=cant,
                                       lugar=lugar_2, fecha_inicio=date1)
            db.session.add(n_contrato)
            db.session.commit()
            flash('El contrato ha sido registrado correctamente.')
            return redirect('/contrato')
    else:
        pass

@app.route('/contrato/delete/<string:tipo>/<int:id>', methods=['GET', 'POST'])
def contract_delete(tipo,id):
    s=0
    ps = 0
    if tipo=='persona':
        s = db.session.query(ContratoPersona).get_or_404(id)
    else:
        ps = db.session.query(ContratoDueno).get_or_404(id)
        
    if request.method=='GET':
        if not s==0:
            return render_template('contract_delete.html', nit=s.nit)
        elif not ps==0:
            return render_template('contract_delete.html', nit=ps.nit)
        else:
            return redirect('/contrato')
    elif request.method=='POST':
        if not s==0:
            db.session.delete(s)
            db.session.commit()
            flash('El Contrato ha sido eliminado correctamente.')
        elif not ps==0:
            db.session.delete(ps)
            db.session.commit()
            flash('El Contrato ha sido eliminado correctamente.')
        return redirect('/contrato')
    else:
        pass

@app.route('/contrato/edit/<string:tipo>/<int:id>/', methods=['GET', 'POST'])
def contract_edit(tipo,id):
    s=0
    ps = 0
    cdno = ContratoDueno.query.all()
    lugares = []
    for i in cdno:
        lugares.append(i.lugar)
        
    cs = CodigoSimple.query.all()
    cps = CodigoPagoSalarial.query.all()
    cpm = CodigoPagoMora.query.all()
    lista = []
    for i in cs:
        lista.append((i.codigo,i.descripcion))
    for i in cps:
        lista.append((i.codigo,i.descripcion))
    for i in cpm:
        lista.append((i.codigo,i.descripcion))
    
    if tipo == 'persona':
        s = db.session.query(ContratoPersona).get_or_404(id)
    else:
        ps = db.session.query(ContratoDueno).get_or_404(id)
        
    if request.method=='GET':
        if not s==0:
            return render_template('contract_edit.html', tipo=tipo, obj=s, negocio=lugares, lista=lista)
        elif not ps==0:
            return render_template('contract_edit.html', tipo=tipo, obj=ps, negocio=lugares, lista=lista)
        else:
            return redirect('/contrato')
    elif request.method=='POST':
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        ci = request.form.get('ci')
        nit = request.form.get('nit')
        cod = request.form.getlist('codigos[]')
        separator = ','
        my_string = separator.join(cod)
        if tipo=='persona':
            salario = request.form.get('salario')
            lugar = request.form.get('lugar')
            fecha = request.form.get('date')
            s.nombre=nombre
            s.apellidos=apellidos
            s.ci=ci
            s.nit=nit
            s.codigos=my_string
            s.salario=salario
            s.lugar=lugar
            s.fecha_inicio=fecha
            db.session.commit()
            flash('El contrato ha sido editado correctamente.')
            return redirect('/contrato')
        else:
            lugar_2 = request.form.get('lugar_2')
            date1 = request.form.get('date1')
            cant = request.form.get('cant')
            ps.nombre=nombre
            ps.apellidos=apellidos
            ps.ci=ci
            ps.nit=nit
            ps.codigos=my_string
            ps.cant_trabajadores=cant
            ps.lugar=lugar_2
            ps.fecha_inicio=date1
            db.session.commit()
            flash('El contrato ha sido editado correctamente.')
            return redirect('/contrato')
    else:
        return render_template('contract_edit.html')

@app.route('/contrato/personaAdmin/<string:tipo>/<int:id>', methods=['GET', 'POST'])
def admin_p(tipo,id):
    if tipo == 'persona':
        p = ContratoPersona.query.get_or_404(id)
        pagosPersona(id)
        now = datetime.now()
        codigos = len(p.codigos.split(','))
        dias = 0
        pagos=0
        hoy = ''
        fecha_fin = ""
        fecha_inicio = ''
        if now.month<10:
            fecha_inicio = '0{}'.format(now.month)
            fecha_fin = "{}-0{}-{}".format(obtener_dias_del_mes(str(now.month),now.year),now.month,now.year)
            hoy = "{}-0{}-{}".format(now.day,now.month,now.year)
        else:
            fecha_inicio = '{}'.format(now.month)
            fecha_fin = "{}-{}-{}".format(obtener_dias_del_mes(str(now.month),now.year),now.month,now.year) 
            hoy = "{}-{}-{}".format(now.day,now.month,now.year) 
        registros = PagoPersona.query.filter(PagoPersona.fecha.between(fecha_inicio, fecha_fin)).all()
        todos = PagoPersona.query.filter_by(persona_nit=p.nit,estado=True).order_by(PagoPersona.id.desc()).all()
        for i in registros:
            if not i.estado:
                dias = dias_de_retraso(i.fecha)
            else:
                if i.fecha[3:5]==hoy[3:5] and i.fecha[6:]==hoy[6:]:
                    pagos+=1
        if request.method=='GET':        
            return render_template('admin_persona.html',obj=p, pagos = registros, hoy=hoy,atraso=dias,cod=pagos,total=codigos, todas=todos)
        elif request.method=='POST':
            try:
                action = request.form.get('action')
                if action == 'cod':
                    cod = request.form.get('codigo')
                    repo = PagoPersona.query.filter_by(persona_nit=p.nit,estado=False,codigo=cod).order_by(PagoPersona.id.desc()).first()
                    repo.estado=True
                    db.session.commit()
                    return redirect(url_for('admin_p',tipo=tipo,id=id))
            except Exception as e:
                print(e)
    
@app.route('/contrato/personaAdmin/impfijo/<string:tipo>/<int:id>')
def impFijo(tipo,id):
    if tipo == 'persona':
        p = ContratoPersona.query.get_or_404(id)
        lista = ImpFijo.query.filter_by(nit=p.nit).all()
        return render_template('imp_fijo.html',obj=p, imp=lista)
    else:
        return redirect(url_for('admin_p',tipo=tipo,id=id))
    
@app.route('/contrato/personaAdmin/impfijo/add/<string:tipo>/<int:id>', methods=['GET', 'POST'])
def impFijoAdd(tipo,id):
    if tipo == 'persona':
        p = ContratoPersona.query.get_or_404(id)
        if request.method=='GET':
            cs = CodigoSimple.query.all()
            cps = CodigoPagoSalarial.query.all()
            cpm = CodigoPagoMora.query.all()
            lista = []
            for i in cs:
                lista.append((i.codigo,i.descripcion))
            for i in cps:
                lista.append((i.codigo,i.descripcion))
            for i in cpm:
                lista.append((i.codigo,i.descripcion))
            return render_template('imp_fijoAdd.html',obj=p,lista=lista)
        elif request.method=='POST':
            cod = request.form.get('codigos')
            imp = request.form.get('importe')
            n_importe = ImpFijo(codigo=cod,imp=imp,nit=p.nit)
            db.session.add(n_importe)
            db.session.commit()
            flash('El importe fijo ha sido añadido correctamente.')
            return redirect(url_for('impFijo', tipo=tipo, id=id))
    else:
        return redirect(url_for('impFijo',tipo=tipo,id=id))
    
@app.route('/contrato/personaAdmin/impfijo/edit/<string:tipo>/<int:id>/<int:second>', methods=['GET', 'POST'])
def impFijoEdit(tipo,id,second):
    if tipo == 'persona':
        p = ContratoPersona.query.get_or_404(id)
        s = ImpFijo.query.get_or_404(second)
        if request.method=='GET':
            cs = CodigoSimple.query.all()
            cps = CodigoPagoSalarial.query.all()
            cpm = CodigoPagoMora.query.all()
            lista = []
            for i in cs:
                lista.append((i.codigo,i.descripcion))
            for i in cps:
                lista.append((i.codigo,i.descripcion))
            for i in cpm:
                lista.append((i.codigo,i.descripcion))
            return render_template('imp_fijoEdit.html',obj=p,lista=lista,value=s)
        elif request.method=='POST':
            cod = request.form.get('codigos')
            imp = request.form.get('importe')
            s.codigo=cod
            s.imp=imp
            s.nit = p.nit
            db.session.commit()
            flash('El importe fijo ha sido editado correctamente.')
            return redirect(url_for('impFijo', tipo=tipo, id=id))
    else:
        return redirect(url_for('impFijo',tipo=tipo,id=id))

@app.route('/contrato/personaAdmin/impfijo/delete/<string:tipo>/<int:id>/<int:second>', methods=['GET', 'POST'])
def imp_FijoDelete(tipo,id,second):
    if tipo == 'persona':
        p = ContratoPersona.query.get_or_404(id)
        s = ImpFijo.query.get_or_404(second)
        
    if request.method=='GET':
        return render_template('imp_FijoDelete.html', nit=s.codigo, obj=p)
    elif request.method=='POST':
        db.session.delete(s)
        db.session.commit()
        flash('El Importe ha sido eliminado correctamente.')
        return redirect(url_for('impFijo', tipo=tipo, id=id))
    else:
        pass

#Crear Tablas BD
def create_all_tables():
    with app.app_context():
        db.create_all()

#Aqui se comprueban los apgos de la persona
def pagosPersona(id):
    j = ContratoPersona.query.get_or_404(id)
    lista = ImpFijo.query.filter_by(nit=j.nit).all()
    pagos = PagoPersona.query.filter_by(persona_nit=j.nit).all()
    now = datetime.now()
    mes_actual = 0
    if now.month<10:
        mes_actual = '0{}'.format(now.month)
    else:
        mes_actual = '{}'.format(now.month)
    
    codigos = []
    for i in lista:
        codigos.append(i.codigo)
    cod = 0
    for i in j.codigos.split(','):
        if not i in codigos:
            cod = i
    
    if not cod == 0:
        cod_sal = CodigoPagoSalarial.query.filter_by(codigo=cod).first()
        imp = 0
        if j.salario <= cod_sal.monto_excento:
            pass
        elif j.salario > cod_sal.monto_excento and j.salario <= cod_sal.monto_pago1:
            decimal_porcentaje = cod_sal.porcentaje1 / 100
            imp = j.salario*decimal_porcentaje
        elif j.salario > cod_sal.monto_pago1 and j.salario <= cod_sal.monto_pago2:
            decimal_porcentaje = cod_sal.porcentaje2 / 100
            imp = j.salario*decimal_porcentaje
        elif j.salario > cod_sal.monto_pago2 and j.salario <= cod_sal.monto_pago3:
            decimal_porcentaje = cod_sal.porcentaje3 / 100
            imp = j.salario*decimal_porcentaje
        elif j.salario > cod_sal.monto_pago3 and j.salario <= cod_sal.monto_pago4:
            decimal_porcentaje = cod_sal.porcentaje4 / 100
            imp = j.salario*decimal_porcentaje
        elif j.salario > cod_sal.monto_pago4 and j.salario <= cod_sal.monto_pago5:
            decimal_porcentaje = cod_sal.porcentaje5 / 100
            imp = j.salario*decimal_porcentaje
        elif j.salario > cod_sal.monto_pago6:
            decimal_porcentaje = cod_sal.porcentaje6 / 100
            imp = j.salario*decimal_porcentaje
            
        if not imp == 0:
            r = PagoPersona.query.filter_by(persona_nit=j.nit, codigo=cod).order_by(PagoPersona.id.desc()).first()
            if r:
                if not mes_actual in r.fecha[3:5]:
                    nuevo_pago = PagoPersona(persona_nit=j.nit, codigo=cod,
                                            fecha="{}-{}-{}".format(j.fecha_inicio[:2],mes_actual,now.year),
                                            importe=imp,estado=False)
                    db.session.add(nuevo_pago)
                    db.session.commit()
            else:
                nuevo_pago = PagoPersona(persona_nit=j.nit, codigo=cod,
                                            fecha="{}-{}-{}".format(j.fecha_inicio[:2],mes_actual,now.year),
                                            importe=imp,estado=False)
                db.session.add(nuevo_pago)
                db.session.commit()

    for imp_fijo in lista:
        r = PagoPersona.query.filter_by(persona_nit=j.nit, codigo=imp_fijo.codigo).order_by(PagoPersona.id.desc()).first()
        if r:
            if not mes_actual in r.fecha[3:5]:
                nuevo_pago = PagoPersona(persona_nit=j.nit, codigo=imp_fijo.codigo,
                                        fecha="{}-{}-{}".format(j.fecha_inicio[:2],mes_actual,now.year),
                                        importe=imp_fijo.imp,estado=False)
                db.session.add(nuevo_pago)
                db.session.commit()
        else:
            nuevo_pago = PagoPersona(persona_nit=j.nit, codigo=imp_fijo.codigo,
                                        fecha="{}-{}-{}".format(j.fecha_inicio[:2],mes_actual,now.year),
                                        importe=imp_fijo.imp,estado=False)
            db.session.add(nuevo_pago)
            db.session.commit()
    
def es_bisiestro(anio:int)->bool:
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0) 

def obtener_dias_del_mes(mes:str,anio:int)->int:
    if mes in ['4','6','9','11']:
        return 30
    if mes == '2':
        if es_bisiestro(anio):
            return 29
        else:
            return 28
    else:
        return 31

def dias_de_retraso(fecha):
    fecha_str = datetime.strptime(fecha, '%d-%m-%Y').date()
    fecha_actual = datetime.now().date()
    dias_retraso = (fecha_actual - fecha_str).days
    if dias_retraso < 0:
        return 0
    else:
        return dias_retraso

if __name__ == '__main__':
    create_all_tables()
    #app.run()
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    ui.run()
