import sys
import os
import argparse

from sequana.pipelines_common import *
from sequana.snaketools import Module
from sequana import logger
logger.level = "INFO"

col = Colors()

NAME = "mapper"
m = Module(NAME)
m.is_executable()


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME):
        usage = col.purple(
            """This script prepares the sequana pipeline mapper layout to
            include the Snakemake pipeline and its configuration file ready to
            use.

            In practice, it copies the config file and the pipeline into a
            directory (mapper) together with an executable script

            For a local run, use :

                sequana_pipelines_mapper --input-directory PATH_TO_DATA

            For a run on a SLURM cluster:

                sequana_pipelines_mapper --input-directory PATH_TO_DATA

        """
        )
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        so = InputOptions()
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline")
        pipeline_group.add_argument("--mapper", default='bwa', 
             choices=['bwa', 'minimap2'])
        pipeline_group.add_argument("--reference-file", required=True, 
             )


def main(args=None):

    if args is None:
        args = sys.argv

    options = Options(NAME).parse_args(args[1:])

    manager = PipelineManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    cfg = manager.config.config

    # --------------------------------------------------- input  section
    cfg.input_directory = os.path.abspath(options.input_directory)
    cfg.input_pattern = options.input_pattern
    cfg.input_readtag = options.input_readtag
    cfg.paired_data = options.paired_data

    cfg.general.mapper = options.mapper
    cfg.general.reference_file = os.path.abspath(options.reference_file)

    manager.exists(cfg.general.reference_file)


    # checks read tag
    import glob
    filenames = glob.glob(cfg.input_directory+os.sep + cfg.input_pattern)
    if len(filenames) == 0:
        raise ValueError("Could not find any files with your pattern {} in {}".format(cfg.input_pattern, cfg.input_directory))

    if cfg.input_readtag:
        from sequana import FastQFactory
        try:
            ff = FastQFactory(cfg.input_directory + os.sep + cfg.input_pattern, read_tag=cfg.input_readtag)
        except:
            logger.warning("""Check the read tag and input patter/directory. You may
proceed but maybe the read tag is incorrect. It may be ignored when runing the
pipeline""")



    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()

