from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Inventory, User

# Blueprint Initialization
inventory_controller = Blueprint('inventory_controller', __name__)

# Routes
@inventory_controller.route('/')
def dashboard():
    """Dashboard route."""
    if 'username' not in session:
        return redirect(url_for('inventory_controller.login'))
    return render_template('dashboard.html')


@inventory_controller.route('/inventory')
def index():
    """Inventory listing route with optional search."""
    if 'username' not in session:
        return redirect(url_for('inventory_controller.login'))
    
    search_query = request.args.get('search', '')
    
    if search_query:
        items = Inventory.search_items(search_query)
    else:
        items = Inventory.get_all_items()

    total_items = Inventory.count_items()

    return render_template(
        'index.html', items=items, total_items=total_items
    )


@inventory_controller.route('/create', methods=['GET', 'POST'])
def create():
    """Route for adding a new inventory item."""
    if 'username' not in session:
        return redirect(url_for('inventory_controller.login'))

    if request.method == 'POST':
        namaBarang = request.form['namaBarang']
        kodeBarang = request.form['kodeBarang']
        jumlahBarang = request.form['jumlahBarang']
        kondisiBarang = request.form['kondisiBarang']
        gambarBarang = request.form['gambarBarang']
        
        Inventory.add_item(namaBarang, kodeBarang, jumlahBarang, kondisiBarang, gambarBarang)
        flash('Item added successfully!', 'success')
        return redirect(url_for('inventory_controller.index'))
    
    return render_template('create.html')


@inventory_controller.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    """Route for updating an existing inventory item."""
    if 'username' not in session:
        return redirect(url_for('inventory_controller.login'))

    item = Inventory.get_item_by_id(item_id)
    if request.method == 'POST':
        namaBarang = request.form['namaBarang']
        kodeBarang = request.form['kodeBarang']
        jumlahBarang = request.form['jumlahBarang']
        kondisiBarang = request.form['kondisiBarang']
        gambarBarang = request.form['gambarBarang']
        
        Inventory.update_item(item_id, namaBarang, kodeBarang, jumlahBarang, kondisiBarang, gambarBarang)
        flash('Item updated successfully!', 'success')
        return redirect(url_for('inventory_controller.index'))
    
    return render_template('update.html', item=item)


@inventory_controller.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    """Route for deleting an inventory item."""
    if 'username' not in session:
        return redirect(url_for('inventory_controller.login'))
    
    Inventory.delete_item(item_id)
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('inventory_controller.index'))


@inventory_controller.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.verify_password(username, password):
            session['username'] = username
            return redirect(url_for('inventory_controller.dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@inventory_controller.route('/logout')
def logout():
    """User logout route."""
    session.pop('username', None)
    return redirect(url_for('inventory_controller.login'))

@inventory_controller.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create_user(username, password)
        return redirect(url_for('inventory_controller.login'))
    
    return render_template('register.html')

@inventory_controller.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """Route for changing password."""
    if 'username' not in session:
        return redirect(url_for('inventory_controller.login'))

    if request.method == 'POST':
        username = session['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        
        if User.verify_password(username, old_password):
            User.update_password(username, new_password)
            flash('Password changed successfully', 'success')
            return redirect(url_for('inventory_controller.dashboard'))
        else:
            flash('Old password is incorrect', 'error')
    
    return render_template('change_password.html')
