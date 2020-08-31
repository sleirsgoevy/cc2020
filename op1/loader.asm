use32

global _start
_start:
global main
main:
incbin "loader.bin"

pad:
times 0x2000+_start-pad db 0

payload:
incbin "rom.signed"
