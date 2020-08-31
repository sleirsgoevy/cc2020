use32
org 0x80002400

magic:
db 0x50, 0x4f, 0x53, 0x4f
version:
dw 1
filesize:
dw end-magic
signature_offset:
dd signature-magic
entry:
dd _start-magic

_start:
int 0x22
mov eax, 0x179
int 0x21

pad:
times 64+magic-pad db 0
signature:
times 16 db 0
end:
