SRCS = $(wildcard *.cpp)

BIN = ConsoleApplication1

GEN := test_intcmp.cpp

SRCS += $(GEN)
OBJS := $(subst .cpp,.o,$(SRCS))
DEPS := $(addprefix .,$(subst .cpp,.d,$(SRCS)))

.PHONY: all clean

all: $(BIN)

-include $(DEPS)

$(BIN): $(OBJS)
	g++ -o $@ $^

$(GEN): gen_code.py
	python $<

%.o: %.cpp
	g++ -Wall -g -MD -MP -MF .$*.d -c $< -o $@

clean:
	rm -f $(BIN)
	rm -f $(OBJS)
	rm -f $(GEN)
	rm -f .*.d


