# -*- coding: utf-8 -*-
# Подключаем объект приложения Flask из __init__.py
import functools
from blog import app #,db
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for
from . import dbservice




navlinks = [
    {
        'name': 'Главная',
        'path': '/main'
    },
    {
        'name': 'Дом',
        'path': '/home'
    },
    {
        'name': 'Меню',
        'path': '/menu'
    },
    {
        'name': 'Галерея',
        'path': '/gallery'
    },
    {
        'name': 'Доставка',
        'path': '/delivery'
    },
    {
        'name': 'Контакты',
        'path': '/contacts'
    },
]




# Функция-декоратор для проверки авторизации пользователя
def login_required(route_func):
    @functools.wraps(route_func)
    def decorated_route(*args, **kwargs):
        # Если не установлен параметр сессии user или значение cookie 'AuthToken' не равно логину пользователя
        if not session.get('user') or request.cookies.get('AuthToken') != session.get('user'):
            # перенаправляем на страницу регистрации
            return redirect(url_for('register'))
        return route_func(*args, **kwargs)
    return decorated_route


@app.route('/')
@app.route('/home')
def main():
    return render_template('home.html', title='Главная', navlinks=navlinks)

@app.route('/menu')
def menu():
    return render_template('menu.html', title='Меню', navlinks=navlinks)

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', title='Галерея', navlinks=navlinks)

@app.route('/delivery')
@login_required
def delivery():
    return render_template('delivery.html', title='Доставка', navlinks=navlinks)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакты', navlinks=navlinks)



# Страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если POST-запрос
    if request.method == 'POST':
        # если нажата кнопка "Зарегистрировать", переадресуем на страницу регистрации
        if request.form.get('regBtn') == 'true':
            return redirect(url_for('reg'))
        # иначе запускаем авторизацию по данным формы
        else:
            return dbservice.login_user(request.form)
    else:
        return render_template('login.html', title='Вход', navlinks=navlinks)


# Страница регистрации
@app.route('/reg', methods=['GET', 'POST'])
def register():
    # Если POST-запрос, регистрируем нового пользователя
    if request.method == 'POST':
        return dbservice.register_user(request.form)
    else:
        return render_template('reg.html', title='Регистрация', navlinks=navlinks)



#Получаем все записи ordersform из БД
@app.route('/api/ordersform', methods=['GET'])
def get_contact_req_all():
    response = dbservice.get_contact_req_all()
    return json_response(response)

@app.route('/api/ordersform/<int:id>', methods=['GET'])
# Получаем запись по id
def get_contact_req_by_id(id):
    response = dbservice.get_contact_req_by_id(id)
    return json_response(response)

@app.route('/api/ordersform/author/<string:firstname>', methods=['GET'])
# Получаем запись по имени пользователя
def get_contact_req_by_author(firstname):
    if not firstname:
        # то возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
        # Иначе отправляем json-ответ
    else:
        response = dbservice.get_contact_req_by_author(firstname)
    return json_response(response)






@app.route('/api/ordersform', methods=['POST'])
def create_contact_req():
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в этом объекте нет, например, обязательного поля 'firstname'
    if not request.json or not 'fname':
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе отправляем json-ответ
    else:
        msg = request.json['fname'] + ", ваш запрос получен";
        response = dbservice.create_contact_req(request.json)
        return json_response(response)



@app.route('/api/ordersform/<int:id>', methods=['PUT'])
# Обработка запроса на обновление записи в БД
def update_contact_email_by_id(id):
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    if not request.json:
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе обновляем запись в БД и отправляем json-ответ
    else:
        response = dbservice.update_contact_email_by_id(id, request.json)
        return json_response(response)


@app.route('/api/ordersform/<int:id>', methods=['DELETE'])
# Обработка запроса на удаление записи в БД по id
def delete_contact_req_by_id(id):
    response = dbservice.delete_contact_req_by_id(id)
    return json_response(response)




# Возврат html-страницы с кодом 404 (Не найдено)
@app.route('/notfound')
def not_found_html():
    return render_template('404.html', title='404', err={ 'error': 'Not found', 'code': 404 })

# Формирование json-ответа. Если в метод передается только data (dict-объект), то по-умолчанию устанавливаем код возврата code = 200
# В Flask есть встроенный метод jsonify(dict), который также реализует данный метод (см. пример метода not_found())
def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))

# Пример формирования json-ответа с использованием встроенного метода jsonify()
# Обработка ошибки 404 протокола HTTP (Данные/страница не найдены)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)

# Обработка ошибки 400 протокола HTTP (Неверный запрос)
def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)
