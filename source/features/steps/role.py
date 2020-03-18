from behave import given, then


@given('Я открыл страницу "Роли"')
def open_login_page(context):
    context.browser.get('http://134.122.82.126/accounts/roles/')


@then('Я должен быть на странице "Роли"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://134.122.82.126/accounts/roles/"


@given('Я перехожу на страницу создания Роли')
def should_be_at_main(context):
    context.browser.get('http://134.122.82.126/accounts/roles/add/')