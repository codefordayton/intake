from formation.combinable_base import CombinableFormSpec, FormSpecSelector
from formation.form_base import Form
from formation.display_form_base import DisplayForm
from formation import fields as F
from intake.constants import Counties, Organizations
from formation.validators import (
    gave_preferred_contact_methods, at_least_email_or_phone,
    at_least_address_or_chose_no_mailing_address
)
from intake.constants import (
    COUNTY_CHOICE_DISPLAY_DICT, COUNTIES_REQUIRING_ADDRESS)
from project.jinja2 import oxford_comma
from formation.fields import (
    AddressField, ConsentToCourtAppearance)


class CombinableCountyFormSpec(CombinableFormSpec):

    def is_correct_spec(self, *args, **kwargs):
        counties = kwargs.get('counties', [])
        return self.county in counties

    def build_form_class(self, *args, **kwargs):
        self.add_nice_county_names_to_consentbox()
        self.modify_address_field_based_on_counties()
        return super().build_form_class(*args, **kwargs)

    def add_nice_county_names_to_consentbox(self):
        """
        county name generation for the consent checkbox split could
        be a little less brittle, but for now SB is the only one that
        is being excluded
        """
        self.counties = self.criteria['counties']
        appearance_consent = ConsentToCourtAppearance
        county_names = []
        for county in self.counties:
            if COUNTY_CHOICE_DISPLAY_DICT[county] != "Santa Barbara":
                county_names.append(COUNTY_CHOICE_DISPLAY_DICT[county])
        formatted_county_names = oxford_comma([
            county + " County" for county in county_names])

        self.fields.discard(appearance_consent)
        appearance_consent.update_counties(
            appearance_consent, formatted_county_names)
        self.fields.add(appearance_consent)

    def modify_address_field_based_on_counties(self):
        """
        this feels sloppy but it gets the job done; would love
        to look at other ways to handle the checkbox inclusion/
        exclusion in the mailing address multivaluefield -- it
        seemed like this was the only place to know for sure
        whether a combined form included counties that required
        a mailing address // same technique worked for county names
        in the label update on the appearance consent checkbox
        """
        address_field = AddressField
        counties = self.criteria['counties']
        # do any of these counties require address
        counties_that_dont_require_address = [
            county for county in counties
            if county not in COUNTIES_REQUIRING_ADDRESS
        ]
        if len(counties_that_dont_require_address) == len(counties):
            self.fields.discard(address_field)
            address_field.include_no_address_checkbox(address_field)
            self.fields.add(address_field)
        else:
            self.fields.discard(address_field)
            address_field.exclude_no_address_checkbox(address_field)
            self.fields.add(address_field)


class CombinableOrganizationFormSpec(CombinableFormSpec):

    def is_correct_spec(self, *args, **kwargs):
        organizations = kwargs.get('organizations', [])
        return self.organization in organizations


class SupplementaryDisplayForm(CombinableCountyFormSpec):

    def is_correct_spec(self, *args, **kwargs):
        return True

    fields = {
        F.DateReceived,
        F.Counties,
    }


class OtherCountyFormSpec(CombinableCountyFormSpec):
    """This could be used by Code for America to send applicants
    information on clean slate services in other counties or states.
    """
    county = Counties.OTHER
    fields = {
        F.ContactPreferences,
        F.FirstName,
        F.PhoneNumberField,
        F.EmailField,
        F.AddressField,
        F.HowDidYouHear,
    }
    required_fields = {
        F.ContactPreferences,
        F.FirstName
    }
    optional_fields = {
        F.HowDidYouHear
    }
    validators = [
        gave_preferred_contact_methods
    ]


class SanFranciscoCountyFormSpec(CombinableCountyFormSpec):
    county = Counties.SAN_FRANCISCO
    fields = {
        F.ContactPreferences,
        F.FirstName,
        F.MiddleName,
        F.LastName,
        F.PhoneNumberField,
        F.EmailField,
        F.AddressField,
        F.DateOfBirthField,
        F.SocialSecurityNumberField,
        F.USCitizen,
        F.ServingSentence,
        F.OnProbationParole,
        F.WhereProbationParole,
        F.WhenProbationParole,
        F.BeingCharged,
        F.RAPOutsideSF,
        F.WhenWhereOutsideSF,
        F.FinancialScreeningNote,
        F.CurrentlyEmployed,
        F.MonthlyIncome,
        F.MonthlyExpenses,
        F.HowDidYouHear,
        F.AdditionalInformation,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    required_fields = {
        F.FirstName,
        F.LastName,
        F.AddressField,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    recommended_fields = {
        F.DateOfBirthField,
        F.SocialSecurityNumberField,
    }
    optional_fields = {
        F.HowDidYouHear,
        F.MiddleName,
        F.AdditionalInformation,
    }
    validators = [
        gave_preferred_contact_methods
    ]


class ContraCostaFormSpec(CombinableCountyFormSpec):
    county = Counties.CONTRA_COSTA
    fields = {
        F.ContactPreferences,
        F.FirstName,
        F.MiddleName,
        F.LastName,
        F.PhoneNumberField,
        F.EmailField,
        F.AddressField,
        F.DateOfBirthField,
        F.USCitizen,
        F.ServingSentence,
        F.OnProbationParole,
        F.FinancialScreeningNote,
        F.CurrentlyEmployed,
        F.MonthlyIncome,
        F.IncomeSource,
        F.MonthlyExpenses,
        F.HowDidYouHear,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.AdditionalInformation,
        F.ConsentToCourtAppearance
    }
    required_fields = {
        F.FirstName,
        F.LastName,
        F.AddressField,
        F.USCitizen,
        F.CurrentlyEmployed,
        F.DateOfBirthField,
        F.MonthlyIncome,
        F.IncomeSource,
        F.MonthlyExpenses,
        F.ServingSentence,
        F.OnProbationParole,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    optional_fields = {
        F.HowDidYouHear,
        F.AdditionalInformation
    }
    validators = [
        gave_preferred_contact_methods
    ]


class AlamedaCountyFormSpec(CombinableCountyFormSpec):
    county = Counties.ALAMEDA
    fields = {
        F.ContactPreferences,
        F.FirstName,
        F.MiddleName,
        F.LastName,
        F.PreferredPronouns,
        F.PhoneNumberField,
        F.AlternatePhoneNumberField,
        F.EmailField,
        F.AddressField,
        F.FinancialScreeningNote,
        F.MonthlyIncome,
        F.OnPublicBenefits,
        F.OwnsHome,
        F.HouseholdSize,
        F.DateOfBirthField,
        # F.LastFourOfSSN,
        F.USCitizen,
        F.OnProbationParole,
        F.FinishedHalfProbation,
        F.ReducedProbation,
        F.ServingSentence,
        F.BeingCharged,
        F.HasSuspendedLicense,
        F.OwesCourtFees,
        F.RAPOutsideSF,
        F.WhenWhereOutsideSF,
        F.HowDidYouHear,
        F.AdditionalInformation,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    required_fields = {
        F.FirstName,
        F.LastName,
        F.AddressField,
        F.DateOfBirthField,
        F.MonthlyIncome,
        F.OnPublicBenefits,
        F.OwnsHome,
        F.HouseholdSize,
        F.OnProbationParole,
        F.FinishedHalfProbation,
        F.ReducedProbation,
        F.ServingSentence,
        F.BeingCharged,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    optional_fields = {
        F.AlternatePhoneNumberField,
        F.HowDidYouHear,
        F.AdditionalInformation,
    }
    validators = [
        gave_preferred_contact_methods
    ]


class AlamedaPublicDefenderFormSpec(CombinableOrganizationFormSpec):
    organization = Organizations.ALAMEDA_PUBDEF
    fields = {
        F.ContactPreferences,
        F.FirstName,
        F.MiddleName,
        F.LastName,
        F.PhoneNumberField,
        F.AlternatePhoneNumberField,
        F.EmailField,
        F.AddressField,
        F.FinancialScreeningNote,
        F.MonthlyIncome,
        F.OwnsHome,
        F.HouseholdSize,
        F.DateOfBirthField,
        F.USCitizen,
        F.OnProbationParole,
        F.FinishedHalfProbation,
        F.ReducedProbation,
        F.ServingSentence,
        F.BeingCharged,
        F.HowDidYouHear,
        F.AdditionalInformation,
        F.ConsentToCourtAppearance
    }
    required_fields = {
        F.FirstName,
        F.LastName,
        F.AddressField,
        F.DateOfBirthField,
        F.MonthlyIncome,
        F.OwnsHome,
        F.HouseholdSize,
        F.OnProbationParole,
        F.FinishedHalfProbation,
        F.ReducedProbation,
        F.ServingSentence,
        F.BeingCharged,
        F.ConsentToCourtAppearance
    }
    optional_fields = {
        F.AlternatePhoneNumberField,
        F.HowDidYouHear,
        F.AdditionalInformation,
    }


class MontereyCountyFormSpec(CombinableCountyFormSpec):
    county = Counties.MONTEREY
    fields = {
        F.ContactPreferences,
        F.FirstName,
        F.MiddleName,
        F.LastName,
        F.PhoneNumberField,
        F.EmailField,
        F.AddressField,
        F.FinancialScreeningNote,
        F.MonthlyIncome,
        F.OnPublicBenefits,
        F.HouseholdSize,
        F.DateOfBirthField,
        F.USCitizen,
        F.IsVeteran,
        F.IsStudent,
        F.OnProbationParole,
        F.WhereProbationParole,
        F.WhenProbationParole,
        F.ServingSentence,
        F.BeingCharged,
        F.RAPOutsideSF,
        F.WhenWhereOutsideSF,
        F.HowDidYouHear,
        F.AdditionalInformation,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    required_fields = {
        F.FirstName,
        F.LastName,
        F.AddressField,
        F.DateOfBirthField,
        F.MonthlyIncome,
        F.OnPublicBenefits,
        F.HouseholdSize,
        F.OnProbationParole,
        F.ServingSentence,
        F.BeingCharged,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    optional_fields = {
        F.HowDidYouHear,
        F.AdditionalInformation,
    }
    validators = [
        gave_preferred_contact_methods
    ]


class SolanoCountyFormSpec(CombinableCountyFormSpec):
    county = Counties.SOLANO
    fields = {
        F.ContactPreferences,
        F.FirstName,
        F.MiddleName,
        F.LastName,
        F.PhoneNumberField,
        F.AlternatePhoneNumberField,
        F.EmailField,
        F.AddressField,
        F.DateOfBirthField,
        F.USCitizen,
        F.OnProbationParole,
        F.WhereProbationParole,
        F.WhenProbationParole,
        F.OwesCourtFees,
        F.ServingSentence,
        F.BeingCharged,
        F.RAPOutsideSF,
        F.WhenWhereOutsideSF,
        F.HowDidYouHear,
        F.AdditionalInformation,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    required_fields = {
        F.FirstName,
        F.LastName,
        F.AddressField,
        F.DateOfBirthField,
        F.OnProbationParole,
        F.OwesCourtFees,
        F.ServingSentence,
        F.BeingCharged,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    optional_fields = {
        F.MiddleName,
        F.AlternatePhoneNumberField,
        F.HowDidYouHear,
        F.AdditionalInformation
    }
    validators = [
        gave_preferred_contact_methods,
        at_least_email_or_phone
    ]


class SanDiegoCountyFormSpec(SolanoCountyFormSpec):
    county = Counties.SAN_DIEGO
    fields = (SolanoCountyFormSpec.fields | {
        F.CaseNumber
    }) - {
        F.USCitizen,
    }
    optional_fields = SolanoCountyFormSpec.optional_fields | {
        F.CaseNumber
    }
    validators = [
        gave_preferred_contact_methods,
        at_least_email_or_phone,
        at_least_address_or_chose_no_mailing_address
    ]


class SanJoaquinCountyFormSpec(SolanoCountyFormSpec):
    county = Counties.SAN_JOAQUIN
    validators = [
        gave_preferred_contact_methods
    ]


class FresnoCountyFormSpec(SolanoCountyFormSpec):
    county = Counties.FRESNO
    fields = (SolanoCountyFormSpec.fields | {
        F.Aliases,
        F.CaseNumber,
        F.ReasonsForApplying,
        F.FinancialScreeningNote,
        F.MonthlyIncome,
        F.HowManyDependents,
        F.LastFourOfSocial,
        F.DriverLicenseOrIDNumber,
    }) - {
        F.OwesCourtFees,
        F.RAPOutsideSF,
        F.WhenWhereOutsideSF,
    }
    optional_fields = SolanoCountyFormSpec.optional_fields | {
        F.Aliases,
    }
    required_fields = SolanoCountyFormSpec.required_fields - {
        F.OwesCourtFees,
    }
    validators = [
        gave_preferred_contact_methods
    ]


class SantaClaraCountyFormSpec(SolanoCountyFormSpec):
    county = Counties.SANTA_CLARA
    fields = (SolanoCountyFormSpec.fields | {
        F.FinancialScreeningNote,
        F.CurrentlyEmployed,
        F.MonthlyIncome,
        F.IncomeSource,
        F.MonthlyExpenses,
        F.OnPublicBenefits,
        F.HouseholdSize,
        F.IsMarried,
        F.HasChildren,
        F.IsVeteran,
        F.ReducedProbation,
        F.ReasonsForApplying,
        F.PFNNumber,
        F.PreferredPronouns
    }) - {
        F.USCitizen,
    }
    required_fields = (SolanoCountyFormSpec.required_fields | {
        F.CurrentlyEmployed,
        F.MonthlyIncome,
        F.IncomeSource,
        F.MonthlyExpenses,
        F.OnPublicBenefits,
        F.HouseholdSize,
    }) - {F.PhoneNumberField}
    validators = [
        gave_preferred_contact_methods,
        at_least_address_or_chose_no_mailing_address
    ]


class SantaCruzCountyFormSpec(SolanoCountyFormSpec):
    county = Counties.SANTA_CRUZ
    fields = (SolanoCountyFormSpec.fields | {
        F.FinancialScreeningNote,
        F.MonthlyIncome,
        F.ReasonsForApplying
    }) - {
        F.OwesCourtFees,
        F.RAPOutsideSF,
        F.WhenWhereOutsideSF
    }
    required_fields = SolanoCountyFormSpec.required_fields - {
        F.OwesCourtFees,
    }
    validators = [
        at_least_address_or_chose_no_mailing_address
    ]


class SonomaCountyFormSpec(SolanoCountyFormSpec):
    county = Counties.SONOMA
    fields = SolanoCountyFormSpec.fields
    validators = [
        gave_preferred_contact_methods,
        at_least_address_or_chose_no_mailing_address
    ]


class TulareCountyFormSpec(SolanoCountyFormSpec):
    county = Counties.TULARE
    validators = [
        gave_preferred_contact_methods
    ]


class VenturaCountyFormSpec(CombinableCountyFormSpec):
    county = Counties.VENTURA
    fields = {
        F.ContactPreferences,
        F.FirstName,
        F.MiddleName,
        F.LastName,
        F.PhoneNumberField,
        F.AlternatePhoneNumberField,
        F.EmailField,
        F.AddressField,
        F.OwnsHome,
        F.FinancialScreeningNote,
        F.CurrentlyEmployed,
        F.MonthlyIncome,
        F.IncomeSource,
        F.OnPublicBenefits,
        F.MonthlyExpenses,
        F.OwnsHome,
        F.HowManyDependents,
        F.IsVeteran,
        F.DateOfBirthField,
        F.LastFourOfSocial,
        F.DriverLicenseOrIDNumber,
        F.OnProbationParole,
        F.WhereProbationParole,
        F.OwesCourtFees,
        F.ServingSentence,
        F.BeingCharged,
        F.RAPOutsideSF,
        F.WhenWhereOutsideSF,
        F.CaseNumber,
        F.HowDidYouHear,
        F.AdditionalInformation,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    required_fields = {
        F.CurrentlyEmployed,
        F.MonthlyIncome,
        F.IncomeSource,
        F.MonthlyExpenses,
        F.OnPublicBenefits,
        F.HouseholdSize,
        F.DateOfBirthField,
        F.OnProbationParole,
        F.OwesCourtFees,
        F.ServingSentence,
        F.BeingCharged,
        F.UnderstandsLimits,
        F.ConsentToRepresent,
        F.ConsentToCourtAppearance
    }
    validators = [
        gave_preferred_contact_methods,
        at_least_email_or_phone,
        at_least_address_or_chose_no_mailing_address
    ]


class SantaBarbaraCountyFormSpec(VenturaCountyFormSpec):
    county = Counties.SANTA_BARBARA
    fields = (VenturaCountyFormSpec.fields | {
        F.Aliases,
        F.ReasonsForApplying,
        F.IsMarried,
        F.WhenProbationParole,
        F.HouseholdSize,
        F.HasChildren,
        F.SantaBarbaraCourtAppearanceChoice}) - {
        F.LastFourOfSocial,
        F.DriverLicenseOrIDNumber,
        F.IsVeteran,
        F.HowManyDependents,
        F.ConsentToCourtAppearance
    }
    required_fields = {
        F.IsMarried,
        F.HouseholdSize,
        F.SantaBarbaraCourtAppearanceChoice
    }


class EBCLCIntakeFormSpec(CombinableOrganizationFormSpec):
    organization = Organizations.EBCLC
    fields = {
        F.ContactPreferences,
        F.FirstName,
        F.MiddleName,
        F.LastName,
        F.PreferredPronouns,
        F.PhoneNumberField,
        F.AlternatePhoneNumberField,
        F.EmailField,
        F.AddressField,
        F.FinancialScreeningNote,
        F.MonthlyIncome,
        F.OnPublicBenefits,
        F.OwnsHome,
        F.HouseholdSize,
        F.DateOfBirthField,
        # F.LastFourOfSocial,
        F.USCitizen,
        F.OnProbationParole,
        F.FinishedHalfProbation,
        F.ReducedProbation,
        F.ServingSentence,
        F.BeingCharged,
        F.RAPOutsideSF,
        F.WhenWhereOutsideSF,
        F.HasSuspendedLicense,
        F.OwesCourtFees,
        F.HowDidYouHear,
        F.AdditionalInformation,
        F.ConsentToCourtAppearance
    }
    required_fields = {
        F.FirstName,
        F.LastName,
        F.AddressField,
        F.DateOfBirthField,
        F.MonthlyIncome,
        F.OnPublicBenefits,
        F.OwnsHome,
        F.HouseholdSize,
        F.OnProbationParole,
        F.FinishedHalfProbation,
        F.ReducedProbation,
        F.ServingSentence,
        F.BeingCharged,
        F.ConsentToCourtAppearance
    }
    optional_fields = {
        F.AlternatePhoneNumberField,
        F.HowDidYouHear,
        F.AdditionalInformation,
    }


class DeclarationLetterFormSpec(CombinableFormSpec):
    fields = {
        F.DeclarationLetterNote,
        F.DeclarationLetterIntro,
        F.DeclarationLetterLifeChanges,
        F.DeclarationLetterActivities,
        F.DeclarationLetterGoals,
        F.DeclarationLetterWhy,
    }
    required_fields = {
        F.DeclarationLetterIntro,
        F.DeclarationLetterLifeChanges,
        F.DeclarationLetterActivities,
        F.DeclarationLetterGoals,
        F.DeclarationLetterWhy,
    }


class DeclarationLetterDisplay(DisplayForm):
    display_template_name = "forms/declaration_letter_display.jinja"
    fields = [
        F.DateReceived,
        F.DeclarationLetterIntro,
        F.DeclarationLetterLifeChanges,
        F.DeclarationLetterActivities,
        F.DeclarationLetterGoals,
        F.DeclarationLetterWhy,
        F.FirstName,
        F.MiddleName,
        F.LastName,
    ]


class DeclarationLetterReviewForm(Form):
    fields = [F.DeclarationLetterReviewActions]
    required_fields = [F.DeclarationLetterReviewActions]


class SelectCountyForm(Form):
    fields = [
        F.Counties,
        F.AffirmCountySelection
    ]
    required_fields = [
        F.Counties,
        F.AffirmCountySelection]


INPUT_FORM_SPECS = [
    OtherCountyFormSpec(),
    SanFranciscoCountyFormSpec(),
    ContraCostaFormSpec(),
    AlamedaCountyFormSpec(),
    MontereyCountyFormSpec(),
    SolanoCountyFormSpec(),
    SanDiegoCountyFormSpec(),
    SanJoaquinCountyFormSpec(),
    SantaClaraCountyFormSpec(),
    SantaCruzCountyFormSpec(),
    FresnoCountyFormSpec(),
    SonomaCountyFormSpec(),
    TulareCountyFormSpec(),
    VenturaCountyFormSpec(),
    SantaBarbaraCountyFormSpec(),
]

DISPLAY_FORM_SPECS = INPUT_FORM_SPECS + [
    SupplementaryDisplayForm(),
]

ORG_FORM_SPECS = [
    AlamedaPublicDefenderFormSpec(),
    EBCLCIntakeFormSpec(),
]

display_form_selector = FormSpecSelector(DISPLAY_FORM_SPECS, DisplayForm)
county_form_selector = FormSpecSelector(INPUT_FORM_SPECS, Form)
organization_form_selector = FormSpecSelector(ORG_FORM_SPECS, Form)
