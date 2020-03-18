from django.contrib.auth.mixins import UserPassesTestMixin


class PrincipalstaffofstaffMixin(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        return user.is_staff or user.groups.filter(name='principal_staff')