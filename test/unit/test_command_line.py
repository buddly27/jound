# :coding: utf-8

from scribe.command_line import main


def test_with_defaults():
    """Command executes successfully with defaults."""
    assert main([]) is None
