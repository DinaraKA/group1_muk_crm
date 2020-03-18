Feature: Новости

  Scenario: Вход на страницу просмотра Новости
    Given Я открыл страницу "Новости"
    Then Я должен быть на странице "Новости"

  Scenario:  Cоздание
    Given Я открыл страницу "Входа"
    And Я ввожу текст "adminanet" в поле "username"
    And Я ввожу текст "adminanet" в поле "password"
    Then Я снова открыл страницу "Новости"
    Then Я нажимаю на кнопку "Создать"
    When Я ввожу текст "NewCreate" в поле "title"
    And Я ввожу текст "NewCreate" в поле "text"
    And Я ввожу фото "/home/karamoldoevee/Downloads/test.png" в поле "//*[@id="id_photo"]"
    Then Я нажимаю на кнопку "Создать"
    Then Я должен быть на странице "Новости"

  Scenario: Обновление
    Given Я открыл страницу "Входа"
    And Я ввожу текст "adminanet" в поле "username"
    And Я ввожу текст "adminanet" в поле "password"
    Then Я снова открыл страницу "Новости"
    Then Я перехожу на страницу Детального просмотра
    Then Я нажимаю на кнопку "Обновить"
    When Я очищаю поле "title"
    And Я ввожу текст "NewUpdate" в поле "title"
    And Я очищаю поле "text"
    And Я ввожу текст "NewUpdate" в поле "text"
    And Я ввожу фото "/home/karamoldoevee/Downloads/test.png" в поле "//*[@id="id_photo"]"
    And Я отправляю форму
    Then Я должен быть на странице "Новости"

    Scenario: Удаление
    Given Я открыл страницу "Входа"
    And Я ввожу текст "adminanet" в поле "username"
    And Я ввожу текст "adminanet" в поле "password"
    Then Я снова открыл страницу "Новости"
    Then Я перехожу на страницу Детального просмотра
    Then Я нажимаю на кнопку "Удалить"
    When Я нажимаю на кнопку "Да"
    Then Я должен быть на странице "Новости"