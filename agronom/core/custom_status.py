CUSTOM_430_PIN_ALREADY_SET = 430


code_and_detail = {
    CUSTOM_430_PIN_ALREADY_SET: (
        'pin already set',
        {'detail': 'Pin already set'}
    ),
}


def is_custom_status(status):
    return 430 <= status <= 499
