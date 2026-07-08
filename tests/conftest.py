def pytest_itemcollected(item):
    """
    Hook bawaan Pytest untuk memanipulasi nama tes di terminal.
    Kita akan mengganti path file dengan docstring dari fungsi tes tersebut.
    """
    if item.obj.__doc__:
        # 1. Ambil teks docstring dan bersihkan spasi kosong
        doc = item.obj.__doc__.strip()

        # 2. Ambil nama Class tempat tes ini berada (Hapus kata "Test" di depannya)
        class_name = ""
        if item.parent and item.parent.name.startswith("Test"):
            class_name = item.parent.name.replace("Test", "")

        # 3. Ganti ID asli dengan format "NamaClass ➔ Deskripsi"
        if class_name:
            item._nodeid = f"{class_name} ➔ {doc}"
        else:
            item._nodeid = doc
