# coding: utf-8
from flask import render_template, json, Blueprint, request
#from ..initApp import app
from .. import config
from ..database import *
from .. import utils
from werkzeug.wrappers import Response 


validation = Blueprint('validation', __name__, static_url_path="/validation", static_folder="static", template_folder="templates")



@validation.route("/")
def indexValidation():
    db = getConnexion()
    sql = config.LOAD_OBS
    res = utils.sqltoDict(sql, db.cur)
    nom_vern = None
    for r in res:
        if r['nom_vern'] == None:
            r['nom_vern'] = '-'
        r['nom_vern'] = r['nom_vern'].decode('utf-8')

    geojson = utils.simpleGeoJson(res, 'geom', ['id_synthese'])
    db.closeAll()
    return render_template('indexValidation.html', URL_APPLICATION=config.URL_APPLICATION, taxList=res, geojson = geojson, page_title=u"Interface de validation des données", MAPCONFIG = config.MAPCONFIG)




@validation.route('/delete/<id_synt>')
def deleteRow(id_synt):
    db = getConnexion()
    id_synt = str(id_synt)
    sql = """DELETE FROM """+ config.OBS_TABLE +""" WHERE """+config.ID_OBSERVATION+""" = %s; """
    param = [id_synt]
    db.cur.execute(sql, param) 
    db.conn.commit()
    db.closeAll()
    return json.dumps({'success':True, 'id_synthese':id_synt}), 200, {'ContentType':'application/json'}


@validation.route('/validate', methods=['GET', 'POST'])
def validate():
    db = getConnexion()
    #id_synt = str(id_synt)
    tab = list()
    id_synt = tuple()
    if request.method == 'POST':
        id_synt = request.json['validate']
        if type(id_synt) != str:
            tab.append(id_synt)
            tupleSynth = tuple(tab)
        else:
            tupleSynth = tuple(id_synt)
        sql = config.VALIDATE_OBS
        param = [tupleSynth]
        db.cur.execute(sql,param) 
        db.conn.commit()
    db.closeAll()
    return json.dumps({'success':True, 'id_synthese':id_synt}), 200, {'ContentType':'application/json'}
