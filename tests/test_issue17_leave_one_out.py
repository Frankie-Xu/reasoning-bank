import ast
import unittest
from pathlib import Path
ROOT = Path(__file__).parents[1]
MODULES = [ROOT / "WebArena/memory_management.py", ROOT / "third_party/src/minisweagent/memory/memory_management.py"]
def _functions(path):
    tree = ast.parse(path.read_text())
    return {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
class Issue17Test(unittest.TestCase):
    def test_both_selectors_expose_leave_one_out_controls(self):
        for path in MODULES:
            funcs = _functions(path); self.assertTrue({"select_memory", "screening"} <= funcs.keys())
            for name in ("select_memory", "screening"):
                args = {a.arg for a in funcs[name].args.args + funcs[name].args.kwonlyargs}; self.assertIn("exclude_task_ids", args)
            source = path.read_text(); self.assertIn("str(sid) not in excluded", source); self.assertIn("excluded_ids.add(str(task_id))", source)
    def test_read_only_default_and_opt_in_append(self):
        for path in MODULES:
            rendered = ast.unparse(_functions(path)["screening"]); self.assertIn("append_current", rendered); self.assertIn("False", rendered)
if __name__ == "__main__": unittest.main()
