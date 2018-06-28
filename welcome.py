
from flask import Flask,render_template , request , flash , redirect , jsonify
from sightengine.client import SightengineClient
#from sightengine import client
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

client = SightengineClient('962007868', 'QeNZj4S6hMa2LmcLQEUE') # don't forget to add your credentials

#UPLOAD_FOLDER = os.path.basename('uploads')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    #file = request.files['image']
    #filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    #file.save(filename)
    if request.method == 'POST':
        f = request.files['image']
        print(f)
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        f.save(secure_filename(f.filename))
        print 'file uploaded successfully'
    UPLOAD_FOLDER = os.path.dirname(__file__)
    print(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    print(file)
    filepath = app.config['UPLOAD_FOLDER'] + '/' + f.filename
    print(filepath)
    c =[]

    output = client.check('nudity', 'wad', 'celebrities', 'scam', 'face-attributes','type','text','offensive','properties').set_file(f.filename)
    print (output)
    # contains nudity
    if output['nudity']['safe'] > 0.7:
        data = {'nudity':'is safe from NUDITY'}
        c.append(data)
        print('SAFE FROM NUDIITY')
    elif output['nudity']['partial'] > 0.5 or output['nudity']['raw'] > 0.5:
        a = 1
        data = {'nudity': 'contains NUDITY'}
        c.append(data)
        print('NUDITY')
        # contains weapon, alcohol or drugs
    if output['weapon'] > 0.4:
        a = 1
        data = {'wag': 'WEAPON'}
        c.append(data)
        print('WEAPON')
        # contains scammers
    if output['alcohol'] > 0.4:
        a = 1
        data = {'wag': 'ALCOHAL'}
        c.append(data)
    if output['drugs'] > 0.45:
        a = 1
        data = {'wag': 'Drugs'}
        c.append(data)
    if output['scam']['prob'] > 0.5:
        a = 3
        data = {'scam':'Scammer'}
        c.append(data)
        print('SCAMMER')
    # contains celebrities
    if output['type']['illustration'] > 0.7:
        a = 4
        data = {'photo':'illustrator'}
        c.append(data)
        print('ILLUSTRATOR')
    if 'celebrity' in output['faces'][0]:
        print('yes celebrity')
        if output['faces'][0]['celebrity'][0]['prob'] > 0.5:
            a = 5
            print('celebrity')
            b = output['faces'][0]['celebrity'][0]['name']
            data = {'celebrity':b}
            c.append(data)
            print(b)
    # contains children
    if output['offensive']['prob'] > 0.8:
        data = {'offensive':'OFFENSIVE'}
        d = 0
        c.append(data)
        print('OFFENSIVE')
    if 'attributes' in output['faces'][0]:
        if output['faces'][0]['attributes']['minor'] > 0.5:
            data = {'attributes':'MINOR'}
            c.append(data)
            print('MINOR')
        if output['faces'][0]['attributes']['female'] > 0.5:
            data = {'attributes': 'FEMALE'}
            c.append(data)
            print('FEMALE')
        if output['faces'][0]['attributes']['male'] > 0.5:
            data = {'attributes': 'MALE'}
            c.append(data)
            print('MALE')
        if output['faces'][0]['attributes']['sunglasses'] > 0.5:
            data = {'attributes': 'SUNGLASSES'}
            c.append(data)
            print('SUNGLASSES')
    print(c)
    return render_template('index.html', data=c)
    
    
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),debug=True)
