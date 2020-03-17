from behave import given, then, step


@given('Я открыл страницу "Объявления"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/announcements/')


@then('Я должен быть на странице "Объявления"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://localhost:8000/announcements/"


@given('Я перехожу на страницу создания Объявления')
def should_be_at_main(context):
    context.browser.get('http://localhost:8000/announcements/add/')
