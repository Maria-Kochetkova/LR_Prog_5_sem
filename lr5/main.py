from functools import wraps
import requests
from xml.etree import ElementTree as ET
import time
import matplotlib.pyplot as plt

class SingletonMeta(type):
    """Метакласс для реализации шаблом Одиночка (Singleton) для классов,использующих его как метакласс."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def rate_limiter(limit: int, period: int):
    """Декоратор для ограничения частоты вызова функции."""
    def decorator(func):
        last_called = [0.0]

        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < period:
                if last_called[0] + period - elapsed < 0:
                    last_called[0] = time.time()
                else:
                    raise Exception(f"Слишком частый вызов функции. Пожалуйста, подождите.")
            else:
                last_called[0] = time.time()
            return func(*args, **kwargs)

        return wrapper

    return decorator

class CurrencyRates(metaclass=SingletonMeta):
    """Класс для получения и визуализации курсов валют из ЦБ РФ."""

    def __init__(self):
        self.url = "http://www.cbr.ru/scripts/XML_daily.asp"
        self.rates = []
        self.last_request_time = 0

    @rate_limiter(1, 1)
    def get_rates(self, codes_list):
        """Получает курсы валют для указанного списка идентификаторов валют."""

        response = requests.get(self.url)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            self.rates = []

            found_codes = set()

            for item in root.findall('Valute'):
                valute_id = item.get('ID')
                valute = {}
                if valute_id in codes_list:
                    valute_code = item.find('CharCode').text
                    valute_name = item.find('Name').text
                    value = item.find('Value').text.replace(',', '.')
                    valute_nominal = int(item.find('Nominal').text)
                    whole, fractions = value.split('.')
                    if valute_nominal != 1:
                        valute[valute_code] = (valute_name, (whole, fractions), valute_nominal)
                    else:
                        valute[valute_code] = (valute_name, (whole, fractions))
                    self.rates.append(valute)
                    found_codes.add(valute_id)

            for code in codes_list:
                if code not in found_codes:
                    self.rates.append({code: None})

            return self.rates
        else:
            raise Exception("Ошибка при получении данных.")

    def visual_rates(self):
        """Визуализирует полученные курсы валют в виде столбчатой диаграммы."""

        plt.figure(figsize=(10, 6))

        valid_rates = [rate for rate in self.rates if rate[list(rate.keys())[0]] is not None]
        list_rates = [list(rate.keys())[0] for rate in valid_rates]
        list_value = [float(rate[list(rate.keys())[0]][1][0]) for rate in valid_rates]

        plt.bar(list_rates, list_value, color='burlywood')
        plt.title('Курс валют относительно рубля')
        plt.ylabel('RUB')
        plt.grid(axis='y')
        plt.savefig('currencies.jpg')
        plt.close()

if __name__ == '__main__':
    currency_rates = CurrencyRates()
    result = currency_rates.get_rates(["R01235", "R01535", "R01775", "R01720"])
    print(result)
    currency_rates.visual_rates()

