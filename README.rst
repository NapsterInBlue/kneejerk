kneejerk
=============

Image data can be messy.

Especially when considering the time it takes to label, persist, load, and operate-- generating datasets for user-preference Machine Learning projects can be a costly task.

The main goal of ``kneejerk`` is to allow users to *quickly* key in scores as they're served images, persist those scores, and formulate a way to quickly load everything into a format consumable by any number of Data Science libraries.

Getting Started
---------------

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
~~~~~~~~~~~~~

What things you need to install the software and how to install them

.. code:: none

    Give Examples

Installing
~~~~~~~~~~

A step by step series of examples that tell you how to get development environment running

Say what the step will be

.. code:: none

    Give example

And repeat

.. code:: none

    Until finished

End with a very simple demo of the core functionality of the tool.


Project Goals
-------------

- Quick command line interface that:

   - Points at a directory and combs through all images
   - Allows user to key in preference scores
   - Saves results to ``.csv`` of (filepath, score)
   - Allow for random shuffling of the order of images shown

- Loader that converts from the ``.csv`` and image files to ``numpy``
- Handle necessary data cleaning to resolve size mismatches

- Unit tests
- Published on PyPI
- Documentation :)


Contributing
------------

Link to the ``.github/CONTRIBUTING`` file or any other supporting documentation to equip users to start contributing to this project. Most of your specifics should live there.


Running the tests
~~~~~~~~~~~~~~~~~

Explain how to run the automated tests for this system

Authors
-------

Huge shout-out to `avlaskin <https://github.com/avlaskin>`_ on GitHub for early collaboration via his slick library ``quickLabel``, a really cool ``TkInter`` interface that does a very similar task. My data processing extended beyond the scope of his library and so I figured I'd start from scratch instead of blow up his PR feed :)
