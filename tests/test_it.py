import unittest
from unittest.mock import patch

from main import main
from tests.mock import mock_page_response


class CollateralAdjectivesTest(unittest.IsolatedAsyncioTestCase):
    @patch('wikipedia.page', return_value=mock_page_response())
    def setUp(self, _):
        super().setUp()
        self.collateral_adjectives_animals = main()

    async def test_bat_in_two_c_adjectives(self):
        animal = 'Bat'
        c_adjective = 'noctillionine'
        second_c_adjective = 'pteropine'
        self.assertIn(animal, self.collateral_adjectives_animals[c_adjective])
        self.assertIn(animal, self.collateral_adjectives_animals[second_c_adjective])

    async def test_simian(self):
        c_adjective = 'simian'
        self.assertIn('Gorilla', self.collateral_adjectives_animals[c_adjective])
        self.assertIn('Human', self.collateral_adjectives_animals[c_adjective])
        self.assertIn('Ape', self.collateral_adjectives_animals[c_adjective])

    async def test_ursine(self):
        c_adjective = 'ursine'
        self.assertIn(c_adjective, self.collateral_adjectives_animals)
        self.assertEqual(len(self.collateral_adjectives_animals[c_adjective]), 2)
