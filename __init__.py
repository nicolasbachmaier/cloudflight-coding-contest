"""
****************************************
author : Nicolas Bachmaier (AI student)
school : Johannes Kepler University Linz
created: 16.04.24 18:25
created for: CloudFlight Coding Contest
****************************************
"""
import ast
import glob
import os


class Colors:
    green = '\033[92m'
    red = '\033[91m'
    default = '\033[0m'


class Inputs:
    def __init__(self, func, ignore_first_line: bool = True):
        self.ignore_first_line = ignore_first_line
        self.func = func
        outputs_generated = self.generate_outputs()
        tests_passed = self.test_cases()
        if outputs_generated:
            print(f"{Colors.green}Outputs generated: {outputs_generated}{Colors.default}")
        else:
            print(f"{Colors.red}Outputs generated: {outputs_generated}{Colors.default}")
        if tests_passed:
            print(f"{Colors.green}All tests passed: {tests_passed}{Colors.default}")
        else:
            print(f"{Colors.red}All tests passed: {tests_passed}{Colors.default}")

    def parse_line(self, line):
        parts = line.split()
        args = []
        index = 0
        while index < len(parts):
            part = parts[index]
            if part.startswith(("'", '"')):
                start_index = index
                while index < len(parts) and not parts[index].endswith(("'", '"')):
                    index += 1
                if index < len(parts):
                    string_value = ' '.join(parts[start_index:index + 1])
                    args.append(ast.literal_eval(string_value))
                    index += 1
                else:
                    raise ValueError("Unclosed string literal")
            elif '.' in part:
                args.append(float(part))
                index += 1
            elif part.startswith('['):
                start_index = index
                while index < len(parts) and ']' not in parts[index]:
                    index += 1
                if index < len(parts):
                    list_str = ' '.join(parts[start_index:index + 1])
                    list_value = ast.literal_eval(list_str)
                    args.append(list_value)
                    index += 1
                else:
                    raise ValueError("Unclosed list literal")
            elif part.startswith('{'):
                start_index = index
                while index < len(parts) and '}' not in parts[index]:
                    index += 1
                if index < len(parts):
                    dict_str = ' '.join(parts[start_index:index + 1])
                    dict_value = ast.literal_eval(dict_str)
                    args.append(dict_value)
                    index += 1
                else:
                    raise ValueError("Unclosed dict literal")
            elif type(part) == str:
                args.append(part)
                index += 1
            else:
                args.append(int(part))
                index += 1
        return args

    def generate_outputs(self) -> bool:
        try:
            input_files = glob.glob('input/*.in')
            os.makedirs('output', exist_ok=True)

            for input_file in input_files:
                with open(input_file, 'r') as file:
                    if self.ignore_first_line: next(file)
                    output_lines = []
                    for line in file:
                        args = self.parse_line(line.strip())
                        output_line = str(self.func(*args))
                        output_lines.append(output_line)

                output_file = 'output/' + os.path.basename(input_file).replace('.in', '.out')
                with open(output_file, 'w') as file:
                    file.write('\n'.join(output_lines))

            return True
        except Exception as e:
            print(f"{Colors.red}An error occurred: {e}{Colors.default}")
            return False

    def test_cases(self) -> bool:
        try:
            testcase_files = glob.glob('testcases/*.in')
            all_tests_passed = True

            for test_file in testcase_files:
                with open(test_file, 'r') as input_file, open(test_file.replace('.in', '.out'), 'r') as expected_file:
                    if self.ignore_first_line:
                        next(input_file)

                    line_number = 1
                    for input_line, expected_output_line in zip(input_file, expected_file):
                        try:
                            args = self.parse_line(input_line.strip())
                            actual_output = str(self.func(*args))
                            if actual_output.strip() != expected_output_line.strip():
                                print(f"{Colors.red}Test failed for: {test_file}{Colors.default}")
                                print(f"{Colors.red}Line number: {line_number}{Colors.default}")
                                print(f"{Colors.red}Input: {input_line.strip()}{Colors.default}")
                                print(f"{Colors.red}Expected output: {expected_output_line.strip()}{Colors.default}")
                                print(f"{Colors.red}Actual output: {actual_output.strip()}{Colors.default}")
                                all_tests_passed = False
                                break
                        except Exception as e:
                            print(f"{Colors.red}Error occurred for: {test_file}{Colors.default}")
                            print(f"{Colors.red}Line number: {line_number}{Colors.default}")
                            print(f"{Colors.red}Input: {input_line.strip()}{Colors.default}")
                            print(f"{Colors.red}Error: {str(e)}{Colors.default}")
                            all_tests_passed = False
                            break
                        line_number += 1

            return all_tests_passed
        except Exception as e:
            print(f"{Colors.red}An error occurred: {e}{Colors.default}")
            return False
