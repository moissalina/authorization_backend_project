# Пользователи
users = [
    {"id": 1, "first_name": "Admin", "last_name": "User", "patronymic": "", 
     "email": "admin@example.com", "password": "admin123", "role": "admin", "is_active": True},
    {"id": 2, "first_name": "Manager", "last_name": "User", "patronymic": "", 
     "email": "manager@example.com", "password": "manager123", "role": "manager", "is_active": True},
    {"id": 3, "first_name": "John", "last_name": "Doe", "patronymic": "Jr.", 
     "email": "user@example.com", "password": "user123", "role": "user", "is_active": True},
]

# Роли и права
roles_rules = {
    "ADMIN": {
        "read": True,
        "read_all": True,
        "create": True,
        "update": True,
        "delete": True
    },
    "MANAGER": {
        "read": True,
        "read_all": True,
        "create": True,
        "update": True,
        "delete": False
    },
    "USER": {
        "read": True,
        "read_all": False,
        "create": False,
        "update": False,
        "delete": False
    },
    "GUEST": {
        "read": False,
        "read_all": False,
        "create": False,
        "update": False,
        "delete": False
    }
}


# Объекты бизнес-приложения
orders = [
    {"id": 1, "owner_id": 3, "item": "Laptop"},
    {"id": 2, "owner_id": 3, "item": "Phone"},
    {"id": 3, "owner_id": 2, "item": "Monitor"},
]
