CXX = g++
CXXFLAGS = -Wall -std=c++11
TARGET = FactorySimulator
OBJ = FactorySimulator.o main.o

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
	rm -f $(OBJ) $(TARGET)
