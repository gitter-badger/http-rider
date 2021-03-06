from httprider.core.generators import *


class DataGeneratorPresenter:
    def __init__(self, view, parent):
        self.view = view
        self.parent = parent

        # Event handlers to refresh generated values
        self.view.chk_random_string_letters.stateChanged.connect(self.fake_to_form)
        self.view.chk_random_string_digits.stateChanged.connect(self.fake_to_form)
        self.view.txt_random_string_chars.valueChanged.connect(self.fake_to_form)
        self.view.txt_custom_string_template.textEdited.connect(self.fake_to_form)
        self.view.gender_selector.currentIndexChanged.connect(self.fake_to_form)

    def fake_to_form(self):
        # Misc section
        random_string = random_string_generator(
            (
                self.view.txt_random_string_chars.text(),
                self.view.chk_random_string_letters.isChecked(),
                self.view.chk_random_string_digits.isChecked(),
            )
        )
        self.view.lbl_eg_random_string.setText("eg: {}".format(random_string))
        self.view.lbl_eg_uuid.setText("eg: {}".format(random_uuid()))
        self.view.lbl_eg_custom_string.setText(
            "eg: {}".format(
                custom_string_generator(
                    (
                        self.view.txt_custom_string_template.text(),
                        self.view.chk_custom_string_uppercase.isChecked(),
                    )
                )
            )
        )
        # Person section
        gender = self.view.gender_selector.currentText()
        self.view.lbl_eg_person_prefix.setText(
            "eg: {}".format(random_person(("prefix", gender)))
        )
        self.view.lbl_eg_person_first_name.setText(
            "eg: {}".format(random_person(("first_name", gender)))
        )
        self.view.lbl_eg_person_last_name.setText(
            "eg: {}".format(random_person(("last_name", gender)))
        )
        self.view.lbl_eg_person_full_name.setText(
            "eg: {}".format(random_person(("full_name", gender)))
        )
        self.view.lbl_eg_person_suffix.setText(
            "eg: {}".format(random_person(("suffix", gender)))
        )

        # Address section

        self.view.lbl_eg_address_country.setText(
            "eg: {}".format(random_address("country"))
        )
        self.view.lbl_eg_address_full.setText(
            "eg: {}...".format(random_address("address")[:15])
        )
        self.view.lbl_eg_address_secondary.setText(
            "eg: {}".format(random_address("secondary"))
        )
        self.view.lbl_eg_address_street.setText(
            "eg: {}".format(random_address("street"))
        )
        self.view.lbl_eg_address_city.setText("eg: {}".format(random_address("city")))
        self.view.lbl_eg_address_zipcode.setText(
            "eg: {}".format(random_address("zipcode"))
        )
        self.view.lbl_eg_address_state.setText("eg: {}".format(random_address("state")))

    def get_function(self):
        current_index = self.view.tabWidget.currentIndex()
        current_tab = self.view.tabWidget.tabText(current_index).lower()
        if current_tab == "misc":
            if self.view.cmb_random_string.isChecked():
                chars = self.view.txt_random_string_chars.text()
                letters = self.view.chk_random_string_letters.isChecked()
                digits = self.view.chk_random_string_digits.isChecked()
                return f"${{random({chars}, {letters}, {digits})}}"
            if self.view.cmb_uuid.isChecked():
                return f"${{uuid()}}"
            if self.view.cmb_custom_string.isChecked():
                custom_template = self.view.txt_custom_string_template.text()
                upper_case = self.view.chk_custom_string_uppercase.isChecked()
                return f'${{custom("{custom_template}", {upper_case})}}'
        if current_tab == "person":
            if self.view.cmb_person_prefix.isChecked():
                return f'${{person("prefix", "{self.view.gender_selector.currentText()}")}}'
            if self.view.cmb_person_first_name.isChecked():
                return f'${{person("first_name", "{self.view.gender_selector.currentText()}")}}'
            if self.view.cmb_person_last_name.isChecked():
                return f'${{person("last_name", "{self.view.gender_selector.currentText()}")}}'
            if self.view.cmb_person_full_name.isChecked():
                return f'${{person("full_name", "{self.view.gender_selector.currentText()}")}}'
            if self.view.cmb_person_suffix.isChecked():
                return f'${{person("suffix", "{self.view.gender_selector.currentText()}")}}'
        if current_tab == "address":
            if self.view.cmb_address_country.isChecked():
                return f'${{address("country")}}'

            if self.view.cmb_address_full.isChecked():
                return f'${{address("address")}}'
            if self.view.cmb_address_secondary.isChecked():
                return f'${{address("secondary")}}'
            if self.view.cmb_address_street.isChecked():
                return f'${{address("street")}}'
            if self.view.cmb_address_city.isChecked():
                return f'${{address("city")}}'
            if self.view.cmb_address_zipcode.isChecked():
                return f'${{address("zipcode")}}'
            if self.view.cmb_address_state.isChecked():
                return f'${{address("state")}}'
        return "N/A"
