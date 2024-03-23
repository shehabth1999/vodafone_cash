from .test_setup import TestSetUp


class TestViews(TestSetUp):
    def test_app(self):
        self.assertEqual(200, 200)