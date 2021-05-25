#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
PF001

Objetivos:
- Implementar um aplicativo para mostrar a localização de unidades de vacinação
- Determinar a proximidade de acordo com o CEP informado pelo usuário
- Apresentar o resultado em um mapa responsivo
- Atualizar as informações de disponibilidade de vacinas a partir de dados oficiais

'''

import pycep_correios
from geopy.geocoders import Nominatim
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField # Os validadores são usados para garantir que as entradas sejam o que a gente espera.
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minhasenha'

class CEPForm(FlaskForm):
    cep = StringField('Digite o CEP (apenas números)')
    submit = SubmitField('Pesquisar')


@app.route("/", methods=['GET','POST'])
def index():
    form = CEPForm()    
    if form.validate_on_submit():
        cep = form.cep.data
        endereco = pycep_correios.get_address_from_cep(cep)
        geolocator = Nominatim(user_agent="test_app")
        location = geolocator.geocode(endereco['logradouro'] + ", " + endereco['cidade'] + " - " + endereco['bairro'])
        return render_template('map.html', location=location)    
    else:
        print('não validou')
        print(form.cep)
        return render_template('index.html',form=form)

app.run(host='localhost', port=5002, debug=True)
