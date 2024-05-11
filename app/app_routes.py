from flask import render_template, request, jsonify, redirect, url_for, make_response
from flask_mail import Message
from app import app, db, mail
from app.models import User
import jwt
from datetime import datetime, timedelta

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(hours=24)}, app.config['SECRET_KEY'])
    send_verification_email(email, token.decode('utf-8'))

    return jsonify({'message': 'User registered successfully. Check your email for verification link.'}), 200

def send_verification_email(email, token):
    msg = Message('Email Verification', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Click the following link to verify your email: http://localhost:5000/verify_email?token={token}'
    mail.send(msg)

@app.route('/verify_email', methods=['GET'])
def verify_email():
    token = request.args.get('token')
    try:
        email = jwt.decode(token, app.config['SECRET_KEY'])['email']
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_verified = True
            db.session.commit()
            return render_template('confirmation.html')
        else:
            return jsonify({'message': 'User not found'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Verification link expired'}), 400
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not user.is_verified:
        return jsonify({'message': 'Email not verified. Check your email for verification link.'}), 400

    if not password == user.password:
        return jsonify({'message': 'Invalid password'}), 401

    token = jwt.encode({'user_id': user.id, 'email': user.email}, app.config['SECRET_KEY'])
    response = make_response(jsonify({'message': 'Login successful'}), 200)
    response.set_cookie('access_token', token.decode('utf-8'), httponly=True)
    return response

@app.route('/protected', methods=['GET'])
def protected():
    access_token = request.cookies.get('access_token')

    if not access_token:
        return jsonify({'message': 'Unauthorized'}), 401

    try:
        payload = jwt.decode(access_token, app.config['SECRET_KEY'])
        user_id = payload['user_id']
        # Additional logic for protected route
        return jsonify({'message': 'Welcome to protected route'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)