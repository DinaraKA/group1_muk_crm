Feature: Административная Позиция

  Scenario: Вход на страницу просмотра Админ. Позиций
    Given Я открыл страницу "Должности"
    When Я ввожу текст "admin" в поле "username"
    And Я ввожу текст "admin" в поле "password"
    And Я отправляю форму
    Then Я должен быть на странице "Должности"

  Scenario: Успешное создание
    Given Я перехожу на страницу создания Должности
    When Я ввожу текст "Test" в поле "name"
    And Я отправляю форму
    Then Я должен быть на странице "Должности"

  Scenario: Неуспешное создание
    Given Я перехожу на страницу создания Должности
    When Я ввожу текст "Test" в поле "name"
    And Я отправляю форму
    Then Я должен видеть сообщение об ошибке "Объект с таким названием уже существует!"

  Scenario: Обновление
    Given Я открыл страницу "Должности"
    Then Я нажимаю на кнопку "Обновить"
    When Я очищаю поле "name"
    And Я ввожу текст "NewTest" в поле "name"
    And Я отправляю форму
    Then Я должен быть на странице "Должности"

    Scenario: Удаление
    Given Я открыл страницу "Должности"
    Then Я нажимаю на кнопку "Удалить"
    When Я нажимаю на кнопку "Да"
    Then Я должен быть на странице "Должности"