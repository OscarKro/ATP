
.section .text
.align 4


wim:
push {lr}
sub r4, #1
pop {pc}

jet:
push {lr}
add r4, #1
pop {pc}

does:
push {lr}
mov r4, r0
pop {pc}

duif:
add r0,r6
mov pc, r0

schaap:
push {lr}
add [r4] #1
pop {pc}

lam:
push {lr}
sub [r4] #1
pop {pc}

teun:
push {lr}
add r0, r5
mov [r4], [r0]
pop {pc}

aap:
push {lr}
mov r0, [r0]
cmp r0, [r1]
beq r2
pop {pc}

noot:
push {lr}
mov [r4], r0
pop {pc}

vuur:
mov sp, r5
pop {r4,r5,r6,pc}


_aapnootmies:
push {r4,r5,r6,lr}
mov r4, sp
mov r5, r4
sub r4, #1
sub sp, #1000
mov r0, #0
bl noot
bl wim
mov r0, #100
bl noot
bl jet
mov pc, r0
bl schaap
bl mies
mov r0, #1
mov r1, #2
mov r2, #10
bl aap
mov r0, #6
bl duif
mov pc, [r5]
mov r0, #0
bl does
mov r0, #15
bl noot
bl wim
mov r0, #6
bl duif
bl vuur