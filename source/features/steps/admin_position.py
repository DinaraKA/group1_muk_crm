from behave import given, when, then, step


@given('Я открыл страницу "Должности"')
def open_login_page(context):
    context.browser.get('http://localhost:8000/accounts/adminpositions/')


@then('Я должен быть на странице "Должности"')
def should_be_at_list_page(context):
    assert context.browser.current_url == "http://localhost:8000/accounts/adminpositions/"


@given('Я перехожу на страницу создания Должности')
def should_be_at_main(context):
    context.browser.get('http://localhost:8000/accounts/adminposition/add/')


@step('Я ввожу текст "{text}" в поле "{field}"')
def enter_text(context, text, field):
    context.browser.find_element_by_name(field).send_keys(text)


@when('Я отправляю форму')
def submit_form(context):
    context.browser.find_element_by_class_name('btn-primary').click()


@then('Я нажимаю на кнопку "Обновить"')
def click_on_update(context):
    context.browser.find_element_by_class_name('update').click()


@step('Я очищаю поле "{name}"')
def clear_text_field(context, name):
    context.browser.find_element_by_name('name').clear()


@then('Я нажимаю на кнопку "Удалить"')
def click_on_update(context):
    context.browser.find_element_by_class_name('delete').click()


@when('Я нажимаю на кнопку "Да"')
def submit_form(context):
    context.browser.find_element_by_class_name('btn-danger').click()

@then('Я должен видеть сообщение об ошибке "{text}"')
def see_error_with_text(context, text):
    error = context.browser.find_element_by_tag_name('h3')
    assert error.text == text