import sys
import os
import argparse

from sequana_pipetools.options import *
from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog

col = Colors()

NAME = "mapper"


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            epilog=epilog,
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

    def parse_args(self, *args):
        args_list = list(*args)
        if "--from-project" in args_list:
            if len(args_list)>2:
                msg = "WARNING [sequana]: With --from-project option, " + \
                        "pipeline and data-related options will be ignored."
                print(col.error(msg))
            for action in self._actions:
                if action.required is True:
                    action.required = False
        options = super(Options, self).parse_args(*args)
        return options



def main(args=None):

    if args is None:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    from sequana_pipetools.options import before_pipeline
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])


    from sequana.pipelines_common import SequanaManager

    # the real stuff is here
    manager = SequanaManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    if options.from_project is None:
        cfg = manager.config.config

        # --------------------------------------------------- input  section
        cfg.input_directory = os.path.abspath(options.input_directory)
        cfg.input_pattern = options.input_pattern
        cfg.input_readtag = options.input_readtag

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
