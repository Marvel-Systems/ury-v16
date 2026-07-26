import json
from pathlib import Path
from unittest.mock import patch

from frappe.tests import UnitTestCase

from ury import hooks
from ury.ury.api.button_permission import cancel_check


class TestV16Compatibility(UnitTestCase):
	def test_apps_screen_opens_v16_desk_route(self):
		self.assertEqual(hooks.add_to_apps_screen[0]["route"], "/desk/ury")

	def test_workspace_is_available_to_system_managers(self):
		workspace_path = Path(hooks.__file__).parent / "ury/workspace/ury/ury.json"
		workspace = json.loads(workspace_path.read_text())
		roles = {row["role"] for row in workspace["roles"]}

		self.assertIn("System Manager", roles)

	@patch("ury.ury.api.button_permission.frappe.has_permission", return_value=True)
	def test_cancel_permission_uses_public_permission_api(self, has_permission):
		self.assertTrue(cancel_check())
		has_permission.assert_called_once_with("POS Invoice", "cancel", throw=False)
