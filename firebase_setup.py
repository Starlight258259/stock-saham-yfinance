import firebase_admin
from firebase_admin import credentials, firestore

# Menentukan path relatif ke file kredensial
cred = credentials.Certificate('./firebase-credentials.json')  # Pastikan path relatif sesuai dengan lokasi file kredensial

# Menginisialisasi Firebase
firebase_admin.initialize_app(cred)

# Mendapatkan referensi ke Firestore
db = firestore.client()
