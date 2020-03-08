Feature: Новости

  Scenario: Вход на страницу просмотра Новости
    Given Я открыл страницу "Новости"
    When Я ввожу текст "admin" в поле "username"
    And Я ввожу текст "admin" в поле "password"
    And Я отправляю форму
    Then Я должен быть на странице "Новости"

  Scenario: Успешное создание
    Given Я перехожу на страницу создания Новости
    When Я ввожу текст "СreateTest" в поле "title"
    And Я ввожу текст "СreateTest" в поле "text"
    And Я ввожу фото "//*[@id="id_photo"]" в поле "/home/karamoldoevee/Downloads/test.png"
    And Я отправляю форму
    Then Я должен быть на странице "Новости"

  Scenario: Неуспешное создание
    Given Я перехожу на страницу создания Урока
    When Я ввожу текст "СreateTest" в поле "title"
    And Я ввожу текст "СreateTest" в поле "text"
    And Я ввожу фото "//*[@id="id_photo"]" в поле "/home/karamoldoevee/Downloads/test.png"
    And Я отправляю форму
    Then Я должен видеть сообщение об ошибке "Объект с таким названием уже существует!"

  Scenario: Обновление
    Given Я открыл "Новость"
    Then Я нажимаю на кнопку "Обновить"
    When Я очищаю поле "title"
    And Я ввожу текст "UpdateTest" в поле "title"
    And Я очищаю поле "text"
    And Я ввожу текст "UpdateTest" в поле "text"
    When Я очищаю поле "//*[@id="id_photo"]"
    And Я ввожу фото "//*[@id="id_photo"]" в поле "/home/karamoldoevee/Downloads/test.png"
    And Я отправляю форму
    Then Я должен быть на странице "Новости"

    Scenario: Удаление
    Given Я открыл "Новость"
    Then Я нажимаю на кнопку "Удалить"
    When Я нажимаю на кнопку "Да"
    Then Я должен быть на странице "Новости"