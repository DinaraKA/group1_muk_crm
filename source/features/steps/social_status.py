from behave import given, then


@given('Я открыл страницу "Социальный Статус"')
def open_login_page(context):
    context.browser.get('http://134.122.82.126/accounts/social_statuses/')


@then('Я должен быть на странице "Социальный Статус"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://134.122.82.126/accounts/social_statuses/"


@given('Я перехожу на страницу создания Социального Статуса')
def should_be_at_main(context):
    context.browser.get('http://134.122.82.126/accounts/social_statuses/add/')