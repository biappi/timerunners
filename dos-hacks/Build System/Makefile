EXE_SOURCE=simul.c
EXE_NAME=simul.exe

# - #

DOSBOX_PATH=$(SRCROOT)/Dos Tools/dosbox
TURBOC_TOOLCHAIN_PATH=$(SRCROOT)/Dos Tools/Turbo C
TIMERUNNERS_DATA_PATH=$(SRCROOT)/../original/

# - #

DOS_ROOT_DST=$(TARGET_BUILD_DIR)/dosroot

TURBOC_TOOLCHAIN_DST=$(DOS_ROOT_DST)/TC
TIMERUNNERS_DATA_DST=$(DOS_ROOT_DST)/TR

DOSBOX_DST=$(TARGET_BUILD_DIR)/dosbox

REAL_SOURCE_PATH=$(SRCROOT)/Sources
DOS_SOURCE_PATH=$(DOS_ROOT_DST)/src

REAL_SOURCE_FILE_PATH=$(SRCROOT)/Sources/$(EXE_SOURCE)
DOS_SOURCE_FILE_PATH=$(DOS_ROOT_DST)/src/$(EXE_SOURCE)

# - #

DOS_BUILD_DIR=C:\BUILD
DOS_BUILD_PATH=$(DOS_ROOT_DST)/build
DOS_BUILT_PRODUCT=$(DOS_BUILD_PATH)/$(EXE_NAME)

# - #

$(TARGET_BUILD_DIR)/$(EXE_NAME): $(DOSBOX_DST) $(DOS_SOURCE_FILE_PATH)
	@ rm -fr "$(DOS_BUILD_PATH)"
	@ mkdir -p "$(DOS_BUILD_PATH)"

	@ TERM=xterm                                \
		$(DOSBOX_DST)                           \
		-c "mount c $(DOS_ROOT_DST)"            \
		-c "set path=c:\tc"                     \
		-c "c:"                                 \
		-c "cd build"                           \
		-c "tcc c:\src\$(EXE_SOURCE) > tcc.log" \
		-c "exit"                               \
		2>&1 > /dev/null

	@ cat "$(DOS_BUILD_PATH)/TCC.LOG"
	@ mkdir -p "$(TARGET_BUILD_DIR)"
	@ cp "$(DOS_BUILD_PATH)/$(EXE_NAME)" "$(TARGET_BUILD_DIR)/$(EXE_NAME)"

.PHONY: clean
clean:
	@ rm -fr "$(TARGET_BUILD_DIR)"


# - #

$(DOS_SOURCE_FILE_PATH): $(REAL_SOURCE_FILE_PATH)
	mkdir -p "$(DOS_ROOT_DST)"
	cp -r "$(TURBOC_TOOLCHAIN_PATH)" "$(TURBOC_TOOLCHAIN_DST)"
	cp -r "$(TIMERUNNERS_DATA_PATH)" "$(TIMERUNNERS_DATA_DST)"
	ln -s "$(REAL_SOURCE_PATH)" "$(DOS_SOURCE_PATH)"

$(DOSBOX_DST):
	mkdir -p "$(TARGET_BUILD_DIR)"
	cp "$(DOSBOX_PATH)" "$(DOSBOX_DST)"
