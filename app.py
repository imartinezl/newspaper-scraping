from newspaper import Article
url = 'https://www.diariovasco.com/economia/macroparque-eolico-siemens-asteasu-20190210001331-ntvo.html'

article = Article(url)
article.download()
article.parse()
article.text
article.title



from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return article.title

@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': article.title
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

if __name__ == '__main__':
    app.run(debug=True, port=5000)




