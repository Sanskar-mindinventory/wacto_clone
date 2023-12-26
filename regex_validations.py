import re
from rest_framework import serializers


class RegexValidation:
    def __init__(self, field_data, regex_pattern, error_message):
        self.field_data = field_data
        self.regex_pattern = regex_pattern
        self.error_message = error_message

    def regex_validator(self):
        if re.fullmatch(self.regex_pattern, self.field_data):
            return self.field_data
        else:
            raise serializers.ValidationError(self.error_message)
        
    def regex_auth_validator(self):
        if re.fullmatch(self.regex_pattern, self.field_data):
            return self.field_data
        return None
        
