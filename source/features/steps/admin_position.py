from behave import given, when, then, step

from selenium.common.exceptions import NoSuchElementException


@given('Я открыл страницу "Просмотра"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/accounts/adminpositions/')


@then('Я должен быть на странице "Просмотра"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://localhost:8000/accounts/adminpositions/"


@given('Я перехожу на страницу создания')
def should_be_at_main(context):
    context.browser.get('http://localhost:8000/accounts/adminposition/add/')


@step('Я ввожу текст "{text}" в поле "{name}"')
def enter_text(context, text, name):
    context.browser.find_element_by_name(name).send_keys(text)


@when('Я отправляю форму')
def submit_form(context):
    context.browser.find_element_by_class_name('btn-primary').click()


@then('Я должен быть на странице "Просмотра"')
def should_be_at_main(context):
    assert context.browser.current_url == "http://localhost:8000/accounts/adminpositions/"


@given('Я открыл страницу "Просмотра"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/accounts/adminpositions/')


@then('Я нажимаю на кнопку "Обновить"')
def click_on_update(context):
    context.browser.find_element_by_class_name('update').click()


@step('Я очищаю поле "{text}"')
def clear_text_field(context, text):
    context.browser.find_element_by_name('name').clear()


@step('Я очищаю поле "{text}"')
def clear_text_field(context, text):
    context.browser.find_element_by_name('name').clear()


@step('Я ввожу текст "{text}" в поле "{name}"')
def enter_text(context, text, name):
    context.browser.find_element_by_name(name).send_keys(text)


@when('Я отправляю форму')
def submit_form(context):
    context.browser.find_element_by_class_name('btn-primary').click()


@then('Я должен быть на странице "Просмотра"')
def should_be_at_main(context):
    assert context.browser.current_url == "http://localhost:8000/accounts/adminpositions/"


@given('Я открыл страницу "Просмотра"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/accounts/adminpositions/')


@then('Я нажимаю на кнопку "Удалить"')
def click_on_update(context):
    context.browser.find_element_by_class_name('delete').click()


@when('Я нажимаю на кнопку "Да"')
def submit_form(context):
    context.browser.find_element_by_class_name('btn-danger').click()


@then('Я должен быть на странице "Просмотра"')
def should_be_at_main(context):
    assert context.browser.current_url == "http://localhost:8000/accounts/adminpositions/"