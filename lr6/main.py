from xml.etree import ElementTree as ET
import requests
import json
import csv
import io

class SingletonMeta(type):
    """Метакласс для реализации шаблом Одиночка (Singleton) для классов,использующих его как метакласс."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CurrenciesList(metaclass=SingletonMeta):
    """Базовый класс для получения курсов валют."""

    def __init__(self):
        self.url = "http://www.cbr.ru/scripts/XML_daily.asp"


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


class Decorator:
    """Абстрактный декоратор для класса CurrenciesList."""

    def __init__(self, currencies_list):
        self._currencies_list = currencies_list

    def get_rates(self, codes_list):
        return self._currencies_list.get_rates(codes_list)


class ConcreteDecoratorJSON(Decorator):
    """Декоратор для преобразования данных в формат JSON."""

    def get_rates(self, codes_list):
        rates = self._currencies_list.get_rates(codes_list)
        return json.dumps(rates, ensure_ascii=False, indent=5)


class ConcreteDecoratorCSV(Decorator):
    """Декоратор для преобразования данных в формат CSV."""

    def get_rates(self, codes_list):
        rates = self._currencies_list.get_rates(codes_list)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Currency Code", "Currency Name", "Whole", "Fraction", "Nominal"])

        for rate in rates:
            for code, details in rate.items():
                if details is None:
                    writer.writerow([code, "Не найдено", "", "", ""])
                else:
                    name, (whole, fraction), *nominal = details
                    nominal_value = nominal[0] if nominal else ""
                    writer.writerow([code, name, whole, fraction, nominal_value])

        return output.getvalue()


if __name__ == '__main__':
    # Использование базовой версии
    currency_list = CurrenciesList()
    rates = currency_list.get_rates(["R01235", "R01535"])
    print("Базовая версия:")
    print(rates)

    # Использование JSON декоратора
    json_decorator = ConcreteDecoratorJSON(currency_list)
    json_rates = json_decorator.get_rates(["R01235", "R01535"])
    print("\nДанные в формате JSON:")
    print(json_rates)

    # Использование CSV декоратора
    csv_decorator = ConcreteDecoratorCSV(currency_list)
    csv_rates = csv_decorator.get_rates(["R01235", "R01535"])
    print("\nДанные в формате CSV:")
    print(csv_rates)
