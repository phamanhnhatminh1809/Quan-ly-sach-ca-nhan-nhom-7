class Sach:
    def __init__(self, id = "", ten = "", tacGia = "", namXB = "", duongDan = ""):
        self.id = id
        self.ten = ten
        self.tacGia = tacGia
        self.namXB = namXB
        self.duongDan = duongDan
    
    def toDict(self):
        return {
            "id": self.id,
            "ten": self.ten,
            "tacgia": self.tacGia,
            "namxb": self.namXB,
            "duongdan": self.duongDan
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            id = data["id"],
            ten = data["ten"],
            tacGia = data.get("tacgia", ""),
            namXB = data.get("namxb", ""),
            duongDan = data.get("duongdan", "")
        )
    