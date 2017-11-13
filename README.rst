#####
Jound
#####

Jound is a Python program which can invent new words from the analysis of a
list of words.

It can analyze a text and assemble all words it contains to a file. This list
of words can then be analyzed in order to generate a statistical file which
records the number of occurrences of each letter after a particular combination
of two letters. Finally, the statistical file can be used in order to generate
words using a `Markov chain`_.

.. code-block:: bash

    >>> jound assemble Moby_Dick.txt
    [jound] INFO: Assemble words from target: Moby_Dick.txt
    [jound] INFO: Writing 7756 words to ./words.txt

    >>> jound analyze words.txt
    [jound] INFO: Generate statistics from target: words.txt
    [jound] INFO: Writing statistics to ./stats.bin

    >>> jound generate 10 -s stats.bin
    gook
    shancity
    ruts
    woure
    duchic
    appermoven
    speriatrawk
    gantinge
    faltch
    jound


This project was inspired by this excellent article:
`La machine à inventer des mots`_ (in French)


.. _Markov chain: https://en.wikipedia.org/wiki/Markov_chain
.. _La machine à inventer des mots: https://sciencetonnante.wordpress.com/2015/10/16/la-machine-a-inventer-des-mots-video/
