*** Settings ***
Resource    test_data.robot

*** Test Cases ***
My First Test Case
    Sleep   ${SHORT_SLEEP}
    Should Be True   ${False}    Element Not Found Exception

My Second Test Case
    Sleep   ${HIGH_SLEEP}