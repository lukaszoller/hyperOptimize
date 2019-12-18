def isPositiveNumber(inputStr):  # Code for validation from: https://riptutorial.com/tkinter/example/27780/adding-validation-to-an-entry-widget
    if inputStr.isdigit():
        if int(inputStr) >= 0:
            return True
    else:
        return False