from selenium.webdriver.common.by import By
from model.group import Group


class GroupHelper:
    def __init__(self, app):
        self.app = app

    def open_groups_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/group.php") and len(wd.find_elements(By.NAME, "new")) > 0):
            wd.find_element(By.LINK_TEXT, "groups").click()

    def create(self, group):
        wd = self.app.wd
        self.open_groups_page()
        # Создаем новую группу
        wd.find_element(By.NAME, "new").click()
        self.fill_group_form(group)
        # Подтверждение создания группы на странице group
        wd.find_element(By.NAME, "submit").click()
        self.return_to_groups_page()
        self.group_cache = None

    def fill_group_form(self, group):
        self.change_field_value("group_name", group.name)
        self.change_field_value("group_header", group.header)
        self.change_field_value("group_footer", group.footer)

    def change_field_value(self, fild_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element(By.NAME, fild_name).click()
            wd.find_element(By.NAME, fild_name).clear()
            wd.find_element(By.NAME, fild_name).send_keys(text)

    def return_to_groups_page(self):
        wd = self.app.wd
        wd.find_element(By.LINK_TEXT, "group page").click()

    def delete_first_group(self):
        self.delete_group_by_index(0)

    def delete_group_by_index(self, index):
        wd = self.app.wd
        self.open_groups_page()
        self.select_group_by_index(index)
        # Удалить выбранную группу
        wd.find_element(By.NAME, "delete").click()
        self.return_to_groups_page()
        self.group_cache = None

    def select_group_by_index(self, index):
        wd = self.app.wd
        wd.find_elements(By.NAME, "selected[]")[index].click()

    def select_first_group(self):
        wd = self.app.wd
        wd.find_element(By.NAME, "selected[]").click()

    def select_group_by_id(self, id):
        wd = self.app.wd
        wd.find_element(By.CSS_SELECTOR, "input[value='%s']" % id).click()

    def delete_group_by_id(self, id):
        wd = self.app.wd
        self.open_groups_page()
        self.select_group_by_id(id)
        # Удалить выбранную группу
        wd.find_element(By.NAME, "delete").click()
        self.return_to_groups_page()
        self.group_cache = None


    def modify_group_by_index(self, index, new_group_data):
        wd = self.app.wd
        self.open_groups_page()
        self.select_group_by_index(index)
        # Открываем кнопку модификации группы
        wd.find_element(By.NAME, "edit").click()
        # Заполняем форму модификации группы
        self.fill_group_form(new_group_data)
        # подтверждение модификации группы
        wd.find_element(By.NAME, "update").click()
        self.return_to_groups_page()
        self.group_cache = None

    def modify_first_group(self):
        self.modify_group_by_index(0)

    def count(self):
        wd = self.app.wd
        self.open_groups_page()
        return len(wd.find_elements(By.NAME, "selected[]"))

    group_cache = None

    def get_group_list(self):
        if self.group_cache is None:
            wd = self.app.wd
            self.open_groups_page()
            self.group_cache = []
            for element in wd.find_elements(By.CSS_SELECTOR, "span.group"):
                text = element.text
                id = element.find_element(By.NAME, "selected[]").get_attribute("value")
                self.group_cache.append(Group(name=text, id=id))
        return list(self.group_cache)
