comp-generate-teams
===================

Synopsis
--------

::


  sr comp-generate-teams [-h] [-o FILE] [--server URL]

Description
-----------

Generate the ``teams.yaml`` for a compstate repository, from the information
given in srweb. This includes team names from the team-status system.


Options
-------

--help, -h
    Display help and exit.

--server <url>
    The srweb server to query. If unspecified, studentrobotics.org is assumed.

--output <file>, -o <file>
    ``teams.yaml`` file to which to write the database. ``stdout`` if
    unspecified.

Examples
--------

.. code::

    $ sr comp-generate-teams -o sr2015-comp/teams.yaml
