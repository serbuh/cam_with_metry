# https://www.arducam.com/docs/camera-for-jetson-nano/mipi-camera-modules-for-jetson-nano/driver-installation/
# install:
# cd installs
# ./install.sh
# or:
# sudo dpkg -i arducam-nvidia-l4t-kernel_4.9.140-32.4.4-20201027211359_arm64.deb
# rollback: sudo dpkg -r arducam-nvidia-l4t-kernel

# Check video stream with gstreamer
# gst-launch-1.0 v4l2src device=/dev/video0 ! xvimagesink
echo "read me (inside .sh)"
