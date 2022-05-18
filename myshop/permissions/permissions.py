from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

class AuthenticatedOnlyPermission(PermissionDenied):
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('myshop:index')
        return super(AuthenticatedOnlyPermission, self).dispatch(request, *args, **kwargs)

class DefaultUserOnlyPermission(PermissionDenied):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_salesman:
            return redirect('myshop:index')
        return super(DefaultUserOnlyPermission, self).dispatch(request, *args, **kwargs)

class SalesmanOnlyPermission(PermissionDenied):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_salesman:
            return redirect('myshop:index')
        return super(SalesmanOnlyPermission, self).dispatch(request, *args, **kwargs)

