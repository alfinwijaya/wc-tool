import unittest
import subprocess

class TestCCWCScript(unittest.TestCase):
    def test_count_bytes(self):
        cmd_args = ['python', 'ccwc.py', '-c', 'test.txt']
    
        result = subprocess.run(cmd_args, capture_output=True, text=True)

        expected_output = '342190 test.txt'
        self.assertIn(expected_output, result.stdout)

    def test_count_lines(self):
        cmd_args = ['python', 'ccwc.py', '-l', 'test.txt']
    
        result = subprocess.run(cmd_args, capture_output=True, text=True)

        expected_output = '7145 test.txt'
        self.assertIn(expected_output, result.stdout)

    def test_count_words(self):
        cmd_args = ['python', 'ccwc.py', '-w', 'test.txt']
    
        result = subprocess.run(cmd_args, capture_output=True, text=True)

        expected_output = '58164 test.txt'
        self.assertIn(expected_output, result.stdout)

    def test_count_characters(self):
        cmd_args = ['python', 'ccwc.py', '-m', 'test.txt']
    
        result = subprocess.run(cmd_args, capture_output=True, text=True)

        expected_output = '339292 test.txt'
        self.assertIn(expected_output, result.stdout)

    def test_using_all_options(self):
        cmd_args = ['python', 'ccwc.py', '-c', 'test.txt', '-l', 'test.txt', '-w', 'test.txt', '-m', 'test.txt']
    
        result = subprocess.run(cmd_args, capture_output=True, text=True)

        expected_output = '342190 7145 58164 339292 test.txt'
        self.assertIn(expected_output, result.stdout)

    def test_no_optional_args(self):
        cmd_args = ['python', 'ccwc.py', 'test.txt']
    
        result = subprocess.run(cmd_args, capture_output=True, text=True)

        expected_output = '342190 7145 58164 test.txt'
        self.assertIn(expected_output, result.stdout)

    def test_multiple_files(self):
        cmd_args = ['python', 'ccwc.py', '-c', 'test.txt', '-l', 'test.txt', '-c', 'test2.txt']
    
        result = subprocess.run(cmd_args, capture_output=True, text=True)

        # I make two version because the order can be inconsistent
        expected_output = [ f'342190 7145 test.txt\n504 test2.txt\n342694 7145 total\n',
                            f'504 test2.txt\n342190 7145 test.txt\n342694 7145 total\n']
        self.assertIn(result.stdout, expected_output)

    def test_file_not_found(self):
        cmd_args = ['python', 'ccwc.py', '-c', 'test3.txt']
    
        result = subprocess.run(cmd_args, capture_output=True, text=True)

        expected_output = f'ccwc: test3.txt: No such file or directory'
        self.assertIn(expected_output, result.stdout)

    def test_using_standard_input(self):
        ps_command =  (
            '$OutputEncoding = [console]::OutputEncoding = [System.Text.Encoding]::UTF8;'
            'cat test.txt | python ccwc.py -c -l -w -m'
        )

        result = subprocess.run(['powershell', ps_command], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0, f"Command failed with return code {result.returncode}")

        expected_output = "342190 7145 58164 339292"
        self.assertIn(expected_output, result.stdout)

    def test_using_standard_input_without_args(self):
        ps_command =  (
            '$OutputEncoding = [console]::OutputEncoding = [System.Text.Encoding]::UTF8;'
            'cat test.txt | python ccwc.py'
        )

        result = subprocess.run(['powershell', ps_command], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0, f"Command failed with return code {result.returncode}")

        expected_output = "342190 7145 58164"
        self.assertIn(expected_output, result.stdout)

if __name__ == "__main__":
    unittest.main()