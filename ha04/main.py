from flask import Flask, render_template, request, url_for, flash, redirect
from markupsafe import escape
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

posts = [
    {
        'subject': 'Some subject',
        'description': 'This is post about whether',
        'author': "Val Smith",
        'date': '01.04.2022'
    },
    {
        'subject': 'Some subject #2',
        'description': 'This is post about kittens',
        'author': "Vic Smith",
        'date': '03.04.2022'
    }
]

messages = {'1234':
                {'title': 'Message One',
                 'content': 'Message One Content',
                 'datetime': 'today!'},
            '5678':
                {'title': 'Message Two',
                 'content': 'Message Two Content',
                 'datetime': 'long time ago'}
            }


@app.route('/')
def main_page():
    return render_template('main_page.html', posts=posts, title='Main')


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        subject = request.form['subject']
        description = request.form['description']

        if not subject:
            flash('Title is required!')
        elif not description:
            flash('Content is required!')
        else:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            posts[str(abs(hash(dt_string + subject)))] = {'subject': subject,
                                                          'description': description,
                                                          'datetime': dt_string}
            return redirect(url_for('main'))
    return render_template('new_post.html', title='New post')


@app.route('/postpage/<string:post_id>')
def postpage(post_id=None):
    post_d = messages[post_id]
    return render_template('post_view.html',
                           title=escape(post_d['title']),
                           content=escape(post_d['content']),
                           datetime=escape(post_d['datetime'])
                           )
