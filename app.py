from flask import Flask , request ,  render_template,session,redirect,url_for ,Response
from markupsafe import escape
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from database import session as db_session
from models import User , Product , Blog,Cart
import os
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)
app.secret_key='Watches12SHOP45SITE'
2

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
                    session['id'] = user.id
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
        #   new_admin=User(username="admin",email="admin@jewelerry.in",role='admin',password=generate_password_hash('admin@123'), phone= "1234567897")
        #   db_session.add(new_admin)
        #   db_session.commit()
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
@app.route('/addProduct/', methods=['GET', 'POST'])
def add_product():
    username = session.get('username')
    if request.method == 'POST':
        product_name = request.form.get('pname')
        product_desc = request.form.get('desc')
        product_price = request.form.get('pprice')

        # Handling image uploads
        img_files = [request.files.get(f'img{i}') for i in range(1, 6)]  
        saved_paths = []

        for img in img_files:
            if img:
                img.save(os.path.join("static/UserImg",img.filename))
                saved_paths.append(f"/static/UserImg/{img.filename}")
            else:
                saved_paths.append(None)  

        if len(saved_paths) == 5:  
            new_product = Product(
                productname=product_name,
                productDesc=product_desc,
                productPrice=float(product_price),
                img1=saved_paths[0],
                img2=saved_paths[1],
                img3=saved_paths[2],
                img4=saved_paths[3],
                img5=saved_paths[4],
            )

            try:
                db_session.add(new_product)
                db_session.commit()
                return render_template('add_product.html', success="Product added successfully!", username=username)
            except Exception as e:
                db_session.rollback()
                return render_template('add_product.html', error="An error occurred while adding the product.", username=username, exception=str(e))
        else:
            return render_template('add_product.html', error="Please upload all 5 images.", username=username)

    return render_template('add_product.html', username=username)     

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
        blogDescription = request.form.get('bdesc') 
        img = request.files.get('img')
        url = request.form.get('url')

        
        if not blogTitle or not blogDescription or not url or not img:
            return render_template('blog.html', error="Please fill all the fields.", username=username)

        
        img_path = None
        if img:
            img_path = os.path.join("static/UserImg", img.filename)
            img.save(img_path)

        
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
     role = session.get('role')
     all_data = db_session.query(Blog).all()
     for blog in all_data:
          blog.bimg = blog.bimg.replace("\\", "/")
          db_session.commit()
     return render_template('show_blog.html' , data = all_data , username=username , role = role)

#about us
@app.route("/about_us/")
def about():
     username = session.get('username')
     return render_template('aboutus.html' , username=username)

#deleting a product
@app.route('/delete/<int:id>')
def deleted (id):
     data = db_session.query(Product).get(id)
     # print(data, "bhj")
     db_session.delete(data)
     db_session.commit()
     return redirect('/show_product/')


# Updating a product
@app.route('/update/<int:abc>')
def update(abc):
    username = session.get('username')
    data = db_session.query(Product).get(abc)
    if not data:
        return render_template("update.html", error="Product not found", username=username)
    return render_template("update.html", username=username, mydata=data)

# Saving updated data
@app.route('/Updateddata/<int:x>', methods=['POST'])
def dd(x):
    username = session.get('username')
    data = db_session.query(Product).get(x)
    if not data:
        return render_template('update.html', error="Product not found", username=username)

    if request.method == 'POST':
        # Fetch updated form data
        product_name = request.form.get('pname')
        product_description = request.form.get('desc')
        product_price = request.form.get('pprice')

        # Update the fields
        data.productname = product_name
        data.productDesc = product_description
        data.productPrice = float(product_price) if product_price else data.productPrice

        # Handling image uploads
        img_files = [request.files.get(f'img{i}') for i in range(1, 6)]  # img1 to img5
        saved_paths = []

        for i, img in enumerate(img_files):
            if img:
                filename = secure_filename(img.filename)
                img.save(os.path.join("static/UserImg", filename))
                saved_path = f"/static/UserImg/{filename}"
                saved_paths.append(saved_path)
                # Dynamically update the image fields in the Product model
                setattr(data, f'img{i + 1}', saved_path)

        try:
            db_session.commit()
            return render_template('update.html', success="Product updated successfully.", username=username, mydata=data)
        except Exception as e:
            db_session.rollback()
            return render_template('update.html', error=f"An error occurred: {str(e)}", username=username, mydata=data)

    return render_template('update.html', username=username, mydata=data)

   
#deleting a Blog
@app.route('/deleted/<int:bc>')
def deletedd (bc):
     data = db_session.query(Blog).get(bc)
     # print(data, "bhj")
     db_session.delete(data)
     db_session.commit()
     return redirect('/blogs/')

# Updating a blog
@app.route('/upblog/<int:z>')
def update_blog(z):  # Renamed the function
    username = session.get('username')
    data = db_session.query(Blog).get(z)
    return render_template("update_blog.html", username=username, mydata=data)

# Saving updated blog data
@app.route('/Updblog/<int:y>', methods=['POST'])
def dod(y):
    username = session.get('username')
    dataa = db_session.query(Blog).get(y)
    if request.method == 'POST':
        blogTitle = request.form.get('btitle')
        blogDescription = request.form.get('bdesc')
        img = request.files.get('img')
        url = request.form.get('url')
        
        
        dataa.blogtitle = blogTitle
        dataa.blogDesc = blogDescription
        dataa.url = url
        
        
        if img:
            img.save(os.path.join("static/UserImg", img.filename))  
            img_path = f"/static/UserImg/{img.filename}"  
            dataa.bimg = img_path 

        try:
            db_session.commit()
            return render_template('update_blog.html', success="blog updated successfully.", username=username, mydata=dataa)
        except Exception as e:
            db_session.rollback()
            return render_template('update_blog.html', error=f"An error occurred: {str(e)}", username=username, data=dataa)





 
#add to cart
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')  # Assuming you save `user_id` in session
    quantity = request.form.get('quantity', 1)

    cart_item = db_session.query(Cart).filter_by(product_id=product_id, user_id=user_id).first()

    if cart_item:
        cart_item.quantity += int(quantity)
    else:
        new_item = Cart(product_id=product_id, user_id=user_id, quantity=quantity)
        db_session.add(new_item)

    try:
        db_session.commit()
        return redirect(url_for('view_cart'))
    except Exception as e:
        db_session.rollback()
        return f"Error: {e}"
   
   
#view cart
@app.route('/cart/')
def view_cart():
#     if 'username' not in session:
#         return redirect(url_for('login'))

    user_id = session.get('user_id')
    cart_items = db_session.query(Cart).filter_by(user_id=user_id).all()

    total = sum(item.product.productPrice * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

#remove from cart
@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart_item = db_session.query(Cart).get(item_id)
    if cart_item:
        db_session.delete(cart_item)
        db_session.commit()
    return redirect(url_for('view_cart'))

# Update quantity
@app.route('/update_quantity/<int:item_id>', methods=['POST'])
def update_quantity(item_id):
    new_quantity = int(request.form['quantity'])
    cart_item = db_session.query(Cart).get(item_id)  # Use Cart instead of CartItem
    if cart_item:
        cart_item.quantity = new_quantity
        db_session.commit()
    return redirect(url_for('view_cart'))  # Updated to 'view_cart'

#product detail page
@app.route('/product_detail/<int:i>')
def  detail(i):
    data = db_session.query(Product).get(i)
    return render_template('product_detail.html', mydata = data)


     
     


if __name__ == '__main__':
     app.run(debug=True)