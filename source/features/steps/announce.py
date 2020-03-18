from behave import given, then, step


@given('Я открыл страницу "Объявления"')
def open_login_page(context):
    context.browser.get('http://134.122.82.126/announcements/')


@then('Я должен быть на странице "Объявления"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://134.122.82.126/announcements/"


@given('Я перехожу на страницу создания Объявления')
def should_be_at_main(context):
    context.browser.get('http://134.122.82.126/announcements/add/')


@then('Я снова открыл страницу "Объявления"')
def open_login_page(context):
    context.browser.get('http://134.122.82.126/announcements/')
