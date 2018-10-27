from flask import Flask, render_template, url_for, flash, redirect
from Forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

tickets = [
    {
        'event': 'Enter Shikari',
        'date': '31.11.2018',
        'category': 'music',
        'price': '1000'
    },
    {
        'event': 'Stoned Jesus',
        'date': '21.11.2018',
        'category': 'music',
        'price': '400'
    },
    {
        'event': 'Avengers 14',
        'date': '11.11.2018',
        'category': 'film',
        'price': '200'
    },
    {
        'event': 'Carpet',
        'date': '01.11.2018',
        'category': 'film',
        'price': '10'
    },
    {
        'event': 'MC Mcdonalds',
        'date': '05.01.2019',
        'category': 'misc',
        'price': '5000'
    },
    {
        'event': 'New Year with real Santa',
        'date': '31.12.2018',
        'category': 'misc',
        'price': '1000000'
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', tickets=tickets)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
