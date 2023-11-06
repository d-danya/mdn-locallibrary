from django import test

class YourTestClass(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        print('serUpTestData: Run once to set up non-modified daa for all class methods.')
        pass
    def setUp(self):
        print('setUp: Run once for every test method to serup clean data.')
        pass
    def test_false_is_false(self):
        print('Method: test_false_is_falss.')
        self.assertFalse(False)
    def test_false_is_true(self):
        print('Method: test_false_is_true.')
        self.assertTrue(self)
    def test_one_plus_one_equals_two(self):
        print('Method: test_one_plus_one_equals_two.')
        self.assertEqual(1 + 1, 2)

