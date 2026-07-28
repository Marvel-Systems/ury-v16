import json
from pathlib import Path
from unittest.mock import patch

from frappe.tests import UnitTestCase

from ury import hooks
from ury.ury.api.button_permission import cancel_check
from ury.ury.hooks.ury_pos_invoice import calculate_and_set_times


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

	@patch("ury.ury.hooks.ury_pos_invoice.now_datetime")
	def test_invoice_times_accept_string_creation(self, now_datetime):
		now_datetime.return_value = frappe.utils.get_datetime("2026-07-27 12:01:02")
		doc = frappe._dict(creation="2026-07-27 12:00:00")

		calculate_and_set_times(doc, None)

		self.assertEqual(doc.total_spend_time, "00:01:02")
		self.assertEqual(
			doc.arrived_time,
			frappe.utils.get_datetime("2026-07-27 12:00:00"),
		)
