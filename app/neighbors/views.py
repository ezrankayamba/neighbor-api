# app/home/views.py

from flask import render_template, request, redirect, session
from app import db
from . import neighbors
from app.models import Neighbor, Sms, Token
import app.utils as utils
from sqlalchemy import text
from flask import jsonify, request
import datetime
import random


@neighbors.route('/sendotp', methods=['POST'])
def send_otp():
    data = request.get_json()
    token = random.randint(100001, 999999)
    msg = '{} is one time password. Use this within 3 minutes'.format(token)
    msisdn = data['msisdn']
    sms = utils.send_sms(msg, msisdn)
    print(sms)
    res = {
        'status': -1,
        'message': "Successfully sent the OTP",
        'smsResultCode': sms['statusCode']
    }
    if sms['statusCode'] in [100, 101, 102]:
        m1 = Sms(message=msg, msisdn=msisdn,
                 message_id=sms['messageId'], status=1)
        now = datetime.datetime.now()
        expiry_date = now + datetime.timedelta(minutes=3)
        m2 = Token(token=token, owner_id=msisdn,
                   status=0, expiry_date=expiry_date)
        db.session.add(m1)
        db.session.add(m2)
        db.session.commit()
        res['status'] = 0
        res['message'] = "Successfully sent the OTP"
        return jsonify(res)
    else:
        return jsonify(res)


@neighbors.route('/validateotp', methods=['POST'])
def validate_otp():
    data = request.get_json()
    msisdn = data['msisdn']
    token = data['token']
    tkn = Token.query.filter(Token.owner_id == msisdn, Token.token ==
                             token, Token.expiry_date >= utils.my_datetime(), Token.status == 0).first()
    if tkn is None:
        res = {
            'status': -1,
            'message': "Token validation failed. It might be invalid, expired or already used!"
        }
        return jsonify(res)
    # Update as used
    tkn.status = 1
    db.session.commit()
    return jsonify({'status': 0, 'message': 'Successful validation of token'})


@neighbors.route('/create', methods=['POST'])
def create_neighbor():
    data = request.get_json()
    msisdn = data['msisdn']
    token = data['token']
    name = data['name']
    fcmId = data['fcmId']
    fcmToken = data['fcmToken']
    res = {
        'status': -1,
        'message': "User record failed: OTP is not valid or already used"
    }
    tkn = Token.query.filter(Token.owner_id == msisdn,
                             Token.token == token, Token.status == 1).first()
    if tkn is None:
        return jsonify(res)
    nb = Neighbor.query.filter(Neighbor.msisdn == msisdn).first()
    if nb is None:
        nb = Neighbor(name=name, msisdn=msisdn, status=1,
                      fcm_id=fcmId, fcm_token=fcmToken)
        db.session.add(nb)
    else:
        nb.fcm_id = fcmId
        nb.fcmToken = fcmToken
        nb.last_update = utils.my_datetime()
    db.session.commit()
    return jsonify({'result': 0, 'message': 'Successfully created neighbor: {}'.format(name), 'id': nb.id})
