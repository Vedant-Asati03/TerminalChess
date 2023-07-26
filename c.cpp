#include <iostream>
#include <vector>
#include <chrono>

void fibonacciSequence(int no) {
    std::vector<int> numbers = {0, 1};

    for (int i = 2; i <= no; i++) {
        int next_no = numbers[i - 1] + numbers[i - 2];
        numbers.push_back(next_no);
    }

    for (int i = 0; i < numbers.size(); i++) {
        std::cout << i << " - " << numbers[i] << "\n";
    }
}

int main() {
    int n = 10000;

    // Start the timer
    auto start = std::chrono::high_resolution_clock::now();

    fibonacciSequence(n);

    // Stop the timer
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);

    std::cout << "Time taken by the function: " << duration.count() << " seconds" << std::endl;

    return 0;
}
