#!/bin/bash
# run_mapping.sh
# Script to launch the Python 3D Mapping application

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PROJECT_DIR/src"

show_help() {
    echo "KRIA 3D Mapping (Python) - Launcher"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help      Show help"
    echo "  --headless      Run without GUI"
    echo ""
}

# Check Environment
echo -e "${YELLOW}[Check] Checking environment...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[Error] python3 not found.${NC}"
    exit 1
fi

# Check for pyrealsense2
if ! python3 -c "import pyrealsense2" &> /dev/null; then
    echo -e "${YELLOW}[Warning] pyrealsense2 module not found in python path.${NC}"
    echo -e "          Checking if it's installed in system..."
    # You might want to add PYTHONPATH setup here if it's in a custom location on Yocto
    # export PYTHONPATH=$PYTHONPATH:/usr/lib/python3.x/site-packages
fi

# Check RealSense USB
if lsusb | grep -i "Intel.*RealSense" > /dev/null; then
    echo -e "${GREEN}[Check] RealSense device detected.${NC}"
else
    echo -e "${YELLOW}[Warning] RealSense device NOT detected on USB.${NC}"
fi

# Run
echo -e "${GREEN}[Run] Starting Application...${NC}"
cd "$SRC_DIR"

# Pass arguments to python script
python3 main.py "$@"
