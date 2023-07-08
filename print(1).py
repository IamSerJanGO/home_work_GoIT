result = None
operand = None
operator = None
wait_for_number = True
wait_for_number2 = False
operator_flag = False
finish_flag = True

while finish_flag:
    while wait_for_number:
        result = input('Enter yor number: ')
        try:
            result = float(result)
            operator_flag = True
            wait_for_number = False
        except ValueError:
            print(f"{result} is not correct")
    while operator_flag:
        operator = input('Enter your operator: ')
        if operator in '+-*/=':
            wait_for_number2 = True
            operator_flag = False
        # elif operator == '=':
        #     print(result)
        #     finish_flag = False
        else:
            print(f'{operator} is not correct !')
    if operator == '=':
        print(result)
        break

    while wait_for_number2:
        operand = input("Enter your number: ")
        try:
            operand = float(operand)
            wait_for_number2 = False
            operator_flag = True
            if operator == "+":
                result += operand
            elif operator == '-':
                result -= operand
            elif operator == '*':
                result *= operand
            elif operator == '/':
                if operand != 0:
                    result /= operand
                else:
                    print("Error: Division by zero!")
                    wait_for_number2 = True

        except ValueError:
            print(f'{operand} is not correct')
