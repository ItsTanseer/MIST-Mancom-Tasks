.model small
.stack 100h

.data
    prompt  db "Enter a string: $"
    buffer  db 50         
            db ?           
            db 50 dup('$') 

    outmsg  db 0Dh,0Ah,"Capitalized: $"

.code
main proc
    mov ax, @data
    mov ds, ax
    mov dx, offset prompt
    mov ah, 09h
    int 21h

    mov dx, offset buffer
    mov ah, 0Ah
    int 21h

    lea di, buffer+2

process_loop:
    mov al, [di]     
    cmp al, '$'         
    je done_process

    cmp al, 'a'
    jb skip_lower     
    cmp al, 'z'
    ja skip_lower    

    sub al, 20h       

    mov [di], al       

skip_lower:
    inc di              
    jmp process_loop

done_process:

    mov dx, offset outmsg
    mov ah, 09h
    int 21h
    lea dx, buffer+2
    mov ah, 09h
    int 21h
    mov ah, 4Ch
    int 21h
main endp
end main
