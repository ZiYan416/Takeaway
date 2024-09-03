# import caching as caching
from flask import Flask, jsonify, request
from sqlalchemy import text
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
import auth

import json
import random
import datetime
from redis import StrictRedis

# 创建redis对象
redis_store = StrictRedis(host=BaseConfig.REDIS_HOST, port=BaseConfig.REDIS_PORT, decode_responses=True)

# 跨域
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)

# 初始化密码加密哈希函数
ph = PasswordHasher()

# 添加配置数据库
app.config.from_object(BaseConfig)
# 初始化拓展,app到数据库的ORM映射
db = SQLAlchemy(app)

# 检查数据库连接是否成功
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())


# 路由定义

# 用户登录DONE
@app.route("/api/user/login", methods=["POST"])
@cross_origin()
def user_login():
    print(request.json)
    userortel = request.json.get("userortel").strip()
    password = request.json.get("password").strip()

    # 查找用户信息
    sql_check_user = text('select * from user where telephone = :telephone')
    data = db.session.execute(sql_check_user, {'telephone': userortel}).first()
    print(data)

    if data:
        user = {'id': data[0], 'username': data[1], 'password': data[2], 'telephone': data[3]}
        try:
            # 验证密码
            ph.verify(user['password'], password)
            # 生成token
            token = auth.encode_func(user)
            print(token)
            return jsonify({"code": 200, "msg": "登录成功", "token": token, "role": data[4]})
        except VerifyMismatchError:
            return jsonify({"code": 1000, "msg": "用户名或密码错误"})
    else:
        return jsonify({"code": 1000, "msg": "用户名或密码错误"})


# 用户注册DONE
@app.route("/api/user/register/test", methods=["POST"])
@cross_origin()
def register():
    rq = request.json
    # 获取用户名、密码和手机号
    username = rq.get("username").strip()
    password = rq.get("password").strip()
    telephone = rq.get("telephone").strip()

    # 检查用户是否已经存在
    sql_check_user = text('select * from user where telephone = :telephone')
    data = db.session.execute(sql_check_user, {'telephone': telephone}).fetchall()
    if not data:
        try:
            # 加密密码
            hashed_password = ph.hash(password)

            # 插入新用户信息到数据库
            sql_insert_user = text(
                'insert into user(username, password, telephone, role) values(:username, :password, :telephone, 0)')
            db.session.execute(sql_insert_user, {'username': username, 'password': hashed_password, 'telephone': telephone})

            # 获取新插入用户的ID
            sql_get_user_id = text('select id from user where telephone = :telephone')
            user_id = db.session.execute(sql_get_user_id, {'telephone': telephone}).fetchone()[0]

            # 插入新用户信息到 user_msg 表
            sql_insert_user_msg = text(
                'insert into user_msg(id, real_name, sex, age, mail, phone, user_name) values(:id, NULL, NULL, NULL, '
                'NULL, :telephone, :username)')
            db.session.execute(sql_insert_user_msg, {'id': user_id, 'telephone': telephone, 'username': username})

            db.session.commit()
            return jsonify({"status": 200, "msg": "注册成功"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": 500, "msg": f"注册失败: {str(e)}"})
    else:
        return jsonify({"status": 1000, "msg": "该用户已存在"})


# 获取店铺列表
@app.route("/api/user/shop", methods=["GET"])
@cross_origin()
def user_get_shop():
    data = db.session.execute(text('select * from fastfood_shop')).fetchall()

    Data = []
    for i in range(len(data)):
        dic = dict(shop_name=data[i][0], price=data[i][1], sale=data[i][2])
        Data.append(dic)
    print(Data)
    # return jsonify({"status":"200", "tabledata": Data})
    return jsonify(status=200, tabledata=Data)


# 下订单
@app.route("/api/user/addorder", methods=["POST"])
@cross_origin()
def user_addorder():
    rq = request.json
    # 获取各个参数
    shopname = rq.get("shop_name")
    ordermoney = rq.get("order_money")
    quantity = rq.get('quantity', 1)
    consphone = get_token_phone(request.headers.get('token'))
    consname = rq.get("cons_name")
    consaddre = rq.get("cons_addre")
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # print(shop_name, order_money, cons_phone, cons_name, cons_addre)
    sql_insert_oorder = text('''
        INSERT INTO oorder (shop_name, order_money, cons_phone, cons_name, cons_addre, create_time)
        VALUES (:shop_name, :order_money, :cons_phone, :cons_name, :cons_addre, :create_time)
    ''')
    for _ in range(quantity):
        db.session.execute(sql_insert_oorder, {
            'shop_name': shopname,
            'order_money': ordermoney,
            'cons_phone': consphone,
            'cons_name': consname,
            'cons_addre': consaddre,
            'create_time': create_time
        })
    db.session.commit()
    # db.session.execute('insert into fastfood_shop(shop_name, price, m_sale_v) values("解耦哎",10,100)')
    # db.session.commit()
    return jsonify(status=200, msg="成功下单")


def get_token_phone(token):
    data = auth.decode_func(token)
    phone = data['telephone']
    return (phone)


# 用户界面未送达订单
@app.route("/api/user/unsend", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_unsend():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        print(phone)
        data = db.session.execute(text('select * from oorder where checked=0 and cons_phone="%s"' % phone)).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], price=data[i][2],
                       cons_name=data[i][4], cons_addre=data[i][5], create_time=data[i][7])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)

    if request.method == 'POST':
        rq = request.json
        order_ids = rq.get("order_ids")
        cons_name = rq.get("cons_name")
        cons_addre = rq.get("cons_addre")
        for order_id in order_ids:
            db.session.execute(
                text('update oorder set cons_name=:cons_name, cons_addre=:cons_addre where order_id=:order_id'),
                {'cons_name': cons_name, 'cons_addre': cons_addre, 'order_id': order_id}
            )
        db.session.commit()
        return jsonify(status=200, msg="订单信息修改成功")

    if request.method == 'DELETE':
        delete_ids = request.json.get("delete_ids")
        for order_id in delete_ids:
            db.session.execute(text('delete from oorder where order_id=:order_id'), {'order_id': order_id})
        db.session.commit()
        return jsonify(status=200, msg="订单删除成功")


@app.route("/api/user/sending", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_sending():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))

        data = db.session.execute(text('select * from sending_order where cons_phone="%s"' % phone)).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2],
                       cons_phone=data[i][3],
                       cons_name=data[i][4], cons_addre=data[i][5], disp_id=data[i][6], deliver_time=data[i][7],
                       disp_phone=data[i][8])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


@app.route("/api/user/sended", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_sended():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute(text('select * from sended_order where cons_phone="%s"' % phone)).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2],
                       cons_phone=data[i][3],
                       cons_name=data[i][4], cons_addre=data[i][5], disp_id=data[i][6], deliver_time=data[i][7],
                       disp_phone=data[i][8])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


# 获取个人信息DONE
@app.route("/api/user/usermsg", methods=["POST", "GET"])
@cross_origin()
def usermsg():
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        data = db.session.execute(text('select * from user_msg where phone="%s"' % phone)).fetchall()
        Data = dict(real_name=data[0][1], sex=data[0][2], age=data[0][3], mail=data[0][4], phone=data[0][5],
                    user_name=data[0][6])

        return jsonify(status=200, data=Data)


# 修改个人信息DONE
@app.route("/api/user/updateUserInfo", methods=["POST"])
@cross_origin()
def user_msg_chg():
    if request.method == 'POST':
        age = request.json.get('age')
        mail = request.json.get('mail')
        phone = request.json.get('phone')
        real_name = request.json.get('real_name')
        sex = request.json.get('sex')
        user_name = request.json.get('user_name')

        # 使用参数绑定来防止 SQL 注入
        sql_update_user_msg = text('''
            UPDATE user_msg 
            SET age = :age, 
                mail = :mail, 
                real_name = :real_name, 
                sex = :sex, 
                user_name = :user_name 
            WHERE phone = :phone
        ''')

        db.session.execute(sql_update_user_msg, {
            'age': age,
            'mail': mail,
            'real_name': real_name,
            'sex': sex,
            'user_name': user_name,
            'phone': phone
        })
        db.session.commit()
        return jsonify(status=200, msg="修改成功")


# 修改密码DONE
@app.route("/api/user/pwd_chg", methods=["POST"])
@cross_origin()
def user_pwd_chg():
    if request.method == 'POST':
        new_pwd = request.json.get('new_pwd')
        old_pwd = request.json.get('old_pwd')
        phone = get_token_phone(request.headers.get('token'))

        # 查找用户信息
        sql_check_user = text('select * from user where telephone = :telephone')
        data = db.session.execute(sql_check_user, {'telephone': phone}).first()

        if not data:
            return jsonify(status=1000, msg="用户不存在")

        user = {'id': data[0], 'username': data[1], 'password': data[2], 'telephone': data[3]}

        try:
            # 验证旧密码
            ph.verify(user['password'], old_pwd)
        except VerifyMismatchError:
            return jsonify(status=1000, msg="原始密码错误")

        # 加密新密码
        hashed_new_pwd = ph.hash(new_pwd)

        # 更新密码
        try:
            db.session.execute(text('update user set password = :password where telephone = :telephone'),
                               {'password': hashed_new_pwd, 'telephone': phone})
            db.session.commit()
            return jsonify(status=200, msg="修改成功")
        except Exception as e:
            db.session.rollback()
            return jsonify(status=500, msg=f"修改失败: {str(e)}")


@app.route("/api/manager/shop", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_shop():
    # 获取店铺信息
    if request.method == 'GET':
        data = db.session.execute(text('select * from fastfood_shop')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(shop_name=data[i][0], price=data[i][1], sale=data[i][2])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    if request.method == 'POST' and request.json.get('action') == "add":
        rq = request.json
        shop_name = rq.get('shop_name')
        price = rq.get('price')
        m_sale_v = rq.get('m_sale_v')
        exist = db.session.execute(text('select * from fastfood_shop where shop_name="%s"' % shop_name)).fetchall()
        if not exist:
            db.session.execute(text('insert fastfood_shop(shop_name,price,m_sale_v) value("%s",%d,%d)' % (
                shop_name, int(price), int(m_sale_v))))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该店铺已存在")

    if request.method == 'POST' and request.json.get('action') == "change":
        rq = request.json
        shop_name = rq.get('shop_name')
        price = rq.get('price')
        m_sale_v = rq.get('m_sale_v')
        db.session.execute(text('update fastfood_shop set price="%d", m_sale_v="%d" where shop_name="%s" ' % (
            int(price), int(m_sale_v), shop_name)))
        db.session.commit()
        return jsonify(status=200, msg="修改成功")
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        db.session.execute(text('delete from fastfood_shop where shop_name="%s"' % want_delete))
        db.session.commit()
        return jsonify(status=200, msg="删除成功")


# @app.route("/api/manager/server", methods=["POST", "GET", "DELETE"])
# @cross_origin()
# def manager_server():
#     if request.method == 'GET':
#         data = db.session.execute(text('select * from server')).fetchall()
#         Data = []
#         for i in range(len(data)):
#             dic = dict(service_id=data[i][0], service_name=data[i][1], fastfood_shop_name=data[i][2])
#             Data.append(dic)
#         shop_range = db.session.execute(text('select shop_name from fastfood_shop')).fetchall()
#         Shop = []
#         for i in range(len(shop_range)):
#             dic = dict(shop_name=shop_range[i][0])
#             Shop.append(dic)
#         print(Shop)
#         return jsonify(status=200, tabledata=Data, shop_range=Shop)
#     if request.method == 'POST':
#         rq = request.json
#         service_id = rq.get('service_id')
#         service_name = rq.get('service_name')
#         fastfood_shop_name = rq.get('fastfood_shop_name')
#         exist = db.session.execute(text('select * from server where service_id="%s"' % service_id)).fetchall()
#         if not exist:
#             db.session.execute(
#                 text('insert server(service_id,service_name,fastfood_shop_name) value("%s","%s","%s")' % (
#                     service_id, service_name, fastfood_shop_name)))
#             db.session.commit()
#             return jsonify(status=200, msg="添加成功")
#         else:
#             return jsonify(status=1000, msg="该编号已存在")
#     if request.method == 'DELETE':
#         want_delete = request.json.get('want_delete')
#         db.session.execute(text('delete from server where service_id="%s"' % want_delete))
#         db.session.commit()
#         return jsonify(status=200, msg="解雇成功")


@app.route("/api/manager/dispatcher", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_dispatcher():
    if request.method == 'GET':
        data = db.session.execute(text('select * from dispatcher')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(dispatcher_id=data[i][0], dispatcher_name=data[i][1], dispatcher_phone=data[i][2])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    if request.method == 'POST':
        rq = request.json
        dispatcher_id = rq.get('dispatcher_id')
        dispatcher_name = rq.get('dispatcher_name')
        dispatcher_phone = rq.get('dispatcher_phone')
        exist = db.session.execute(text('select * from dispatcher where dispatcher_id="%s"' % dispatcher_id)).fetchall()
        if not exist:
            db.session.execute(
                text('insert dispatcher(dispatcher_id,dispatcher_name,dispatcher_phone) value("%s","%s","%s")' % (
                    dispatcher_id, dispatcher_name, dispatcher_phone)))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该编号已存在")
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        db.session.execute(text('delete from dispatcher where dispatcher_id="%s"' % want_delete))
        db.session.commit()
        return jsonify(status=200, msg="解雇成功")


@app.route("/api/manager/wuliu", methods=["GET"])
@cross_origin()
def manager_wuliu():
    ended = request.args.get('id')
    if ended == '0':
        data = db.session.execute(text('select * from wuliu where ended=0')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], cons_phone=data[i][1], disp_id=data[i][2], deliver_time=data[i][3])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    else:
        data = db.session.execute(text('select * from wuliu where ended=1')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], cons_phone=data[i][1], disp_id=data[i][2], deliver_time=data[i][3])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


# 管理员未发货订单
@app.route("/api/manager/unsend", methods=["GET", "POST"])
@cross_origin()
def manager_unsend():
    if request.method == 'GET':
        data = db.session.execute(text('select * from oorder where checked=0')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], price=data[i][2], create_time=data[i][7],
                       cons_phone=data[i][3],
                       cons_name=data[i][4], cons_addre=data[i][5])
            Data.append(dic)

        disp_range = db.session.execute(text('select * from dispatcher')).fetchall()  # 获取所有的送货员就id，供选择
        Disp_range = []
        for i in range(len(disp_range)):
            dic = dict(disp_id=disp_range[i][0])
            Disp_range.append(dic)
        return jsonify(status=200, tabledata=Data, disp_range=Disp_range)

    if request.method == 'POST':
        rq = request.json
        order_ids = rq.get('order_ids')  # 这里改为 order_ids 列表
        disp_id = rq.get('dispatcher_id')
        deliver_time = rq.get('deliver_time')

        for order_id in order_ids:
            cons_phone = db.session.execute(
                text('select cons_phone from oorder where order_id=:order_id').params(order_id=order_id)).first()
            db.session.execute(
                text(
                    'insert into wuliu(order_id, cons_phone, disp_id, deliver_time) values(:order_id, :cons_phone, :disp_id, :deliver_time)')
                .params(order_id=order_id, cons_phone=cons_phone[0], disp_id=disp_id, deliver_time=deliver_time)
            )

        db.session.commit()
        return jsonify(status=200, msg="成功派发")


# 管理员已发货订单
@app.route("/api/manager/sending", methods=["GET"])
@cross_origin()
def manager_sending():
    if request.method == 'GET':
        data = db.session.execute(text('select * from sending_order')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2],
                       cons_phone=data[i][3],
                       cons_name=data[i][4], cons_addre=data[i][5], disp_id=data[i][6], deliver_time=data[i][7])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


@app.route("/api/manager/sended", methods=["GET", "DELETE"])
@cross_origin()
def manager_sended():
    if request.method == 'GET':
        data = db.session.execute(text('select * from sended_order')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2],
                       cons_phone=data[i][3],
                       cons_name=data[i][4], cons_addre=data[i][5], disp_id=data[i][6], deliver_time=data[i][7])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    if request.method == 'DELETE':
        order_id = request.json.get("order_id")
        db.session.execute(text('delete from sended_order where order_id=:order_id'), {'order_id': int(order_id)})
        db.session.commit()
        return jsonify(status=200, msg="删除成功")


# 管理员物流界面确认收货
@app.route("/api/user/confirm-receipt", methods=["POST"])
@cross_origin()
def confirm_receipt():
    rq = request.json
    order_ids = rq.get('order_ids')
    actual_deliver_time = rq.get('actual_deliver_time')

    if not order_ids:
        return jsonify(status=400, msg="订单ID缺失")
    if not actual_deliver_time:
        return jsonify(status=400, msg="实际送餐时间缺失")

    try:
        for order_id in order_ids:
            # 检查订单是否存在
            exist = db.session.execute(text('select * from oorder where order_id=:order_id'), {'order_id': order_id}).fetchall()
            if not exist:
                return jsonify(status=404, msg=f"订单 {order_id} 不存在")

            # 更新订单的checked字段为2
            db.session.execute(text('update oorder set checked=2 where order_id=:order_id'), {'order_id': order_id})
            # 更新wuliu表的ended字段为1和deliver_time为实际送餐时间（分钟）
            db.session.execute(text('update wuliu set ended=1, deliver_time=:actual_deliver_time where order_id=:order_id'),
                               {'order_id': order_id, 'actual_deliver_time': actual_deliver_time})

        db.session.commit()
        return jsonify(status=200, msg="确认收货成功")
    except Exception as e:
        db.session.rollback()
        return jsonify(status=500, msg="数据库错误", error=str(e))



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='5000')
    # 开启了debug模式
