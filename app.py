from flask import Flask
from flask import render_template
from flask import request, session, redirect, url_for, flash
from flask import jsonify
import json

app = Flask(__name__)
app._static_folder = 'static'

app.debug = True
app.secret_key = 'somesecretkey'


# file names
podcast_options_json = 'options.json'
podcast_options_audio = 'options.mp3'
podcast_audio_dir = 'audio'
data_dir = 'data'
log_file_name = 'view_log'
survey_result_file_name = 'survey_result'


# global vars
podcast_options = {}
lastRequestIsVoice = True

"""
    Testing endpoints
"""
@app.route('/ping')
def ping():
    return "pong"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('show_login'))



"""
    Logging In and Dispatching
    TODO: check duplicate submission
"""
@app.route('/login', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def show_login():
    if request.method == 'POST':
        session['user-id'] = request.form["user-id"]
        return redirect(url_for('show_consent_form'))
    return render_template('login.html')


@app.route('/consent-form')
def show_consent_form():
    if 'user-id' not in session:
        return redirect(url_for('show_login'))
    else:
        return render_template('consent_form.html')


# Dispatching client to two systems
@app.route('/_dispatch')
def dispatch():
    # Client must login
    if 'user-id' not in session:
        return redirect(url_for('show_login'))
    # Client must agree consent form
    if request.referrer != url_for('show_consent_form', _external = True):
        print ("Log: Illegal access to dispatcher")
        return redirect(url_for('show_login'))

    # Alternatively dispatch request to voice-based and visual-based system
    global lastRequestIsVoice
    if lastRequestIsVoice:
        lastRequestIsVoice = False
        session['is-voice'] = False
        return redirect(url_for('show_visual_sys'))
    else:
        lastRequestIsVoice = True
        session['is-voice'] = True
        return redirect(url_for('show_voice_sys'))


"""
    Voice/Visual System and Survey
"""
# endpoint for visual based rec system
@app.route('/visual-sys')
def show_visual_sys():
    # Client must login
    if 'user-id' not in session:
        return redirect(url_for('show_login'))
    # validate that request comes from dispatcher
    if request.referrer != url_for('show_consent_form', _external = True):
        print ("Log: Illegal access to visual system")
        return redirect(url_for('show_login'))
    global podcast_options
    ncols = 4
    return render_template('visual_sys.html', podcast_options = podcast_options, ncols = ncols)


# endpoint for voice based rec system
@app.route('/voice-sys')
def show_voice_sys():
    # Client must login
    if 'user-id' not in session:
        return redirect(url_for('show_login'))
    # validate that request comes from dispatcher
    if request.referrer != url_for('show_consent_form', _external = True):
        print ("Log: Illegal access to voice system")
        return redirect(url_for('show_login'))
    return render_template('voice_sys.html', audio_file=podcast_options_audio)


# shared audio player
@app.route('/player/<int:podcast_id>')
def play_audio(podcast_id):
    if ('user-id' not in session):
        return redirect(url_for('show_login'))

    session['podcast-id'] = podcast_id
    audio_file = podcast_audio_dir + '/' + podcast_options['podcasts'][podcast_id]['file-name']
    return render_template('player.html', audio_file=audio_file, pause_offset = 300)


# display survey
@app.route('/survey')
def show_survey():
    if ('user-id' not in session) or ("podcast-id" not in session) or ('is-voice' not in session):
        return redirect(url_for('show_login'))
    else:
        return render_template('survey.html')


# save data and logout
@app.route('/thankyou', methods=['Post', 'GET'])
def save_result_and_logout():
    if request.referrer != url_for('show_survey', _external = True) \
        or ('user-id' not in session) \
        or ('podcast-id' not in session) \
        or ('is-voice' not in session):
        return redirect(url_for('show_login'))

    # save completed survey
    survey_result = request.form.copy()
    survey_result['user-id'] = session['user-id']
    survey_result['podcast-id'] = session['podcast-id']
    survey_result['is-voice'] = session['is-voice']
    fd = open(data_dir + '/' + survey_result_file_name, 'a+')
    fd.write(json.dumps(survey_result))
    fd.write('\n')
    fd.close()

    session.clear()
    return render_template('thankyou.html')


# helper: collect view history
@app.route('/_data-collector', methods=['POST'])
def collect_data():
    log = {}
    log["history"] = request.json
    log["user-id"] = session['user-id']

    fd = open(data_dir + '/' + log_file_name, 'a+')
    fd.write(json.dumps(log))
    fd.write('\n')
    fd.close()
    return ""


@app.errorhandler(404)
def page_not_found(e):
    return "Page Not Found. To login, please visit /login"

if __name__ == "__main__":

    # Load podcasts
    with open(app._static_folder + "/" + podcast_options_json) as podcasts_fd:
        podcast_options = json.load(podcasts_fd)
    # start server
    app.run(threaded=True)
