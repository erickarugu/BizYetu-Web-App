from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'bebc92367e831fa89a5bc4aabb1e1785'

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))

	login_form = LoginForm()
	if login_form.validate_on_submit():
		if login_form.email.data == 'admin@blog.com' and login_form.password.data == 'password':
			flash(f'Welcome {login_form.email.data}!', 'success')
			return redirect(url_for('home'))
		else:
			flash(f'Login Unsuccessful. Please check your Email and Password', 'danger')
	return render_template('home.html', title='Home', form=form, login_form=login_form)


@app.route('/about')
def about():
	return render_template('about_us.html', title='About')

if __name__ == '__main__':
	app.run(debug=True)