from flask import Flask, request, redirect, url_for
# from google.cloud import storage
from firebase_admin import credentials, initialize_app, storage
import uuid
import os
from dotenv import load_dotenv


# 加載環境變量
load_dotenv()

# 從環境變量中獲取 Firebase 存儲桶名稱
firebase_storage_bucket = os.getenv('FIREBASE_STORAGE_BUCKET')

# Init firebase with your credentials
cred = credentials.Certificate("my-credentials.json")
initialize_app(cred, {'storageBucket': firebase_storage_bucket})

app = Flask(__name__)

def upload_image_to_firebase(file_path, destination):
    # 初始化 Firebase Storage 客戶端
    client = storage.bucket()
    # client = storage.Client()
    blob = client.blob(destination)
    blob.upload_from_filename(file_path)

    # 上傳文件
    blob = client.blob(destination)
    blob.upload_from_filename(file_path)

    # Opt : if you want to make public access from the URL
    blob.make_public()

    return blob.public_url

@app.route("/")
def hello():
    return 'Hello, Here is Kawa\'s Blog!'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        # 生成隨機文件名
        random_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]

        # 保存文件到本地
        file_path = '/tmp/' + random_filename
        file.save(file_path)
        
        # 將文件上傳到 Firebase Storage
        image_url = upload_image_to_firebase(file_path, 'images/' + random_filename)
        
        return image_url

# 定義404錯誤處理
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
