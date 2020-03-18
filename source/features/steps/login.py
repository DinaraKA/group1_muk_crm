from behave import given, then

from selenium.common.exceptions import NoSuchElementException


@given('Я открыл страницу "Входа"')
def open_login_page(context):
    context.browser.get('http://134.122.82.126/accounts/login/')


@then('Я должен быть на главной странице')
def should_be_at_main(context):
    assert context.browser.current_url == "http://134.122.82.126/"


@then('Я должен видеть ссылку на личный кабинет пользователя "{username}"')
def see_cabinet_link(context, username):
    try:
        link = context.browser.find_element_by_link_text(f'Привет, {username}!')
    except NoSuchElementException:
        link = None
    assert link is not None, f"На странице должна быть ссылка \"Привет, {username}!\""


@then('Я должен быть на странице входа')
def should_be_at_login(context):
    assert context.browser.current_url.split("?")[0] == 'http://134.122.82.126/accounts/login/'


@then('Я должен видеть сообщение об ошибке с текстом "{text}"')
def see_error_with_text(context, text):
    error = context.browser.find_element_by_css_selector('.text-danger')
    assert error.text == text



