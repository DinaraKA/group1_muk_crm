from behave import given, then


@given('Я открыл страницу Регистрации')
def open_login_page(context):
    context.browser.get('http://134.122.82.126/accounts/user/create/')


@then('Я должен быть на странице Регистрации')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://134.122.82.126/user/create/"
