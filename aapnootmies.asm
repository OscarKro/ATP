
.section .text
.align 4
.global aapnootmies

_H90:
push {lr}
_HL1:
ldr r0, [r4]
add r0, #1
str r0, [r4]
_HL2:
ldr r0, [r4]
bl print
_HL3:
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
beq _HL4
bne _HL5
_HL4:
b _HL1
_HL5:
b _HL2
_HL6:
pop {pc}

aapnootmies:
push {r4,r5,r6,lr}
mov r4, sp
mov r5, r4
sub r4, #4
sub sp, #400
mov r6, pc
_L11:
mov r0,#0
str r0, [r4]
_L12:
sub r4, #4
_L13:
mov r0,#100
str r0, [r4]
_L14:
add r4, #4
_L15:
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
beq _L16
bne _L17
_L16:
b _L12
_L17:
bl _H90
_L18:
b _L8
_L19:
mov sp, r5
pop {r4,r5,r6,pc}