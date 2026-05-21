Huffman Coding File CompressorA lightweight, high-performance lossless data compression tool written in Python. This project utilizes the Huffman Coding algorithm to compress standard text files into optimized binary files (.bin) and restore them back to their exact original form with 100% data fidelity.🚀 How it WorksThe tool processes text files through a structured, multi-step pipeline executed entirely in memory:[ Text Input ] ➔ [ Frequency Map ] ➔ [ Min-Heap Priority Queue ] ➔ [ Huffman Tree Root ]
                                                                             │
[ Decompressed Text ] ◀── [ Bitstream Translation ] ◀── [ 8-Bit Padded Bytes ] ◀┘
Analysis: It counts the frequency of every unique character in your text file.Tree Building: A Priority Queue (Min-Heap) continuously merges the two rarest characters until a single unified Huffman Tree is formed.Encoding: Unique, variable-length bit strings are generated based on the tree paths (frequent characters get short paths, rare characters get longer paths).Bit-Packing: The custom bitstream is packed into actual physical bytes, utilizing an 8-bit descriptive metadata header to track explicit bit padding.⚙️ FeaturesLossless Compression: Restores files perfectly down to the single byte with zero data degradation.Smart Bit Padding Header: Appends a dedicated, 8-bit prefix tracking precise bit layout metrics to ensure correct reconstruction.Performance Benchmark Readouts: Displays processing times, file footprint changes, and compression ratios automatically upon every run.💻 UsagePrerequisitesPython 3.x installed.Standard libraries utilized: heapq, os, time. (No third-party packages required).Running the ApplicationPlace your text file (e.g., sample.txt) in the project directory.Execute the script from your terminal:Bashpython huffman.py
Type out the relative path of your target file when prompted:Plaintext   === Huffman Coding File Compressor ===
   Enter the file path to compress: sample.txt
Output Readout SampleOnce the script completes, your workspace will generate a compressed .bin file alongside an automated validation script logging your efficiency statistics:PlaintextStarting Compression...
Compression completed successfully!
Original size: 10432 bytes
Compressed size: 5812 bytes
Compression ratio: 44.29%
Time taken: 0.0124 seconds
Compressed file saved as: sample.bin

Starting Decompression...
Decompression completed successfully!
Time taken: 0.0089 seconds
Decompressed file saved as: sample_decompressed.txt
Performance AnalysisData Profile StructureExpected EfficiencyDescriptionHighly Repetitive70% - 90% SavingsIdeal for files with skewed letter frequencies (e.g., logs, genomic data sequence profiles).Natural Prose Text35% - 55% SavingsStandard books, articles, or source code containing typical linguistic patterns. Code ArchitectureThe implementation splits the lifecycle cleanly across two main classes:HuffmanNode: Tracks char values, structural branch weights (freq), and left/right node children pointers while implementing custom logical sorting handlers (__lt__).HuffmanCoding: Drives the entire application pipeline, housing individual tracking functions for text encoding, byte array calculations, file padding isolation, and text decoding.