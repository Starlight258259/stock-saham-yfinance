import firebase_admin
from firebase_admin import credentials, firestore

# Path ke file kredensial Firebase JSON
cred = credentials.Certificate('path/to/your/firebase-credentials.json')

# Inisialisasi Firebase
firebase_admin.initialize_app(cred)

# Inisialisasi Firestore
db = firestore.client()
