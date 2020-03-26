#import các thư viện cần thiết
from flask import Flask,request,jsonify 
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy là 1 ORM (ánh xạ các object đến các bảng trong databbase)
from flask_migrate import Migrate  #Migrate 
app = Flask(__name__) # khởi tạo 1 thể hiện của lớp Flask với tham số là tên của 1 ứng dụng hoặc 1 package.

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://winter:12345@localhost:5432/testdb" #Config database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # loại bỏ cảnh báo SQLALCHEMY_TRACK_MODIFICATIONS option will be disabled. :))
app.url_map.strict_slashes = False #mọi route đều đc tạo 
db = SQLAlchemy(app) #khởi tạo 1 instance của Flask-SQLAlchemy
migrate = Migrate(app,db) #khởi tạo 1 instance của Flask-Migrate cho phép thay đổi, di chuyển dữ liệu từ model sang database sử dụng alembic(model thay đổi thì object trong db cũng thay đổi theo)

class CarsModel(db.Model): #tạo lớp model map với 1 bảng tương ứng trong database
    __tablename__ = 'cars' #tên bảng
    #Các trường trong bảng
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String())
    color = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self,brand, color, doors): #hàm dựng sẽ được gọi đến khi khởi tạo 1 đối tượng mới
        self.brand = brand
        self.color = color
        self.doors = doors
    def __ini__(self,id):
        self.id = id
    def __repr__(self): #hiển thị thông tin
        return f"<Car {self.brand}>"

@app.route('/')
def hello():
    return 'hello,world'

@app.route('/cars', methods=['POST', 'GET'])# định tuyến trang đến các path được khai báo trước và sử dụng các http request post,get
def handle_cars(): 
    if request.method == 'POST':
        if request.is_json: #trường hợp request có dạng json
            data = request.get_json() #lưu lại dữ liệu json vào biến data được gửi lên server
            new_car = CarsModel(brand=data['brand'], color=data['color'], doors=data['doors']) #khởi tạo đối tượng model với các tham số truyền vào được lấy từ request gửi lên
            db.session.add(new_car) #mở session và thêm mới dữ liệu vào db bằng phương thức add
            db.session.commit() #commit vào db
            return jsonify(data) #trả về dữ liệu dạng json
        else:
            return jsonify(error= "The request payload is not in JSON format") #trả về thông báo lỗi với dữ liệu ko phải dưới dạng json

    elif request.method == 'GET':
        cars = CarsModel.query.all()#truy vấn tất cả dữ liệu trong db
        results = [
            {   "id" : car.id,
                "name": car.brand,
                "model": car.color,
                "doors": car.doors
            } for car in cars]

        return jsonify(results)

@app.route('/cars/<car_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_car(car_id):
    car = CarsModel.query.get_or_404(car_id)#trả về trang 404 nếu id không tồn tại

    if request.method == 'GET':
        results = {
            "name": car.brand,
            "model": car.color,
            "doors": car.doors
        }
        return jsonify(results)

    elif request.method == 'PUT':
        data = request.get_json()
        car.brand = data['brand']
        car.color = data['color']
        car.doors = data['doors']
        db.session.add(car)
        db.session.commit()
        return jsonify(data)

    elif request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return jsonify(deleted=car.brand)

if __name__ == '__name__':
 app.run()
