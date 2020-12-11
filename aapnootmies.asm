
.section .text
.align 4
.global aapnootmies

aapnootmies:
push {r4,r5,r6,lr}
mov r4, sp
mov r5, r4
sub r4, #4
sub sp, #400
mov r6, pc
_L0:
mov r0,#1
str r0, [r4]
_L1:
sub r4, #4
_L2:
mov r0,#100
str r0, [r4]
_L3:
add r4, #4
_L4:
ldr r0, [r4]
bl print
_L5:
mov r0,#1
mov r1,#2
mov r3,#4
mul r0,r3
mul r1,r3
sub r0, r5, r0
sub r1, r5, r1
ldr r0, [r0]
ldr r1, [r1]
cmp r0, r1
beq _L8
_L6:
ldr r0, [r4]
add r0, #1
str r0, [r4]
_L7:
b _L4
_L8:
mov sp, r5
pop {r4,r5,r6,pc}
