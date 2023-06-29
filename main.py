from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='kusumachandashwini'


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/prisondbms'
db=SQLAlchemy(app)

# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class Block(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    branch=db.Column(db.String(100))



class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))





class Prisoner(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.String(50))
    pname=db.Column(db.String(50))
    sen=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    block=db.Column(db.String(50))
    crime=db.Column(db.String(50))
    date=db.Column(db.String(50),nullable=False)
    

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/prisonerdetails')
def studentdetails():
    query=Prisoner.query.all() 
    return render_template('studentdetails.html',query=query)


@app.route('/block',methods=['POST','GET'])
def department():
    if request.method=="POST":
        dept=request.form.get('dept')
        query=Block.query.filter_by(branch=dept).first()
        if query:
            flash("Department Already Exist","warning")
            return redirect('/block')
        dep=Block(branch=dept)
        db.session.add(dep)
        db.session.commit()
        flash("Cell Block Added","success")
    return render_template('block.html')


@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=="POST":
        rollno=request.form.get('roll')
        bio=Prisoner.query.filter_by(pid=rollno).first()
        return render_template('search.html',bio=bio)
        
    return render_template('search.html')

@app.route("/delete/<string:id>",methods=['POST','GET'])
@login_required
def delete(id):
    post=Prisoner.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash("Slot Deleted Successful","danger")
    return redirect('/prisonerdetails')


@app.route("/edit/<string:id>",methods=['POST','GET'])
@login_required
def edit(id):
    # dept=db.engine.execute("SELECT * FROM `department`")    
    if request.method=="POST":
        rollno=request.form.get('rollno')
        sname=request.form.get('sname')
        sem=request.form.get('sem')
        gender=request.form.get('gender')
        branch=request.form.get('branch')
        crime=request.form.get('crime')
        date=request.form.get('date')
        post=Prisoner.query.filter_by(id=id).first()
        post.pid=rollno
        post.pname=sname
        post.sen=sem
        post.gender=gender
        post.branch=branch
        post.crime=crime
        post.date=date
        db.session.commit()
        flash("Slot is Updates","success")
        return redirect('/prisonerdetails')
    dept=Block.query.all()
    posts=Prisoner.query.filter_by(id=id).first()
    return render_template('edit.html',posts=posts,dept=dept)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        # new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        newuser=User(username=username,email=email,password=encpassword)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addprisoner',methods=['POST','GET'])
@login_required
def addprisoner():
    # dept=db.engine.execute("SELECT * FROM `department`")
    dept=Block.query.all()
    if request.method=="POST":
        prid=request.form.get('pid')
        p_name=request.form.get('pname')
        sentence=request.form.get('sen')
        gender=request.form.get('gender')
        cblock=request.form.get('branch')
        crime=request.form.get('crime')
        date=request.form.get('date')
        query=Prisoner(pid=prid,pname=p_name,sen=sentence,gender=gender,block=cblock,crime=crime,date=date)
        db.session.add(query)
        db.session.commit()

        flash("Entry Confirmed","info")


    return render_template('prisoner.html',dept=dept)
@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    