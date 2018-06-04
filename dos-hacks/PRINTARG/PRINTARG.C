#include <stdio.h>

void print_hex(unsigned char * buf, int size) {
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

struct arguments {
    unsigned char    header[10];
    unsigned char    r;
    unsigned char    anonymous_1;  
    unsigned short   anonymous_2;
    void           * swap_buf;
    unsigned short   pla_file_length;
    void           * pla_file_content__token_buf;
    unsigned short   var_buf_size;
    void           * var_buf;
    unsigned short   switch_buf_size;
    void           * switch_buf;
    unsigned short   settings_size;
    void           * settings;
    unsigned short   font_buf_size;
    void           * font_buf;
    unsigned char    anonymous_3[6];
    unsigned short   lib_buf_size;
    void           * lib_buf;
    unsigned short   lib_buf_2_size;
    void           * lib_buf_2;
    unsigned short   lib_buf_3_size;
    void           * lib_buf_3;
    unsigned short   lib_buf_4_size;
    void           * lib_buf_4;

    unsigned short   anonymous_4;
    unsigned short   pal_buf_size;
    void           * pal_buf;
    unsigned short   retcode_buf_size;
    void           * retcode_buf;
    unsigned short   text_buf_size;
    void           * text_buf;
    unsigned short   spl_mus_buf_size;
    void           * spl_mus_buf;
    unsigned short   spl_mus_buf_1_size;
    void           * spl_mus_buf_1;
    unsigned short   img_buf_size;
    void           * img_buf;
    unsigned short   infols_buf_size;
    void           * infols_buf;

    unsigned char    anonymous_5[10];
};

void print_args(struct arguments * args) {
    FILE *h = fopen("head", "w");
    fwrite(args, 0x84, 1, h);
    fclose(h);

    print_hex(args, 0x84);
    getch();

    printf(""
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
    "   anonymous_3[6]  %x\n"
    "   lib_buf_size    %x\n"
    "   lib_buf         %p\n"
    "   lib_buf_2_size  %x\n"
    "   lib_buf_2       %p\n"
    "   lib_buf_3_size  %x\n"
    "   lib_buf_3       %p\n"
    "   lib_buf_4_size  %x\n"
    "   lib_buf_4       %p\n"
    "   anonymous_4     %x\n"
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

    args->anonymous_4,
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

int main(int argc, char ** argv) {
    int i;

    printf("Arguments:\n\n");

    for (i = 0; i < argc; i++) {
        printf(" - %s\n", argv[i]);

        if (strlen(argv[i]) == 9) {
            char * p;
            sscanf(argv[i], "%p", &p);
            printf("%p\n", p);

            print_args((struct arguments *)p);
        }
    }

    printf("sizeof %x\n", sizeof(struct arguments));
    getch();
}

