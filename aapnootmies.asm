
.section .text
.align 4


aapnootmies:
push {r4,r5,r6,lr}
mov r4, sp
mov r5, r4
sub r4, #1
sub sp, #100
mov r6, pc
_L0:
b _L6
_L1:
add [r4] #1
_L2:
nop // how to do cout? ask jan
_L3:
mov r0, #1
mov r1, #2
add r0, r5
add r1, r5
mov r0, [r0]
mov r1, [r1]
cmp r0, r1
beq _L5
_L4:
b _L1
_L5:
mov r0,r4
b _L?//there should be a weide here, ask jan
_L6:
mov r0, #0
mov [r4], r0
_L7:
sub r4, #1
_L8:
mov r0, #10
mov [r4], r0
_L9:
mov r0, #0
sub r0, r5, r0
mov r4, r0
_L10:
mov r0, #14
mov [r4], r0
_L11:
sub r4, #1
_L12:
b _L1
_L13:
mov sp, r5
pop {r4,r5,r6,pc}
