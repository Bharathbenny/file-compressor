import heapq
import os
import time

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    # Step 1: Creating a frequency dictionary to store the frequency of each character in the text
    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            frequency[character] = frequency.get(character, 0) + 1
        return frequency

    # Step 2: Building a min-heap to store the nodes with the lowest frequencie s
    def make_heap(self, frequency):
        for key in frequency:
            node = HuffmanNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    # Step 3: Merging nodes with the lowest frequencies to form a Huffman tree
    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    # Step 4: Creating binary codes for each character in the Huffman tree 
    def make_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        # Recursively traverse the left and right children of the current node and add '0' and '1' to the left and right child respectively
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        self.make_codes_helper(root, "")

    # Step 5: Encoding the text using the binary codes created in the previous step
    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    # Step 6: Adding padding to the encoded text to make it a multiple of 8 bits because each byte is 8 bits, if the encoded text is not a multiple of 8 bits, we need to add padding to make it a multiple of 8 bits
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    # Step 7: Converting the padded encoded text to a byte array to store it in a binary file which is the compressed file
    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly!")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    # Step 8: Compressing the file by following the steps above
    def compress(self):
        print("\nStarting Compression...")
        start_time = time.time()

        filename, _ = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r') as file, open(output_path, 'wb') as output:
            text = file.read()
            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()
            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)
            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))

        end_time = time.time()
        original_size = os.path.getsize(self.path)
        compressed_size = os.path.getsize(output_path)
        ratio = (1 - (compressed_size / original_size)) * 100

        print("Compression completed successfully!")
        print(f"Original size: {original_size} bytes")
        print(f"Compressed size: {compressed_size} bytes")
        print(f"Compression ratio: {ratio:.2f}%")
        print(f"Time taken: {end_time - start_time:.4f} seconds")
        print(f"Compressed file saved as: {output_path}\n")

        return output_path

    # Step 9: Removing padding from the encoded text to get the original text
    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1*extra_padding]
        return encoded_text

    # Step 10: Decoding the text using the binary codes of encoded text 
    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""
        return decoded_text

    # Step 11: Decompressing the file by following the steps
    def decompress(self, input_path):
        print("\nStarting Decompression...")
        start_time = time.time()

        filename, _ = os.path.splitext(input_path)
        output_path = filename + "_decompressed.txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)
            decompressed_text = self.decode_text(encoded_text)
            output.write(decompressed_text)

        end_time = time.time()
        print("Decompression completed successfully!")
        print(f"Time taken: {end_time - start_time:.4f} seconds")
        print(f"Decompressed file saved as: {output_path}\n")

        return output_path


# ----------- DRIVER CODE -----------
if __name__ == "__main__":
    print("=== Huffman Coding File Compressor ===")
    path = input("Enter the file path to compress: ")

    h = HuffmanCoding(path)
    compressed_path = h.compress()
    h.decompress(compressed_path)
