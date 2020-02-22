# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import telnetlib
#from app import *
from app import app
from app import db
from flask import render_template, request, flash, session, url_for, redirect, make_response, jsonify
import pdfkit
#from flask import send_file, send_from_directory, safe_join, abort, jsonify
import pymysql.cursors
import pymysql
from models import User, SwInfo, VlanInfo
from flask_security import login_required


@app.route("/login",methods = ['POST', 'GET'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    user = User.query.filter_by(login=login, password=password).first()
    if not user:
        flash('Please enter correct data')
        return render_template('login.html')
    return render_template('index.html')



@app.route("/shell",methods = ['POST', 'GET'])
@login_required
def shell():
    return render_template('shell.html')



@app.route("/vagrant",methods = ['POST', 'GET'])
@login_required
def vagrant():
    ip = request.form.get('ip')
    command = request.form.get('command')
    command_success = 'python scripts/command.py'+' ' + str(ip) + ' ' +  '"' + command + '"'
    result = subprocess.check_output(
                [command_success], shell=True)
    print(result)
    return render_template('top.html', result=result)


#Resume
@app.route('/summary')
def resume():

    return render_template('index.html', title='Resume')


@app.route('/summary/pdf')
def pdf():
    rendered = render_template('test.html')
    pdf = pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type'] ='application/pdf'
    response.headers['Content-Disposition'] ='attachment; filename=output.pdf'

    return response



#Generator
@app.route('/generator')
@login_required
def config():

    return render_template('config.html', title='Generator')



@app.route('/get-config', methods = ['POST'])
@login_required
def getconfig():
    vlanext = request.form.get('vlanext')
    vlanextid = request.form.get('vlanextid')
    vlannat = request.form.get('vlannat')
    vlannatid = request.form.get('vlannatid')
    vlanfake = request.form.get('vlanfake')
    vlanfakeid = request.form.get('vlanfakeid')
    vlansw = request.form.get('vlansw')
    vlanswid = request.form.get('vlanswid')
    ip = request.form.get('ip')
    gateway = ip[:6]+'.1'
    return render_template('get-config.html',vlanext=vlanext, vlanextid=vlanextid, 
                          vlannat=vlannat, vlannatid=vlannatid, vlanfake=vlanfake ,
                          vlanfakeid=vlanfakeid, vlansw=vlansw, vlanswid=vlanswid, ip=ip, gateway=gateway)



@app.route('/vlan-list')
@login_required
def vlanlist():
    conn = ( pymysql.connect(host = '185.190.150.7',
                             user = 'script',
                             password = 'golden1306!',
                             database = 'service',
                             charset='utf8' ) )

    cursor = conn.cursor()
    mySql_select_Query = '''SELECT h.id
                             , k.name type
                             , h.name
                             , h.startIp
                             , h.stopIp
                             , h.gateway
                             , h.mask
                             , vl.vlan vlans
                             ,(SELECT count(*) FROM eq_bindings WHERE INET_ATON(ip) BETWEEN INET_ATON(startIp) and INET_ATON(stopIp)) bindings
                             FROM `eq_neth` h
                             JOIN eq_kinds k on k.id = h.type
                             LEFT JOIN (SELECT GROUP_CONCAT(vl.vlan) vlan, neth FROM eq_vlan_neth n JOIN eq_vlans vl on vl.id = n.vlan GROUP BY neth) vl on vl.neth = h.id
                             ORDER  by 2,4'''
    cursor.execute(mySql_select_Query)
    return render_template('vlan-list.html', cursor=cursor)
    cursor.close()
    conn.close()


@app.route("/get-image/<image_name>")
def get_image(image_name):

    try:
        return send_from_directory(app.config["FILE_STORAGE"], filename=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

#SWITCH_INFO

@app.route("/switch-info" ,methods = ['POST', 'GET'])
def swinfo():
    sw = SwInfo.query.all()
    return render_template('SW_INFO/switch-info.html',sw=sw)



@app.route("/switch-add/new",methods = ['POST', 'GET'])
@login_required
def swnew():

    return render_template('SW_INFO/switch-add-new.html')




@app.route("/switch-add",methods = ['POST', 'GET'])
@login_required
def swadd():

    sw = request.form.get('sw')
    ip = request.form.get('ip')
    location = request.form.get('location')
    presence = request.form.get('presence')
    fvlan = request.form.get('fvlan')
    model = request.form.get('model')

    s = SwInfo(sw=sw, ip=ip, location=location, presence=presence, fixed_vlan=fvlan, model=model)
    db.session.add(s)
    db.session.commit()
    return redirect(url_for('swinfo'))


@app.route("/switch-edit=<int:id>",methods = ['POST', 'GET'])
@login_required
def swedit(id):
    switches = SwInfo.query.filter(SwInfo.id == id)
    return render_template('SW_INFO/switch-edit.html',switches=switches)


@app.route("/switch-update",methods = ['POST', 'GET'])
@login_required
def swupdate():

    if request.method == 'POST':
        id = request.form.get('id')
        sw = request.form.get('sw')
        ip = request.form.get('ip')
        location = request.form.get('location')
        presence = request.form.get('presence')
        fvlan = request.form.get('fvlan')
        model = request.form.get('model')

        s = SwInfo.query.filter(SwInfo.id == id).first()
        s.sw = sw
        s.ip = ip
        s.location = location
        s.presence = presence
        s.fixed_vlan = fvlan
        s.model = model
        db.session.commit()

    return redirect(url_for('swinfo'))

#VLAN_INFO

@app.route("/switch-vlan" ,methods = ['POST', 'GET'])
def vinfo():
    vlan = VlanInfo.query.all()
    return render_template('VLAN_INFO/switch-vlan.html',vlan=vlan)


@app.route("/switch-vlan/new" ,methods = ['POST', 'GET'])
def vnew():

    return render_template('VLAN_INFO/switch-vlan-new.html')

@app.route("/switch-vlan/add" ,methods = ['POST', 'GET'])
def vadd():

    if request.method == 'POST':
        vlanid = request.form.get('vlanid')
        vlanname = request.form.get('vlanname')
        network = request.form.get('network')
        group = request.form.get('group')
        desc = request.form.get('desc')
       
        v = VlanInfo(vlanid=vlanid, vlanname=vlanname, network=network, group=group, desc=desc)
        db.session.add(v)
        db.session.commit()


    return redirect(url_for('vinfo'))


@app.route("/vlan-edit=<int:id>",methods = ['POST', 'GET'])
@login_required
def vedit(id):
    vlan = VlanInfo.query.filter(VlanInfo.id == id)
    return render_template('VLAN_INFO/switch-vlan-edit.html',vlan=vlan)



@app.route("/switch-vlan/edit",methods = ['POST', 'GET'])
@login_required
def vupdate():

    if request.method == 'POST':
        id = request.form.get('id')
        vlanid = request.form.get('vlanid')
        vlanname = request.form.get('vlanname')
        network = request.form.get('network')
        group = request.form.get('group')
        desc = request.form.get('desc')

        v = VlanInfo.query.filter(VlanInfo.id == id).first()
        v.vlanid = vlanid
        v.vlanname = vlanname
        v.network = network
        v.group = group
        v.desc = desc
        db.session.commit()

    return redirect(url_for('vinfo'))






#OLT_INFO

@app.route("/olt/pon/",methods = ['POST', 'GET'])
def pon():

    port = request.args.get('port')
    vlan = request.args.get('vlan')

    try:
        command_success = 'python scripts/olt.py' 
        result = subprocess.check_output(
                [command_success], shell=True)
    except:
        pass

    try:
        if len(port) > 0 and len(vlan) > 0:
            flash('ONU Successfully Registered')
        command_success2 = 'python scripts/pon55.py' + ' ' + str(port) + ' ' + str(vlan)
        result2 = subprocess.check_output(
                [command_success2], shell=True)
    except:
        pass
    return render_template('olt.html', result=result)

@app.route('/switch-vlan')
def svlan():

    return render_template('switch-vlan.html', title='SVlan')

