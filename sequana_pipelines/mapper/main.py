#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os
import sys

import click_completion
import rich_click as click

click_completion.init()

NAME = "mapper"

from sequana_pipetools import SequanaManager
from sequana_pipetools.options import *

help = init_click(
    NAME,
    groups={
        "Pipeline Specific": [
            "--aligner-choice",
            "--annotation-file",
            "--capture-annotation-file",
            "--create-bigwig",
            "--do-coverage",
            "--nanopore",
            "--pacbio",
            "--reference-file",
        ],
    },
)


@click.command(context_settings=help)
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickInputOptions)
@include_options_from(ClickGeneralOptions)
@click.option(
    "--aligner-choice",
    "mapper",
    default="bwa",
    type=click.Choice(["bwa", "bwa_split", "minimap2", "bowtie2"]),
    help="""Choose one of the valid mapper. bwa_split is experimental. it first split the fastq files in chunks of 1Mreads,
aligns the reads with bwa and merge back the sub BAM files. Should be equivalent to using bwa but could be used on
cluster to speed up analysis.""",
)
@click.option("--reference-file", required=True, help="You input reference file in fasta format")
@click.option("--annotation-file", help="Used by the sequana_coverage tool if provided")
@click.option("--do-coverage", is_flag=True, help="Use sequana_coverage (prokaryotes)")
@click.option(
    "--pacbio",
    is_flag=True,
    help="If set, automatically set the input-readtag to None and set minimap2 options to -x map-pb",
)
@click.option(
    "--nanopore",
    is_flag=True,
    help="If set, automatically set the input-readtag to None and set minimap2 options to -x map-ont",
)
@click.option("--create-bigwig", is_flag=True, help="create the bigwig files from the BAM files")
@click.option(
    "--capture-annotation-file",
    type=click.Path(),
    help="SAF formatted file for capture efficiency calculation with featureCounts.",
)
def main(**options):
    # the real stuff is here
    manager = SequanaManager(options, NAME)
    options = manager.options

    # creates the working directory
    manager.setup()

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

    if options.nanopore:
        cfg.minimap2.options = " -x map-ont "
        cfg.input_readtag = ""

    if options.capture_annotation_file:
        cfg.feature_counts.do = True
        cfg.feature_counts.options = "-F SAF "
        cfg.feature_counts.gff = os.path.abspath(options.capture_annotation_file)

    # Given the reference, let us compute its length and the index algorithm
    from sequana import FastA

    f = FastA(cfg.general.reference_file)
    N = f.get_stats()["total_length"]

    # seems to be a hardcoded values in bwa according to the documentation
    if N >= 2000000000:
        cfg["bwa"]["index_algorithm"] = "bwtsw"
        cfg["bwa_split"]["index_algorithm"] = "bwtsw"
    else:
        cfg["bwa"]["index_algorithm"] = "is"
        cfg["bwa_split"]["index_algorithm"] = "is"

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()
