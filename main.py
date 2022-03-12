from wsgiref import simple_server
import atexit
import uuid
import pandas as pd
import os
from flask import Flask, session, request, Response, jsonify, render_template,redirect,url_for,flash,Markup
import json

from uploadsValidation import Validation
from json_values import Json_values
from prediction import Prediction


app = Flask(__name__)
# app.secret_key = "super secret key"

@app.route('/',methods = ['GET'])
def home_page():
    return render_template('home.html')

@app.route('/columns_details',methods =['GET'])
def cols():
    json_values_obj = Json_values('file_validation.json')
    keys, values,description = json_values_obj.data()

    # data = {keys}
    # ,keys,values
    with open('file_validation.json', 'r') as f:
        dic = json.load(f)
        f.close()
    return render_template('column_details.html',values= values,keys = keys,description = description)


@app.route('/add_data',methods = ['POST','GET'])
def add():
    if(request.method == 'GET'):
        return render_template('add_csv.html')
    elif(request.method == 'POST'):
        try:

            validation = Validation(request.files['csvfile'],'uploads','file_validation.json')
            validation.save()
            numberofcols,col_name,check = validation.checkFile()
            print(col_name)
            if(check):
                strr = "Number of columns are not equal. Number of Columns should be " + str(numberofcols) + '.'
                return render_template('result_of_add.html',data = strr)

            # return redirect(request.url)

            return render_template('result_of_add.html',data = "Data Has been added and file is validated")

        except (UnicodeDecodeError,TypeError) as x:
            # return Response("Error : %s"% UnicodeDecodeError)
            return render_template('result_of_add.html',data = "Please enter a .csv extension")

        except ValueError:
            return render_template('result_of_add.html', data = 'Column are not matching!')
        except Exception as e:
            print("Exception is: ",repr(e))
            # return Response("Error : %s"% Exception)
            return e


@app.route('/predict',methods =['GET','POST'])
def predict():
    if(request.method == 'GET'):
        return render_template('predict.html')
    elif(request.method == 'POST'):
        try:
            validation = Validation(request.files['csvfile'],'predict_uploads','predict_cols_validation.json')
            validation.save()
            numberofcols, col_name,check = validation.checkFile()

            if(check):
                strr = "Number of columns are not equal. Number of Columns should be " + str(numberofcols) + '.'
                return render_template('result_of_add.html',data = strr)
            # print(request.files['csvfile'].filename)
            predict_obj = Prediction(request.files['csvfile'].filename)
            output_filename = predict_obj.predict_data()
            print(output_filename)

            return render_template('result_of_add.html',data = "Data Has been added and file is validated")

        except (UnicodeDecodeError,TypeError) as x:
            print("checking")
            return render_template('result_of_add.html',data = "Please enter a .csv extension")
        except Exception:
            print("Exception checking",repr(Exception))
            render_template('result_of_add.html',data = "Exception")


port =int(os.getenv("PORT",5001))

if __name__ == '__main__':
    host = '0.0.0.0'
    httpd = simple_server.make_server(host=host, port = port, app = app)
    print("http://localhost:5001/" )
    httpd.serve_forever()


