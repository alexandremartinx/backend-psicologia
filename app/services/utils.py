def validate_required_fields_exists(requiredFields: list, passedFields: dict) -> str|None :
    for field in passedFields:
        if field not in requiredFields:
            return field
    
    return

def normalize_form_values(form_data: dict) -> dict:
    for key, value in form_data.items():
        if isinstance(value, str):
            form_data[key] = value.strip()
    
    return form_data

def remove_non_digits(value: str):
    return ''.join([char for char in value if char.isdigit()])

def _validate_cnpj(cnpj: str|int) -> bool:
    DIVIDER = 11
    def get_first_digit(number, weight):
            total = 0

            for i in range(len(weight)):
                total += int(number[i]) * weight[i]

            rest_division = total % DIVIDER

            if rest_division < 2:
                return '0'

            return str(11 - rest_division)

    def get_second_digit(updated_number, weight):
        total = 0

        for i in range(len(weight)):
            total += + int(updated_number[i]) * weight[i]

        rest_division = total % DIVIDER

        if rest_division < 2:
            return '0'

        return str(11 - rest_division)


    if isinstance(cnpj, str):
        cnpj = remove_non_digits(cnpj)
    
    if isinstance(cnpj, int):
        cnpj = str(cnpj).zfill(14)

    if len(cnpj) != 14 or len(set(cnpj)) == 1:
        return False

    first_cnpj_weight = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    second_cnpj_weight = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    first_part = cnpj[:12]
    first_digit = cnpj[12]
    second_digit = cnpj[13]

    if not (first_digit == get_first_digit(number=first_part, weight=first_cnpj_weight)
            and second_digit == get_second_digit(updated_number=cnpj[:13], weight=second_cnpj_weight)):
        return False
    
    return True

def validate_document_by_document_type(document: str, document_type: str) -> bool:
    if document_type == 'CNPJ':
        _validate_cnpj(document)
    return True