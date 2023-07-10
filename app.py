import ast
import sys

def translate_python_to_javascript(python_code):
    python_ast = ast.parse(python_code)
    javascript_code = translate_ast_to_javascript(python_ast)
    return javascript_code

def translate_ast_to_javascript(node):
    if isinstance(node, ast.Module):
        body = [translate_ast_to_javascript(stmt) for stmt in node.body]
        return '\n'.join(body)
    
    if isinstance(node, ast.FunctionDef):
        function_name = node.name
        parameters = [param.arg for param in node.args.args]
        body = [translate_ast_to_javascript(stmt) for stmt in node.body]
        function_code = f"function {function_name}({', '.join(parameters)}) " + "{{\n" + '\n'.join(body) + "\n}}"
        return function_code

    if isinstance(node, ast.Expr):
        return translate_ast_to_javascript(node.value)

    if isinstance(node, ast.BinOp):
        left = translate_ast_to_javascript(node.left)
        operator = translate_operator(node.op)
        right = translate_ast_to_javascript(node.right)
        return f"({left} {operator} {right})"

    if isinstance(node, ast.Return):
        value = translate_ast_to_javascript(node.value)
        return f"return {value};"

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Constant):
        return repr(node.value)

    if isinstance(node, ast.Assign):
        targets = [translate_ast_to_javascript(target) for target in node.targets]
        value = translate_ast_to_javascript(node.value)
        assignments = [f"var {target} = {value};" for target in targets]
        return '\n'.join(assignments)

    if isinstance(node, ast.If):
        test = translate_ast_to_javascript(node.test)
        body = [translate_ast_to_javascript(stmt) for stmt in node.body]
        else_body = [translate_ast_to_javascript(stmt) for stmt in node.orelse]
        if_else_code = f"if ({test}) " + "{{\n" + '\n'.join(body) + "\n}}"
        if_else_code += " else " + "{{\n" + '\n'.join(else_body) + "\n}}" if else_body else ""
        return if_else_code

    if isinstance(node, ast.While):
        test = translate_ast_to_javascript(node.test)
        body = [translate_ast_to_javascript(stmt) for stmt in node.body]
        while_code = f"while ({test}) " + "{{\n" + '\n'.join(body) + "\n}}"
        return while_code

    if isinstance(node, ast.Compare):
        left = translate_ast_to_javascript(node.left)
        comparators = [translate_ast_to_javascript(cmp) for cmp in node.comparators]
        operators = [translate_operator(op) for op in node.ops]
        comparisons = [f"{left} {operators[i]} {comparators[i]}" for i in range(len(operators))]
        return ' && '.join(comparisons)

    if isinstance(node, ast.Call):
        func = translate_ast_to_javascript(node.func)
        args = [translate_ast_to_javascript(arg) for arg in node.args]
        arguments = ', '.join(args)
        return f"{func}({arguments})"

    if isinstance(node, ast.Tuple):
        elements = [translate_ast_to_javascript(elt) for elt in node.elts]
        return f"[{', '.join(elements)}]"

    if isinstance(node, ast.Attribute):
        value = translate_ast_to_javascript(node.value)
        attr = node.attr
        return f"{value}.{attr}"

    raise NotImplementedError(f"Translation not implemented for {type(node).__name__}")

def translate_operator(operator):
    operator_mapping = {
        ast.Add: '+',
        ast.Sub: '-',
        ast.Mult: '*',
        ast.Div: '/',
        ast.Eq: '===',
        ast.NotEq: '!==',
        ast.Lt: '<',
        ast.LtE: '<=',
        ast.Gt: '>',
        ast.GtE: '>=',
    }
    return operator_mapping.get(type(operator), '')

def format_javascript_code(code, example_number, python_code):
    formatted_code = f"Example {example_number}:\n\nPython code:\n{python_code}\n\nTranslated JavaScript code:\n{code}"
    return formatted_code


def format_example_code(example_number, python_code, javascript_code):
    formatted_code = f"===============================\nExample {example_number}:\n\nPython code:\n\n{python_code}\n\nJavaScript code:\n\n{javascript_code}\n"
    return formatted_code

# Define the example Python code directly in the script
example_python_code = [
    """
# Example 1: Recursive function to calculate the factorial of a number
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

result = factorial(5)
""",
    """
# Example 2: Using a while loop to find the first Fibonacci number greater than 1000
a, b = 0, 1
while b <= 1000:
    a, b = b, a + b

result = b
""",
    """
# Example 3: String manipulation
message = "Hello, World!"
upper_message = message.upper()
lower_message = message.lower()
length = len(message)
"""
]

# Verifying if a specific file was provided
if len(sys.argv) > 1:
    # Get the file name
    file_name = sys.argv[1]
    
    # Read the content of the file
    with open(file_name, "r") as file:
        python_code = file.read()

    # Translate the Python code to JavaScript
    javascript_code = translate_python_to_javascript(python_code)
    
    # Format and print the resulting Python and JavaScript code
    formatted_code = format_example_code("File", python_code, javascript_code)
    print(formatted_code)
else:
    # Execute all default examples
    for example_number, python_code in enumerate(example_python_code, start=1):
        # Translate the Python code to JavaScript
        javascript_code = translate_python_to_javascript(python_code)
        
        # Format and print the resulting Python and JavaScript code
        formatted_code = format_example_code(example_number, python_code, javascript_code)
        print(formatted_code)