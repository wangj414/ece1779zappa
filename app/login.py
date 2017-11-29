from botocore.exceptions import ClientError
from werkzeug.utils import redirect

from app import webapp
from flask import render_template, session, request, url_for

import boto3

from app.main import get_table


@webapp.route('/login', methods=['GET'])
def login_page():
    return render_template('loginpage.html')




@webapp.route('/logininfo', methods=['post'])
def login():

    table = get_table('UserInfo')
    session['email'] = request.form.get('email',"")
    email = session['email']
    password = request.form.get('password', "")
    try:
        response = table.get_item(
            Key = {
                'email': email,
            })
    except ClientError as e:
        session.pop('email', None)
        err_msg = [e.response['Error']['Message']]
        return render_template('index.html',
                                login_err_msg=err_msg
                                )
    else:
        if 'Item' not in response:
            session.pop('email', None)
            err_msg = ["Account does not exist."]
            return render_template('index.html',
                                    login_err_msg=err_msg
                                    )
        elif response['Item']['active']:
            user = response['Item']
            if (password != user['password']):
                session.pop('email', None)
                err_msg = ["Incorrect password."]
                return render_template('index.html',
                                        login_err_msg=err_msg
                                        )
            else:
                return redirect(url_for('index'))
        else:
            session.pop('email', None)
            err_msg = ["Your email hasn't been verified. You can register again if you lost the verification email. "]
            return render_template('index.html',
                                    login_err_msg=err_msg
                                    )

@webapp.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))
