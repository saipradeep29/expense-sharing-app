from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app, db
from app.forms import LoginForm, RegisterForm, GroupForm, ExpenseForm
from app.models import User, Group, Expense, ExpenseSplit
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, mobile=form.mobile.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/group/new', methods=['GET', 'POST'])
@login_required
def new_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data)
        db.session.add(group)
        db.session.commit()
        current_user.groups.append(group)
        db.session.commit()
        flash('Group created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_group.html', form=form)

@app.route('/group/<int:group_id>')
@login_required
def group(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template('group.html', group=group)

@app.route('/group/<int:group_id>/expense/new', methods=['GET', 'POST'])
@login_required
def new_expense(group_id):
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(description=form.description.data, amount=form.amount.data, group_id=group_id, split_method=form.split_method.data)
        db.session.add(expense)
        db.session.commit()

        if form.split_method.data == 'equal':
            split_amount = form.amount.data / len(group.members)
            for member in group.members:
                split = ExpenseSplit(user_id=member.id, expense_id=expense.id, amount=split_amount)
                db.session.add(split)
        elif form.split_method.data == 'exact':
            for split in form.exact_splits.entries:
                split_record = ExpenseSplit(user_id=split.data['user_id'], expense_id=expense.id, amount=split.data['amount'])
                db.session.add(split_record)
        elif form.split_method.data == 'percentage':
            for split in form.percentage_splits.entries:
                split_record = ExpenseSplit(user_id=split.data['user_id'], expense_id=expense.id, amount=(split.data['percentage']/100)*form.amount.data, percentage=split.data['percentage'])
                db.session.add(split_record)
        db.session.commit()

        flash('Expense added successfully!', 'success')
        return redirect(url_for('group', group_id=group_id))
    return render_template('create_expense.html', form=form)

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    user = User(username=data['username'], email=data['email'], mobile=data['mobile'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'username': user.username, 'email': user.email, 'mobile': user.mobile})

@app.route('/api/expense', methods=['POST'])
@login_required
def add_expense():
    data = request.json
    expense = Expense(description=data['description'], amount=data['amount'], group_id=data['group_id'], split_method=data['split_method'])
    db.session.add(expense)
    db.session.commit()

    if data['split_method'] == 'equal':
        split_amount = data['amount'] / len(expense.group.members)
        for member in expense.group.members:
            split = ExpenseSplit(user_id=member.id, expense_id=expense.id, amount=split_amount)
            db.session.add(split)
    elif data['split_method'] == 'exact':
        for split_data in data['splits']:
            split = ExpenseSplit(user_id=split_data['user_id'], expense_id=expense.id, amount=split_data['amount'])
            db.session.add(split)
    elif data['split_method'] == 'percentage':
        for split_data in data['splits']:
            split = ExpenseSplit(user_id=split_data['user_id'], expense_id=expense.id, amount=(split_data['percentage']/100)*data['amount'], percentage=split_data['percentage'])
            db.session.add(split)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'}), 201

@app.route('/api/expense/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_expenses(user_id):
    expenses = Expense.query.join(ExpenseSplit).filter(ExpenseSplit.user_id == user_id).all()
    return jsonify([{
        'description': expense.description,
        'amount': expense.amount,
        'date': expense.date,
        'group': expense.group.name,
        'split_method': expense.split_method
    } for expense in expenses])

@app.route('/api/expense/overall', methods=['GET'])
@login_required
def get_overall_expenses():
    expenses = Expense.query.all()
    return jsonify([{
        'description': expense.description,
        'amount': expense.amount,
        'date': expense.date,
        'group': expense.group.name,
        'split_method': expense.split_method
    } for expense in expenses])

@app.route('/api/expense/balance-sheet', methods=['GET'])
@login_required
def download_balance_sheet():
    # Generate and return balance sheet (e.g., CSV or PDF)
    pass
