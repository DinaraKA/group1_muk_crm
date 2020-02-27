from behave import given, when, then, step


@given('Я открыл страницу "Социальный Статус"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/accounts/social_statuses/')


@then('Я должен быть на странице "Социальный Статус"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://localhost:8000/accounts/social_statuses/"


@given('Я перехожу на страницу создания Социального Статуса')
def should_be_at_main(context):
    context.browser.get('http://localhost:8000/accounts/social_statuses/add/')