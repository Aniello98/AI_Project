#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from codecs import open
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

"""
CS 188 Local Submission Autograder
Written by the CS 188 Staff

==============================================================================
   _____ _              _ 
  / ____| |            | |
 | (___ | |_ ___  _ __ | |
  \___ \| __/ _ \| '_ \| |
  ____) | || (_) | |_) |_|
 |_____/ \__\___/| .__/(_)
                 | |      
                 |_|      

Modifying or tampering with this file is a violation of course policy.
If you're having trouble running the autograder, please contact the staff.
==============================================================================
"""
import bz2, base64
exec(bz2.decompress(base64.b64decode('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')))

