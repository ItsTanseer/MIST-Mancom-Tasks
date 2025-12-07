.model small
.stack 100h
.data
    num1 db 5
    num2 db 3
    msg  db "The sum is: $"
.code

main proc
    mov ax, @data
    mov ds, ax

    mov al, num1
    add al, num2

    mov dx, offset msg
    mov ah, 09h
    int 21h

    add al, 30h
    mov dl, al
    mov ah, 02h
    int 21h

    mov ah, 4Ch
    int 21h
main endp
end main
