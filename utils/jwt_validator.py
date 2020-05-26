from flask_jwt_extended import decode_token


def validate(jwt_token: str, user_id: str):
    if decode_token(jwt_token)['identity'] == user_id:
        return True

    return False
