import os
from urllib import request
import pymysql
import ar_master
import smtplib, ssl
from flask import Flask, render_template, flash, request, session, current_app, send_from_directory
from werkzeug.utils import redirect, secure_filename
from time import strptime


port = 587
smtp_server = "smtp.gmail.com"
sender_email = "serverkey2018@gmail.com"
password ="12313213213"

# ps = PorterStemmer()
app = Flask(__name__, static_folder="static")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
user='root'
password=''
host='127.0.0.1'

mm = ar_master.master_flask_code()
################################################################### HOME
@app.route("/")
def homepage():
    return render_template('index.html')
@app.route("/admin")
def admin():
    return render_template('admin.html')
@app.route("/admin_login", methods = ['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['pass'] == 'admin':
            return render_template('admin_home.html',error=error)
        else:
            return render_template('admin.html', error=error)

@app.route("/admin_home")
def admin_home():
    return render_template('admin_home.html')


@app.route("/admin_hospital_details",methods = ['GET', 'POST'])
def admin_doctor():
    data=mm.select_direct_query("select * from hospital_details")
    return render_template('admin_hospital_details.html',items=data)


@app.route("/admin_patient",methods = ['GET', 'POST'])
def admin_patient():
    data=mm.select_direct_query("select id,name,contact,email,address	 from user_details")
    return render_template('admin_patient.html',items=data)


@app.route("/admin_appointment",methods = ['GET', 'POST'])
def admin_appointment():

    data=mm.select_direct_query("select id,patient,symptoms,problem,doctor,date,time from booking_details")
    return render_template('admin_appointment.html',items=data)

@app.route("/admin_Report")
def admin_Report():
    return render_template('admin_Report.html')

@app.route("/report_user_list",methods = ['GET', 'POST'])
def report_user_list():
    data = mm.select_direct_query("select id,name,address,date from user_details order by date DESC ")
    return render_template('report_user_list.html',items=data)


@app.route("/report_hospital_list",methods = ['GET', 'POST'])
def report_hospital_list():
    data = mm.select_direct_query("select id,hospital_name,date,area from hospital_details order by date DESC ")
    return render_template('report_hospital_list.html',items=data)

@app.route("/report_total_cost",methods = ['GET', 'POST'])
def report_total_cost():
    data = mm.select_direct_query("SELECT ed.hospital,ed.treatment_name,SUM(ts.treatment_cost + ts.operation_cost + ts.room_rent + ts.lab_charge + ed.doctor_fees + ed.nurse_fees +ed.maintenance_fees + dc.drug_cost ) AS total FROM treatment_cost_details AS ts INNER JOIN examination_details AS ed ON ts.hospital_code = ed.hospital_code INNER JOIN drug_cost_details AS dc ON ts.hospital_code = dc.hospital_code GROUP BY ed.hospital")
    return render_template('report_total_cost.html',items=data)




@app.route("/hospital_register", methods = ['GET', 'POST'])
def hospital_register():
    if request.method == 'POST':
        hospital_name = request.form['hname']
        area = request.form['area']
        dean = request.form['dean']
        hospital_code=request.form['hcode']
        address=request.form['address']
        Date= request.form['Date']
        username=request.form['username']
        password=request.form['password']

        maxin=mm.find_max_id("hospital_details")
        qry=("insert into hospital_details values('" + str(maxin) + "','" + str(hospital_name) + "','" + str(
            area) + "','" + str(dean) + "','" + str(hospital_code) + "','" + str(address)+ "','" +str(username) + "','" + str(
        password) + "','" + str(Date) + "')")
        result=mm.insert_query(qry)
        # print(result)
        return render_template('hospital_register.html',flash_message=True,data="Success")
    return render_template('hospital_register.html')

@app.route("/admin_train")
def admin_train():
    data=mm.select_single_colum("doctor_details","doctor_name")
    return render_template('admin_train.html',items=data[0])

@app.route("/hospital_add_treatment", methods = ['GET', 'POST'])
def hospital_add_treatment():
    hospital=session['hospital']
    place=session['place']
    if request.method == 'POST':
        treatment_name = request.form['treatment_name']
        treatment_cost = request.form['treatment_cost']
        operation_cost = request.form['operation_cost']
        room_rent=request.form['room_rent']
        lab_charge=request.form['lab_charge']
        category=request.form['select']
        hospital_code = request.form['hcode']

        maxin=mm.find_max_id("treatment_cost_details")
        qry=("insert into treatment_cost_details values('" + str(maxin) + "','" + str(hospital)+ "','" + str(hospital_code) + "','" + str(treatment_name) + "','" + str(
            treatment_cost) + "','" + str(operation_cost) + "','" + str(room_rent) + "','" + str(lab_charge) + "','" + str(place) + "','" + str(category) + "')")
        result=mm.insert_query(qry)

        return render_template('hospital_add_treatment.html',flash_message=True,data="Success")
    return render_template('hospital_add_treatment.html')


@app.route("/hospital_add_drugs", methods = ['GET', 'POST'])
def hospital_add_drugs():
    hospital=session['hospital']
    place = session['place']
    if request.method == 'POST':
        hospital_code = request.form['hcode']
        treatment_name = request.form['treatment_name']
        drug_name = request.form['drug_name']
        drug_cost = request.form['drug_cost']


        maxin=mm.find_max_id("drug_cost_details")
        qry = ("insert into drug_cost_details values('" + str(maxin) + "','" + str(hospital) + "','" + str(hospital_code) + "','" + str(treatment_name) + "','" + str(drug_name) + "','" + str(drug_cost) + "','"+str(place)+"')")
        result = mm.insert_query(qry)

        return render_template('hospital_add_drugs.html',flash_message=True,data="Success")
    return render_template('hospital_add_drugs.html')



@app.route("/hospital_add_examination", methods = ['GET', 'POST'])
def hospital_add_examination():
    hospital=session['hospital']
    place=session['place']
    if request.method == 'POST':
        treatment_name = request.form['treatment_name']
        doctor_fees = request.form['doctor_fees']
        nurse_fees = request.form['nurse_fees']
        maintenance_fees = request.form['maintenance_fees']
        hospital_code = request.form['hcode']

        maxin=mm.find_max_id("examination_details")
        qry=("insert into examination_details values('" + str(maxin) + "','" + str(hospital)+ "','" + str(hospital_code) + "','" + str(treatment_name) + "','" + str(doctor_fees) + "','" + str(nurse_fees) + "','" + str(maintenance_fees) + "','" + str(place) + "')")
        result=mm.insert_query(qry)


        return render_template('hospital_add_examination.html',flash_message=True,data="Success")
    return render_template('hospital_add_examination.html')
############################################################################################################
@app.route("/hospital")
def hospital():
    return render_template('hospital.html')

@app.route("/hospital_login", methods = ['GET', 'POST'])
def hospital_login():
    error = None
    if request.method == 'POST':
        n = request.form['uname']
        g = request.form['pass']
        qry="SELECT * from hospital_details where username='" + str(n) + "' and password='" + str(g) + "'"
        result=mm.select_login(qry)
        data=mm.select_direct_query(qry)
        session['place']=data[0][5]
        session['hospital']=data[0][1]
        if result=="no":
            return render_template('hospital.html', flash_message=True, data="Login Failed")
        else:
            # session['hospital'] = request.form['uname']
            return hospital_home()

@app.route("/hospital_home")
def hospital_home():

    return render_template('hospital_home.html')


###########################################################################################################
@app.route("/doctor")
def doctor():
    return render_template('doctor.html')
@app.route("/user")
def user():
    return render_template('user.html')
@app.route("/patient_login", methods = ['GET', 'POST'])
def patient_login():
    error = None
    if request.method == 'POST':
        n = request.form['uname']
        g = request.form['pass']
        qry="SELECT * from user_details where username='" + str(n) + "' and password='" + str(g) + "'"
        result=mm.select_login(qry)
        if result=="no":
            return render_template('patient.html', flash_message=True, data="Login Failed")
        else:
            session['patient'] = request.form['uname']
            return render_template('patient_home.html', sid=n)
@app.route("/patient_register",methods = ['GET', 'POST'])
def patient_register():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']
        Date = request.form['Date']
        maxin = mm.find_max_id("user_details")
        qry = ("insert into user_details values('" + str(maxin) + "','" + str(name) + "','" + str(contact) + "','" + str(email) + "','" + str(address) + "','" + str(username) + "','" + str(password) + "','" + str(Date) + "')")
        result = mm.insert_query(qry)
        if result==1:
            return render_template('patient_register.html', flash_message=True, data="Register Successfully")
        else:
            return render_template('patient_register.html', flash_message=True, data="Register Failed")

    return render_template('patient_register.html')


@app.route("/patient_home")
def patient_home():
    return render_template('patient_home.html')



@app.route("/patient_upload_document",methods = ['GET', 'POST'])
def patient_upload_document():
    user=session['patient']
    if request.method == 'POST':
        smoking = request.form['smoling']
        drinking = request.form['drinking']
        region = request.form['region']
        payment = request.form['select3']
        f = request.files['file']
        f.save(os.path.join("static/uploads/", secure_filename(f.filename)))
        maxin = mm.find_max_id("upload_data")
        mm.insert_query("insert into upload_data values ('" + str(maxin) + "','" + str(user) + "','" + str(smoking) + "','" + str(drinking) + "','" + str(region) + "','" + str(payment) + "','" + str(f.filename) + "','waiting','0')")
        return render_template('patient_upload_document.html', flash_message=True, data="Request Send Successfully")
    return render_template('patient_upload_document.html')




@app.route("/patient_search",methods = ['GET', 'POST'])
def patient_search():
    user=session['patient']
    data=mm.select_direct_query("select * from upload_data where user='"+str(user)+"' and status='Accept'")
    if data:
        return render_template('patient_search.html',items=data)
    else:
        return render_template('patient_home.html', flash_message=True, data="Request Not Accepted")



@app.route('/patient_search1/<string:id>', methods=['GET','POST'])
def patient_search1(id):
    data=mm.select_direct_query("select * from upload_data where id='"+str(id)+"'")
    session['smoking']=data[0][2]
    session['drinking']=data[0][3]
    session['region']=data[0][4]
    session['payment']=data[0][5]

    return render_template('patient_search1.html',items=data)



@app.route("/patient_search2",methods = ['GET', 'POST'])
def patient_search2():
    user = session['patient']
    smoking = session['smoking']
    drinking = session['drinking']
    region = session['region']
    payment = session['payment']
    hospital_name = {}
    if request.method == 'POST':
        age = request.form['age']
        session['age'] = age
        disease = request.form['disease']
        city = request.form['city']
        category = request.form['select']
        qry = "select * from treatment_cost_details where category='"+str(category)+"' and treatment_name='"+str(disease)+"' and place='"+str(city)+"'"
        treatment_data = mm.select_direct_query(qry)
        qry1 = "select * from examination_details where treatment_name='"+str(disease)+"' and place='"+str(city)+"'"
        examination_data = mm.select_direct_query(qry1)
        qry2 = "select * from drug_cost_details where treatment_name='" + str(disease) + "' and place='" + str(city)+"'"
        drug_cost_data = mm.select_direct_query(qry2)
        print(treatment_data)
        for x in treatment_data:
            cc=x[1]
            hospital_name[cc] = 0
        for x in examination_data:
            cc=x[1]
            hospital_name[cc] = 0
        for x in drug_cost_data:
            cc=x[1]
            hospital_name[cc] = 0
        for x in treatment_data:
            hospital = x[1]

            treatment_cost = x[4]
            operation_cost = x[5]
            room_rent = x[6]
            lab_charge = x[7]


            pre_data = int(hospital_name[hospital])
            print(treatment_cost)
            pre_data += int(treatment_cost)+int(operation_cost)+int(room_rent)+int(lab_charge)
            hospital_name[hospital] = pre_data
        for x in examination_data:
            hospital = x[1]
            doctor_fees = x[4]
            nurse_fees = x[5]
            maintenance_fees = x[6]
            pre_data = int(hospital_name[hospital])
            pre_data += int(doctor_fees)+int(nurse_fees)+int(maintenance_fees)
            hospital_name[hospital] = pre_data
        for x in drug_cost_data:
            hospital = x[1]
            drug_cost = x[5]
            pre_data = int(hospital_name[hospital])
            pre_data += int(drug_cost)
            hospital_name[hospital] = pre_data
        # print(hospital_name)
        hospital_name = dict(sorted(hospital_name.items(), key=lambda item: item[1], reverse=False))
        data=[]
        for key, val in hospital_name.items():
            tdata=[str(key),str(val)]
            data.append(tdata)

        return render_template('patient_search2.html',items=data)



@app.route('/patient_search3/<string:id>', methods=['GET','POST'])
def patient_search3(id):
    qq="select * from hospital_details where username='"+str(id)+"'"
    hospital1=mm.select_direct_query(qq)
    hospital_name=hospital1[0][1]
    qry="select * from treatment_cost_details where hospital='"+str(id)+"'"
    qry1 = "select * from examination_details where hospital='"+str(id)+"'"
    qry2 = "select * from drug_cost_details where hospital='" + str(id) + "'"
    treatment_data=mm.select_direct_query(qry)
    examination_data = mm.select_direct_query(qry1)
    drug_cost_data = mm.select_direct_query(qry2)
    print(treatment_data)
    print(examination_data)
    print(drug_cost_data)
    total=0
    for x in treatment_data:
        treatment_cost = x[4]
        operation_cost = x[5]
        room_rent = x[6]
        lab_charge = x[7]
        total+=int(treatment_cost)
        total+=int(operation_cost)
        total+=int(room_rent)
        total+=int(lab_charge)
    for x in examination_data:
        doctor_fees = x[4]
        nurse_fees = x[5]
        maintenance_fees = x[6]
        total += int(doctor_fees)
        total += int(nurse_fees)
        total += int(maintenance_fees)
    for x in drug_cost_data:
        drug_cost = x[5]
        total += int(drug_cost)


    age=session['age']
    ag = int(age)
    per = 100
    if ag <= 30:
        per = 100
    elif ag <= 50:
        per = 80
    elif ag <= 60:
        per = 50
    else:
        per = 0
    payment = session['payment']
    total_given = (total / 100) * per

    if payment == "Cashless":
        total_given = total_given

    else:
        total_given = (total_given/100)*80
        per = (per / 100) * 80

    per=format(per, '.2f')
    total_given=format(total_given, '.2f')

    return render_template('patient_search3.html',hospital_name=hospital_name,payment=payment,per=per,total_given=total_given,total=total, treatment_data=treatment_data,examination_data=examination_data,drug_cost_data=drug_cost_data)



@app.route("/admin_user_request")
def admin_user_request():
    data=mm.select_direct_query ("SELECT * FROM upload_data where status='waiting'")
    return render_template('admin_user_request.html',items=data)


@app.route('/admin_user_request_accept/<string:id>', methods=['GET','POST'])
def admin_user_request_accept(id):
    mm.insert_query("update  upload_data set status='Accept' where id='"+str(id)+"'")
    return admin_user_request()


@app.route('/admin_user_request_reject/<string:id>', methods=['GET','POST'])
def admin_user_request_reject(id):
    mm.insert_query("update  upload_data set status='Reject' where id='"+str(id)+"'")
    return admin_user_request()

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # print(filename)
    uploads = os.path.join(current_app.root_path, "static/uploads/")
    # print(uploads)
    f=filename
    return send_from_directory(uploads,filename ,as_attachment=True)

######################################
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True,host="0.0.0.0",port=4888)
