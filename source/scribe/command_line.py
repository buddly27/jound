# :coding: utf-8

import os
import sys
import re
import argparse
import logging
import codecs
import string

import requests
import numpy as np

logging.basicConfig(
    stream=sys.stderr, level=logging.INFO,
    format="[%(name)s] %(levelname)s: %(message)s"
)

logger = logging.getLogger("scribe")


def construct_parser():
    """Return argument parser."""
    parser = argparse.ArgumentParser(
        prog="scribe",
        description="A word generator using statistics from a book",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose_count",
        action="count", default=0,
        help="increases log verbosity for each occurrence."
    )

    subparsers = parser.add_subparsers(
        title="Subcommands",
        description="Additional subcommands.",
        dest="subcommand"
    )

    # Assemble sub-parser

    assemble_subparser = subparsers.add_parser(
        "assemble", help="Assemble all world contained in a file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    assemble_subparser.add_argument(
        "target", help="Path to the targeted file to analyse."
    )

    assemble_subparser.add_argument(
        "-o", "--output",
        help="Path to the generated file.",
        default=os.path.join(os.getcwd(), "words.txt")
    )

    assemble_subparser.add_argument(
        "-s", "--start", type=int,
        help="Cut off the targeted content before this index value.",
    )

    assemble_subparser.add_argument(
        "-e", "--end", type=int,
        help="Cut off the targeted content after this index value.",
    )

    # Analyze sub-parser

    analyze_subparser = subparsers.add_parser(
        "analyze", help=(
            "Process a list of work to generate transition probabilities."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    analyze_subparser.add_argument(
        "target", help="Path to the list of words to process."
    )

    analyze_subparser.add_argument(
        "-o", "--output",
        help="Path to the generated file.",
        default=os.path.join(os.getcwd(), "probability.bin")
    )

    return parser


def main(arguments=None):
    """Scribe command line interface."""
    if arguments is None:
        arguments = []

    # Process arguments.
    parser = construct_parser()
    namespace = parser.parse_args(arguments)

    logger.setLevel(max(2 - namespace.verbose_count, 0) * 10)

    if namespace.subcommand == "assemble":
        logger.info("Assemble words from target: {0}".format(namespace.target))

        try:
            output = validate_output(namespace.output)
            content = fetch_target_content(
                namespace.target,
                start=namespace.start,
                end=namespace.end
            )

            words = set()
            for word in yield_words_from_content(content):
                words.add(word)

            logger.info("Writing {0} words to {1}".format(len(words), output))

            with open(output, "w") as f:
                f.write("\n".join(sorted(words)))

        except Exception as err:
            logger.error(
                "[{0}] {1}".format(err.__class__.__name__, str(err))
            )

    elif namespace.subcommand == "analyze":
        logger.info(
            "Generate probabilities from target: {0}".format(namespace.target)
        )

        try:
            output = validate_output(namespace.output)
            content = fetch_target_content(namespace.target)
            matrix = create_probability_matrix_from_words(content.split("\n"))
            matrix.tofile(output)

        except Exception as err:
            logger.error(
                "[{0}] {1}".format(err.__class__.__name__, str(err))
            )


def validate_output(path):
    """Return validated output *path*.

    Raise :exc:`IOError` if the output directory is inaccessible.

    """
    output = os.path.abspath(path)
    output_directory = os.path.dirname(output)
    if not os.access(output_directory, os.W_OK):
        raise IOError(
            "The output directory is inaccessible: {0}".format(
                output_directory
            )
        )

    return output


def fetch_target_content(target, start=None, end=None):
    """Return content from *target*.

    *target* can be a file or a url.

    *start* and *end* indices can be set to return a particular slice of the
    content.

    Example::

        >>> fetch_target_content(
        ...     "https://www.gutenberg.org/files/2701/old/moby10b.txt",
        ...     start=35044, end=35302
        ... )
        CHAPTER 1\\r\\n\\r\\nLoomings.\\r\\n\\r\\n\\r\\nCall me Ishmael.
        Some years ago--never mind how long\\r\\nprecisely--having little or no
        money in my purse, and nothing\\r\\nparticular to interest me on shore,
        I thought I would sail about a\\r\\nlittle and see the watery part of
        the world.

    """
    if re.match("^https?://", target):
        r = requests.get(target)
        if r.status_code is not 200:
            raise IOError(
                "The targeted url is inaccessible: {0}".format(target)
            )

        r.encoding = "ISO-8859-1"
        return r.text[start:end]

    target_file = os.path.abspath(target)
    if not os.path.isfile(target_file) and os.access(target_file, os.R_OK):
        raise IOError(
            "The targeted file is not readable: {0}".format(target_file)
        )

    with codecs.open(target_file, "r", encoding="ISO-8859-1") as f:
        return f.read()[start:end]


def yield_words_from_content(content):
    """Yield each word found in *content*.

    Filter out whitespaces, numbers and punctuation.

    Example::

        >>> content = (
        ...     "Call me Ishmael.  Some years ago--never mind how long "
        ...     "precisely--having little or no money in my purse, and nothing"
        ... )
        >>> list(yield_words_from_content(content))
        [
            "Call", "me", "Ishmael", "Some", "years", "ago", "never", "mind",
            "how", "long", "precisely", "having", "little", "or", "no", "money",
            "in", "my", "purse", "and"
        ]

    """
    word = ""

    for letter in content:
        if (
            letter not in string.whitespace and
            letter not in string.punctuation and
            not letter.isdigit()
        ):
            word += letter
        elif len(word) > 0:
            yield word
            word = ""


def create_probability_matrix_from_words(words):
    """Return probability matrix generated from list of *words*.
    """
    matrix = np.zeros((256, 256, 256), dtype="int32")

    letter_buffer1 = 0
    letter_buffer2 = 0

    for word in words:
        word = "\n{}\n".format(word)
        for letter in word:
            if (
                letter not in string.punctuation and
                not letter.isdigit()
            ):
                ordinal = ord(letter)
                matrix[letter_buffer1, letter_buffer2, ordinal] += 1
                letter_buffer1 = letter_buffer2
                letter_buffer2 = ordinal

    return matrix
