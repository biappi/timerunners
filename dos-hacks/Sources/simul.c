#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <dos.h>
#include <mem.h>

typedef unsigned char  uint8_t;
typedef unsigned short uint16_t;

void getch();

void print_hex(void * data, int size) {
    unsigned char * buf = (unsigned char *) data;
    int i;

    for (i = 0; i < size; i++) {
        if ((i % 16) == 0)
            printf("%04x |  ", i);

        printf("%02x ", buf[i]);

        if (((i + 1) % 16) == 0)
            printf("\n");
    }

    printf("\n");
}

struct info_ls_additional {
    char pla_file_path_storage[0x45];
    char unk5_file_path_storage[0x45];
};

struct info_ls {
    uint8_t    unk1;
    uint8_t    unk2;
    uint16_t   unk3;
    uint8_t  * pla_file_path;
    uint8_t  * unk5_file_path;
    uint8_t    language_string[3];
    uint8_t  * unk7_func;
    uint8_t  * unk8_func;
    uint8_t  * noop_1_func;
    uint8_t  * unk10_func;
    uint8_t    unk11;
    
    struct info_ls_additional additional;
};

struct arguments {
    uint8_t          header[10];
    uint8_t          r;
    uint8_t          anonymous_1;
    uint16_t         anonymous_2;
    uint8_t        * swap_buf;
    uint16_t         pla_file_length;
    uint8_t        * pla_file_content__token_buf;
    uint16_t         var_buf_size;
    uint8_t        * var_buf;
    uint16_t         switch_buf_size;
    uint8_t        * switch_buf;
    uint16_t         settings_size;
    uint8_t        * settings;
    uint16_t         font_buf_size;
    uint8_t        * font_buf;
    uint8_t          anonymous_3[6];
    uint16_t         lib_buf_size;
    uint8_t        * lib_buf;
    uint16_t         lib_buf_2_size;
    uint8_t        * lib_buf_2;
    uint16_t         lib_buf_3_size;
    uint8_t        * lib_buf_3;
    uint16_t         lib_buf_4_size;
    uint8_t        * lib_buf_4;
    uint16_t         pal_buf_size;
    uint8_t        * pal_buf;
    uint16_t         retcode_buf_size;
    uint8_t        * retcode_buf;
    uint16_t         text_buf_size;
    uint8_t        * text_buf;
    uint16_t         spl_mus_buf_size;
    uint8_t        * spl_mus_buf;
    uint16_t         spl_mus_buf_1_size;
    uint8_t        * spl_mus_buf_1;
    uint16_t         img_buf_size;
    uint8_t        * img_buf;
    uint16_t         infols_buf_size;
    struct info_ls * infols_buf;
    uint8_t          anonymous_5[12];
};


void write_file(char * filename, void * buf, unsigned short len) {
    FILE * file = fopen(filename, "wb");
    fwrite(buf, len, 1, file);
    fclose(file);
}

void append_file(char * filename, void * buf, unsigned short len) {
    FILE * file = fopen(filename, "ab");
    fwrite(buf, len, 1, file);
    fclose(file);
}


void read_file(char * filename, void ** buf, unsigned short * len) {
    FILE * file;
    
    file = fopen(filename, "rb");
    fseek(file, 0, SEEK_END);
    
    *len = ftell(file);

    if (*len != 0) {
        allocmem((*len + 0x10) >> 4, *buf);
    }
    else {
        *buf = 0;
    }
    
    fseek(file, 0, SEEK_SET);
    fread(*buf, *len, 1, file);
    fclose(file);
}

void write_files(struct arguments * args) {
    struct info_ls_additional add;
    
    memset(&add, 0, sizeof(add));
    
    write_file("c:\\out\\pla",      args->pla_file_content__token_buf,
                                                         args->pla_file_length);
    write_file("c:\\out\\var",      args->var_buf,       args->var_buf_size);
    write_file("c:\\out\\switch",   args->switch_buf,    args->switch_buf_size);
    write_file("c:\\out\\settings", args->settings,      args->settings_size);
    write_file("c:\\out\\font",     args->font_buf,      args->font_buf_size);
    write_file("c:\\out\\lib1",     args->lib_buf,       args->lib_buf_size);
    write_file("c:\\out\\lib2",     args->lib_buf_2,     args->lib_buf_2_size);
    write_file("c:\\out\\lib3",     args->lib_buf_3,     args->lib_buf_3_size);
    write_file("c:\\out\\lib4",     args->lib_buf_4,     args->lib_buf_4_size);
    write_file("c:\\out\\pal",      args->pal_buf,       args->pal_buf_size);
    write_file("c:\\out\\retcode",  args->retcode_buf,   args->retcode_buf_size);
    write_file("c:\\out\\text",     args->text_buf,      args->text_buf_size);
    write_file("c:\\out\\spl0",     args->spl_mus_buf,   args->spl_mus_buf_size);
    write_file("c:\\out\\spl1",     args->spl_mus_buf_1, args->spl_mus_buf_1_size);
    write_file("c:\\out\\img",      args->img_buf,       args->img_buf_size);
    write_file("c:\\out\\infols",   args->infols_buf,    args->infols_buf_size);
    write_file("c:\\out\\args",     args,                0x84);
    
    printf(" > %s\n", args->infols_buf->pla_file_path);
    printf(" > %s\n", args->infols_buf->unk5_file_path);
    
    memcpy(add.pla_file_path_storage,  args->infols_buf->pla_file_path,  0x45);
    memcpy(add.unk5_file_path_storage, args->infols_buf->unk5_file_path, 0x45);

    
    append_file("c:\\out\\infols", "  ", 2);
    append_file("c:\\out\\infols", &add, sizeof(add));
}

void read_files(struct arguments ** args) {
    unsigned short len;
    struct arguments * f;
    
    read_file("c:\\out\\args", (void **)args, &len);
    
    f = *args;
    
    read_file("c:\\out\\pla",      &(f->pla_file_content__token_buf),
                                                        &(f->pla_file_length));
    read_file("c:\\out\\var",      &(f->var_buf),       &(f->var_buf_size));
    read_file("c:\\out\\switch",   &(f->switch_buf),    &(f->switch_buf_size));
    read_file("c:\\out\\settings", &(f->settings),      &(f->settings_size));
    read_file("c:\\out\\font",     &(f->font_buf),      &(f->font_buf_size));
    read_file("c:\\out\\lib1",     &(f->lib_buf),       &(f->lib_buf_size));
    read_file("c:\\out\\lib2",     &(f->lib_buf_2),     &(f->lib_buf_2_size));
    read_file("c:\\out\\lib3",     &(f->lib_buf_3),     &(f->lib_buf_3_size));
    read_file("c:\\out\\lib4",     &(f->lib_buf_4),     &(f->lib_buf_4_size));
    read_file("c:\\out\\pal",      &(f->pal_buf),       &(f->pal_buf_size));
    read_file("c:\\out\\retcode",  &(f->retcode_buf),   &(f->retcode_buf_size));
    read_file("c:\\out\\text",     &(f->text_buf),      &(f->text_buf_size));
    read_file("c:\\out\\spl0",     &(f->spl_mus_buf),   &(f->spl_mus_buf_size));
    read_file("c:\\out\\spl1",     &(f->spl_mus_buf_1), &(f->spl_mus_buf_1_size));
    read_file("c:\\out\\img",      &(f->img_buf),       &(f->img_buf_size));
    read_file("c:\\out\\infols",   &(f->infols_buf),    &(f->infols_buf_size));
    
    f->infols_buf->pla_file_path  = &(f->infols_buf->additional.pla_file_path_storage);
    f->infols_buf->unk5_file_path = &(f->infols_buf->additional.unk5_file_path_storage);
    
    printf(" -- %p\n", &(f->infols_buf->additional.pla_file_path_storage));
    f->infols_buf->additional.unk5_file_path_storage[0] = 0;
    getch();
}

void dump_args(struct arguments * args) {
    printf(
    "   header          %s\n"
    "   r               %c\n"
    "   anonymous_1     %x\n"
    "   anonymous_2     %x\n"
    "   swap_buf        %p\n"
    "   pla_file_length %x\n"
    "   pla_file_content__token_buf\n"
    "                   %p\n"
    "   var_buf_size    %x\n"
    "   var_buf         %p\n"
    "   switch_buf_size %x\n"
    "   switch_buf      %p\n"
    "   settings_size   %x\n"
    "   settings        %p\n"
    "   font_buf_size   %x\n"
    "   font_buf        %p\n"
    "   anonymous_3[6]  %s\n"
    "   lib_buf_size    %x\n"
    "   lib_buf         %p\n"
    "   lib_buf_2_size  %x\n"
    "   lib_buf_2       %p\n"
    "   lib_buf_3_size  %x\n"
    "   lib_buf_3       %p\n"
    "   lib_buf_4_size  %x\n"
    "   lib_buf_4       %p\n"
    "   pal_buf_size    %x\n"
    "   pal_buf         %p\n"
    "   retcode_buf_size %x\n"
    "   retcode_buf     %p\n"
    "   text_buf_size   %x\n"
    "   text_buf        %p\n"
    "   spl_mus_buf_size %x\n"
    "   spl_mus_buf     %p\n"
    "   spl_mus_buf_1_size %x\n"
    "   spl_mus_buf_1   %p\n"
    "   img_buf_size    %x\n"
    "   img_buf         %p\n"
    "   infols_buf_size %x\n"
    "   infols_buf      %p\n",

    args->header,
    args->r,
    args->anonymous_1,
    args->anonymous_2,
    args->swap_buf,
    args->pla_file_length,
    args->pla_file_content__token_buf,
    args->var_buf_size,
    args->var_buf,
    args->switch_buf_size,
    args->switch_buf,
    args->settings_size,
    args->settings,
    args->font_buf_size,
    args->font_buf,
    args->anonymous_3,
    args->lib_buf_size,
    args->lib_buf,
    args->lib_buf_2_size,
    args->lib_buf_2,
    args->lib_buf_3_size,
    args->lib_buf_3,
    args->lib_buf_4_size,
    args->lib_buf_4,
    args->pal_buf_size,
    args->pal_buf,
    args->retcode_buf_size,
    args->retcode_buf,
    args->text_buf_size,
    args->text_buf,
    args->spl_mus_buf_size,
    args->spl_mus_buf,
    args->spl_mus_buf_1_size,
    args->spl_mus_buf_1,
    args->img_buf_size,
    args->img_buf,
    args->infols_buf_size,
    args->infols_buf);
}

void dump_infols(struct info_ls * info) {
    printf(
    "    unk1            %x\n"
    "    unk2            %x\n"
    "    unk3            %x\n"
    "    pla_file_path   %p\n"
    "    unk5_file_path  %p\n"
    "    language_string %s\n"
    "    unk7_func       %p\n"
    "    unk8_func       %p\n"
    "    noop_1_func     %p\n"
    "    unk10_func      %p\n"
    "    unk11           %x\n",
    info->unk1,
    info->unk2,
    info->unk3,
    info->pla_file_path,
    info->unk5_file_path,
    info->language_string,
    info->unk7_func,
    info->unk8_func,
    info->noop_1_func,
    info->unk10_func,
    info->unk11);
}

void * pointer_from_string(char * string) {
    char * p = NULL;
    
    if (strlen(string) != 9)
        return p;
    
    sscanf(string, "%p", &p);
    return p;
}

void set_mode(unsigned char mode) {
    union REGS regs;
    
    regs.h.ah = 0x00;
    regs.h.al = mode;
    int86(0x10, &regs, &regs);
}

int main(int argc, char ** argv) {
    struct arguments * args;
    
    if (argc == 2) {
        printf("sizeof %x\n", sizeof(struct arguments));
        
        args = (struct arguments *)pointer_from_string(argv[1]);
        printf("arguments: %p\n", args);
            
        write_files(args);
        
        print_hex((void *)args, 0x84);
        
        getch();
        dump_infols(args->infols_buf);
    }
    else {
        char cmdline[200];
        
        read_files(&args);
        
        sprintf(cmdline, "c:\\tr\\cods\\plr_tr.exe %p", args);
        printf("cmdline: %s\n", cmdline);

        printf("buf: %p\n", args->swap_buf);
        args->swap_buf = (void *)0xA0000000L;
        printf("buf: %p\n", args->swap_buf);
        
        dump_infols(args->infols_buf);
        printf(" > %s\n", args->infols_buf->pla_file_path);
        printf(" > %s\n", args->infols_buf->unk5_file_path);

        getch();
        
        
        set_mode(0x13);
        system(cmdline);
        set_mode(0x03);
        
        /*
         
         -------------------------------------------------------------------------
         bp 3022:027E                  # start of main player
         bp 3022:0278                  # end of main player
         iv 3EB7:1F76 warn             # warning count
         bpm 3EB7:1F76

         */
        
        print_hex(args->retcode_buf, args->retcode_buf_size);
    }
    
    getch();
}

