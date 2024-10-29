from flask import Flask, request, jsonify
from models import create_user, get_user_by_username, create_product, get_products_by_farmer, get_all_products, get_all_users, delete_user, delete_product
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '84379ce8fbb9e277fe343c1c98fa002a468cb2f90e935721910d148963585519'
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

@app.route('/admin/users', methods=['GET'])
@jwt_required()
def view_all_users():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    users = get_all_users()
    return jsonify({'users': users}), 200

@app.route('/admin/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user_route(user_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    delete_user(user_id)
    return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/admin/product/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product_route(product_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    delete_product(product_id)
    return jsonify({'message': 'Product deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
