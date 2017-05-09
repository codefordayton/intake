from formation.tests.utils import PatchTranslationTestCase

from formation.forms import county_form_selector
from formation.forms import gave_preferred_contact_methods
from formation import fields as F
from intake.constants import Counties


class TestCombinableFormSpec(PatchTranslationTestCase):

    def test_can_combine_validators(self):
        CombinedForm = county_form_selector.get_combined_form_class(
            counties=[
                Counties.SAN_FRANCISCO,
                Counties.CONTRA_COSTA
            ])
        self.assertListEqual(CombinedForm.validators,
                             [gave_preferred_contact_methods]
                             )

    def test_combines_optional_fields_properly(self):
        CombinedForm = county_form_selector.get_combined_form_class(
            counties=[
                Counties.SAN_FRANCISCO,
                Counties.CONTRA_COSTA
            ])
        expected_optional_fields = {
            F.HowDidYouHear,
            F.AdditionalInformation
        }
        self.assertTrue(
            expected_optional_fields == set(CombinedForm.optional_fields)
        )

    def test_includes_list_of_counties_in_appearance_consent_label_if_sb(self):
        CombinedForm = county_form_selector.get_combined_form_class(
            counties=[
                Counties.CONTRA_COSTA,
                Counties.FRESNO,
                Counties.SAN_DIEGO,
                Counties.SAN_FRANCISCO,
                Counties.SANTA_BARBARA
            ])
        expected_consent_county_label = (
            "In Contra Costa County, Fresno County, San Diego County, "
            "and San Francisco County, do you understand that attorneys "
            "need to attend court on your behalf, even if you aren't there?")
        consent_label = F.ConsentToCourtAppearance.label
        self.assertEqual(
            expected_consent_county_label,
            consent_label)

    def test_no_county_names_in_consent_label_if_not_sb(self):
        CombinedForm = county_form_selector.get_combined_form_class(
            counties=[
                Counties.CONTRA_COSTA,
                Counties.FRESNO,
                Counties.SAN_DIEGO,
                Counties.SAN_FRANCISCO
            ])
        expected_consent_county_label = (
            "Do you understand that attorneys "
            "need to attend court on your behalf, even if you aren't there?")
        consent_label = F.ConsentToCourtAppearance.label
        self.assertEqual(CombinedForm.counties, [
            Counties.CONTRA_COSTA,
            Counties.FRESNO,
            Counties.SAN_DIEGO,
            Counties.SAN_FRANCISCO])
        self.assertEqual(
            expected_consent_county_label,
            consent_label)

    def test_excludes_santa_barbara_from_consent_label_county_names(self):
        CombinedForm = county_form_selector.get_combined_form_class(
            counties=[
                Counties.SANTA_BARBARA,
                Counties.SAN_FRANCISCO,
                Counties.CONTRA_COSTA
            ])
        expected_consent_county_label = (
            "In San Francisco County and Contra Costa County, "
            "do you understand that attorneys need to attend "
            "court on your behalf, even if you aren't there?")
        consent_label = F.ConsentToCourtAppearance.label
        self.assertEqual(
            expected_consent_county_label,
            consent_label)

    def test_only_santa_barbara_does_not_show_consent_to_appearance(self):
        CombinedForm = county_form_selector.get_combined_form_class(
            counties=[
                Counties.SANTA_BARBARA
            ])
        consent_field = F.ConsentToCourtAppearance
        self.assertNotIn(consent_field, CombinedForm.fields)

    def test_mailing_address_checkbox_absent_if_address_required(self):
        CombinedForm = county_form_selector.get_combined_form_class(
            counties=[
                Counties.SANTA_BARBARA,
                Counties.SAN_FRANCISCO,
                Counties.CONTRA_COSTA
            ])
        field_keys = list(CombinedForm.get_field_keys())
        address_checkbox_key = 'no_mailing_address'
        self.assertNotIn(address_checkbox_key, field_keys)
