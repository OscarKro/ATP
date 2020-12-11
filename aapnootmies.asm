.section .text
.align 4
.global aapnootmies

aapnootmies:
push {r4,r5,r6,lr}
mov r4, sp
mov r5, r4
sub r4, #1
sub sp, #100
mov r6, pc
_L0:
mov r0, #0
mov [r4], r0
_L1:
sub r4, #1
_L2:
mov r0, #10
mov [r4], r0
_L3:
add r4, #1
_L4:
add [r4] #1
_L5:
mov r0, [r4]
bl print
_L6:
mov r0, #1
mov r1, #2
add r0, r5
add r1, r5
mov r0, [r0]
mov r1, [r1]
cmp r0, r1
beq _L8
_L7:
b _L4
_L8:
mov sp, r5
pop {r4,r5,r6,pc}
