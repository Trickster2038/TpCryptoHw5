# Crypto - Homework 5

В данном репозитории представлена реализация домашнего задания 5 по курсу криптографии в технопарке mail.ru -  эмулятор криптографической системы брелок-машина

## Состав документации
- особенности программы
- состав программы
- установка и запуск
- включение логирования
- тестирование

## Основные особенности программы
- реализована на python 3.8.5
- программа обеспечивает взаимодествие сторон посредством 3-этапного "рукопожатия"
- программа позволяет осуществлять перезадание ключей шифрования случайным образом по желанию пользователя ("нажатию на кнопку" на брелоке или в машине)
- программа позволяет перепривязывать пару брелок-машина
- после каждого "рукопожатия" и выполнения команды криптографические challenges стираются - переиспользование команды без нового "рукопожатия" невозможно
- попытка подключения к протоколу активного злоумышленника Евы приводит к исключению, прерывающему дальнейшие действия в рамках "рукопожатия", затем исключение обрабатывается
- возможно включение детального логирования (см. ниже)

## Состав программы
- crypto_side.py
    - класс ChallengeMsg - обертка для challenge, позволяющая работать с ЭЦП-библиотекой rsa
    - класс VerifyError - наследуемый класс исключения, позволяющий определить что произошло именно нарушение работы протокола шифрования
    - класс CryptoSide - "абстрактный" класс, содержащий основные методы участника системы ЭЦП и протокола "рукопожатия" (генерация challenge, подпись ответного challenge, проверка отправленно challenge, их очистка), также позволяет хранить id команды для машины (специфично для данной задачи)
    
        *Особенность именования внутри класса: b_side - "Bob side" второй участник протокола*

- prorocol.py
   - функция register - привязка брелока к машине
   - функции handshake, challenge, response - выполняют атомарные этапы "рукопожатия", каждая функция отвечает односторонней отправке пакета данных
   - функция response также автоматически выполняет отправленную машине команду (если "рукопожатие" прошло успешно и не вызвало исключений)

    *Вместе эти 2 файла реализуют основную логику программы, оставшиеся файлы лишь реализуют обертку и тесты*

- vehicles.py - классы Trinket, Car - обертки для класса CryptoSide, делающие основную программу более читаемой
- logger.py - класс Logger - реализует легко включаемое/выключаемое логирование в консоль (см. ниже)
- hw5.py - основная программа, реализующая тестирование протоколов в различных ситуациях

## Запуск приложения

1. Установить python >= 3.8.5

2. Перед запуском приложения установить библиотеки rsa, pycryptodome
```cmd
$ pip install rsa
$ pip install pycryptodome
```
3. Запустить основную программу
- Windows
```cmd
> python hw5.py
```
- Linux *(не протестировано)*
```sh
$ ./hw5.py
```
## Включение логирования
Для включения продвинутого логирования необходимо модифицировать параметры Logger'a в файле hw5.py
*(пример лога см. в конце документа)*
```py
11|    Logger.config(1)
```
## Тестирование
- Валидное открытие машины (закрытие машины и обработка неизвестной команды - аналогичны)
```cmd
===== TEST: Bob, Alice, open =====

1: (handshake) trinket-Bob -> Camry 3.5, 0 (id command), 6b3c5331997478e3b600 (challenge for car)
2: (challenge) Camry 3.5 -> trinket-Bob, 0173b4a5 (challenge for trinket), 1837af26 (confirm challenge for car)
3: (response) trinket-Bob -> Camry 3.5, 3da5135bbf46a31e53ff (confirm challenge for trinket)
4: (action) car: opened
```
- Попытка вмешательства активного злоумышленника Евы
```cmd
===== TEST: Bob, Eva, open =====

1: (handshake) trinket-Bob -> Camry 3.5, 0 (id command), 607799e4c40f85bda0fb (challenge for car)
VerifyError('unverified signature')
```
- Попытка переиспользования команды
```cmd
===== TEST: Bob, Alice, open x2 =====

1: (handshake) trinket-Bob -> Camry 3.5, 0 (id command), 9d8dde3ac5c2e11b9eb5 (challenge for car)
2: (challenge) Camry 3.5 -> trinket-Bob, b4ea1a37 (challenge for trinket), 009f9b73 (confirm challenge for car)
3: (response) trinket-Bob -> Camry 3.5, 1650e62d65125a486940 (confirm challenge for trinket)
4: (action) car: opened
VerifyError('double use of command')
```
- Валидное открытие машины в режиме продвинутого логирования
*(лог промежуточных действий предшествует итоговому сообщению о завершении этапа протокола)*
```cmd
===== TEST: Bob, Alice, open =====

> log: trinket-Bob command set: 0
> log: trinket-Bob challenge generated
> log: Camry 3.5 got challenge
> log: Camry 3.5 command set: 0
1: (handshake) trinket-Bob -> Camry 3.5, 0 (id command), f7edc3207dafe6cc8118 (challenge for car)
> log: Camry 3.5 challenge generated
> log: trinket-Bob got challenge
> log: Camry 3.5 prepare to sign...
> log: Camry 3.5 signed
> log: trinket-Bob checking sign...
2: (challenge) Camry 3.5 -> trinket-Bob, 7a311ccd (challenge for trinket), 83239e68 (confirm challenge for car)
> log: trinket-Bob prepare to sign...
> log: trinket-Bob signed
> log: Camry 3.5 checking sign...
3: (response) trinket-Bob -> Camry 3.5, 966f91d4f4eef576cfe7 (confirm challenge for trinket)
4: (action) car: opened
> log: Camry 3.5 challenges expired
> log: trinket-Bob challenges expired
```