import difflib
import logging
from error_handler import ErrorHandler
from validator import Validator

class Corrector:
    def __init__(self, keywords, error_handler):
        logging.debug("Initializing Corrector class")
        self.valid_keywords = keywords
        self.error_handler = error_handler
        self.validator = Validator(keywords, error_handler)

    def correct_syntax(self, lines):
        logging.debug("Attempting to correct syntax")
        corrected_lines = []
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                corrected_lines.append(line)
                continue

            # Check for multi-word keywords
            keyword = None
            for valid_keyword in self.valid_keywords:
                if line_stripped.startswith(valid_keyword):
                    keyword = valid_keyword
                    break

            if keyword is None:
                # If no valid keyword is found, attempt to correct the first word
                first_word = line_stripped.split()[0]
                closest_matches = difflib.get_close_matches(first_word, self.valid_keywords, n=1, cutoff=0.8)
                if closest_matches:
                    corrected_line = closest_matches[0] + line_stripped[len(first_word):]
                    corrected_lines.append(corrected_line)
                else:
                    corrected_lines.append(line)
            else:
                corrected_lines.append(line)
        return corrected_lines

    def handle_invalid_syntax(self, line_number, line):
        logging.debug(f"Handling invalid syntax at line {line_number}")
        corrected_line = self.correct_syntax([line])[0]
        if corrected_line != line:
            self.error_handler.add_error(line_number, 'warning', f"Corrected Gherkin syntax: {corrected_line}")
        return corrected_line

    def validate_syntax(self, lines):
        logging.debug("Validating syntax")
        self.validator.validate_syntax(lines)
