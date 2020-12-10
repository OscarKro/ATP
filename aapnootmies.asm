
.section .text
.align 4


aapnootmies:
push {r4,r5,r6,lr}
mov r4, sp
mov r5, r4
sub r4, #1
sub sp, #1000
mov r6, pc
b _D5
mov r0, #5
mov [r4], r0
add r4, #1
mov pc, [r5]
_D5:
mov r0, #10
mov [r4], r0
sub r4, #1
mov sp, r5
pop {r4,r5,r6,pc}
