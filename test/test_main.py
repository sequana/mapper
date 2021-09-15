import easydev
import os
import tempfile
import subprocess
import sys

from . import test_dir

sharedir = f"{test_dir}/data"

def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = """sequana_mapper --input-directory {} 
            --working-directory {} --force""".format(sharedir, directory.name)
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()
    import sequana_pipelines.mapper.main as m
    sys.argv = ["test", "--input-directory", sharedir, 
            "--reference-file", sharedir + "/measles.fa",
            "--working-directory", directory.name, "--force"]
    m.main()


def test_standalone_script_minimap2():
    directory = tempfile.TemporaryDirectory()
    import sequana_pipelines.mapper.main as m
    sys.argv = ["test", "--input-directory", sharedir, 
            "--reference-file", sharedir + "/measles.fa",
            "--working-directory", directory.name, "--force", "--mapper", "minimap2"]
    m.main()

def test_full():

    with tempfile.TemporaryDirectory() as directory:
        print(directory)
        wk = directory

        cmd = "sequana_mapper --input-directory {} "
        cmd += " --working-directory {}  --force "
        cmd += " --reference-file "+  sharedir + "/measles.fa"
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())

        stat = subprocess.call("sh mapper.sh".split(), cwd=wk)

        assert os.path.exists(wk + "/multiqc/multiqc_report.html")

def test_version():
    cmd = "sequana_mapper --version"
    subprocess.call(cmd.split())

