import os
import subprocess
import sys
import tempfile

from click.testing import CliRunner

from sequana_pipelines.mapper.main import main

from . import test_dir

sharedir = f"{test_dir}/data"


def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = """sequana_mapper --input-directory {}
            --working-directory {} --force""".format(
        sharedir, directory.name
    )
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()

    runner = CliRunner()
    results = runner.invoke(
        main,
        [
            "--input-directory",
            sharedir,
            "--reference-file",
            sharedir + "/measles.fa",
            "--working-directory",
            directory.name,
            "--force",
        ],
    )
    assert results.exit_code == 0


def test_standalone_script_minimap2():
    directory = tempfile.TemporaryDirectory()
    runner = CliRunner()
    results = runner.invoke(
        main,
        [
            "--input-directory",
            sharedir,
            "--reference-file",
            sharedir + "/measles.fa",
            "--working-directory",
            directory.name,
            "--force",
            "--aligner-choice",
            "minimap2",
        ],
    )
    assert results.exit_code == 0


def test_standalone_script_saf(tmpdir):
    directory = tempfile.TemporaryDirectory()

    runner = CliRunner()
    results = runner.invoke(
        main,
        [
            "--input-directory",
            sharedir,
            "--reference-file",
            sharedir + "/measles.fa",
            "--working-directory",
            directory.name,
            "--force",
            "--capture-annotation-file",
            sharedir + "/test.saf",
        ],
    )
    assert results.exit_code == 0


def test_full():

    with tempfile.TemporaryDirectory() as directory:
        print(directory)
        wk = directory

        cmd = "sequana_mapper --input-directory {} "
        cmd += " --working-directory {}  --force "
        cmd += " --reference-file " + sharedir + "/measles.fa"
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())

        stat = subprocess.call("sh mapper.sh".split(), cwd=wk)

        assert os.path.exists(wk + "/multiqc/multiqc_report.html")


def test_version():
    cmd = "sequana_mapper --version"
    subprocess.call(cmd.split())
