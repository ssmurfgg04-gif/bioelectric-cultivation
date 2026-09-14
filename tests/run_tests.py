"""Test harness: python -m tests.run_tests [--full]"""

from __future__ import annotations

import sys


def main() -> int:
    full = "--full" in sys.argv
    from tests import test_units
    test_units.main()
    from tests import test_fidelity
    test_fidelity.main()
    from tests import test_d3_semantics
    test_d3_semantics.main()
    from tests import test_vmem_inference
    test_vmem_inference.main()
    if full:
        print("\n--- falsification suite (experiments) ---\n")
        from tests import test_falsification
        test_falsification.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())
