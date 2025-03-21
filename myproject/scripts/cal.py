# def calculator(num1, operation, num2):
#      try:
#           num1 = float(num1)
#           num2 = float(num2)
#      #    num1 = float(input("first Number: "))
#      #    num2 = float(input("Second Number: "))
#      #    operation = input ("Choose Operator: (+) (*) (-) (/) (%):  ")
#           match operation:
#                case "+":
#                     return(num1 + num2)
#                case "*":
#                     return(num1 * num2)
#                case "-":
#                     return(num1 - num2)
#                case "/":
#                     return(num1 / num2)
#                case "%":
#                     return(num1 % num2)
#                case "**":
#                     return(num1**num2)
#                case _:
#                     return("Error: Wrong Operation")

#      except ZeroDivisionError:
#           return ("Division by Zero is not allowed")
#      except ValueError:
#           return("Enter Numbers Only!: ")
#      except OverflowError:
#           return("Number is too large")



# function calculate() {
#     const expression = document.getElementById('expression').textContent;
#     try {
#         let processedExpr = expression
#             .replace(/×/g, '*')
#             .replace(/÷/g, '/')
#             .replace(/π/g, 'Math.PI')
#             .replace(/sin\(/g, 'Math.sin(')
#             .replace(/cos\(/g, 'Math.cos(')
#             .replace(/tan\(/g, 'Math.tan(')
#             .replace(/log\(/g, 'Math.log10(')
#             .replace(/ln\(/g, 'Math.log(')
#             .replace(/sqrt\(/g, 'Math.sqrt(')
#             .replace(/\^/g, '**');

#         const result = eval(processedExpr);
#         document.getElementById('result').textContent = result;
#         addToHistory(expression, result);
#     } catch (error) {
#         document.getElementById('result').textContent = 'Error';
#     }
# }