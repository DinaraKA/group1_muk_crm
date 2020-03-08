from behave import given, then


@given('Я открыл страницу "Тема"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/themes/')


@then('Я должен быть на странице "Тема"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://localhost:8000/themes/"


@given('Я перехожу на страницу создания Темы')
def should_be_at_main(context):
    context.browser.get('http://localhost:8000/themes/add/')
