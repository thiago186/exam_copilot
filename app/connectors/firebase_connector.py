"""These file contains the firebase bucket connector"""

from firebase_admin import storage, credentials

from config import settings
from schemas.mongodb_ import 

credentials = credentials.Certificate(settings.FIREBASE_CREDENTIALS_FILENAME)

firebase_admin.initialize_app(cred,{'storageBucket': settings.FIREBASE_BUCKET_URL}) # connecting to firebase

def upload_image(image: )
