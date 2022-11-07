from flask import Flask, render_template, request, redirect, url_for, session

from app.utils import allowed_file, save_image, save_resize_image

UPLOAD_FOLDER = './app/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/file_list')
def show_list():
    if session.get('filenames'):
        return render_template(
            'show_list.html',
            files=session['filenames']
        )
    return redirect(url_for('upload_file'))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('files')
        if files:
            filenames = []
            for file in files:
                if file.filename == '':
                    return redirect(request.url)
                try:
                    if allowed_file(file.filename, ALLOWED_EXTENSIONS):
                        name, ext, filename = save_image(file, app.config['UPLOAD_FOLDER'])
                        filenames.append(f'{filename}.{ext}')
                        resize_filename = save_resize_image(filename, ext, app.config['UPLOAD_FOLDER'])
                        filenames.append(resize_filename)
                    else:
                        raise Exception
                except:
                    return 'Upload error'
            session['filenames'] = filenames
            return redirect(url_for('show_list'))
    return render_template(
        'upload_file.html'
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
