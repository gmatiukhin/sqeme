(begin
    (define os (py_import "os"))
    (define color (py_import "colorama"))
    (define getcwd (. os "getcwd"))
    (define cwd (getcwd))
    (print (
        ++ "The current path is: " (. color "Fore" "GREEN") cwd (. color "Fore" "RESET")
        " and this is being output using " (. color "Fore" "RED") "Python's Colorama module" (. color "Fore" "RESET")"!"))
    (list)
)