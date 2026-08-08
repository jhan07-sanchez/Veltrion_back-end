from django.test import TestCase

from apps.core.exceptions.custom_exceptions import UserRoleAlreadyExistsException
from apps.users.models import Role, User, UserRole
from apps.users.services.user_role_service import UserRoleService


class UserRoleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
            email="test@example.com",
            document_number="123456789",
        )
        self.role = Role.objects.create(
            role_name="admin_role", permissions={"users.view": True}
        )

    def test_create_and_soft_delete(self):
        ur = UserRoleService.create_user_role({"user": self.user, "role": self.role})
        self.assertIsNotNone(ur.id_user_role)
        self.assertIsNone(ur.deleted_at)

        UserRoleService.deactivate_user_role(ur)
        ur.refresh_from_db()
        self.assertIsNotNone(ur.deleted_at)

    def test_restore_on_recreate(self):
        ur = UserRoleService.create_user_role({"user": self.user, "role": self.role})
        UserRoleService.deactivate_user_role(ur)
        ur.refresh_from_db()
        self.assertIsNotNone(ur.deleted_at)

        # Recreating should restore
        ur2 = UserRoleService.create_user_role({"user": self.user, "role": self.role})
        self.assertEqual(ur.id_user_role, ur2.id_user_role)
        self.assertIsNone(ur2.deleted_at)

    def test_unique_constraint(self):
        UserRoleService.create_user_role({"user": self.user, "role": self.role})
        with self.assertRaises(UserRoleAlreadyExistsException):
            UserRoleService.create_user_role({"user": self.user, "role": self.role})

    def test_filter_active_user_roles(self):
        ur1 = UserRoleService.create_user_role({"user": self.user, "role": self.role})

        user2 = User.objects.create_user(
            username="user2", password="123", email="u2@u.com", document_number="222"
        )
        ur2 = UserRoleService.create_user_role({"user": user2, "role": self.role})
        UserRoleService.deactivate_user_role(ur2)

        # Simulating filter ?is_active=true (deleted_at is null)
        active_roles = UserRole.all_objects.filter(deleted_at__isnull=True)
        self.assertIn(ur1, active_roles)
        self.assertNotIn(ur2, active_roles)

        # Simulating filter ?is_active=false (deleted_at is not null)
        inactive_roles = UserRole.all_objects.filter(deleted_at__isnull=False)
        self.assertIn(ur2, inactive_roles)
        self.assertNotIn(ur1, inactive_roles)
