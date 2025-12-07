CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wall -Wextra

TARGET = bplustree_driver
SRCS = src/main.cpp src/bplustree.cpp
OBJS = $(SRCS:.cpp=.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET) *.dat

test: $(TARGET)
	./$(TARGET)

.PHONY: all clean test
