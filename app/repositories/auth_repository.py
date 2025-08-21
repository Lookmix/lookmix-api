from app.application import db


def save_auth_metadata(data):
    db["auth_metadata"].insert_one(data)


def save_otp_metadata(data):
    db["otp_metadata"].insert_one(data)


def increment_otp_attempts(data):
    db["otp_metadata"].update_one(
        { "_id": data },
        {"$inc": { "attempts": 1 }}
    )

def get_otp_attempts(data):
    otp_metadata = db['otp_metadata'].find_one({'_id': data})

    if otp_metadata:
        return otp_metadata['attempts']
    return -1


# def get_by_jti(jti):
#     return db["auth_meta"].find_one({"jti": jti})


# def update_revoke(jti, token_data):
# =    return db["auth_meta"].update_one({"jti": jti},
#                                           {"$set": token_data},
#                                           upsert=False)


# def get_non_revoked_refresh_token(user_id):
#     return db["auth_meta"].find_one({"user_id": user_id,
#                                      "token_type": "refresh",
#                                      "revoked": False})


# def get_non_revoked_access_token(user_id):
#     return db['auth_meta'].find_one({"user_id": user_id,
#                                         "token_type": "access",
#                                         "revoked": False})

# def save_many_auth_metadata(data):
#     db["auth_metadata"].insert_many(data)