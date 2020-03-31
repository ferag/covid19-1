from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import Form
from flask_oidc import OpenIDConnect
from wtforms import SelectField, TextField
from datetime import datetime
import sqlite3
import pandas as pd

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_OPENID_REALM': 'http://localhost:5000/oidc_callback'
})
oidc = OpenIDConnect(app)
IMG_FOLDER = '/static/img/'


def get_random_img():
    conn = sqlite3.connect('db/covid19.db')
    c = conn.cursor()
    info = oidc.user_getinfo(['email', 'openid_id'])
    user = info.get('email')
    x = c.execute("SELECT edad, sexo, codigo, informe FROM images WHERE codigo NOT IN (SELECT image FROM user_answers WHERE  user='%s') ORDER BY random() LIMIT 1;" % user).fetchall()
    for row in x:
        img = IMG_FOLDER + row[2] +'.DCM.JPG'
        img_id = row[2]
        edad = int(row[0])
        sex="Man"
        if int(row[1])==2:
           sex= "Woman"
        informe=int(row[3])

    conn.close()
    return edad, sex, img_id, img, informe


def check_images_left():
    conn = sqlite3.connect('db/covid19.db')
    c = conn.cursor()
    info = oidc.user_getinfo(['email', 'openid_id'])
    user = info.get('email')
    x = c.execute("SELECT COUNT(*) FROM (SELECT edad, sexo, codigo, informe FROM images WHERE codigo NOT IN (SELECT image FROM user_answers WHERE  user='%s'))" % user).fetchone()
    conn.close()
    if x[0] < 1:
        return False
    else:
        return True


def delete_answers(user):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    conn = sqlite3.connect('db/covid19.db')
    c = conn.cursor()
    x = c.execute("SELECT user, image, true_answer,  answer FROM user_answers WHERE user = '%s'" % user).fetchall()
    for row in x:
        print("INSERT INTO historic_answers(user, image, ans_date, true_answer, answer) VALUES('%s', '%s', '%s', %i, %i)" % (row[0], row[1], dt_string, row[2], row[3]))
        c.execute("INSERT INTO historic_answers(user, image, ans_date, true_answer, answer) VALUES('%s', '%s', '%s', %i, %i)" % (row[0], row[1], dt_string, row[2], row[3]))
    c.execute("DELETE FROM user_answers WHERE user = '%s'" % user)
    conn.commit()
    conn.close()
    return

@app.route('/')
def index():

    if oidc.user_loggedin:
        info = oidc.user_getinfo(['email', 'openid_id'])
        user = info.get('email')
        print ("Deleting answers before starting the session")
        delete_answers(user)
        return ('Hello, %s, <a href="/logged">See private</a> '
                '<a href="/logout">Log out</a>') % \
            oidc.user_getfield('email')
    else:
        return 'Welcome anonymous, <a href="/logged">Log in</a>'

@app.route('/logged', methods=['GET'])
@oidc.require_login
def logged():
    info = oidc.user_getinfo(['email', 'openid_id'])
    form = ProfileForm(request.form)
    return render_template('logged.html', email=info.get('email'), openid_id=info.get('openid_id'), form=form)

@app.route('/logout')
def logout():
    oidc.logout()
    return 'Hi, you have been logged out! <a href="/">Return</a>'

@app.route('/results')
@oidc.require_login
def results():
    conn =sqlite3.connect('db/covid19.db')
    c = conn.cursor()
    #user=session('user_id')
    info = oidc.user_getinfo(['email', 'openid_id'])
    user = info.get('email')
    x = c.execute("SELECT * FROM user_answers WHERE user = '%s'" % user).fetchall()
    failed_answers=c.execute("SELECT * FROM user_answers WHERE user = '%s' AND answer != true_answer " % user).fetchall()
    conn.close()
    total_answered=len(x)
    right_answered=0
    badly_answered=0
    TP, TN, FP, FN= 0,0,0,0
    for row in x:
        answer = row[3]
        true_answer= row[2]
        #counter for the total score
        if (true_answer==answer):
            right_answered+=1
        else:
            badly_answered+=1
        #Counter for the specificity and sensibility
        if (true_answer==1 and (answer==2 or answer==0)):
            FN+=1
        elif(true_answer==1 and answer==1):
            TP+=1
        elif((true_answer==2 or true_answer==0) and answer==1):
            FP+=1
        elif((true_answer==2 or true_answer==0) and (answer==2 or answer==0)):
            TN+=1


    if (total_answered==0):
        total_score="You have to try with more samples. Your total number of answered questions is 0"
    else:
        total_score=int(100.*right_answered/total_answered)
    try:
        sensitivity='%.2f'%(TP/(TP+FN))
    except:
        sensitivity="NaN --> Try again with more samples"
    try:
        specificity='%.2f'%(TN/(TN+FP))
    except:
        specificity="NaN --> Try again with more samples"

    res=[total_score, sensitivity,specificity]

    print("Deleting the answers for this session")
    delete_answers(user)
    
    return render_template('results.html', res=res, failed_answers=failed_answers,  image=session['messages']['img'])

class TrainingForm(Form):
 
    type_of_diag = SelectField(
        u'Type of Diagnosis',
        choices=[('pat_covid_com', 'Patological (covid-19 compatible)'),
                 ('pat_no_covid_com', 'Patological (NO covid-19 compatible)'),
                 ('non_pat', 'Non Patological')])
    img_id = TextField(u'IMG ID','')


class ProfileForm(Form):
    type_of_profile = SelectField(
        u'Profile',
        choices=[('noanswer', 'N/A'),
                 ('abdradio', ' Abdominal radiologist '),
                 ('Neuroradio', ' Neuroradiologist '),
                 ('breastradio', ' Breast radiologist '),
                 ('muscradio', ' Musculoskeletal radiologist '),
                 ('generalradio', 'General radiologist'),
                 ('interradio', 'Interventional radiologist'),
                 ('pediradio', ' Pediatric radiologist ') ,  
                 ('thoraradio', ' Thoracic radiologist '),
                 ('radioresi', 'Radiology resident'),
                 ('resiother', 'Resident (other than radiology) ') ,  
                 ('medicalstudent', ' Estudiante de medicina'),
                 ('assophypulmo', ' Associate Physician of Pulmonology '), 
                 ('internassisphysi', ' Internist Assistant Physician '),  
                 ('deputyemerg, ' Deputy emergency physician '),    
                 ('assodoctorother', ' Associate doctor of another specialty ')])
    user_profile=TextField(u'USER PROFILE','')

@app.route('/send_results', methods=['POST'])
@oidc.require_login
def send_results():
    try:
        
        form = TrainingForm(request.form)
        type_of_diag = form['type_of_diag'].data
        answer = 0
        print("RESULT: %s" % type_of_diag)
        if type_of_diag=="pat_covid_com":
            answer=1
        elif type_of_diag=="non_pat":
            answer=0
        elif type_of_diag=="pat_no_covid_com":
            answer=2

        conn = sqlite3.connect('db/covid19.db')
        c = conn.cursor()
        info = oidc.user_getinfo(['email', 'openid_id'])
        c.execute("INSERT INTO user_answers(user, image, true_answer,answer) VALUES ('%s', '%s', %i, %i)" % (
            info.get('email'),
            session['messages']['id_image'],
            session['messages']['informe'],
            int(answer)))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Ooops! We had a problem")
        print(e)
    return redirect(url_for('training'))

@app.route('/training', methods=['GET','POST'])
@oidc.require_login
def training():
    info = oidc.user_getinfo(['email', 'openid_id'])
    user=info.get('email')
    error = ""
    if check_images_left() == False:
        print("No images left. Redirecting to results---")
        return redirect(url_for('results'))
    edad, sex,  img_id, img, informe = get_random_img() #get_random
    form = TrainingForm(request.form)
    profile= ProfileForm(request.form)
    type_of_profile = profile['type_of_profile'].data
    conn = sqlite3.connect('db/covid19.db')
    c = conn.cursor()
    c.execute("UPDATE users set profile = '%s' WHERE id  ='%s' and profile is null or profile = 'noanswer' " % (type_of_profile, user)).fetchall()
    form.img_id = img_id
    session['messages'] = {'id_image': img_id, 'img': img, 'informe': int(informe)}
    if request.method == 'POST':
        type_of_diag = form.type_of_diag.data
        if type_of_diag=="pat_covid_com":
            answer=1
        elif type_of_diag=="non_pat":
            answer=0
        elif type_of_diag=="pat_no_covid_com":
            answer=2
        type_of_diag = form.type_of_diag.data
        session['user_id'] = info.get('email')
        if len(type_of_diag) == 0:
            error = "Please supply data"

    try:
        info = oidc.user_getinfo(['email', 'openid_id'])
        print("SELECT COUNT(*) FROM users WHERE id='%s'" % (info.get('email')))
        x = c.execute("SELECT COUNT(*) FROM users WHERE id='%s'" % (info.get('email')))
        row = c.fetchone()
        if row[0] > 0:
            return render_template('training.html', form=form, message=error, edad=edad, sex=sex, img=img, img_id=img_id)
        else:
            return 'You are not an allowed user'
        conn.close()
    except Exception as e:
        conn.close()
        print(e)
        return 'Ooops!, <a href="/logged">Log in</a>'

# Run the application
#app.run(debug=True)
