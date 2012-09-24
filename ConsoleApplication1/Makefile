SRCS := $(wildcard *.cpp)
OBJS := $(subst .cpp,.o,$(SRCS))

BIN = ConsoleApplication1

$(BIN): $(OBJS)
	g++ -o $@ $^

%.o: %.cpp
	g++ -Wall -g -c $< -o $@

