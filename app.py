from flask import Flask , request ,  render_template,session,redirect,url_for ,jsonify
from markupsafe import escape
from werkzeug.security import generate_password_hash,check_password_hash
from database import session as db_session
from models import User , Product , Blog
import os

app = Flask(__name__)
app.secret_key='Watches12SHOP45SITE'


# home page
@app.route("/")
def home():
     username=session.get('username')
     return render_template('index.html',username=username)


# login
@app.route("/login/",methods=['GET','POST'])
def login():
     username=session.get('username')
     if request.method=='POST':
          email=request.form.get('email')
          password=request.form.get('password')
          user=db_session.query(User).filter_by(email=email).first()
          if user:
               if check_password_hash(user.password,password):
                    session['username']=user.username
                    session['role']=user.role
                    if user.role=='user':
                         print(user.username)
                         return render_template('login.html',username=user.username)
                    elif user.role=='admin':
                         return render_template('admin.html',username=user.username)
                    else:
                         return render_template('index.html',username=None)
               else:
                    return render_template('login.html',password_error="Wrong password")
          else:
               print("USER ERROR")
     return render_template('login.html',username=username)


#sign up
@app.route("/signup/",methods=['GET','POST'])
def signup():
     username=session.get('username')
     if request.method=='POST':     
          uname=request.form.get('username')
          email=request.form.get('email') 
          password=request.form.get('password')
          phone = request.form.get('phone')
          role='user'
          hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

          new_user=User(username=uname,email=email,role=role,password=hashed_password, phone = phone)
          
          #admin
          # new_admin=User(username="admin",email="admin@jewelerry.in",role='admin',password=generate_password_hash('admin@123'), phone= "1234567897")
          # db_session.add(new_admin)
          # db_session.commit()
          try:
               db_session.add(new_user)
               db_session.commit()
               return  render_template('signup.html',success="Account Created Successfully")
          except:
               db_session.rollback()
               return render_template('signup.html',error="This email already exists!")
          
          
     return render_template('signup.html',username=username)

# admin page
@app.route('/admin/')
def admin():
     
     if 'username' not in session or session.get('role') !='admin':
          return redirect(url_for('signup'))
     
     return render_template('admin.html')
#logout
@app.route('/logout/')
def logout():
     session.clear()
     return render_template('index.html')

# add_products
@app.route('/addProduct/' , methods=['GET', 'POST']    )
def add_product():
     username=session.get('username')
     if request.method == 'POST':
          ProductName = request.form.get('pname')
          productDescription = request.form.get('desc')
          productPrice = request.form.get('pprice')
          img = request.files.get('img')
          
          if img:
               img.save(os.path.join("static/UserImg",img.filename))
               path = f"/static/UserImg/{img.filename}"
               data = Product(productname = ProductName ,productDesc = productDescription,productPrice = productPrice  ,img = path)
               
               db_session.add(data)
               db_session.commit()
               
               try:
                    db_session.add(data)
                    db_session.commit()
                    return  render_template('add_product.html',success="Product added Successfully",username=username)
               except:
                    db_session.rollback()
                    return render_template('add_product.html',error="Their is some error Kindly fill all fields!",username=username)
               
               
          
     return render_template('add_product.html',username=username)
     

#showing users to admin 
@app.route("/view_user/")
def userr():
     username = session.get('username')
     all_data = db_session.query(User).all()
     return render_template('user.html',username=username, userData = all_data)


# add blog page
@app.route("/blog/", methods=['GET', 'POST'])
def blog():
    username = session.get('username')
    
    if request.method == 'POST':
        blogTitle = request.form.get('btitle')
        blogDescription = request.form.get('bdesc')  # Corrected to match the form
        img = request.files.get('img')
        url = request.form.get('url')

        # Check if all required fields are filled
        if not blogTitle or not blogDescription or not url or not img:
            return render_template('blog.html', error="Please fill all the fields.", username=username)

        # Save the uploaded image if it exists
        img_path = None
        if img:
            img_path = os.path.join("static/UserImg", img.filename)
            img.save(img_path)

        # Create a new Blog entry
        data = Blog(blogtitle=blogTitle, blogDesc=blogDescription, bimg=img_path, url=url)

        try:
            db_session.add(data)
            db_session.commit()
            return render_template('add_blog.html', success="Blog added successfully.", username=username)
        except Exception as e:
            db_session.rollback()
            return render_template('add_blog.html', error=f"An error occurred: {str(e)}", username=username)

    return render_template('add_blog.html', username=username)

#showing product
@app.route('/show_product/', methods=['GET'])
def show_product():
    username = session.get('username')
    role = session.get('role')
    products = db_session.query(Product).all()
    return render_template('view_product.html', products=products, username=username ,role = role)

#show blog page
@app.route("/blogs/")
def show_blog():
     username = session.get('username')
     all_data = db_session.query(Blog).all()
     for blog in all_data:
          blog.bimg = blog.bimg.replace("\\", "/")
          db_session.commit()
     return render_template('show_blog.html' , data = all_data , username=username)

#about us
@app.route("/about_us/")
def about():
     return render_template('aboutus.html')



if __name__ == '__main__':
     app.run(debug=True)