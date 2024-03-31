(
    begin
    (
        +                   # $out = "Hello World " + ($A)
        "Hello World "
        (
            +               # $A = $B + "Scheme"
            (
                +           # $B = "and " + "also "
                (+ "and" " ")
                (+ "also" " ")
            )
            'Scheme'
        )
    )
)