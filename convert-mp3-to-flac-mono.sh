#!/bin/bash  
echo "***Converting mp3 files into stereo flac***"
for MP3_FILE_LOCATION in ./raw_mp3_episodes/*
do
    MP3_FILE_NAME="${MP3_FILE_LOCATION##*/}"
    BASE_FILE_NAME=${MP3_FILE_NAME%.mp3}
    echo "Converting $BASE_FILE_NAME into mono flac"
    ffmpeg -i $MP3_FILE_LOCATION "./flac_stereo/${BASE_FILE_NAME}.flac" 
done

for FLAC_STEREO_LOCATION in ./flac_stereo/*
do
    FLAC_STEREO_FILE_NAME="${FLAC_STEREO_LOCATION##*/}"
    ffmpeg -i $FLAC_STEREO_LOCATION -ac 1 "./flac_mono/${FLAC_STEREO_FILE_NAME}"
done