from fields.tests.helpers import setup_cadastral_info, setup_field


class WeatherTestMixin:
    def setUp(self):
        super().setUp()

        self.cad_info = setup_cadastral_info(self.user)
        self.field = setup_field(self.cad_info)
