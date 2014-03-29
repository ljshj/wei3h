# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import db
from app.zaiwenling.forms import MusicForm
from app.zaiwenling.models import Music

mod = Blueprint('zaiwenling', __name__, url_prefix='/zaiwenling')


import pymongo
from bson.objectid import ObjectId
conn = pymongo.Connection('localhost', 5430)
db = conn.test

@mod.route('/index/')
@mod.route('/')
def index():
    return render_template('zaiwenling/index.html')

@mod.route('/addmusic/', methods=['GET', 'POST'])
def add_music():
    form = MusicForm(request.form)
    if form.validate_on_submit():

        music = Music(music_title=form.music_title.data, music_artist=form.music_artist.data, music_pic=form.music_pic.data, music_audio=form.music_audio.data)

        db.session.add(music)
        db.session.commit()

        return redirect(url_for('zaiwenling.list_music'))
    return render_template('zaiwenling/add_music.html', form=form)

@mod.route('/music/<id>/')
def get_music(id):
    music = Music.query.filter_by(id=id).first()
    return render_template('zaiwenling/music.html', music=music)

@mod.route('/musics/')
def list_music():
    musics = Music.query.all()
    return render_template('zaiwenling/musics.html', musics=musics)

@mod.route('/waimai/<id>/')
def get_waimai(id):
    waimai = db.waimai.find_one({'_id': ObjectId(id)}, {'_id': 0})
    return render_template('zaiwenling/waimai.html', waimai=waimai)

@mod.route('/waimais/')
def list_waimai():
    waimais = []
    for i in db.waimai.find():
        id = str(i['_id'])
        del i['_id']
        i['objid'] = id

        waimais.append(i)

    return render_template('zaiwenling/waimais.html', waimais=waimais)

@mod.route('/editwaimai/<id>/')
def edit_waimai(id=''):
    waimai = db.waimai.find_one({'_id': ObjectId(id)})

    return render_template('zaiwenling/editwaimai.html', waimai=waimai)

@mod.route('/updatewaimai/', methods=['POST'])
def update_waimai():
    form = request.form
    id = form['_id']
    name = form['name']
    phone = form['phone']
    rate = form['rate']
    tag = form['tag']
    address = form['address']
    ttime = form['ttime']
    valid = form['valid']
    beiz = form['beiz']
    db.waimai.update({'_id': ObjectId(id)}, {'$set': {'name': name, \
        'phone': phone, 'rate': rate, 'tag': tag, \
        'address': address, 'ttime': ttime, 'valid': valid, \
        'beiz': beiz}})
    return redirect(url_for('zaiwenling.get_waimai', id=str(id)))

@mod.route('/about/')
def about():
    return render_template('zaiwenling/about.html')

@mod.route('/bd/')
def bd():
    return render_template('zaiwenling/bd.html')

