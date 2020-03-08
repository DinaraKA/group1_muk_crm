Feature: Аудитория

  Scenario: Вход на страницу просмотра Аудитории
    Given Я открыл страницу "Аудитория"
    When Я ввожу текст "admin" в поле "username"
    And Я ввожу текст "admin" в поле "password"
    And Я отправляю форму
    Then Я должен быть на странице "Аудитория"

  Scenario: Успешное создание
    Given Я перехожу на страницу создания Аудитории
    When Я ввожу текст "CreateTest" в поле "name"
    And Я ввожу текст "35" в поле "places"
    And Я ввожу текст "CreateTest" в поле "description"
    And Я отправляю форму
    Then Я должен быть на странице "Аудитория"

  Scenario: Неуспешное создание
    Given Я перехожу на страницу создания Аудитории
    When Я ввожу текст "CreateTest" в поле "name"
    And Я ввожу текст "35" в поле "places"
    And Я ввожу текст "CreateTest" в поле "description"
    And Я отправляю форму
    Then Я должен видеть сообщение об ошибке "Объект с таким названием уже существует!"

  Scenario: Обновление
    Given Я открыл страницу "Аудитория"
    Then Я нажимаю на кнопку "Обновить"
    When Я очищаю поле "name"
    And Я ввожу текст "UpdateTest" в поле "name"
    And Я очищаю поле "places"
    And Я ввожу текст "33" в поле "places"
    And Я очищаю поле "description"
    And Я ввожу текст "UpdateTest" в поле "description"
    And Я отправляю форму
    Then Я должен быть на странице "Аудитория"

    Scenario: Удаление
    Given Я открыл страницу "Аудитория"
    Then Я нажимаю на кнопку "Удалить"
    When Я нажимаю на кнопку "Да"
    Then Я должен быть на странице "Аудитория"