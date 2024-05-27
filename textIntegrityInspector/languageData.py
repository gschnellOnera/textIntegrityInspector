

# Elementary data dictionary
elementaryData = {
    'acuteAccentsLower': "á, é, í, ó, ú",
    'acuteAccentsUpper': "Á, É, Í, Ó, Ú",
    'graveAccentLower': "à, è, ù",
    'graveAccentUpper': "À, È, Ù",
    'circumflexAccentsLower': "â, ê, î, ô, û",
    'circumflexAccentsUpper': "Â, Ê, Î, Ô, Û",
    'diaeresisLower': "ä, ë, ï, ö, ü, ÿ",
    'diaeresisUpper': "Ä, Ë, Ï, Ö, Ü",
    'cedilla': "Ç, ç",
    'ligatures': "Œ, œ, Æ, æ",
    'punctuation': " , …, ’, ‘, «, »",
    'math': "², ±, μ",
    'unit': "°, €",
    'edition': "§, ©",
    'eszett': "ß",  # German character
    'tildes': "ñ, Ñ, á, é, í, ó, ú, Á, É, Í, Ó, Ú"  # Spanish characters with tildes
}

# Language-specific data dictionary
languageData = {
    'fr': [
        'acuteAccentsLower',
        'acuteAccentsUpper',
        'graveAccentLower',
        'graveAccentUpper',
        'circumflexAccentsLower',
        'circumflexAccentsUpper',
        'diaeresisLower',
        'diaeresisUpper',
        'cedilla',
        'ligatures',
        'punctuation',
        'math',
        'unit',
        'edition'
    ],
    'en': [
        'punctuation',
        'math',
        'unit',
        'edition'
    ],
    'de': [
        'acuteAccentsLower',
        'acuteAccentsUpper',
        'diaeresisLower',
        'diaeresisUpper',
        'ligatures',
        'punctuation',
        'math',
        'unit',
        'edition'
    ],
    'es': [
        'acuteAccentsLower',
        'acuteAccentsUpper',
        'diaeresisLower',
        'diaeresisUpper',
        'ligatures',
        'punctuation',
        'math',
        'unit',
        'edition'
    ],
    'it': [
        'acuteAccentsLower',
        'acuteAccentsUpper',
        'graveAccentLower',
        'graveAccentUpper',
        'circumflexAccentsLower',
        'circumflexAccentsUpper',
        'diaeresisLower',
        'diaeresisUpper',
        'punctuation',
        'math',
        'unit',
        'edition'
    ]
}


                    
def display_languages():
    ascii = ','.join([chr(c) for c in range(0x20,0x80)] + ['\\n','\\r','\\t'])
    print("Supported Languages and Accepted Characters:")
    print(f"Accepte all normal ASCII characters: {ascii}")
    accepted_chars=''
    for language, charsDef in languageData.items():
        for group_char in charsDef:
            accepted_chars += ', ' + elementaryData[group_char]
        print(f"\nLanguage: {language}\nAccepted Characters: {accepted_chars[2:]}")

def get_special_characters(language):
    specific_chars = languageData.get(language, [])
    return ''.join(elementaryData[key] for key in specific_chars).replace(",", "").replace(" ", "")

