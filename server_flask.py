from flask import Flask, render_template, request, redirect, url_for, flash
import os
import time
from examples.image_to_animation import image_to_animation, annotations_to_animation, image_to_annotations

app = Flask(__name__)

# Define the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'static'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# Define a function to check if a filename has an allowed extension
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/start')
def index():
    return render_template('upimage.html')

@app.route('/upvideo')
def upvideo():
    return render_template('upvideo.html')

@app.route('/test_gif')
def test_gif():
    img_fn = './examples/drawings/person4.jpg'
    char_anno_dir = './static/person4'
    motion_cfg_fn = './examples/config/motion/dab.yaml'
    retarget_cfg_fn = './examples/config/retarget/fair1_ppf.yaml'

    # image_to_animation(img_fn, char_anno_dir, motion_cfg_fn, retarget_cfg_fn)
    annotations_to_animation(char_anno_dir, motion_cfg_fn, retarget_cfg_fn)

    return render_template('hello.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    # Check if the file is an allowed file type
    if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        # Save the file to the upload folder
        filename = file.filename
        img_fn = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(img_fn)
        flash('File saved successfully')
        # return redirect(url_for('upvideo'))
        print('start to make gif')
        char_anno_dir = os.path.join(app.config['RESULT_FOLDER'], filename.split('.')[0])
        motion_cfg_fn = './examples/config/motion/dab.yaml'
        retarget_cfg_fn = './examples/config/retarget/fair1_ppf.yaml'
        image_to_annotations(img_fn, char_anno_dir)
        # image_to_animation(img_fn, char_anno_dir, motion_cfg_fn, retarget_cfg_fn)
        # time.sleep(10)
        print('make gif successfully')
        return redirect(url_for('result_gif', filename=filename))
    else:
        flash('Invalid file type')
        return redirect(request.url)


@app.route('/upload_video', methods=['POST'])
def upload_video():
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    # Check if the file is an allowed file type
    if file and allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
        # Save the file to the upload folder
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File saved successfully')
        return redirect(url_for('result_video', filename=filename))
    else:
        flash('Invalid file type')
        return redirect(request.url)

@app.route('/video/<filename>')
def result_video(filename):
    return render_template('video.html', filename=filename.split('.')[0]+'.mp4')

@app.route('/gif/<filename>')
def result_gif(filename):
    # return render_template('gif.html', filename=filename.split('.')[0] +'/' + 'video.gif')
    return render_template('gif.html', filename='person.gif')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('hello.html')

@app.route('/video2')
def video2():
    return render_template('video.html')


if __name__ == '__main__':

    # app.secret_key = 'super_secret_key'
    # app.run(debug=True)

    char_anno_dir = './static/person4'
    motion_cfg_fn = './examples/config/motion/zombie.yaml'
    retarget_cfg_fn = './examples/config/retarget/fair1_ppf.yaml'

    # image_to_animation(img_fn, char_anno_dir, motion_cfg_fn, retarget_cfg_fn)
    annotations_to_animation(char_anno_dir, motion_cfg_fn, retarget_cfg_fn)


    #brew install mesa
    #export DYLD_LIBRARY_PATH=/usr/local/lib

    # fullName = util.find_library( name )
    # fullName = '/System/Library/Frameworks/OpenGL.framework/OpenGL'