from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from .models import Book

class PermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.editor_group = Group.objects.create(name='Editors')
        self.editor_group.permissions.add(
            Permission.objects.get(codename='can_create_book'),
            Permission.objects.get(codename='can_edit_book')
        )
        self.user.groups.add(self.editor_group)

    def test_editor_permissions(self):
        self.assertTrue(self.user.has_perm('bookshelf.can_create_book'))
        self.assertTrue(self.user.has_perm('bookshelf.can_edit_book'))
        self.assertFalse(self.user.has_perm('bookshelf.can_delete_book'))