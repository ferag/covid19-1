from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import Form
from wtforms import SelectField, TextField
import sqlite3
import pandas as pd

conn = sqlite3.connect('db/covid19.db')
c = conn.cursor()

user="lari.lloret@googlemail.com"
#x=c.execute("SELECT * FROM user_answers WHERE user = '%s' " % user).fetchall()
#y=c.execute("SELECT * FROM user_answers WHERE user ='%s' " % user).fetchall()
#print(y)
#("SELECT edad, sexo,codigo, informe FROM images ORDER BY random() LIMIT 1;"
#x=c.execute("SELECT edad, sexo, codigo, informe FROM images  WHERE codigo NOT IN (SELECT image FROM user_answers WHERE user ='%s' % user) ORDER BY random()").fetchall()
#x=c.execute("SELECT edad, sexo, codigo, informe FROM images WHERE codigo NOT IN (SELECT image FROM user_answers WHERE  user='%s');" % user).fetchall()
#print(x)



#x=c.execute("SELECT * FROM images").fetchall()
#print(x)

#x=c.execute("ALTER TABLE user_answers ADD diagnostico text;")
#x=c.execute("ALTER TABLE user_answers ADD diagnosis text;")

#x=c.execute("PRAGMA table_info(user_answers)").fetchall()
print(x)
