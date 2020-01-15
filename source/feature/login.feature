Feature: Вход

  Scenario: Вход под админом
    Given Я открыл страницу "Входа"
    When Я ввожу текст "admin" в поле "username"
    And Я ввожу текст "admin" в поле "password"
    And Я отправляю форму
    Then Я должен быть на главной странице