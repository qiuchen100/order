# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, jsonify, request
from common.models.food.FoodCat import FoodCat
from common.libs.Helper import getCurrentDate
from application import app, db

route_food = Blueprint('food_page', __name__)


@route_food.route('/index')
def index():
    status_mapping = app.config['STATUS_MAPPING']
    return render_template('food/index.html', status_mapping=status_mapping, params=request.values)


@route_food.route('/set')
def set():
    return render_template('food/set.html')


@route_food.route('/info')
def info():
    return render_template('food/info.html')


@route_food.route('/cat')
def cat():
    query = FoodCat.query
    status = request.values.get('status')
    if status and int(status) > -1:
        query = query.filter(FoodCat.status == status)
    food_cat_list = query.order_by(FoodCat.id.desc()).all()
    status_mapping = app.config['STATUS_MAPPING']
    return render_template('food/cat.html', food_cat_list=enumerate(food_cat_list),
                           status_mapping=status_mapping, params=request.values)


@route_food.route('/cat-set', methods=['GET', 'POST'])
def cat_set():
    resp = {'code': 200, 'msg': '修改菜品分类成功！', 'data': {}}
    if request.method == 'GET':
        id = request.args.get('id')
        food_cat = FoodCat.query.filter_by(id=id).first()
        return render_template('food/cat_set.html', food_cat=food_cat)
    req = request.values
    id = req.get('id', 0)
    name = req.get('name')
    weight = req.get('weight')
    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入正确的分类名称！"
        return jsonify(resp)
    if weight is None or int(weight) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的权重，必须为整数且大于等于1！"
        return jsonify(resp)
    food_cat = FoodCat.query.filter_by(id=id).first() or FoodCat()
    food_cat.name = name
    food_cat.weight = weight
    food_cat.updated_time = getCurrentDate()
    if not id:
        food_cat.created_time = getCurrentDate()
        resp['msg'] = '添加新菜品分类成功！'
    db.session.add(food_cat)
    db.session.commit()
    return jsonify(resp)


@route_food.route('/cat-ops', methods=['POST'])
def cat_ops():
    resp = {'code': 200, 'msg': '删除菜品分类成功！', 'data': {}}
    id = request.values.get('id')
    food_cat = FoodCat.query.filter_by(id=id).first()
    if food_cat:
        if food_cat.status == 0:
            food_cat.status = 1
            resp['msg'] = '恢复菜品分类成功！'
        else:
            food_cat.status = 0
            food_cat.updated_time = getCurrentDate()
        db.session.add(food_cat)
        db.session.commit()
        return jsonify(resp)
    resp['code'] = -1
    resp['msg'] = "该菜品分类不存在！"
    return jsonify(resp)