import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()  # ← Создаём экземпляр Migrate глобально

def create_app():
    app = Flask(__name__, 
                template_folder='../templates')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True  # Для отладки
    
    # Инициализируем расширения
    db.init_app(app)
    migrate.init_app(app, db)  # ← Подключаем миграции к приложению
    
    # 🔥 Импорт моделей ДО любых операций с БД
    from app import models
    
    # Регистрируем блупринты
    from app.routes import main
    app.register_blueprint(main)
    
    # Логирование для отладки запуска
    with app.app_context():
        app.logger.info(f"Application started. DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    return app