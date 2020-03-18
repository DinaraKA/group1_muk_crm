from behave import given, then


@given('Я открыл страницу "Должности"')
def open_login_page(context):
    context.browser.get('http://134.122.82.126/accounts/adminpositions/')


@then('Я должен быть на странице "Должности"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://134.122.82.126/accounts/adminpositions/"


@given('Я перехожу на страницу создания Должности')
def should_be_at_main(context):
    context.browser.get('http://134.122.82.126/accounts/adminposition/add/')
