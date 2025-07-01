import os
import tempfile
import shutil
import pytest
from loc_counter import count_loc_eloc, scan_folder

def create_temp_file(content, suffix='.py'):
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

def test_count_loc_eloc_py():
    code = """
# コメント

def foo():
    pass  # インラインコメント

print('hello')
"""
    path = create_temp_file(code)
    loc, eloc = count_loc_eloc(path)
    os.remove(path)
    assert loc == 7
    assert eloc == 3

def test_count_loc_eloc_cpp():
    code = """
// コメント
int main() {
    /* block
    comment */
    return 0;
}
"""
    path = create_temp_file(code, suffix='.cpp')
    loc, eloc = count_loc_eloc(path)
    os.remove(path)
    assert loc == 7
    assert eloc == 3

def test_scan_folder():
    temp_dir = tempfile.mkdtemp()
    py_code = "print('a')\n# comment\nprint('b')\n"
    js_code = "// comment\nconsole.log('a');\nconsole.log('b');\n"
    py_path = os.path.join(temp_dir, 'a.py')
    js_path = os.path.join(temp_dir, 'b.js')
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(py_code)
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_code)
    results = scan_folder(temp_dir)
    shutil.rmtree(temp_dir)
    assert any('a.py' in r[0] and r[1] == 3 and r[2] == 2 for r in results)
    assert any('b.js' in r[0] and r[1] == 3 and r[2] == 2 for r in results)
