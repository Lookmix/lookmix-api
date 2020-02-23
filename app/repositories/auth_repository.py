from app import db


def save_data_token(data_token):
    db["oauth2_tokens"].insert_one(data_token)


def save_data_tokens(data_tokens):
    db["oauth2_tokens"].insert_many(data_tokens)


def get_by_jti(jti):
    return db["oauth2_tokens"].find_one({"jti": jti})


def update_revoke(jti, token_data):
    return db["oauth2_tokens"].update_one({"jti": jti},
                                          {"$set": token_data},
                                          upsert=False)


def get_non_revoked_refresh_tokens_by_user_id(user_id):
    return db["oauth2_tokens"].find({"user_id": user_id,
                                     "token_type": "refresh",
                                     "revoked": False})

