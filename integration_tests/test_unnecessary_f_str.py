from codemodder.codemods.remove_unnecessary_f_str import UnnecessaryFStr
from integration_tests.base_test import (
    BaseIntegrationTest,
    original_and_expected_from_code_path,
)


class TestLimitReadline(BaseIntegrationTest):
    codemod = UnnecessaryFStr
    code_path = "tests/samples/unnecessary_f_str.py"
    original_code, expected_new_code = original_and_expected_from_code_path(
        code_path, [(0, 'bad = "hello"\n')]
    )
    expected_diff = '--- \n+++ \n@@ -1,2 +1,2 @@\n-bad = f"hello"\n+bad = "hello"\n good = f"{2+3}"\n'
    expected_line_change = "1"
    change_description = UnnecessaryFStr.CHANGE_DESCRIPTION
