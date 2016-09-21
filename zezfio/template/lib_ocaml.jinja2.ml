let split line s =
  let rec do_work lst word = function
  | 0 -> word::lst
  | i ->
    begin
      match line.[i-1] with
      | a when a ≡ s →
        if word <> "" then 
           do_work (word∷lst) "" (i-1) 
        else
           do_work lst "" (i-1)
      | a -> do_work lst ( (Char.escaped a)^word) (i-1)
    end
  in do_work [] "" (String.length line)
♢
(* 
Scalars
=======
*)

let read_scalar type_conversion group name =
  let line = 
   Zezfio.get @@ String.concat [ group ; "." ; name ]
  in
  type_conversion line


let fortran_bool_of_string = function 
  | "T" | "t" -> true 
  | "F" | "f" -> false 
  | x -> raise (Failure ("fortran_bool_of_string should be T or F: "^x))
;; 
 
let fortran_string_of_bool = function 
 | true -> "T\n" 
 | false-> "F\n" 
;; 
 
let read_int   = read_scalar   int_of_string
let read_int64 = read_scalar Int64.of_string
let read_float = read_scalar float_of_string
let read_string= read_scalar (fun (x:string) -> x)
let read_bool  = read_scalar fortran_bool_of_string

(*
Write
-----
*)

let print_int    out_channel i = Printf.sprintf out_channel "%20d\n" i 
and print_int64  out_channel i = Printf.sprintf out_channel "%20Ld\n" i 
and print_float  out_channel f = Printf.sprintf out_channel "%24.15e\n" f 
and print_string out_channel s = Printf.sprintf out_channel "%s\n" s 
and print_bool   out_channel b = Printf.sprintf out_channel "%s\n" (fortran_string_of_bool b)

let write_scalar print_fun group name s = 
  print_fun s
  |> Zezfio.set 
;; 
   
let write_int    = write_scalar print_int 
and write_int64  = write_scalar print_int64 
and write_float  = write_scalar print_float 
and write_bool   = write_scalar print_bool 
and write_string = write_scalar print_string 
;; 






let ezfio_set_file filename =
  Zezfio.initialize filename

{% for cat, attributes in json_config.iteritems() %}
  {% for var in attributes["attributes"] %}

let ezfio_set_{{cat}}_{{var.name}} buffer =
  let buffer_size =
    Zezfio.nbytes "{{cat}}.{{var.name}}" 
  in
  Zezfio.set "{{cat}}.{{var.name}}" buffer buffer_size


let ezfio_get_{{cat}}.{{var.name}} () =
  Zezfio.get "{{cat}}.{{var.name}}" 
  |> {{ c2stuff[var.type].fortran_type }}


let ezfio_has_{{cat}}.{{var.name}} = 
  Zezfio.has "{{cat}}.{{var.name}}" 
  
  {% endfor %}
{% endfor %}
