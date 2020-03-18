from behave import given, then


@given('Я открыл страницу "Аудитория"')
def open_login_page(context):
    context.browser.get('http://134.122.82.126/auditories/')


@then('Я должен быть на странице "Аудитория"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://134.122.82.126/auditories/"


@given('Я перехожу на страницу создания Аудитории')
def should_be_at_main(context):
    context.browser.get('http://134.122.82.126/auditories/add/')
