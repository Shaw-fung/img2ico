from flask import Flask, request, render_template, send_file
from flask_wtf.csrf import CSRFProtect
from PIL import Image
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# 启用CSRF保护
csrf = CSRFProtect(app)

# 允许上传的文件类型和大小
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大16MB

# 验证上传的文件类型和大小
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
@csrf.exempt  # 豁免CSRF保护
def convert():
    # 获取上传的图片文件
    png_file = request.files['file']
    
    # 验证文件类型和大小
    if not png_file or not allowed_file(png_file.filename) or png_file.content_length > MAX_CONTENT_LENGTH:
        return render_template('error.html', message='Invalid file type or size')
    
    # 打开图片文件并转换为ICO格式
    try:
        img = Image.open(png_file)
        ico_file = io.BytesIO()
        img.save(ico_file, format='ICO')
        ico_file.seek(0)
    except:
        return render_template('error.html', message='Failed to convert image')
    
    # 返回转换后的ICO文件
    return send_file(ico_file, mimetype='image/vnd.microsoft.icon', as_attachment=True, download_name='converted.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
