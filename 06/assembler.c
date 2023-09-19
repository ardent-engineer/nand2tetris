#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

void ins_A(int n);
void number();
void ins_D();
int check_type();

char instruction[30];
char read[30];
char num_bin[30];
char num_bina[30];

char before_eq[10];
char after_eq[10];
char aftersemi[10];
typedef struct
{
    char name[15];
    int value;
}
label;
label lables[200];
typedef struct commands
{
    char c[10];
    char cbin[10];
}
commands;
commands comp[] = {{"0", "0101010"}, {"1","0111111"}, {"-1", "0111010"}, {"D", "0001100"},
{"A", "0110000"}, {"!D", "0001101"}, {"!A", "0110001"}, {"-D", "0001111"}, {"-A", "0110011"},
{"D+1", "0011111"}, {"A+1", "0110111"}, {"D-1","0001110"}, {"A-1", "0110010"}, {"D+A", "0000010"},
{"D-A", "0010011"}, {"A-D", "000111"}, {"D&A", "0000000"}, {"D|A", "0010101"}, {"M", "1110000"},
{"!M", "1110001"}, {"-M", "1110011"}, {"M+1", "1110111"}, {"M-1", "1110010"}, {"D+M", "1000010"},
{"M-D", "1000111"}, {"D&M", "1000000"}, {"D|M", "1010101"}, "D-M", "1010011"};

commands destination[] = {{"M", "001"}, {"D", "010"}, {"MD", "011"}, {"A", "100"}, {"AM", "101"},
{"AD", "110"}, {"AMD", "111"}};

commands jmp[] = {{"JGT", "001"}, {"JEQ", "010"}, {"JGE", "011"}, {"JLT", "100"}, {"JNE", "101"},
{"JLE", "110"}, {"JMP", "111"}};

int num = 0;

FILE *rom;
FILE *CPU;

char read_label[30];

int main()
{
    int j = 0;
    fclose(fopen("out.txt", "w"));
    rom = fopen("code.txt", "r");
    while(fgets(read, 30, rom) != 0)
    {
        j = 0;
        for (int i = 0; read[i] != '\0'; i++)
        {
            if (read[i] == ' ')
            {
                continue;
            }
            instruction[j] = read[i];
            j++;
        }
        instruction[j] = '\0';
        if (instruction[0] == '@')
        {
            number();
            ins_A(num);
        }
        else
        {
            ins_D();
        }
    }
}
// void record_names()
// {
//     while(fgets(read, 30, rom))
//     {    
//         for(int i = 0, j = 0; read[i-1] != '\0'; i++)
//         {
//             if (read[i] != ' ')
//             {
//                 read_label[j] = read[i];
//                 j++;
//             }
//         }
//     }
//     if(read) 
// }
void number()
{
    num = 0;
    int check = 0;
    for (int i = 1; instruction[i] != '\n'; i++)
    {
        check = instruction[i] - '0';
        num = (num + check)*10;
    }
    num /= 10;
}

void ins_A(int n)
{
    for (int i = 0; i < 30; i++)
    {
        num_bin[i] = '\0';
        num_bina[i] = '0';
    }
    int i;
    for(i=0;n>0;i++)
    {
        num_bin[i]=n%2;
        n=n/2;
    }
    int j = 0;

    for(i=i-1;i>=0;i--)
    {

        num_bina[j] = num_bin[i]+'0';
        j++;
    }
    num_bina[j] = '\0';
    for(i = 16; i < 30; i++)
    instruction[i] = '\0';
    sprintf(instruction, "0%15s", num_bina);
    for (i = 0; i < 30; i++)
    {
        if (!(instruction[i] == '0' || instruction[i] == '1'))
        {
            instruction[i] = '0';
        }
    }
    instruction[16] = '\0'; 
    CPU  = fopen("out.txt","a+");
    fprintf(CPU, "%s\n", instruction);
    fclose(CPU);

}
void ins_D()
{
    if (check_type()==3)
    {
        int i;
        for (i = 0; instruction[i] != ';'; i++)
        {
            after_eq[i] = instruction[i];
        }
        after_eq[i] = '\0';
        i++;
        int j;
        for (j = 0; instruction[i] != '\0'; i++, j++)
        {
            aftersemi[j] = instruction[i];
        }
        aftersemi[j-1] = '\0';
        for (i = 0; i < sizeof(comp); i++)
        {
            if(!strcmp(after_eq, comp[i].c))
            {
                strcpy(after_eq, comp[i].cbin);
            }
        }

        for (i = 0; i < sizeof(comp); i++)
        {
            if(!strcmp(aftersemi, jmp[i].c))
            {
                strcpy(aftersemi, jmp[i].cbin);
            }
        }
        sprintf(instruction, "111%s000%s", after_eq, aftersemi);
    }
    else if (check_type()==2)
    {
        int i;
        for (i = 0; instruction[i] != '='; i++)
        {
            before_eq[i] = instruction[i];
        }
        before_eq[i] = '\0';
        i++;
        int j = 0;
        for (; instruction[i] != ';' && instruction[i] != '\0'; i++)
        {
            after_eq[j] = instruction[i];
            j++;
        }
        after_eq[j-1] = '\0';
        for (i = 0; i < sizeof(destination); i++)
        {
            if(!strcmp(before_eq, destination[i].c))
            {
                strcpy(before_eq, destination[i].cbin);
            }
        }
        for (i = 0; i < sizeof(comp); i++)
        {
            if(!strcmp(after_eq, comp[i].c))
            {
                strcpy(after_eq, comp[i].cbin);
            }
        }
        sprintf(instruction, "111%s%s000", after_eq, before_eq);
    }
    else if (check_type()==1)
    {
        int i;
        for (i = 0; instruction[i] != '='; i++)
        {
            before_eq[i] = instruction[i];
        }
        before_eq[i] = '\0';
        i++;
        int j = 0;
        for (; instruction[i] != ';' && instruction[i] != '\0'; i++)
        {
            after_eq[j] = instruction[i];
            j++;
        }
        after_eq[i-2] = '\0';
        j = j+i-2;
        for (i = 0; instruction[i] != '\0'; i++, j++)
        {
            aftersemi[i] = instruction[j];
        }
        aftersemi[10] = '\0';
        for (i = 0; i < sizeof(destination); i++)
        {
            if(!strcmp(before_eq, destination[i].c))
            {
                strcpy(before_eq, destination[i].cbin);
            }
        }
        for (i = 0; i < sizeof(comp); i++)
        {
            if(!strcmp(after_eq, comp[i].c))
            {
                strcpy(after_eq, comp[i].cbin);
            }
        }
        for (i = 0; i < sizeof(comp); i++)
        {
            if(!strcmp(aftersemi, jmp[i].c))
            {
                strcpy(aftersemi, jmp[i].cbin);
            }
        }
        sprintf(instruction, "111%s%s%s", after_eq, before_eq, aftersemi);
    }
    instruction[16] = '\0';
    CPU  = fopen("out.txt","a+");
    fprintf(CPU, "%s\n", instruction);
    fclose(CPU);
    
}
int check_type()
{
    for (int i = 0; instruction[i] != '\0'; i++)
    {
        if(instruction[i] == '=')
        {
            for (int j = i+1; instruction[j] != '\0'; j++)
            {
                if (instruction[j] == ';')
                {
                    return 1;
                }
            }
            return 2;
        }
    }
    for (int i = 0; instruction[i] != '\0'; i++)
    {
        if (instruction[i] == ';')
        {
            return 3;
        }
    }
}




// void ins_A();
// long long converted(int decimalnum);
// FILE *code;
// typedef struct symTab
// {
//     char name[30];
//     int value;
// }
// symTab;

// symTab temp;
// char num_bin[30];
// symTab Table[500];
// char ins[30];
// int main()
// {
//     code = fopen("code.txt", "r");
//     fflush(stdin);
//     fflush(stdout);
//     fgets(ins, sizeof(ins), code);
//     printf("%s", ins);
//     ins_A();
// }

// void ins_A()
// {
//     long long num = 0;
//     for (int j = 1; isdigit(ins[j]); j++)
//     {
//          num = (num+((int)(ins[j] - '0')))*10;
//     }
//     num /= 10;
//     for(int i = 0; i < 17; i++)
//     {
//         ins[i] = 'A';
//     }
//     ins[0] = '0';
//     temp.value = converted(num);
//     for (int j = 16; j > 0; j--)
//     {
//         ins[j] = temp.value%10;
//         temp.value /= 10;
//     }
//     for (int j = 0; j < 17; j++)
//     {
//         if (ins[j] == 'A')
//             ins[j] = '0';
//     }
//     ins[17] = '\0';
//     fclose(code);
//     fclose(fopen("out.txt", "w"));
//     code = fopen("out.txt", "a");
//     fprintf(code, "%s", ins);
//     num = converted(num)/10;
//     sprintf(num_bin, "%lld", num);
//     printf("\n%s", num_bin);


// }

// long long converted(int decimalnum)
// {
//     long long binarynum = 0;
//     int rem=0, Temp = 1;

//     while (decimalnum>0)
//     {
//         rem = decimalnum%2;
//         decimalnum = decimalnum / 2;
//         binarynum = binarynum + rem*Temp;
//         Temp = Temp * 10;
//     }
//     return binarynum;
// }
