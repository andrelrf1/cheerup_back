from decouple import config
import pyrebase

__firebase_config = {
    'apiKey': config('API_KEY'),
    'authDomain': config('AUTH_DOMAIN'),
    'databaseURL': config('DATA_BASE_URL'),
    'projectId': config('PROJECT_ID'),
    'storageBucket': config('STORAGE_BUCKET'),
    'messagingSenderId': config('MESSAGING_SENDER_ID'),
    'appId': config('APP_ID'),
    'measurementId': config('MEASUREMENT_ID'),
    'serviceAccount': 'cheerup-firebase-credential.json'
}

__firebase = pyrebase.initialize_app(__firebase_config)
__db = __firebase.database()


def create(collection: str, data: dict):
    data = __db.child(collection).push(data)
    return data


def update(collection: str, document_id: str, data: dict):
    __db.child(collection).child(document_id).update(data)


def get_by_id(collection: str, document_id: str):
    collection_data = __db.child(collection).get()
    data = None
    if collection_data.each():
        for document in collection_data.each():
            if document.key() == document_id:
                data = {document.key(): document.val()}
                break

    return data


def get_by_param(collection: str, param: str, value):
    collection_data = __db.child(collection).get()
    data = None
    if collection_data.each():
        for document in collection_data.each():
            if document.val()[param] == value:
                data = {document.key(): document.val()}
                break

    return data


def delete(collection: str, document_id: str):
    __db.child(collection).child(document_id).remove()
