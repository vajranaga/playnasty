import pytest

from playnasty.cli import main


def test_readme_example(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--text", "HELLO WORLD", "--date", "230101"]) == 0
    assert capsys.readouterr().out == "Transformed text: ZEBNO6OTB9\n"


def test_show_boxes(capsys: pytest.CaptureFixture[str]) -> None:
    main(["--text", "AB", "--date", "230101", "--show-boxes"])
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Cipherbox 1:"
    assert lines[8] == "Cipherbox 2:"
    assert all(len(line.split()) == 6 for line in lines[1:7] + lines[9:15])
    assert lines[-1].startswith("Transformed text: ")


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        (["--text", "HI", "--date", "24-11-22"], "6 digits"),
        (["--text", "HI", "--date", "241301"], "not a real calendar date"),
        (["--text", "HI!", "--date", "230101"], "only A-Z"),
        (["--date", "230101"], "--text"),
    ],
)
def test_errors_exit_2(argv: list[str], message: str, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(argv)
    assert exc.value.code == 2
    assert message in capsys.readouterr().err
