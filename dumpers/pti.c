#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef struct {
	uint16_t   line_id;
	uint8_t    length;
	char     * string;
} pti_item_line_t;

typedef struct {
	uint16_t          first_line_in_this_item;
	uint16_t          first_line_in_next_item;
	uint16_t          nr_of_lines;
	uint16_t          size_in_disk;
	uint32_t          offset;
	pti_item_line_t * lines;
} pti_item_info_t;

typedef struct {
	char            textinfo[64];
	pti_item_info_t items[16];
	uint16_t        unknown1;
	uint8_t         xor_key;
	uint8_t         unknown2;
} pti_header_t;

uint8_t read_8(uint8_t ** i)
{
	uint8_t a = **i;
	*i = *i + 1;
	return a;
}

uint16_t read_16 (uint8_t ** i)
{
	return read_8(i) + (read_8(i) << 8);
}

uint32_t read_32 (uint8_t ** i)
{
	return  read_8(i) +
	       (read_8(i) <<  8) +
	       (read_8(i) << 16) +
	       (read_8(i) << 24);
}

uint8_t * load_file (char * theFile)
{
	FILE    * f;
	size_t    s;
	uint8_t * b;

	f = fopen(theFile, "r");
	fseek(f, 0, SEEK_END),
	
	s = ftell(f);
	b = malloc(s);
	
	rewind(f);
	fread(b, 1, s, f);

	return b;
}

int main(int argc, char * argv[])
{
	char    * f   = argc == 2 ? argv[1] : "Texts.kit";
	uint8_t * pti = load_file(f);
	uint8_t * cur = pti;
	int       i;
	
	pti_header_t header;
	memset(&header, 0, sizeof(pti_header_t));

	memcpy(header.textinfo, pti, 64);
	
	cur = pti + 0x100;
	
	header.unknown1 = read_16(&cur);
	header.xor_key  = read_8(&cur);
	header.unknown2 = read_8(&cur);

	cur = pti + 0x40;

	for (i = 0; i < 16; i++)
	{
		int k;
		pti_item_info_t * info = &(header.items[i]);
		
		info->first_line_in_this_item = read_16(&cur);
		info->first_line_in_next_item = read_16(&cur);
		info->nr_of_lines = read_16(&cur);
		info->size_in_disk = read_16(&cur);
		info->offset = read_32(&cur);
		
		info->lines = (pti_item_line_t*)malloc(info->nr_of_lines * sizeof(pti_item_line_t));
		
		uint8_t * temp = pti + info->offset;
		for (k = 0; k < info->nr_of_lines; k++)
		{
			info->lines[k].line_id = read_16(&temp);
			info->lines[k].length  = read_8(&temp);
			
			{
				int j;
				size_t   size   = info->lines[k].length + 1;
				char   * string = malloc(size);
				
				memset(string, 0, size);
				
				for (j = 0; j < info->lines[k].length; j++)
					*(string + j) = *(temp + j) ^ header.xor_key;
				
				info->lines[k].string = string;
			}
			
			temp += info->lines[k].length + 1;
		}
	}
	
/* - */

	printf("textinfo: %s\n", header.textinfo);
	printf("unknown1: %d\n", header.unknown1);
	printf("xor key : %d\n", header.xor_key);
	printf("unknown2: %d\n\n", header.unknown2);
	
	for (i = 0; i < 16; i++)
	{
		int k;
		
		if (header.items[i].nr_of_lines == 0)
			continue;
		
		printf("item %d\n-------\n", i);
		printf("  first in this: %04x\n",
			header.items[i].first_line_in_this_item);
		printf("  first in next: %04x\n",
			header.items[i].first_line_in_next_item);
		printf("  nr of lines  : %04x\n",
			header.items[i].nr_of_lines);
		printf("  size in disk : %04x\n",
			header.items[i].size_in_disk);
		printf("  offset       : %08x\n",
			header.items[i].offset);
		
		for (k = 0; k < header.items[i].nr_of_lines; k++)
		{
			printf("    line %04x, len: %02x - %s\n", 
				header.items[i].lines[k].line_id,
				header.items[i].lines[k].length,
				header.items[i].lines[k].string);
		}
		
		printf("\n");
	}
}
