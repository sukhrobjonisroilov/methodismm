import datetime
import random

from methodism import MESSAGE, generate_key, code_decoder, exception_data

from api.models import OtpToken, User, AuthToken
from base.errors import MSG
from base.helper import cr


def auth_one(request, params):
    if "email" not in params:
        return cr(False, message=MESSAGE['ParamsNotFull'])
    code = random.randint(100_000, 999_999)

    shifrlash = generate_key(50) + "@" + str(code) + "@" + generate_key(20)
    shifr = "pbkdf2_sha256$600000$" + code_decoder(shifrlash)
    token = OtpToken.objects.create(key=shifr, email=params['email'])
    return cr(True, data={"token": token.key, "otp": code})


def auth_two(request, params):
    if "otp" not in params or "token" not in params:
        return cr(False, message=MESSAGE['ParamsNotFull'])
    otp = OtpToken.objects.filter(key=params['token']).first()
    if not otp:
        return cr(False, message=MESSAGE['NotData'])
    if otp.is_expired or otp.is_verified:
        return cr(False, message=MESSAGE['TokenUnUsable'])

    now = datetime.datetime.now()
    if (now - otp.created).total_seconds() >= 120:
        otp.is_expired = True
        otp.save()
        return cr(False, message=MSG['VaqtTugadi'])

    unhash = code_decoder(otp.key.lstrip("pbkdf2_sha256$600000$"), decode=True)
    code = unhash.split('@')[1]
    if str(code) != str(params['otp']):
        otp.tries += 1
        otp.save()
        return cr(False, message=MSG['OTPCodeError'])
    user = User.objects.filter(email=otp.email).first()
    return cr(True, data={'is_registered': user is not None})


def login(request, params):
    if "email" not in params or "password" not in params:
        return cr(False, message=MESSAGE['ParamsNotFull'])
    user = User.objects.filter(email=params['email']).first()
    if not user or not user.check_password(str(params['password'])):
        return cr(False, message=MESSAGE['UserPasswordError'])

    token = AuthToken.objects.get_or_create(user=user)[0]
    return cr(True, data={'token': token.key})


def register(request, params):
    if 'email' not in params or 'password' not in params:
        return cr(False, message=MESSAGE['ParamsNotFull'])
    user = User.objects.filter(email=params['email']).first()
    if user:
        return cr(False, message=MSG['UserBor'])
    user = User.objects.create_user(email=params['email'], password=params['password'])
    token = AuthToken.objects.create(user=user)
    return cr(True, data={'token': token.key})
def loginout(request,params):
    token =AuthToken.objects.get(user=params['user'])
    token.delete()
    return  cr(True,message=MSG[''])