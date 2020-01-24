*** Settings ***
Resource    test_data.robot

*** Test Cases ***
My Third Test Case
    Sleep   ${MEDIUM_SLEEP}
    Should Be True   ${False}    Alert Found

My Fourth Test Case
    Sleep   ${HIGH_SLEEP}