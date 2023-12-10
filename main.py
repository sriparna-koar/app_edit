import cv2
#pip install flask opencv-python
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
 


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.static_folder = 'static'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def processImage(filename, operation):
    image=cv2.imread(f"uploads/{filename}")
    match operation:
        case "gray":
            gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            newfilename=f"static/{filename}"
            cv2.imwrite(newfilename,gray)
            return newfilename
        case "cjpg":
            newfilename=f"static/{filename.split('.')[0]+'.jpg'}"
            cv2.imwrite(newfilename,image)
            return newfilename
        case "cwebp":
            newfilename=f"static/{filename.split('.')[0]+'.webp'}"
            cv2.imwrite(newfilename,image)
            return newfilename
        case "cpng":
            newfilename=f"static/{filename.split('.')[0]+'.png'}"
            cv2.imwrite(newfilename,image)
            return newfilename
        case "invert":
             inverted = cv2.bitwise_not(image)
             newfilename = f"static/{filename.split('.')[0] + '_invert.jpg'}"
             cv2.imwrite(newfilename, inverted)
             return newfilename
        case "blur":
            blurred = cv2.GaussianBlur(image, (15, 15), 0)
            newfilename = f"static/{filename.split('.')[0] + '_blur.jpg'}"
            cv2.imwrite(newfilename, blurred)
            return newfilename
        case "rotate":
            rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            newfilename = f"static/{filename.split('.')[0] + '_rotate.jpg'}"
            cv2.imwrite(newfilename, rotated)
            return newfilename






@app.route("/")
def hello_world():
    return render_template("index.html")
@app.route("/edit",methods=["GET","POST"])
def edit():
    if(request.method=="POST"):
        if 'file' not in request.files:
            flash('No file part')
            return "ERROR"
        print(request.form)
        file = request.files['file']
        operation=request.form['operation']
        print(file, operation)
        
        if file.filename == '':
            flash('No selected file')
            return "Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            newfilename=processImage(filename, operation)
            return f"File updated available <a href ='{newfilename}'>here </a>"
              

    return render_template("index.html")
app.run(debug=True,port=5000)