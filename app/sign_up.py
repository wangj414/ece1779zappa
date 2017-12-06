import hashlib

from botocore.exceptions import ClientError
# from werkzeug.utils import redirect

from app import webapp
from flask import render_template, session, request, url_for

import boto3

# from app.config import my_email
from app.main import get_table


@webapp.route('/signup', methods=['GET'])
def sign_up_page():
	return render_template('signuppage.html')



@webapp.route('/signupinfo', methods=['post'])
def signup():
    table = get_table('UserInfo')
    email = request.form.get('email', "")
    password = request.form.get('password', "")
    name = request.form.get("name", "")
    print("Before "+email)
    try:
        response = table.get_item(
            Key={
                'email': email,
            })
    except ClientError as e:
        err_msg = e.response['Error']['Message']
        print(err_msg)
        return render_template('index.html',err_msg=err_msg)

    if ('Item' in response) and response['Item']['active']:
        err_msg = ["Account already exists."]
        return render_template('index.html',
                               clickSignUp=True,
                               signup_err_msg=err_msg,
                            )
    else:
        src = email + password
        # code = hashlib.sha256(src.encode('utf-8')).hexdigest()
        code = 'Test'
        response = table.put_item(
            Item={
                'email': email,
                'password': password,
                'name': name,
                'active': False,
                'code': code,
                'favorites': []
            })

        ses = boto3.client('ses')

        link = "https://h1u79dg2z9.execute-api.us-east-1.amazonaws.com/dev/" + 'sign_up/verify/' + email + '&' + code
        print(email)
        response = ses.send_email(
            Source=webapp.config['my_email'],
            Destination={
                'ToAddresses': [
                    email,
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Welcome to Yammme'
                },
                'Body': {
                    # 'Text': {
                    #     'Data': 'string',
                    #     'Charset': 'string'
                    # },
                    'Html': {
                        'Data': '''
    <h2>Hi
    ''' +

                                name

                                + '''
    !</h2>
    <p>Welcome to the <a href="
    ''' +
                                "https://h1u79dg2z9.execute-api.us-east-1.amazonaws.com/dev/"
                                + '''
    ">Yammme</a>.</p>
    <h3>Verify Your Account</h3>
    <p>To complete your registration, please verify your email address by clicking this <a href="
    ''' +
                                link
                                + '''
    "> Link </a>.</p>
    <p>Alternatively, you can copy and paste the following link into your browser's address window: </p>
    <p>
    ''' +
                                link + '''
    </p>
    			                '''
                    }
                }
            }
        )

    signUpMsg = ["To complete the registration, check your emails.",
                     "You'll get an email with a link to comfirm that the address is yours."]
    return render_template('index.html',signUpMsg=signUpMsg)

@webapp.route('/sign_up/verify/<email>&<code>')
def verify(email, code):
	print (email)
	print (code)

	table = get_table('UserInfo')
	try:
		response = table.get_item(
			Key={
			'email': email
			})
	except Exception as e:
		raise e
	else:
		if 'Item' in response:
			user = response['Item']
			if user['active'] == True:
				return 'Your Account is Active.'
			elif user['code'] == code:
				response = table.update_item(
					Key={
						'email': email
					},
					UpdateExpression="set active = :a",
					ExpressionAttributeValues={
						':a': True
					},
					ReturnValues="UPDATED_NEW"
				)
				signUpMsg = ["Congratulations!",
					"Your account has been successfully created!",
					"Please login with your email and have fun! "
				]
				return render_template('index.html',
										clickSignUp=True,
										needSignUp=True,
										signUpMsg=signUpMsg
										)
		else:
			signUpMsg = ['Your must Sign Up before activation.']
			return render_template('index.html',
									clickSignUp=True,
									signUpMsg=signUpMsg
									)






