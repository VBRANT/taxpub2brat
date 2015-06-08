Notes on Pensoft
================

Originally these notes were purely to document the content of this folder. However, I am now extending them to serve as the basis for a short publication, possibly as a software article in Bioinformatics.

Purpose
-------

Hui wants to use clean, marked up documents as training data. A good source of such documents is Pensoft, who supply their published manuscripts in a variety of formats including TaxPub, which is appropriate for her purposes.

This folder contains the training data documents and all scripts and outputs associated with them.

TaxPub is… explanation here, link to source on git, link to Zookeys XML comparison article, etc

Files
-----

Three examples:

1. Yang ZH, Yu JY, Mao-Fa Y (2012) Two new species of Oxycera (Diptera, Stratiomyidae) from Ningxia, China. ZooKeys 198: 69-77. doi: 10.3897/zookeys.198.2624

2. Wei J-F, Feng J-N (2012) Two new species of Megacanthaspis Takagi (Hemiptera, Sternorrhyncha, Coccoidea, Diaspididae) from China. ZooKeys 210: 1–8. doi: 10.3897/zookeys.210.3071

3. Gobbi M, Priore C, Tattoni C, Lencioni V (2012) Surprising longhorned beetle (Coleoptera, Cerambycidae) richness along an Italian alpine valley. ZooKeys 208: 27–39. doi: 10.3897/zookeys.208.3193

For each file the TaxPub XML and PDF versions were downloaded from [Pensoft’s web-site](http://www.pensoft.net/).

The last four numbers of the DOI form the first four numbers in names of the downloaded files.

Notes
-----

The XML version does not correspond directly with the plain text in the PDF. For example, the academic editor section records the dates of  receiving, accepting and publishing, but the actions are `date-type` attributes and are not recorded as text, though that is how they are presented in the document; similarly keywords, where the words themselves are present in the XML version but the commas separating them are omitted. This is a not unreasonable re-purposing of the material but be aware it means that to simply extract text from the XML version will not produce the printed version.

The two text versions are different. In part, the Adobe output being produced in Windows has the usual two byte CRLF line feeds. Two textual differences to  note:

- hyphens in the PDF text are retained in the txt output, they are not present in the XML derived plain text version
- the key to species table is very different between the two versions, with extra line breaks and leaders in the pdf text version absent from the HTML derived version

The files’ content has not been corrected. For example, in Yang _et al_ (2012) the third word of abstract is left as `speices` rather than amended to `species`.

BRAT
----

Brief introduction to and explanation of BRAT (BioNLP Rapid Annotation Tool).

"online environment for collaborative text annotation" http://brat.nlplab.org/

stand-off format of files http://brat.nlplab.org/standoff.html

This script produces files that contain text-bound annotations only. Therefore, the annotation file's contents match the [BioNLP Shared Task 2011 format](http://2011.bionlp-st.org/home/file-formats). However, the file has the BRAT suffix of `.ann` instead of the BioNLP suffix of `.a1`.

Need paper to cite too

Scripts
-------

select-taxon-name.xsl - this is a stand-alone XSL to select taxon names from TaxPub documents. The taxon-name element fulfills two uses in TaxPub.  This XSL covers both uses. The first use of taxon-name is as simple inline mark up, usually within the `<italic>` and `</italic>` tags around a taxon name in the text. This use permits a relatively simple selection process, retrieving the text node for each taxon-name element. The second use of taxon-name is more involved, for the element is a part of a taxonomic treatment. As such its role is to break down the binomial into its constituent parts, each identified by child taxon-name-part elements. Therefore, having selected a taxon-name element, the XSL first attempts to retrieve an associated child text node. If successful, the text is formatted and written out in conjunction with a mark-up type of taxon-name. However, if a child text node is not found then the XSL attempts to retrieve child taxon-name-part nodes, using the taxon-name-part attribute as the mark-up type and the contents of the taxon-name-part elements child text node as the mark-up text.

taxpub2brat.py - this is a Python 3 script to produce an annotation file in BRAT stand-off format to mark-up and matching text extracted from a}

first stage - extract text, uses crude regex, but woerks because well-formed, valid XML. If that change, or if `<` and `>` are ever permitted in attributes then will have to revisit this regex. Tried to use XSL but became very complicated as sometimes extracted text needs to be followed by . having parsed XML into a node tree, lines lost so couldn't use them.

second stage - had working XSL so re-used that. This means the sdcript has an external dependency. Could be avoided if rewrite to use a parser within the script instead. output is in two parts, first the type of entity second the entity text.

third stage - use output from second part to `find` entities in text. Made easy beacuse entitites extracted in the order in which they occur in the text. In additon, XML is not formatted for printing so all words are complete. Therefoer, the entity can be found by a simple find function without havig to allow for the entity breaking over a line and so being hyphenated or any of the other compliocations that typically arise when searching for words in a text.



Installation
------------

Copy the two files, `taxpub2brat.py` and `select-taxon-name.xsl` to your working directory.

Requires Python3. Depending on your source Python installation you may need to install the LXML module too.

This script has been run successfully in both Windows and UNIX environments.

Use
---

Open a Terminal (UNIX) or Command Prompt (Windows) in your working directory and run the following command:

    python taxpub2brat.py <input_file_name>

where <input_file_name> the full name of your TaxPub document, including the XML file extension. For example:

    python taxpub2brat.py 2624-G-2-layout.xml

Outputs
-------

This will produce four new files:

    2624-G-2-layout.txt
    2624-G-2-layout.ann
    2624-G-2-layout-taxpub2brat.log
    2624-G-2-layout-taxpub2brat.txt
