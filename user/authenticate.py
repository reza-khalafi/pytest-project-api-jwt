import datetime
import jwt
from user.models import User


class Authenticate(object):

    def __init__(self):
        pass

    def create_access_token(self, user_id):
        payload = {
            "id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, "secret", algorithm="HS256")
        return token


    def get_user_by_request(self, request):
        if 'Authorization' not in request.headers:
            return None
        token = request.headers['Authorization']
        if token is None:
            return None
        token = token.replace("Bearer ", "")
        print(f"token is: {token}")
        # blacklist = Blacklist.objects.filter(token=token).first()
        # if blacklist:
        #     return None
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            if 'id' not in payload:
                return None
            else:
                user = User.objects.filter(id=payload['id']).first()
                if not user:
                    return None
                return user
        except:
            return None




