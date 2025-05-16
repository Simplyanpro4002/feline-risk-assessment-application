from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired
from models import db, User, Result
from forms import LoginForm, RegistrationForm
from scoring import calculate_raw_score, calculate_standard_score, get_risk_profile
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///risk_assessment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Questions data
QUESTIONS = [
    {
        'id': 1,
        'text': "How would the other cats' siblings describe your cat-self when it comes to taking risks?",
        'options': [
            ('a', "A bold whiskered gambler — you pounce first and think later"),
            ('b', "A curious strategist — you take calculated leaps after sniffing out the details"),
            ('c', "A cautious cat — you tread carefully and avoid surprises"),
            ('d', "A cozy corner-dweller — you avoid all risk, even if the treat bowl is on the line")
        ]
    },
    {
        'id': 2,
        'text': "Grandma Cat left behind 4 blind boxes to test your instincts. Which box would you choose?",
        'options': [
            ('a', "$1,000"),
            ('b', "50% chance to win $5,000"),
            ('c', "25% chance to win $10,000"),
            ('d', "5% chance to win $100,000")
        ]
    },
    {
        'id': 3,
        'text': "You've been saving part of your inheritance from Grandma Cat for a once-in-nine-lives luxury retreat at the most famous international Cat Spa. Just before your departure, the market takes a sharp downturn and your portfolio drops. What do you do?",
        'options': [
            ('a', "Cancel the trip"),
            ('b', "Downgrade to a local modest spa"),
            ('c', "Go as planned"),
            ('d', "Extend your vacation")
        ]
    },
    {
        'id': 4,
        'text': "If you unexpectedly received $20,000 as a bonus from Grandma Cat's estate, what would you do?",
        'options': [
            ('a', "Deposit in bank/CD"),
            ('b', "Invest in safe bonds"),
            ('c', "Invest in stocks/mutual funds")
        ]
    },
    {
        'id': 5,
        'text': "Imagine Grandma Cat left you a basket of stocks. How comfortable are you managing them?",
        'options': [
            ('a', "Not at all"),
            ('b', "Somewhat"),
            ('c', "Very")
        ]
    },
    {
        'id': 6,
        'text': "When you hear the word 'risk,' what does your inner cat think of first?",
        'options': [
            ('a', "Loss"),
            ('b', "Uncertainty"),
            ('c', "Opportunity"),
            ('d', "Thrill")
        ]
    },
    {
        'id': 7,
        'text': "Analysts claim that collectibles, precious metals, and cat-themed art are going to rise in value. But Grandma Cat's legacy fund is currently held in safe government bonds. What would you do?",
        'options': [
            ('a', "Keep the bonds as they are"),
            ('b', "Sell half the bonds — invest half in collectibles and half in money markets"),
            ('c', "Sell all the bonds and go all-in on rising-value hard assets"),
            ('d', "Sell everything, borrow extra, and go big on cat art and vintage assets")
        ]
    },
    {
        'id': 8,
        'text': "Choose 1 Investment best - worst case scenario:",
        'options': [
            ('a', "Gain $200, lose $0"),
            ('b', "Gain $800, lose $200"),
            ('c', "Gain $2,600, lose $800"),
            ('d', "Gain $4,800, lose $2,400")
        ]
    },
    {
        'id': 9,
        'text': "You've been given an additional $1,000 from Grandma Cat's 'Lucky Whisker' fund. You must choose:",
        'options': [
            ('a', "A guaranteed gain of $500"),
            ('b', "A 50/50 chance to win the full $1,000 or nothing")
        ]
    },
    {
        'id': 10,
        'text': "You've been given an additional $1,000 from Grandma Cat's 'Lucky Whisker' fund. But you might have to pay something in return. You are now asked to choose between:",
        'options': [
            ('a', "A sure loss of $500"),
            ('b', "A 50% chance to lose $1,000 and a 50% chance to lose nothing")
        ]
    },
    {
        'id': 11,
        'text': "One of Grandma Cat's mysterious cousins left you $100,000, but there's a catch: you must invest it all in just one treasure trove. Which would you choose?",
        'options': [
            ('a', "A cozy savings account or money market mutual fund—safe and snug."),
            ('b', "A mutual fund with a mix of stocks and bonds—balanced, like a well-groomed tail."),
            ('c', "A paw-picked portfolio of 15 common stocks."),
            ('d', "Shiny things! Commodities like gold, silver, and oil")
        ]
    },
    {
        'id': 12,
        'text': "You receive a $20,000 inheritance from Grandma Cat's investment vault. How would you allocate it across risk levels?",
        'options': [
            ('a', "60% low-risk, 30% medium, 10% high"),
            ('b', "30% low, 40% medium, 30% high"),
            ('c', "10% low, 40% medium, 50% high")
        ]
    },
    {
        'id': 13,
        'text': "Your trusted alley-cat friend, Professor Paws, has sniffed out a rare opportunity: a gold mine that could return 50 to 100 times your investment—if it pans out. But there's only a 20% chance it strikes rich. If it fails, you lose every last treat. How much would you invest from your stash?",
        'options': [
            ('a', "Nothing"),
            ('b', "One month's salary"),
            ('c', "Three month's salary"),
            ('d', "Six month's salary")
        ]
    },
    {
        'id': 14,
        'text': "As one of Grandma Cat's chosen heirs, you must decide how to grow your share of the portfolio. You're reviewing a range of investments—from stable income streams to high-growth claws in volatile markets. How would you balance growth potential and stability, knowing that inflation slowly nibbles away at your purchasing power?",
        'options': [
            ('a', "My goal is to minimize swings in my portfolio's value, even if growth does not keep pace with inflation."),
            ('b', "My goal is for growth to at least keep pace with inflation, with the risk of modest swings in my portfolio's value."),
            ('c', "My goal is for growth to exceed inflation, with the risk of modest to larger swings in my portfolio's value."),
            ('d', "My goal is for growth to significantly exceed inflation, with the risk of larger swings in my portfolio's value.")
        ]
    },
    {
        'id': 15,
        'text': "Market turbulence has rattled Grandma Cat's diversified portfolio, and your share has declined by 20% over a short period. All the other heirs are watching how you'll react to this downturn. What is your most likely course of action?",
        'options': [
            ('a', "I would not change my portfolio."),
            ('b', "I would wait at least one year before changing to options that are more conservative."),
            ('c', "I would wait at least three months before changing to options that are more conservative."),
            ('d', "I would immediately change to options that are more conservative.")
        ]
    }
]

class QuestionForm(FlaskForm):
    answer = RadioField('Answer', validators=[DataRequired()])
    submit = SubmitField('Next')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered')
            return render_template('register.html', form=form)
        
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login with your credentials.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.args.get('action') == 'prev' and session.get('current_question', 0) > 0:
        session['current_question'] -= 1
        return redirect(url_for('index'))

    if 'current_question' not in session:
        session['current_question'] = 0
        session['answers'] = {}
    
    if session['current_question'] >= len(QUESTIONS):
        return redirect(url_for('results'))
    
    question = QUESTIONS[session['current_question']]
    form = QuestionForm()
    form.answer.choices = question['options']
    
    if str(question['id']) in session.get('answers', {}):
        form.answer.data = session['answers'][str(question['id'])]
    
    if form.validate_on_submit():
        session['answers'][str(question['id'])] = form.answer.data
        session['current_question'] += 1
        return redirect(url_for('index'))
    
    return render_template('question.html', 
                         question=question,
                         form=form,
                         progress=session['current_question'],
                         total_questions=len(QUESTIONS))

@app.route('/results')
@login_required
def results():
    if 'answers' not in session:
        return redirect(url_for('index'))
    
    # Calculate scores
    raw_score = calculate_raw_score(session['answers'])
    standard_score = calculate_standard_score(raw_score)
    risk_profile = get_risk_profile(standard_score)
    
    # Save results to database
    result = Result(
        user_id=current_user.id,
        answers=session['answers'],
        raw_score=raw_score,
        standard_score=standard_score,
        risk_group=risk_profile['group']
    )
    db.session.add(result)
    db.session.commit()
    
    answers = session['answers']
    session.clear()
    return render_template(
        'results.html',
        answers=answers,
        questions=QUESTIONS,
        raw_score=raw_score,
        standard_score=standard_score,
        risk_profile=risk_profile
    )

if __name__ == '__main__':
    app.run(debug=True) 