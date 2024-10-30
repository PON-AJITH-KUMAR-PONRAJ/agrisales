from flask import Flask, request, jsonify
from models import create_user, get_user_by_username, create_product, get_products_by_farmer, get_all_products, create_order, get_orders_by_customer, get_orders_by_farmer, update_order_status, delete_all_users, get_all_users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '5180db6812cb8827379272f2c7014b1b4fd90c4d533b2d95ee3ef43a062b0895'
jwt = JWTManager(app)

@app.route('/')
def home():
    return 'Welcome to Uzhavan Agri Sales Management API!'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not role:
        return jsonify({'message': 'Role is required'}), 400

    hashed_password = generate_password_hash(password)
    create_user(username, hashed_password, role)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity={'id': user['id'], 'username': user['username'], 'role': user['role']})
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/create_product', methods=['POST'])
@jwt_required()
def create_product_route():
    data = request.get_json()
    current_user = get_jwt_identity()
    farmer_id = current_user['id']
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')

    create_product(name, price, description, farmer_id)
    return jsonify({'message': 'Product created successfully'}), 201

@app.route('/products', methods=['GET'])
@jwt_required()
def products():
    current_user = get_jwt_identity()
    if current_user['role'] == 'farmer':
        farmer_id = current_user['id']
        products = get_products_by_farmer(farmer_id)
    else:
        products = get_all_products()

    return jsonify({'products': products}), 200

@app.route('/create_order', methods=['POST'])
@jwt_required()
def create_order_route():
    data = request.get_json()
    current_user = get_jwt_identity()
    customer_id = current_user['id']
    product_id = data.get('product_id')

    create_order(product_id, customer_id)
    return jsonify({'message': 'Order created successfully'}), 201

@app.route('/farmer/orders', methods=['GET'])
@jwt_required()
def view_orders_by_farmer():
    current_user = get_jwt_identity()
    if current_user['role'] != 'farmer':
        return jsonify({'message': 'Unauthorized access'}), 403

    farmer_id = current_user['id']
    orders = get_orders_by_farmer(farmer_id)
    return jsonify({'orders': orders}), 200

@app.route('/customer/orders', methods=['GET'])
@jwt_required()
def view_orders_by_customer():
    current_user = get_jwt_identity()
    customer_id = current_user['id']
    orders = get_orders_by_customer(customer_id)
    return jsonify({'orders': orders}), 200

@app.route('/order/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order_status_route(order_id):
    data = request.get_json()
    status = data.get('status')
    update_order_status(order_id, status)
    return jsonify({'message': 'Order status updated successfully'}), 200

@app.route('/admin/users', methods=['GET'])
@jwt_required()
def view_all_users():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    users = get_all_users()
    return jsonify({'users': users}), 200

@app.route('/admin/users', methods=['DELETE'])
@jwt_required()
def delete_all_users_route():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    delete_all_users()
    return jsonify({'message': 'All users deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
