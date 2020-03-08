Feature: Дисциплина

  Scenario: Вход на страницу просмотра Дисциплины
    Given Я открыл страницу "Дисциплина"
    When Я ввожу текст "admin" в поле "username"
    And Я ввожу текст "admin" в поле "password"
    And Я отправляю форму
    Then Я должен быть на странице "Дисциплина"

  Scenario: Успешное создание
    Given Я перехожу на страницу создания Дисциплины
    When Я ввожу текст "CreateTest" в поле "name"
    And Я ввожу текст "Айдай Исаева" в поле "teacher"
    And Я отправляю форму
    Then Я должен быть на странице "Дисциплина"

  Scenario: Неуспешное создание
    Given Я перехожу на страницу создания Дисциплины
    When Я ввожу текст "CreateTest" в поле "name"
    And Я ввожу текст "Айдай Исаева" в поле "teacher"
    And Я отправляю форму
    Then Я должен видеть сообщение об ошибке "Объект с таким названием уже существует!"

  Scenario: Обновление
    Given Я открыл страницу "Дисциплина"
    Then Я нажимаю на кнопку "Обновить"
    When Я очищаю поле "name"
    And Я ввожу текст "UpdateTest" в поле "name"
    And Я очищаю поле "teacher"
    And Я ввожу текст "Айдай Исаева" в поле "teacher"
    And Я отправляю форму
    Then Я должен быть на странице "Дисциплина"

    Scenario: Удаление
    Given Я открыл страницу "Дисциплина"
    Then Я нажимаю на кнопку "Удалить"
    When Я нажимаю на кнопку "Да"
    Then Я должен быть на странице "Дисциплина"