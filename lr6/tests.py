import json
import unittest
from unittest.mock import patch, MagicMock
from main import CurrenciesList, ConcreteDecoratorCSV, ConcreteDecoratorJSON


class TestCurrencyRates(unittest.TestCase):

    def setUp(self):
        """Экземпляр класса CurrencyRates для теста."""
        self.currency_rates = CurrenciesList()

    def test_singleton(self):
        """Тест является ли класс CurrencyRates синглтоном."""
        another_instance = CurrenciesList()
        self.assertIs(self.currency_rates, another_instance, "CurrencyRates должен быть синглтоном.")

    @patch('main.requests.get')
    def test_get_rates_success(self, mock_get):
        '''Тест на корректный вывод конкретных валют (Юань, Румынский лей)'''
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

        currency_rates = CurrenciesList()
        rates = currency_rates.get_rates(["R01375", "R01585F"])

        expected_rates = [
            {'CNY': ('Юань', ('13', '4434'))},
            {'RON': ('Румынский лей', ('21', '0451'))},
        ]

        self.assertEqual(rates, expected_rates)
        self.assertEqual(len(rates), 2, "Должно вернуть два курса валюты.")
        self.assertIn("CNY", rates[0], "Курс для CNY должен быть в списке.")
        self.assertIn("RON", rates[1], "Курс для RON должен быть в списке.")

    @patch('requests.get')
    def test_get_rates_json(self, mock_get):
        """Тест получения курсов валют в формате JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = """
            <ValCurs Date="11.01.2025" name="Foreign Currency Market">
                <Valute ID="R01235">
                    <NumCode>036</NumCode>
                    <CharCode>USD</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Доллар США</Name>
                    <Value>73,50</Value>
                    <Previous>74,00</Previous>
                </Valute>
            </ValCurs>
            """
        mock_get.return_value = mock_response

        currencies_list = CurrenciesList()
        json_decorator = ConcreteDecoratorJSON(currencies_list)
        json_rates = json_decorator.get_rates(["R01235"])

        expected_json = json.dumps([{'USD': ('Доллар США', ('73', '50'))}], ensure_ascii=False, indent=5)
        self.assertEqual(json_rates, expected_json, "Данные должны соответствовать ожидаемому формату JSON.")


class TestConcreteDecoratorCSV(unittest.TestCase):

    @patch('requests.get')
    def test_get_rates_csv(self, mock_get):
        """Тест получения курсов валют в формате CSV."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = """
            <ValCurs Date="11.01.2025" name="Foreign Currency Market">
                <Valute ID="R01235">
                    <NumCode>036</NumCode>
                    <CharCode>USD</CharCode>
                    <Nominal>1</Nominal>
                    <Name>Доллар США</Name>
                    <Value>73,50</Value>
                    <Previous>74,00</Previous>
                </Valute>
            </ValCurs>
            """
        mock_get.return_value = mock_response

        currencies_list = CurrenciesList()
        csv_decorator = ConcreteDecoratorCSV(currencies_list)
        csv_rates = csv_decorator.get_rates(["R01235"])

        expected_csv = "Currency Code,Currency Name,Whole,Fraction,Nominal\r\nUSD,Доллар США,73,50,\r\n"
        self.assertEqual(csv_rates, expected_csv, "Данные должны соответствовать ожидаемому формату CSV.")