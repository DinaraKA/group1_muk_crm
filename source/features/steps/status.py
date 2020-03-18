from behave import given, then


@given('Я открыл страницу "Статус"')
def open_login_page(context):
    context.browser.get('http://134.122.82.126/accounts/statuses/')


@then('Я должен быть на странице "Статус"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://134.122.82.126/accounts/statuses/"


@given('Я перехожу на страницу создания Статуса')
def should_be_at_main(context):
    context.browser.get('http://134.122.82.126/accounts/statuses/add/')