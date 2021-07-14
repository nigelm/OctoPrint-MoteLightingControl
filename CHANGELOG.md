# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

In general the major version number is incremented if either the database schema is changed,
or the presented API is incompatibly changed.


Unreleased Changes
------------------

<!-- insertion marker -->
[0.3.3] - 2021-07-14
--------------------
[0.3.2] - 2021-07-14
--------------------
[0.3.1] - 2021-07-11
--------------------
[0.3.0] - 2021-07-11
--------------------
- Dropped untested PHAT support
- Ensured missing USB Motes do not take system out
- Fixed issues with Mote channels
- Made all state changes individually ignorable
- Previously CLient Connect/Disconnect were events, but reusued printer
  Connect/Disconnect colours.  Have just removed them for now.


[0.2.3] - 2021-07-10
--------------------
- First releasable version
- Working navbar light on/off button
- Lighting states for various conditions
- USB Motes tested and working.  No chance to test PHAT Motes

----
