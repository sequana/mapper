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
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
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
             choices=['bwa', 'minimap2', 'bowtie2'])
        pipeline_group.add_argument("--reference-file", required=True,
             )
        pipeline_group.add_argument("--annotation-file",
            help="Used by the sequana_coverage tool if provided" )

        pipeline_group.add_argument("--do-coverage", action="store_true",
            help="Use sequana_coverage (prokaryotes)" )

        pipeline_group.add_argument("--create-bigwig", action="store_true",
            help="create the bigwig files from the BAM files" )


def main(args=None):

    if args is None:
        args = sys.argv

    init_pipeline(NAME)

    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])

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

    if options.annotation_file:
        cfg.general.annotation_file = os.path.abspath(options.annotation_file)
        manager.exists(cfg.general.annotation_file)

    if options.do_coverage:
        cfg.sequana_coverage.do = True

    if options.create_bigwig:
        cfg.general.create_bigwig = True


    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()

