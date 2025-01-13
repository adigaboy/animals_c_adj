import unittest
from unittest.mock import patch

from main import main
from tests.mock import aiohttp_clientsession_mock, mock_download_images


class CollateralAdjectivesTest(unittest.IsolatedAsyncioTestCase):
    @patch('main.download_animal_pic', side_effect=mock_download_images)
    @patch('aiohttp.ClientSession', return_value=aiohttp_clientsession_mock())
    async def test_bat_in_two_c_adjectives(self, _, __):
        collateral_adjectives_animals = await main()
        animal = 'Bat'
        c_adjective = 'noctillionine'
        second_c_adjective = 'pteropine'
        self.assertIn(animal, collateral_adjectives_animals[c_adjective])
        self.assertIn(animal, collateral_adjectives_animals[second_c_adjective])

    @patch('main.download_animal_pic', side_effect=mock_download_images)
    @patch('aiohttp.ClientSession', return_value=aiohttp_clientsession_mock())
    async def test_simian(self, _, __):
        collateral_adjectives_animals = await main()
        c_adjective = 'simian'
        self.assertIn('Gorilla', collateral_adjectives_animals[c_adjective])
        self.assertIn('Human', collateral_adjectives_animals[c_adjective])
        self.assertIn('Ape', collateral_adjectives_animals[c_adjective])

    @patch('main.download_animal_pic', side_effect=mock_download_images)
    @patch('aiohttp.ClientSession', return_value=aiohttp_clientsession_mock())
    async def test_ursine(self, _, __):
        collateral_adjectives_animals = await main()
        c_adjective = 'ursine'
        self.assertIn(c_adjective, collateral_adjectives_animals)
        self.assertEqual(len(collateral_adjectives_animals[c_adjective]), 2)
