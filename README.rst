This is is the **mapper** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet

:Overview: This is a simple pipeline to map several FastQ files onto a reference using different mappers/aligners
:Input: A set of FastQ files.
:Output: A set of BAM files
:Status: draft
:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

You must install Sequana first::

    pip install sequana

Then, just install this package::

    pip install sequana_mapper


Usage
~~~~~

::

    sequana_pipelines_mapper --help
    sequana_pipelines_mapper --input-directory DATAPATH 

This creates a directory with the pipeline and configuration file. You will then need 
to execute the pipeline::

    cd mapper
    sh mapper.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can 
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s mapper.rules -c config.yaml --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- bamtools
- bwa
- multiqc
- sequana_coverage
- minimap2

.. image:: https://raw.githubusercontent.com/sequana/sequana_mapper/master/sequana_pipelines/mapper/dag.png


Details
~~~~~~~~~

This pipeline runs **mapper** in parallel on the input fastq files (paired or not). 
A brief sequana summary report is also produced.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_mapper/master/sequana_pipelines/mapper/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 


Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.8.4     * Fixing multiqc (synchronized with sequana updates) 
0.8.3     * add sequana_coverage rule. 
0.8.2     * add minimap2 mapper 
0.8.1     * fix bamtools stats rule to have different output name for multiqc
0.8.0     **First release.**
========= ====================================================================

