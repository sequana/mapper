
.. image:: https://badge.fury.io/py/sequana-mapper.svg
     :target: https://pypi.python.org/pypi/sequana_mapper

.. image:: https://github.com/sequana/mapper/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/mapper/actions/

.. image:: https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C3.11-blue.svg
    :target: https://pypi.python.org/pypi/sequana
    :alt: Python  3.9 | 3.10 | 3.11

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

This command will scan all files ending in .fastq.gz found in the local
directory, create a directory called mapper/ where a snakemake pipeline can be executed.::

    sequana_mapper --input-directory DATAPATH  --mapper bwa --create-bigwig
    sequana_mapper --input-directory DATAPATH  --mapper bwa --do-coverage


This creates a directory with the pipeline and configuration file. You will then need
to execute the pipeline::

    cd mapper
    sh mapper.sh  # for a local run

This launch a snakemake pipeline. See .sequana/profile/config.yaml to tune the behaviour of Snakemake.

Usage with apptainer
~~~~~~~~~~~~~~~~~~~~~

With apptainer, initiate the working directory as follows::

    sequana_rnaseq --use-apptainer 

Images are downloaded in the working directory but you can store them in a directory globally (e.g.):

    sequana_rnaseq --use-apptainer --apptainer-prefix ~/.sequana/apptainers

and then::

    cd rnaseq
    sh rnaseq.sh


Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- bamtools
- bwa
- multiqc
- sequana_coverage
- minimap2
- bowtie2
- deeptools

.. image:: https://raw.githubusercontent.com/sequana/mapper/main/sequana_pipelines/mapper/dag.png


Details
~~~~~~~~~

This pipeline runs **mapper** in parallel on the input fastq files (paired or not).
A brief sequana summary report is also produced. When using **--pacbio** option,
*-x map-pb* options is automatically added to the config.yaml file and the
readtag is set to None.

The BAM files are filtered to remove unmapped reads to keep BAM files to minimal size. However,
the multiqc and statistics to be found in  {sample}/bamtools_stats/ includes mapped and unmapped reads information. Each BAM file is stored in a directory named after the sample.



Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/mapper/main/sequana_pipelines/mapper/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file.


Changelog
~~~~~~~~~

========= ======================================================================
Version   Description
========= ======================================================================
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
