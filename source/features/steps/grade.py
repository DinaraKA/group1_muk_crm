from behave import given, then


@given('Я открыл страницу "Оценка"')
def open_login_page(context):
    context.browser.get('http://134.122.82.126/grades/')


@then('Я должен быть на странице "Оценка"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://134.122.82.126/grades/"


@given('Я перехожу на страницу создания Оценки')
def should_be_at_main(context):
    context.browser.get('http://134.122.82.126/grades/add/')
