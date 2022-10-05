import time
from flask import Flask
from flask import request
from flask import make_response
app = Flask(__name__)

@app.route('/')
def index():
    return """
<!doctype html>
<title>Index</title>
<ul>
<li><a href="/greet">/greet</a></li>
<li><a href="/unimplemented">/unimplemented</a></li>
<li><a href="/find/out">/find/(something)</a></li>
<li><a href="/exams/1">/exams/(id)</a></li>
<li><a href="/brew">/brew/(beverage)</a></li>
</ul>""", 200

@app.route('/greet')
def greet():
    lang = request.headers.get('Accept-Language', 'cz')

    if '-' in lang:
       lang = lang.split('-')[0]
    if '_' in lang:
       lang = lang.split('_')[0]

    if lang == 'cz':
        return u'Dobrý den'
    if lang == 'pl':
        return u'Dzień dobry'
    if lang == 'en':
        return  'Good morning'

    return 'nuqneH' # Klingon

@app.route('/unimplemented')
def unimplemented():
    raise NotImplementedError

@app.route('/find/<name>')
def finder(name):
    if name in ('keys', 'wallet', 'hope'):
        return f'{name}: not found', 404
    return u'You can find almost all in 🕷 🕸', 200

@app.route('/exams/<id>')
def exam(id):
    try:
        id = int(id)
    except ValueError as e:
        return "Provide a whole number", 400

    if id == -1:
        if 'text/plain' in request.headers['Accept']:
            response = make_response(HIDDEN_EXAM, 200)
            response.headers['Content-Type'] = 'text/plain; charset=UTF-8'
            return response
        return 'Can only respond in plain text', 400

    return "🎼 Can't touch this! 🎼", 401

@app.route('/brew',            methods=['GET','OPTIONS'])
@app.route('/brew/<beverage>', methods=['GET','POST','DELETE','HEAD', 'PUT', 'OPTIONS'])
def brewer(beverage=None):
    teas = ('tea', 'green tea', 'sencha', 'matcha', 'oolong', 'earl-grey')
    if request.method == 'OPTIONS':
        response = make_response(','.join(teas), 200)
        response.headers['Allow'] = 'OPTIONS, POST'
        return response
    if request.method == 'GET':
        return 'You have to create the beverage, not only get it', 400
    if request.method == 'DELETE':
        return f"You can't delete {beverage}", 405
    if request.method not in ('GET', 'POST', 'DELETE'):
        return f"Why do that to {beverage}?", 405
    if beverage in ('coffee', 'caffe'):
        teapot = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Utah_Teapot_mr_maya.jpg/240px-Utah_Teapot_mr_maya.jpg'
        return f'<!doctype html><title>I\'m a teapot!</title> <img src="{teapot}" alt="Utah teapot"/>', 418
    if beverage in teas:
        return 'Here you are: 🍵', 200 
    return 'You drink that?', 400

HIDDEN_EXAM = u"""
1. (6p.) Czym są: HTTP, HTML, JSON?
2. (4p.) Co będzie efektem żądania HTTP:
POST /album/favourites HTTP/1.1
Host: www.musiclib.io
Content-Type: text/plain
Content-Length: 45
open.spotify.com/album/3cNSfvMTPQGNXNlqCioKE1
3. (2p.) Która definicja nawigacji jest najbardziej semantyczna?
a) <span class="red-link">Home</span>
b) <nav><ul><li>Home</li></ul></nav>
c) <div class="main-menu"><ul><li>Home</li></ul></div>
4. (5p.) Kto może być klientem publicznej usługi sieciowej?
a) robot internetowy, b) inna usługa sieciowa,
c) aplikacja mobilna, d) serwis WWW,
e) gry komputerowa, f) mysz komputerowa.
5. (6p.) Jakie są zalety żetonów JSON (JWT)?
a) są czytelne dla człowieka,
b) są zaszyfrowane,
c) przechowują stan skojarzony z użytkownikiem,
d) pozwalają na kontrolę swojej spójności.
6. (5p.) Czym są zapytania asynchroniczne?
7. (7p.) Na czym polega Same-Origin Policy?
8. (5p.) Co to jest CRUD?
a) neandertalczyk,
b) zestaw popularnych operacji łatwo odwzorowywanych w bazach danych,
c) metodyka wytwarzania aplikacji,
d) rodzaj usługi sieciowej.
"""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050)
