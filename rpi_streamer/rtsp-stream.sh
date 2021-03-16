#!/bin/bash

# For HD (16:9) use -w 1920 -h 1080
# For 4K (4:3)  use -w 3280 -h 2464

# -md 2 responsible for setting appropriate mode
# Larn more about modes: https://picamera.readthedocs.io/en/latest/fov.html#sensor-modes

raspivid -o - \
    -t 0 \
    -n \
    -g 15 \
    -rot 180 \
    -pf high \
    -md 2 \
    -fps 15 \
    -b 10000000 \
| cvlc -vvv \
    stream:///dev/stdin \
    --no-audio \
    --h264-fps=15 \
    --sout '#rtp{sdp=rtsp://:8554/stream}' \
    :demux=h264