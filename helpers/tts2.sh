#!/bin/bash
parentdir="$(dirname "$(pwd)")"
echo $parentdir
aws polly synthesize-speech \
--text-type ssml \
--text file://$parentdir/static/testfile.xml \
--output-format mp3 \
--voice-id Joanna \
$parentdir/static/speech.mp3