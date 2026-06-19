# Set PYTHONPATH agar Python mengenali folder src sebagai modul
$env:PYTHONPATH = ".\src"

# Gunakan flag -v (verbose) standar tanpa testdox
python -m pytest -v .\src\tests\