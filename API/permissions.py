from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
	message = 'Для этого действия Вы должны быть влдельцем'
	my_safe_methods = ['PUT', 'GET']

	def has_permission(self, request, view):
		return request.method in self.my_safe_methods

	def has_object_permission(self, request, view, obj):
		if request.method in self.my_safe_methods:
			return True
		return obj.user == request.user


class AdminRealtor(BasePermission):
	def has_permission(self, request, view):
		return request.user.user_type == 'realtor_admin'


class SimpleRealtor(BasePermission):
	def has_permission(self, request, view):
		return request.user.user_type == 'realtor' or request.user.user_type == 'realtor_admin'
