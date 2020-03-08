from behave import given, then


@given('Я открыл страницу "Урок"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/lessons/all/')


@then('Я должен быть на странице "Урок"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://localhost:8000/lessons/all/"


@given('Я перехожу на страницу создания Урока')
def should_be_at_main(context):
    context.browser.get('http://localhost:8000/lessons/add/')
