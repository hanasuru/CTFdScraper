# File Formats [50 pts]

**Category:** Forensic
**Solves:** 64

## Description
>Tentunya kita tahu bahwa ada berbagai macam jenis file, yang pada umumnya dibedakan dari extensionnya (.jpg, .png, .exe, .zip, dll). Tapi, pada kenyataannya, file extension tidak menjadi satu - satunya cara untuk membedakan jenis file.

Jika kita mencoba dump content suatu file kedalam bentuk hexadecimal, kita dapat melihat beberapa byte awal pada file tersebut, dimana byte - byte awal tersebut disebut <a href="https://en.wikipedia.org/wiki/List_of_file_signatures"><b>File Signature</b></a>.

Pada challenge kali ini, akan diberikan sebuah file jpeg yang rusak, dan kalian diminta untuk melihat apakah File Signature nya sudah benar atau belum. Jika belum benar, coba kalian perbaiki file signaturenya agar kalian bisa membuka file tersebut.

Flag pada challenge ini tersembunyi pada foto yang rusak tersebut.

**Hint**
* Flag telah diubah menjadi `case insensitive`

## Solution

### Flag

