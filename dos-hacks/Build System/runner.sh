#!/bin/sh

cp "${TARGET_BUILD_DIR}/dosroot/TR/CODS/ARCADE.EXE" "${TARGET_BUILD_DIR}/dosroot/TR/CODS/ARC_TR.EXE"
cp "${TARGET_BUILD_DIR}/dosroot/TR/CODS/PLAYER.EXE" "${TARGET_BUILD_DIR}/dosroot/TR/CODS/PLR_TR.EXE"

cp "${TARGET_BUILD_DIR}/SIMUL.EXE" "${TARGET_BUILD_DIR}/dosroot/TR/"

TERM=xterm "${SRCROOT}/Dos Tools/dosbox" \
    -c "mount c ${TARGET_BUILD_DIR}/dosroot/" \
    -c "c:" \
    -c "cd TR" \
    -c "simul" \
    2>&1 > /dev/null
