from flask import Flask, render_template,request, jsonify, send_from_directory
import io
import os
import pytesseract	 
from PIL import Image	 

#Support For LINUX Systems Which Supports SUDO Command
#os.system('sudo apt update && sudo apt install tesseract-ocr && sudo apt install libtesseract-dev')


# Function To Determine The Date From String
def substring(strr):
  print(strr)
  strr=strr.lower().replace("/","-").replace("\\","-").replace("--","-").replace(" ","")
  month_list = ["jan","feb","mar","april","may","june","jul","aug","sep","oct","nov","dec"]
  for i,substr in enumerate(month_list):
    if strr.find(substr)==-1:
      pass
      #return False
    else:
      index = strr.index(substr)
      if i<10:
        date = strr[index-3:index-1]+"-"+"0"+str(i+1)+"-"+strr[index+len(substr)+1:index+len(substr)+5]
        #date = strr[index-3:index+len(substr)+5]
      else:
        date = strr[index-3:index-1]+"-"+str(i+1)+"-"+strr[index+len(substr)+1:index+len(substr)+5]
      return date
  if strr.find('-')!=-1 and (strr[strr.index("-")+2]=="-" or strr[strr.index("-")+3]=="-"):
    ind=strr.index("-")
    date1=strr[ind-2:ind+7]
    return date1


# initialize our Flask application
app = Flask(__name__)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_IMAGE_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpe', 'jpeg', 'gif'])

def create_new_folder(local_dir):
	newpath = local_dir
	if not os.path.exists(newpath):
		os.makedirs(newpath)
		
	return newpath


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS

# Starting Web Page
@app.route('/')
def index():
	return render_template("index.html")

# API for getting date
@app.route("/extract_date", methods=["POST"])
def predict():
    
# ensure an image was properly uploaded to our endpoint
    if request.method == "POST" and request.files['image']:
        imagefile = request.files["image"].read()
        image = Image.open(io.BytesIO(imagefile))
        result = pytesseract.image_to_string(image)
        final_date = substring(result)
	#final_date = substring(image)
        data = {"date":final_date}
        print(data)
	# return the data dictionary as a JSON response
        return jsonify(data)

if __name__ == "__main__":
	print("START FLASK")
	
  #Applicable For The Machines Which Requires PORT
	#port = int(os.environ.get('PORT', 5000))
	app.run()