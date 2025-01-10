# Кочеткова Мария Павловна ИВТ-2.2. 
## Лабораторная работа 2. Использование API openweathermap.org.  

Написана реализация функции get_weather_data(place, api_key=None), в которой необходимо получить данные о погоде с 
сайта https://openweathermap.org/.

(Файл mykey.py, содержащий API_key, добавлен в .gitignore)

Функция возвращает объект в формате JSON, включающий:

* информацию о названии города (в контексте openweathermap),
* код страны (2 символа),
* широту и долготу, на которой он находится,
* его временной зоне,
* а также о значении температуры (как она ощущается).

Тестирование [программы](https://github.com/Maria-Kochetkova/LR_Prog_5_sem/blob/main/lr2/getweatherdata.py) с городами:

![](picture/picture1.png)

![](picture/picture2.png)

![](picture/picture3.png)

