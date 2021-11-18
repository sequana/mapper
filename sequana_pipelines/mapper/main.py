#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
##
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import sys
import os
import argparse
import subprocess

from sequana_pipetools.options import *
from sequana_pipetools.options import before_pipeline
from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog
from sequana_pipetools import SequanaManager

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
             choices=['bwa', 'minimap2', 'bowtie2'], 
            help="Choose one of the valid mapper")
        pipeline_group.add_argument("--reference-file", required=True,
             help="You input reference file in fasta format")
        pipeline_group.add_argument("--annotation-file",
            help="Used by the sequana_coverage tool if provided" )

        pipeline_group.add_argument("--do-coverage", action="store_true",
            help="Use sequana_coverage (prokaryotes)" )

        pipeline_group.add_argument("--pacbio", action="store_true",
            help="If set, automatically set the input-readtag to None and set minimap2 options to -x map-pb" )

        pipeline_group.add_argument("--create-bigwig", action="store_true",
            help="create the bigwig files from the BAM files" )

        self.add_argument("--run", default=False, action="store_true",
            help="execute the pipeline directly")


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
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])

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

        if options.pacbio:
            cfg.minimap2.options = " -x map-pb "
            cfg.input_readtag = ""



    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()

    if options.run:
        subprocess.Popen(["sh", '{}.sh'.format(NAME)], cwd=options.workdir)

if __name__ == "__main__":
    main()
