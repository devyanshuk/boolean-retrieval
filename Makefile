MAIN = main.py
BIN = bin/

PY = python3
RM = rm -rf

VERBOSE_FLAG = --verbose

.PHONY: all clean

all:
	$(PY) $(MAIN) $(VERBOSE_FLAG)

clean:
	$(RM) $(BIN)
