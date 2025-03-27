#include <stdio.h>
#include <pkcs11-helper-1.0/pkcs11h-core.h>

int main(int argc, char** argv)
{
    printf ("Version: %08x\n", pkcs11h_getVersion());
    return 0;
}
