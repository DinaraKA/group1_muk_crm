from behave import given, then


@given('Я открыл страницу "Новости"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/news/all/')


@given('Я открыл "Новость"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/news/1/')


@then('Я должен быть на странице "Новости"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://localhost:8000/news/all/"


@given('Я перехожу на страницу создания Новости')
def should_be_at_main(context):
    context.browser.get('http://localhost:8000/news/add/')
