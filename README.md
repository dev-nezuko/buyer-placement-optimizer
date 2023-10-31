# Pearl Certification

This application places home buyers moving to Charlottesville in different available neighborhoods, based on their preferences and compatibility with neighborhood scores in energy efficiency (E), water (W), and resilience (R).

The algorithm ensures to distribute home buyers evenly among neighborhoods, such that no home buyer could subsequently move to a more preferred neighborhood and be a better fit than those already residing there.

## Requirements

- Python 3

## Getting Started

1. **Clone the repository**:
    > git clone <[repository URL](https://github.com/dev-nezuko/buyer-placement-optimizer)>

2. **Move into the repository directory**:
   > cd pearl-certification-assessment

3. **Run the application**:

    > python main.py

&nbsp;

The code will generate an output file named `generated_output.txt`, containing the optimal placement of home buyers in neighborhoods.

## Running test cases

Running the code by following the above steps will also automatically run an associated test, which asserts that the generated output file is correct.

To manually run the tests (after the output file to be tested has been generated), run the following:

  > python -m unittest discover tests
