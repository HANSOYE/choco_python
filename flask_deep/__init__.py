import os
import sys
sys.path.append("..")

from flask import Flask, request, flash
from flask.templating import render_template
from style_transfer import main
from cast import cast_main

app = Flask(__name__)
app.debug = True

''' Main page '''
@app.route('/')
def index():
	return render_template('index.html')

''' Neural Style Transfer '''
@app.route('/b_style_transfer')
def bst_get():
    	return render_template('b_style_transfer.html')

@app.route('/bst_post', methods=['GET','POST'])
def bst_post():
	if request.method == 'POST':
		#Content Image
		content_img = request.files["user_img"]
		content_img.save('./flask_deep/static/testA/' + str(content_img.filename))
		content_img_path = './flask_deep/static/testA/'+str(content_img.filename)

		#Style Image
		style_img = request.files["style_img"]
		style_img.save('./flask_deep/static/testB/' + str(content_img.filename))
		style_img_path = './flask_deep/static/testB/'+str(content_img.filename)

		#Background Style Transfer
		transfer_img_path = cast_main(content_img_path, style_img_path) # return -> file name

		print(f'content: {content_img_path}')
		print(f'transfer: {transfer_img_path}')

		c_list = content_img_path.split('/')
		content_img_path = c_list[-2]+'/'+c_list[-1]
		t_list = transfer_img_path.split('/')
		transfer_img_path = t_list[-3]+'/'+t_list[-2]+'/'+t_list[-1]

	return render_template('bst_post.html',content_img=content_img_path, transfer_img=transfer_img_path)


@app.route('/c_style_transfer')
def cst_get():
    	return render_template('c_style_transfer.html')

@app.route('/cst_post', methods=['GET','POST'])
def cst_post():
	if request.method == 'POST':
		#Content Image
		content_img = request.files["user_img"]
		content_img.save('./flask_deep/static/images/' + str(content_img.filename))
		content_img_path = './flask_deep/static/images/'+str(content_img.filename)

		#Style Image
		style = request.form['style'] #str
		style_id = request.form['style_id'] #str
		#Character Style Transfer
		transfer_img_path, alert = main(content_img_path, style, int(style_id)) # return -> file name
		#print(f'Alert: {alert}')
		c_list = content_img_path.split('/')
		content_img_path = c_list[-2]+'/'+c_list[-1]
		t_list = transfer_img_path.split('/')
		transfer_img_path = t_list[-2]+'/'+t_list[-1]
	if alert:
		flash("얼굴을 탐지하지 못했습니다.\n 성능이 떨어질 수 있습니다.")
		return render_template('cst_post.html',content_img=content_img_path, transfer_img=transfer_img_path)
	else:
		return render_template('cst_post.html',content_img=content_img_path, transfer_img=transfer_img_path)