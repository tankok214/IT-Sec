BINARY_NAME_32:="app_32"
BINARY_NAME_64:="app_64"

D_FILE:="app.d"
SOURCE_FILE:="main.c"
OBJECT_FILE:="app.o"

# compile parameters
gcc_FLAGS:=-mpreferred-stack-boundary=2 -mno-accumulate-outgoing-args -msse2
COMPILER_FLAGS:=-O0 -g3 -c -fmessage-length=0 -D_FORTIFY_SOURCE=0 -MMD -MP -MF$(D_FILE) -MT$(D_FILE) -o $(OBJECT_FILE) $(SOURCE_FILE)
LINKER_FLAGS_32:=-o $(BINARY_NAME_32) $(OBJECT_FILE) 
LINKER_FLAGS_64:=-o $(BINARY_NAME_64) $(OBJECT_FILE) 

# ARCHITECTURE (compiler flag)
FOR_X86:=-m32 
FOR_X64:=-m64

######################################
# Compiler options

# Stack smaching protection (compiler flag)
ENABLE_SSP:=-fstack-protector-all
DISABLE_SSP:=-fno-stack-protector

# RELRO (compiler flag)
ENABLE_FULL_RELRO:=-Wl,-z,relro,-z,now
DISABLE_FULL_RELRO:=-Wl,-z,relro

# FORTIFY SOURCE
ENABLE_FORITY_SOURCE:=-D_FORTIFY_SOURCE=2
DISABLE_FORITY_SOURCE:=-D_FORTIFY_SOURCE=0

#######################################
# Linker options

# POSITION DEPENDENT EXECUTION (linker flag)
ENABLE_PIE:=-pie
DISABLE_PIE:=-no-pie

# NX bit protection (linker flag)
ENABLE_NX:=-z noexecstack # stack not executable
DISABLE_NX:=-z execstack # stack is executable

#######################################
# OS level options

# ASLR (OS level setting)
ENABLE_ASLR:=sudo sysctl -w kernel.randomize_va_space=2
DISABLE_ASLR:=sudo sysctl -w kernel.randomize_va_space=0


default: noProtection

noProtection:
	gcc $(FOR_X86) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X86) $(gcc_FLAGS) $(LINKER_FLAGS_32) $(DISABLE_NX) $(DISABLE_PIE)  $(DISABLE_FULL_RELRO)
	$(DISABLE_ASLR)

noProtection64:
	gcc $(FOR_X64) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X64) $(gcc_FLAGS) $(LINKER_FLAGS_64) $(DISABLE_NX) $(DISABLE_PIE) $(DISABLE_FULL_RELRO)
	$(DISABLE_ASLR)


allProtection:
	gcc $(FOR_X86) $(COMPILER_FLAGS) $(gcc_FLAGS) $(ENABLE_SSP)
	gcc $(FOR_X86) $(gcc_FLAGS) $(LINKER_FLAGS_32) $(ENABLE_NX) $(ENABLE_PIE) $(ENABLE_FULL_RELRO)
	$(ENABLE_ASLR)

allProtection64:
	gcc $(FOR_X64) $(COMPILER_FLAGS) $(gcc_FLAGS) $(ENABLE_SSP)
	gcc $(FOR_X64) $(gcc_FLAGS) $(LINKER_FLAGS_64) $(ENABLE_NX) $(ENABLE_PIE) $(ENABLE_FULL_RELRO)
	$(ENABLE_ASLR)


withSSP:
	gcc $(FOR_X86) $(COMPILER_FLAGS) $(gcc_FLAGS) $(ENABLE_SSP)
	gcc $(FOR_X86) $(gcc_FLAGS) $(LINKER_FLAGS_32) $(DISABLE_NX) $(DISABLE_PIE)  $(DISABLE_FULL_RELRO)
	$(DISABLE_ASLR)

withSSP64:
	gcc $(FOR_X64) $(COMPILER_FLAGS) $(gcc_FLAGS) $(ENABLE_SSP)
	gcc $(FOR_X64) $(gcc_FLAGS) $(LINKER_FLAGS_64) $(DISABLE_NX) $(DISABLE_PIE) $(DISABLE_FULL_RELRO)
	$(DISABLE_ASLR)


withRELRO:
	gcc $(FOR_X86) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X86) $(gcc_FLAGS) $(LINKER_FLAGS_32) $(DISABLE_NX) $(DISABLE_PIE)  $(ENABLE_FULL_RELRO)
	$(DISABLE_ASLR)

withRELRO64:
	gcc $(FOR_X64) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X64) $(gcc_FLAGS) $(LINKER_FLAGS_64) $(DISABLE_NX) $(DISABLE_PIE) $(ENABLE_FULL_RELRO)
	$(DISABLE_ASLR)


withPIE:
	gcc $(FOR_X86) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X86) $(gcc_FLAGS) $(LINKER_FLAGS_32) $(DISABLE_NX) $(ENABLE_PIE)  $(DISABLE_FULL_RELRO)
	$(DISABLE_ASLR)

withPIE64:
	gcc $(FOR_X64) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X64) $(gcc_FLAGS) $(LINKER_FLAGS_64) $(DISABLE_NX) $(ENABLE_PIE) $(DISABLE_FULL_RELRO)
	$(DISABLE_ASLR)

withNX:
	gcc $(FOR_X86) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X86) $(gcc_FLAGS) $(LINKER_FLAGS_32) $(ENABLE_NX) $(DISABLE_PIE)  $(DISABLE_FULL_RELRO)
	$(DISABLE_ASLR)

withNX64:
	gcc $(FOR_X64) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X64) $(gcc_FLAGS) $(LINKER_FLAGS_64) $(ENABLE_NX) $(DISABLE_PIE) $(DISABLE_FULL_RELRO)
	$(DISABLE_ASLR)


withASLR:
	gcc $(FOR_X86) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X86) $(gcc_FLAGS) $(LINKER_FLAGS_32) $(DISABLE_NX) $(DISABLE_PIE)  $(DISABLE_FULL_RELRO)
	$(ENABLE_ASLR)

withASLR64:
	gcc $(FOR_X64) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X64) $(gcc_FLAGS) $(LINKER_FLAGS_64) $(DISABLE_NX) $(DISABLE_PIE) $(DISABLE_FULL_RELRO)
	$(ENABLE_ASLR)

withASLRwithPIE:
	gcc $(FOR_X86) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X86) $(gcc_FLAGS) $(LINKER_FLAGS_32) $(DISABLE_NX) $(ENABLE_PIE)  $(DISABLE_FULL_RELRO)
	$(ENABLE_ASLR)

withASLRwithPIE64:
	gcc $(FOR_X64) $(COMPILER_FLAGS) $(gcc_FLAGS) $(DISABLE_SSP)
	gcc $(FOR_X64) $(gcc_FLAGS) $(LINKER_FLAGS_64) $(DISABLE_NX) $(ENABLE_PIE) $(DISABLE_FULL_RELRO)
	$(ENABLE_ASLR)

shellcode:
	nasm -f elf -o shellcode.o -l shellcode.lst shellcode.s
	ld -o shellcode shellcode.o -m elf_i386
	rm shellcode.o

clean:
	rm -rf $(OBJECT_FILE) $(D_FILE) $(BINARY_NAME_32) $(BINARY_NAME_64)
	rm -rf shellcode BOFShellcode.bin shellcode.bin
