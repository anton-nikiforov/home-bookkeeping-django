from django.forms.widgets import DateTimeBaseInput

class DateInput(DateTimeBaseInput):
    format_key = 'DATE_INPUT_FORMATS'
    input_type = 'date'