from flask import Flask, render_template, request

app = Flask(__name__)

def int_to_binary_padded(number, total_bits):
    if number is None:
        return ""
    binary_str = bin(number)[2:].zfill(total_bits)
    return binary_str

@app.route("/", methods=["GET", "POST"])
def index():
    result_text = None
    binary_calculation = None
    a_val = ''
    b_val = ''
    selected_op = 'AND'

    if request.method == 'POST':
        try:
            a_val = request.form.get('a', '')
            b_val = request.form.get('b', '')
            selected_op = request.form.get('operation', 'AND')

            a = int(a_val)
            b = int(b_val) if b_val else None

            max_bits = 0
            if a is not None:
                 max_bits = max(max_bits, len(bin(abs(a))[2:]))
            if b is not None:
                 max_bits = max(max_bits, len(bin(abs(b))[2:]))
            max_bits = max(max_bits, 4)


            if selected_op == 'AND' and b is not None:
                decimal_result = a & b
                op_symbol = '&'
                bin_a = int_to_binary_padded(a, max_bits)
                bin_b = int_to_binary_padded(b, max_bits)
                bin_result = int_to_binary_padded(decimal_result, max_bits)

                binary_calculation = f"""
  {bin_a}  ({a})
{op_symbol} {bin_b}  ({b})
{'-' * (max_bits + 2)}
  {bin_result}  ({decimal_result})
"""
                result_text = f"{a} {op_symbol} {b} = {decimal_result}"

            elif selected_op == 'OR' and b is not None:
                decimal_result = a | b
                op_symbol = '|'
                bin_a = int_to_binary_padded(a, max_bits)
                bin_b = int_to_binary_padded(b, max_bits)
                bin_result = int_to_binary_padded(decimal_result, max_bits)
                binary_calculation = f"""
  {bin_a}  ({a})
{op_symbol} {bin_b}  ({b})
{'-' * (max_bits + 2)}
  {bin_result}  ({decimal_result})
"""
                result_text = f"{a} {op_symbol} {b} = {decimal_result}"

            elif selected_op == 'XOR' and b is not None:
                decimal_result = a ^ b
                op_symbol = '^'
                bin_a = int_to_binary_padded(a, max_bits)
                bin_b = int_to_binary_padded(b, max_bits)
                bin_result = int_to_binary_padded(decimal_result, max_bits)
                binary_calculation = f"""
  {bin_a}  ({a})
{op_symbol} {bin_b}  ({b})
{'-' * (max_bits + 2)}
  {bin_result}  ({decimal_result})
"""
                result_text = f"{a} {op_symbol} {b} = {decimal_result}"

            elif selected_op == 'NOT':
                decimal_result = ~a
                op_symbol = '~'

                bin_a = bin(a)[2:]
                bin_a_padded = bin_a.zfill(max_bits)

                bin_result_display = "".join('1' if bit == '0' else '0' for bit in bin_a_padded)

                binary_calculation = f"""
  {bin_a_padded}  ({a})
{op_symbol}
{'-' * (max_bits + 2)}
  {bin_result_display}  (Visual flip)
"""
                result_text = f"{op_symbol}{a} = {decimal_result} (Python's result)"


            elif selected_op == 'LSHIFT' and b is not None:
                 if b >= 0:
                   decimal_result = a << b
                   op_symbol = '<<'
                   bin_a = int_to_binary_padded(a, max_bits)
                   result_max_bits = max(max_bits, len(bin(abs(decimal_result))[2:]))
                   bin_result = int_to_binary_padded(decimal_result, result_max_bits)

                   bin_a_display = int_to_binary_padded(a, result_max_bits)


                   binary_calculation = f"""
  {bin_a_display}  ({a})
{op_symbol} {b} bits
{'-' * (result_max_bits + 2)}
  {bin_result}  ({decimal_result})
"""
                   result_text = f"{a} {op_symbol} {b} = {decimal_result}"
                 else:
                   result_text = "⚠️ Shift amount must be non-negative."

            elif selected_op == 'RSHIFT' and b is not None:
                if b >= 0:
                    decimal_result = a >> b
                    op_symbol = '>>'
                    bin_a = int_to_binary_padded(a, max_bits)
                    bin_result = int_to_binary_padded(decimal_result, max(max_bits, len(bin(abs(decimal_result))[2:])))

                    binary_calculation = f"""
  {bin_a}  ({a})
{op_symbol} {b} bits
{'-' * (max_bits + 2)}
  {bin_result}  ({decimal_result})
"""
                    result_text = f"{a} {op_symbol} {b} = {decimal_result}"
                else:
                    result_text = "⚠️ Shift amount must be non-negative."

            else:
                result_text = "⚠️ Invalid operation or missing input."
        except ValueError:
            result_text = "⚠️ Please enter valid integer numbers."
        except Exception as e:
            result_text = f"⚠️ An error occurred: {e}"


    return render_template("index.html",
                           result_text=result_text,
                           binary_calculation=binary_calculation,
                           a_val=a_val,
                           b_val=b_val,
                           selected_op=selected_op)

if __name__ == "__main__":
    app.run(debug=True)