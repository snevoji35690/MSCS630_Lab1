Project Title

Multithreaded Word Frequency Counter

Description

This program demonstrates the use of multithreading to process a text file concurrently.
The input file is divided into N segments, and each segment is processed by a separate thread to compute word-frequency counts. After all threads complete execution, the main process consolidates the intermediate results into a final word-frequency count.

This project was developed as part of an Operating Systems laboratory assignment to illustrate concurrency and thread synchronization.

Requirements

Python 3.9 or higher (tested with Python 3.11)

macOS, Linux, or Windows

No external libraries required (uses standard Python libraries only)

Files Included

wordfreq.py – Main Python program implementing multithreaded word frequency counting

sample.txt – Sample input text file for testing

README.md – Instructions for compiling and running the program

report.docx / report.pdf – Project report describing design and implementation

How to Run the Program

Open a terminal and navigate to the project directory:

cd wordfreq_threads


Run the program using the following command:

python3.11 wordfreq.py sample.txt 4


Where:

sample.txt is the input text file

4 is the number of segments (threads)

Program Output

Intermediate word-frequency counts are printed for each thread.

After all threads finish execution, a final consolidated word-frequency count is displayed.

Example Command
python3.11 wordfreq.py sample.txt 4

Notes

The program automatically adjusts segment boundaries to avoid splitting words across threads.

Each thread stores its results independently to prevent race conditions.

The final result is produced only after all threads have completed execution.
