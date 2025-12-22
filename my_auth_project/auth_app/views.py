from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .mock_data import users, roles_rules, orders
from .utils import generate_jwt, get_user_from_token, hash_password, check_password

def get_user_by_email(email):
    for u in users:
        if u["email"] == email and u["is_active"]:
            return u
    return None

def get_next_user_id():
    return max(u["id"] for u in users) + 1 if users else 1

# Users
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if data.get("password") != data.get("password2"):
            return Response({"error": "Passwords do not match"}, status=400)
        if get_user_by_email(data.get("email")):
            return Response({"error": "User with this email already exists"}, status=400)
        new_user = {
            "id": get_next_user_id(),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "patronymic": data.get("patronymic"),
            "email": data.get("email"),
            "password": hash_password(data.get("password")),
            "role": "USER",
            "is_active": True
}
        users.append(new_user)
        return Response({"message": "User registered"}, status=201)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = get_user_by_email(email)
        if user and check_password(password, user["password"]):
            token = generate_jwt(user["id"])
            return Response({"token": token})
        return Response({"error": "Invalid credentials"}, status=401)

class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Logout successful (Mock)"})


class UpdateProfileView(APIView):
    def patch(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return Response({"error": "Unauthorized"}, status=401)
        try:
            _, token = auth_header.split()
            user = get_user_from_token(token)
        except:
            return Response({"error": "Invalid Authorization header"}, status=401)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        # Update fields
        for field in ["first_name", "last_name", "patronymic", "password"]:
            if request.data.get(field):
                if field == "password":
                    user["password"] = hash_password(request.data[field])
                else:
                    user[field] = request.data[field]
        return Response({"message": "Profile updated"})


class DeleteAccountView(APIView):
    def delete(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return Response({"error": "Unauthorized"}, status=401)
        try:
            _, token = auth_header.split()
            user = get_user_from_token(token)
        except:
            return Response({"error": "Invalid Authorization header"}, status=401)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        # Soft delete
        user["is_active"] = False
        return Response({"message": "Account deleted"})

# Business objects
class OrdersView(APIView):
    def get(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return Response({"error": "Unauthorized"}, status=401)
        try:
            _, token = auth_header.split()
            user = get_user_from_token(token)
        except:
            return Response({"error": "Invalid Authorization header"}, status=401)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        role_perms = roles_rules.get(user["role"], {})
        if role_perms.get("read_all"):
            return Response({"orders": orders})
        elif role_perms.get("read"):
            own_orders = [o for o in orders if o["owner_id"] == user["id"]]
            return Response({"orders": own_orders})
        else:
            return Response({"error": "Access forbidden"}, status=403)

# Admin API
class RolesRulesView(APIView):
    def get(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return Response({"error": "Unauthorized"}, status=401)
        try:
            _, token = auth_header.split()
            user = get_user_from_token(token)
        except:
            return Response({"error": "Invalid Authorization header"}, status=401)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)
        if user["role"] != "admin":
            return Response({"error": "Access forbidden"}, status=403)

        return Response({"roles_rules": roles_rules})

    def patch(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return Response({"error": "Unauthorized"}, status=401)
        try:
            _, token = auth_header.split()
            user = get_user_from_token(token)
        except:
            return Response({"error": "Invalid Authorization header"}, status=401)
        if not user:
            return Response({"error": "Unauthorized"}, status=401)
        if user["role"] != "admin":
            return Response({"error": "Access forbidden"}, status=403)

        role = request.data.get("role")
        perms = request.data.get("permissions")
        if role in roles_rules and isinstance(perms, dict):
            roles_rules[role].update(perms)
            return Response({"message": "Permissions updated"})
        return Response({"error": "Invalid data"}, status=400)
