from flask import Flask, request, jsonify
import os
from datetime import datetime
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
UPLOAD_FOLDER = '/root/autodl-tmp/Flask_YOLOv8/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 创建保存图片、视频的文件夹

@app.route('/imagesUpload', methods=['POST'])
def uploadImages():
    if 'images' not in request.files:
        return jsonify({'error': 'No images part'})
    
    images_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
    now = datetime.now()
    folder_name = now.strftime("%Y-%m-%d-%H-%M-%S")
    images_upload_folder = os.path.join(images_folder, folder_name)
    os.makedirs(images_upload_folder, exist_ok=True)
    
    images = request.files.getlist('images')

    # 将图片上传保存到文件夹中
    for image in images:
        if image.filename == '':
            return jsonify({'error': 'No selected file'})
        if image.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image.save(os.path.join(images_upload_folder, image.filename))
        else:
            return jsonify({'error': 'Unsupported file type'})

    return jsonify({'message': 'Files uploaded successfully', 'folder_name': folder_name})
        
@app.route('/videoUpload', methods=['POST'])
def uploadVideos():
    if 'video' not in request.files:
        return jsonify({'error': 'No video part'})
    
    videos_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'videos')
    now = datetime.now()
    folder_name = now.strftime("%Y-%m-%d-%H-%M-%S")
    videos_upload_folder = os.path.join(videos_folder, folder_name)
    os.makedirs(videos_upload_folder)

    videos = request.files.getlist('videos')

    # 将视频上传保存到文件夹中
    for video in videos:
        if video.filename == '':
            return jsonify({'error': 'No selected file'})
        if video.filename.lower().endswith(('.mp4', '.avi', '.mov')):
            video.save(os.path.join(videos_upload_folder, video.filename))
        else:
            return jsonify({'error': 'Unsupported file type'})

    return jsonify({'message': 'Files uploaded successfully', 'folder_name': folder_name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=6006)
