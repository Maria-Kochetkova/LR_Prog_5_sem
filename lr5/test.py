import unittest
from unittest.mock import patch, MagicMock
from main import CurrencyRates

class TestCurrencyRates(unittest.TestCase):

    def setUp(self):
        """Экземпляр класса CurrencyRates для теста."""
        self.currency_rates = CurrencyRates()

    def test_singleton(self):
        """Тест является ли класс CurrencyRates синглтоном."""
        another_instance = CurrencyRates()
        self.assertIs(self.currency_rates, another_instance, "CurrencyRates должен быть синглтоном.")

    @patch('main.requests.get')
    def test_get_rates_success(self, mock_get):
        '''Тест на корректный вывод конкретных валют (Юань, Румынский лей) и несуществующей валюты'''
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = """<ValCurs Date="01.01.2023" name="Foreign Currency Market">
            <Valute ID="R01375">
                <NumCode>156</NumCode>
                <CharCode>CNY</CharCode>
                <Nominal>1</Nominal>
                <Name>Юань</Name>
                <Value>13,4434</Value>
                <Previous>13,4434</Previous>
            </Valute>
            <Valute ID="R01585F">
                <NumCode>946</NumCode>
                <CharCode>RON</CharCode>
                <Nominal>1</Nominal>
                <Name>Румынский лей</Name>
                <Value>21,0451</Value>
                <Previous>21,0451</Previous>
            </Valute>
        </ValCurs>"""
        mock_get.return_value = mock_response

        currency_rates = CurrencyRates()
        rates = currency_rates.get_rates(["R01375", "R01585F", "R9999"])

        expected_rates = [
            {'CNY': ('Юань', ('13', '4434'))},
            {'RON': ('Румынский лей', ('21', '0451'))},
            {'R9999': None}
        ]

        self.assertEqual(rates, expected_rates)

