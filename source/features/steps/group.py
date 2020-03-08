from behave import given, then


@given('Я открыл страницу "Группы"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/accounts/groups/')


@then('Я должен быть на странице "Группы"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://localhost:8000/accounts/groups/"


@given('Я перехожу на страницу создания Группы')
def should_be_at_main(context):
    context.browser.get('http://localhost:8000/accounts/group/add/')
