
# MIT License

# Copyright (c) 2018 Michael Steudter

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from PIL import Image
from flask import Flask, request, jsonify, send_file, render_template, url_for
import io, time

# define Host-IP and Port for Flask
HOST = '0.0.0.0'
PORT = 8090

# initialize instance of Flask
app = Flask(__name__)


# App Route for wrong path
@app.route('/<path>', methods=['GET','POST'])
def wrongPath(path):
	return jsonify({
'#error':'Imagecropper requires POST-request with image/jpeg (Keyvalue=file) and cropping-parameters: left, upper, right, lower.',
'WebApp':'http://leachim.pythonanywhere.com/'})

# Route for Demo-WebApp

@app.route('/', methods=['GET'])
def index():
	if request.method == 'GET':

		# get paths for files used in the template
		normalize_css = url_for('static', filename='css/normalize.css')
		skeleton_css = url_for('static', filename='css/skeleton.css')
		custom_css = url_for('static', filename='css/custom.css')

		return render_template('index.html', normalize_css=normalize_css, skeleton_css=skeleton_css, custom_css=custom_css)

		

# Route for API-Endpoint
@app.route('/cropper', methods=['POST'])
def cropService():
	if request.method == 'POST':
		startT = time.clock()
# Parameter left, upper, right, lower beziehen sich auf folgende Punkte im Bild:
#	 ___________________
#	|left/upper			|
#	|					|
#	|					|
#	|________right/lower|
#
		try: 

		# try to read arguments POSTed via form

			left = int(request.form['left'])
			upper = int(request.form['upper'])
			right = int(request.form['right'])
			lower = int(request.form['lower'])

			# read image from request
			file = request.files['file']

			# create an Pillow image object with the request's content
			im = Image.open(file, 'r')

			# create a tupel with coordinates for cropping
			box = (left, upper, right, lower)

		except:
			try:
			# try to read arguments of URL-parameters

				left = int(request.args['left'])
				upper = int(request.args['upper'])
				right = int(request.args['right'])
				lower = int(request.args['lower'])

				# read image from request
				file = request.files['file']

				# create an Pillow image object with the request's content
				im = Image.open(file, 'r')

				# create a tupel with coordinates for cropping
				box = (left, upper, right, lower)

			except:

				# error for missing parameters or wrong format
				return jsonify({
					'#error':'Check your parameters. Wrong datatype (Integers only) or missing parameter. The imagefile\'s key has to be named file. Arguments for left, right, lower, upper can be given via URL-parameters or Form.',
					'exampleURL':'http://leachim.pythonanywhere.com/cropper?left=100&upper=200&right=300&lower=400'})

		try: 
		# try to cut out the new image based on the given coordinates for cropping

			region = im.crop(box)

		# Solution is based on Stack-overflow-thread:
		# https://stackoverflow.com/questions/33101935/convert-pil-image-to-byte-array
		# Answered by: Evelyn Jeba (https://stackoverflow.com/users/5440610/evelyn-jeba)
		# cropped image is saved to a new BytesIO Object and is read out as imgByteArray

			imgByteArr = io.BytesIO()
			region.save(imgByteArr, 'jpeg')
			imgByteArr = imgByteArr.getvalue()
			print(str(time.clock()-startT))
		# mimetype has to be defined here, because BytesIO objects are neutral
			return send_file(io.BytesIO(imgByteArr),mimetype='image/jpeg')
			
		except:
		# error if the given coordinates where impossible to cut out
			return jsonify({
			'#error':'Invalid dimensions for area to crop. Requirements: upper < lower und left < right',
			'exampleURL':'http://leachim.pythonanywhere.com/cropper?left=100&upper=200&right=300&lower=400'})



app.run(host=HOST,port=PORT)