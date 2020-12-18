
.section .text
.align 4
.global fibonacci

fibonacci:
push {r4,r5,r6,lr}
mov r4, sp
mov r5, r4
sub r4, #4
sub sp, #400
mov r6, pc
_L0:
mov r0,#1
mov r1, #4
mul r0, r0, r1
sub r0, r5, r0
str r4, [r0]
_L1:
ldr r0, [r4]
bl print
_L2:
mov sp, r5
pop {r4,r5,r6,pc}