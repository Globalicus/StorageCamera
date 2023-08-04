from flask import Flask, request, jsonify
from transitions import Machine
import threading
import time

app = Flask(__name__)


# Класс для представления системы хранения
class StorageCamera:
    states = ['locked', 'unlocked']

    def __init__(self):
        self.state = None
        self.machine = Machine(model=self, states=StorageCamera.states, initial='locked')
        self.machine.add_transition(trigger='unlock', source='locked', dest='unlocked', after='open_door')
        self.machine.add_transition(trigger='lock', source='unlocked', dest='locked', before='close_door')
        self.is_door_open = False

    def open_door(self):
        print("Door is now open")
        self.is_door_open = True
        threading.Thread(target=self._auto_close_door).start()

    def _monitor_door(self):
        time.sleep(5)  # Предполагаем, что дверь закроется через 5 секунд
        if self.is_door_open:
            print("Warning: Door was not closed")
            self.is_door_open = False

    def close_door(self):
        print("Door is now closed")
        self.is_door_open = False

    def reset_state(self):
        self.machine.set_state('locked')
        self.is_door_open = False

    def is_door_unlocked(self):
        return self.is_door_open

    def _auto_close_door(self):
        if self.is_door_open:
            print("Automatic closing door...")
            self.close_door()


# Создаем экземпляр системы хранения
camera = StorageCamera()

# Правильный пароль для проверки
correct_password = "123"


# Разрешаем запросы с других доменов (CORS)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE"
    return response


# Роут для открытия двери
@app.route('/unlock', methods=['POST'])
def unlock_door():
    # Получаем пароль из запроса
    data = request.get_json()
    password = data.get('password')

    if camera.state == 'locked':
        if password == correct_password:
            camera.unlock()
            return jsonify({'message': 'Door is unlocked'})
        else:
            return jsonify({'message': 'Error: Incorrect password'})
    else:
        return jsonify({'message': 'Error: Door is already unlocked'})


# Роут для закрытия двери
@app.route('/lock', methods=['POST'])
def lock_door():
    if camera.state == 'unlocked':
        camera.lock()
        return jsonify({'message': 'Door is locked'})
    else:
        return jsonify({'message': 'Error: Door is already locked'})


# Роут для получения состояния двери
@app.route('/state', methods=['GET'])
def get_door_state():
    return jsonify({'state': camera.state})


if __name__ == '__main__':
    app.run(debug=False)
