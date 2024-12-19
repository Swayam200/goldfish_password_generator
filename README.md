# Random Number Generator Using Fish Movements

## Project Description
This project explores an innovative approach to generating random numbers using the unpredictable swimming patterns of goldfish. By leveraging computer vision and cryptographic techniques, the movements are tracked, analyzed, and processed into secure random seeds for password generation. This project demonstrates the potential of biological systems as a source of true randomness for cryptography and other secure applications.

## Features
- Uses biological entropy (goldfish movements) for randomness generation.
- Tracks fish movements using Python and OpenCV.
- Processes data into random seeds using Euclidean distance metrics.
- Generates secure passwords using SHA-256 and custom algorithms.
- Low-cost, scalable alternative to hardware-based TRNGs.

## Technologies Used
- **Languages:** Python
- **Libraries:** OpenCV, NumPy, hashlib, random
- **Tools:** Camera for recording fish movements
- **Algorithm:** SHA-256 for cryptographic hashing

## How it Works?
### Data Collection
1. Record videos of goldfish swimming in a controlled environment.
2. Ensure consistent lighting and a high-contrast background for better tracking.

### Data Processing
1. Preprocess videos using OpenCV:
   - Stabilize videos to remove noise.
   - Apply filters to isolate fish movements.
2. Track the goldfish's centroid frame by frame and calculate positional data.
3. Compute the Euclidean distance of fish movements relative to a reference point.

### Random Seed and Password Generation
1. Use the positional data to generate random numbers.
2. Hash the random seed using SHA-256 to create cryptographically secure values.
3. Generate a customizable password from the hashed output.

## Installation
### Prerequisites 
- Python 3.x
- OpenCV (`pip install opencv-python`)
- NumPy (`pip install numpy`)

### Steps
1. Clone this repository:
   git clone https://github.com/your-username/goldfish_password_generator

2. Navigate to the project directory:
   cd random-number-generator-fish

3. Install dependencies:
   pip install -r requirements.txt

4. Run the main script:
   python main.py

## Usage
### Input
- A video file of a goldfish swimming.

### Output
- Random numbers derived from fish movements.
- Cryptographically secure passwords.

## Project Structure
- data/                 # Contains sample videos and datasets
- scripts/              # Python scripts for processing and analysis
   - data_preprocessing.py
   - tracking.py
   - random_seed_generation.py
   - password_generator.py
- results/              # Output data and results
- README.md             # Documentation file
- requirements.txt      # List of dependencies

## Example
### Generated Password
Seed: 123456789abcdef  
Hashed Seed: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  
Generated Password: @dXf!3Vq#Aa9  

## Limitations
- Requires a controlled environment for reliable data collection.
- High-resolution tracking may need advanced hardware for processing.
- Currently limited to goldfish; adaptability to other sources needs further research.

## Future Scope
- Extend randomness generation to other biological systems.
- Improve tracking accuracy and scalability of the system.
- Test performance under diverse environmental conditions.
- Integrate into real-world cryptographic applications.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork this repository.
2. Create a new branch:
   git checkout -b feature-name
3. Commit your changes:
   git commit -m 'Add a new feature'
4. Push to the branch:
   git push origin feature-name
5. Create a Pull Request.

## License
This project is licensed under the MIT License. See LICENSE.md for details.

## Acknowledgments
- Dr. Nancy Kumari for guidance and insights throughout the project.
- OpenCV and NumPy communities for their robust tools and documentation.
- The team members for their collaborative effort in completing this project.
