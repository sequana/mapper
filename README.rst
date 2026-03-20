
.. image:: https://badge.fury.io/py/sequana-mapper.svg
     :target: https://pypi.python.org/pypi/sequana_mapper

.. image:: https://github.com/sequana/mapper/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/mapper/actions/

.. image:: https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%20-blue.svg
    :target: https://pypi.python.org/pypi/sequana
    :alt: Python 3.9 | 3.10 | 3.11

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
   :target: http://joss.theoj.org/papers/10.21105/joss.00352
   :alt: JOSS (journal of open source software) DOI

This is the **mapper** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet

:Overview: This is a simple pipeline to map several FastQ files onto a reference using different mappers/aligners
:Input: A set of FastQ files (illumina, pacbio, etc).
:Output: A set of BAM files (and/or bigwig) and HTML report
:Status: Production
:Documentation: This README file, and https://sequana.readthedocs.io
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi:10.21105/joss.00352

Installation
~~~~~~~~~~~~

If you already have all requirements, you can install the packages using pip::

    pip install sequana_mapper --upgrade

You will need third-party software such as fastqc. Please see below for details.

Usage
~~~~~

Scan FastQ files in a directory and set up the pipeline (replace ``DATAPATH`` and ``genome.fa`` with your inputs)::

    sequana_mapper --input-directory DATAPATH --reference-file genome.fa --aligner-choice bwa
    sequana_mapper --input-directory DATAPATH --reference-file genome.fa --aligner-choice bwa --do-coverage
    sequana_mapper --input-directory DATAPATH --reference-file genome.fa --aligner-choice bwa --create-bigwig

For long-read data, use the dedicated presets::

    sequana_mapper --input-directory DATAPATH --reference-file genome.fa --pacbio     # sets minimap2 -x map-pb
    sequana_mapper --input-directory DATAPATH --reference-file genome.fa --nanopore   # sets minimap2 -x map-ont

For capture-seq projects (feature counting)::

    sequana_mapper --input-directory DATAPATH --reference-file genome.fa --capture-annotation-file targets.saf

This creates a ``mapper/`` directory with the pipeline and configuration file. Execute the pipeline locally::

    cd mapper
    sh mapper.sh

See ``.sequana/profile/config.yaml`` to tune Snakemake behaviour (cores, cluster settings, etc.).

Usage with apptainer
~~~~~~~~~~~~~~~~~~~~~

With apptainer, initiate the working directory as follows::

    sequana_mapper --input-directory DATAPATH --reference-file genome.fa --use-apptainer

Images are downloaded in the working directory but you can store them in a shared location::

    sequana_mapper --input-directory DATAPATH --reference-file genome.fa --use-apptainer --apptainer-prefix ~/.sequana/apptainers

and then::

    cd mapper
    sh mapper.sh


Requirements
~~~~~~~~~~~~

This pipeline requires the following executables (install via bioconda/conda):

- **bwa** — short-read aligner (default)
- **minimap2** — long-read aligner (PacBio / Nanopore)
- **bowtie2** — alternative short-read aligner
- **samtools** / **sambamba** — BAM processing
- **bamtools** — BAM statistics
- **deeptools** — bigwig generation (``bamCoverage``)
- **bedtools** — genome arithmetic
- **subread** — feature counting (``featureCounts``, capture-seq only)
- **mosdepth** — fast coverage depth
- **seqkit** — FASTQ statistics
- **multiqc** — aggregated HTML report
- **sequana_coverage** — coverage analysis (prokaryotes)

Install all dependencies at once::

    mamba env create -f environment.yml

.. image:: https://raw.githubusercontent.com/sequana/mapper/main/sequana_pipelines/mapper/dag.png


Details
~~~~~~~~~

This pipeline maps FastQ files (paired or single-end) in parallel onto a reference genome and produces
filtered BAM files, a MultiQC HTML report, and optionally coverage tracks and feature counts.

**Aligner choice** (``--aligner-choice``):

- ``bwa`` (default) — BWA-MEM; index algorithm is auto-selected (``is`` or ``bwtsw``) based on reference size
- ``bwa_split`` — experimental; splits large FastQs into 1 M-read chunks for parallel BWA jobs, then merges
- ``minimap2`` — long-read aligner; use ``--pacbio`` (sets ``-x map-pb``) or ``--nanopore`` (sets ``-x map-ont``)
- ``bowtie2`` — standard short-read aligner

**BAM filtering**: unmapped reads are removed to minimise file size. Statistics reported by MultiQC
(in ``{sample}/bamtools_stats/``) still include both mapped and unmapped read counts.

**Optional outputs**:

- ``--do-coverage`` — runs ``sequana_coverage`` for depth-of-coverage analysis (prokaryotes)
- ``--create-bigwig`` — generates bigwig files via ``bamCoverage`` (deeptools)
- ``--capture-annotation-file`` — enables ``featureCounts`` for capture-seq efficiency metrics



Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/mapper/main/sequana_pipelines/mapper/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file.


Changelog
~~~~~~~~~

========= ======================================================================
Version   Description
========= ======================================================================
1.4.1     * update to use wrappers.shells and wrappers.snippets
            drop wrappers usage
1.4.0     * update wrappers to v24.8.29
          * update sequana_pipetools requirement to >=1.5
1.3.1     * remove temp on BWA BAM file (more practical to keep them)
1.3.0     * uses new sequana_coverage wrapper
1.2.1     * fix bwa_split bwa aggreate stage (bug fix)
1.2.0     * Implement a bwa_split method to speed up mapping of very large
            fastq files.
1.1.0     * BAM files are now filtered to remove unmapped reads
          * set wrappers branch in config file and update pipeline.
          * refactorise to use click and new sequana-pipetools
1.0.0     * Use latest sequana-wrappers and graphviz apptainer
0.12.0    * Use latest pipetools and add singularity containers
0.11.1    * Fix typo when setting coverage to True and allow untagged filenames
0.11.0    * implement feature counts for capture-seq projects
0.10.1    * remove getlogdir and getname
0.10.0    * use new wrappers framework
0.9.0     * fix issue with logger and increments requirements
          * add new option --pacbio to automatically set the options for
            pacbio data (-x map-pb and readtag set to None)
0.8.13    * add the thread option in minimap2 case
0.8.12    * factorise multiqc rule
0.8.11    * Implemente the --from-project option and new framework
          * custom HTMrLl report
0.8.10    * change samtools_depth rule and switched to bam2cov to cope with null
            coverage
0.8.9     * fix requirements
0.8.8     * fix pipeline rule for bigwig + renamed output_bigwig into
            create_bigwig; fix the multiqc config file
0.8.7     * fix config file creation (for bigwig)
0.8.6     * added bowtie2 mapper + bigwig as output, make coverage optional
0.8.5     * create a sym link to the HTML report. Better post cleaning.
0.8.4     * Fixing multiqc (synchronized with sequana updates)
0.8.3     * add sequana_coverage rule.
0.8.2     * add minimap2 mapper
0.8.1     * fix bamtools stats rule to have different output name for multiqc
0.8.0     **First release.**
========= ======================================================================


Contribute & Code of Conduct
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To contribute to this project, please take a look at the
`Contributing Guidelines <https://github.com/sequana/sequana/blob/main/CONTRIBUTING.rst>`_ first. Please note that this project is released with a
`Code of Conduct <https://github.com/sequana/sequana/blob/main/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.
