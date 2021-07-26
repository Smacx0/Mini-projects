/*
	### Extracting PNG IHDR chunks

	Extracting PNG chunks is not a big deal. While learning PNG structure, found that data is stored big endian byteorder. But most of the devices use little endian byteorder and here is sample code to swap between endians and extract metadata. (Just for learning purpose.)
	Reference:
		* https://datatracker.itef.org/doc/html/rfc2083
		* https://geeksforgeeks.org/bit-manipulation-swap-endianness-of-a-number/
*/

#include <iostream>
#include <fstream>
#include <map>

#define INVALID_MAGIC_NUMBER 1;

using namespace std;

typedef union {
	uint8_t sign[8];
	uint64_t value;
} magic_t;

typedef struct {
	uint32_t width;		// 4 bytes
	uint32_t height;	// 4 bytes
	uint8_t bitDepth;	// 1 byte
	uint8_t colorType;	// 1 byte
	uint8_t compression;// 1 byte
	uint8_t filter;		// 1 byte
	uint8_t interlace;	// 1 byte
} header;

class TypeName {
private:
	string name;
public:
	TypeName(){ this->name = "Unknown"; }
	TypeName(string name) { this->name = name; }
	string getName() { return name; }
	// C capable string
	char* cgetName() { return (char*)name.c_str(); }
	
	friend ostream &operator<<(ostream &out, TypeName &obj) {
		out << obj.getName();
		return out;
	}
};

map<uint8_t, TypeName> colorType = {
	{0, TypeName("GreyScale")},
	{2, TypeName("RGB")},
	{3, TypeName("PLTE")},
	{4, TypeName("GreyScale with Alpha")},
	{6, TypeName("RGBA")}
};

map<uint8_t, TypeName> compression = {
	{0, TypeName("Deflate/Inflate")}
};

map<uint8_t, TypeName> filter = {
	{0, TypeName("Adaptive")}
};

map<uint8_t, TypeName> interlace = {
	{0, TypeName("Non-interlaced")},
	{1, TypeName("Interlaced")}
};

uint32_t endian_swap(uint32_t &value){
	int temp = 10;
	char byte = (char)temp;
	if(byte == 10){
		uint32_t a,b,c,d;
		a = (value & 0x000000ff) >> 0;
		b = (value & 0x0000ff00) >> 8;
		c = (value & 0x00ff0000) >> 16;
		d = (value & 0xff000000) >> 24;
		a <<= 24;
		b <<= 16;
		c <<= 8;
		d <<= 0;
		return a | b | c | d;
	}else{
		return value;
	}
}

int main(int argc, char** argv){
	
	if(argc < 2){
		cout << "Argument filename missing.\n";
		return 1;
	}

	ifstream fp;
	fp.open(argv[1], ios::binary | ios::in );

	if(fp.is_open()){
		try{
			
			magic_t png_magic = {0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a};

			magic_t byte;

			fp.read((char*) &byte, sizeof(byte));

			if (byte.value != png_magic.value){
				throw INVALID_MAGIC_NUMBER;
			}

			// ihdr chunk of length 13 and starting position 16. 
			fp.seekg(16, ios::beg);
			
			header ihdr;
			fp.read((char*) &ihdr, sizeof(ihdr));

			printf("%-20s : %s \n%-20s : %u \n%-20s : %u\n",
				"File name", argv[1],
				"Image width", endian_swap(ihdr.width),
				"Image height", endian_swap(ihdr.height)
			);

			printf("%-20s : %hhu \n%-20s : %s \n%-20s : %s \n%-20s : %s \n%-20s : %s \n", 
				"Bit depth", ihdr.bitDepth,
				"Color type", colorType[ihdr.colorType].cgetName(),
				"Compression", compression[ihdr.compression].cgetName(),
				"Filter", filter[ihdr.filter].cgetName(),
				"Interlace", interlace[ihdr.interlace].cgetName()
			);

		}catch(...){
			cout << argv[1] << ": Invalid PNG header.\n";
		}
	}else {
		cout << "Not a valid file\n";
	}
	fp.close();
	return 0;
}