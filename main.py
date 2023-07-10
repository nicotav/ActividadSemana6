import ast

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
        function_code = f"function {function_name}({', '.join(parameters)}) " + "{\n" + '\n'.join(body) + "\n}"
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

    raise NotImplementedError(f"Translation not implemented for {type(node).__name__}")

def translate_operator(operator):
    operator_mapping = {
        ast.Add: '+',
        ast.Sub: '-',
        ast.Mult: '*',
        ast.Div: '/',
    }
    return operator_mapping.get(type(operator), '')

# Example usage:
python_code = """
def add(a, b):
    return a + b
"""

javascript_code = translate_python_to_javascript(python_code)
print(javascript_code)
