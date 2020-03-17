Feature: Новости

  Scenario: Вход на страницу просмотра Новости
    Given Я открыл страницу "Новости"
    Then Я должен быть на странице "Новости"

  Scenario: Успешное создание
    Given Я перехожу на страницу создания Новости
    When Я ввожу текст "NewCreate" в поле "title"
    And Я ввожу текст "NewCreate" в поле "text"
    And Я ввожу фото "/home/karamoldoevee/Downloads/test.png" в поле "//*[@id="id_photo"]"
    Then Я нажимаю на кнопку "Создать"
    Then Я должен быть на странице "Новости"

  Scenario: Обновление
    Given Я открыл "Новость"
    Then Я нажимаю на кнопку "Обновить"
    When Я очищаю поле "title"
    And Я ввожу текст "NewUpdate" в поле "title"
    And Я очищаю поле "text"
    And Я ввожу текст "NewUpdate" в поле "text"
    And Я ввожу фото "/home/karamoldoevee/Downloads/test.png" в поле "//*[@id="id_photo"]"
    And Я отправляю форму
    Then Я должен быть на странице "Новости"

    Scenario: Удаление
    Given Я открыл "Новость"
    Then Я нажимаю на кнопку "Удалить"
    When Я нажимаю на кнопку "Да"
    Then Я должен быть на странице "Новости"