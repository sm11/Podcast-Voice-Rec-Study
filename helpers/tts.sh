#!/bin/bash
aws polly synthesize-speech \
--text-type ssml \
--text file://$(pwd)/static/testfile.xml \
--output-format mp3 \
--voice-id Joanna \
$(pwd)/static/options.mp3