class SteamGame:
    def __init__(self, id, developers=[], tags_en=[], tags_ja=[], release_year=None):
        self.id: int = id
        self.developers: list[str] = developers
        self.tags_en: list[str] = tags_en
        self.tags_ja: list[str] = tags_ja
        self.release_year: str = release_year
    
    def get_keywords(self):
        ret = []
        if self.developers:
            ret.extend(self.developers)
        if self.tags_en:
            ret.extend(self.tags_en)
        if self.tags_ja:
            ret.extend(self.tags_ja)
        if self.release_year:
            ret.extend([self.release_year for x in range(3)])
        ret = [x.replace(' ', '') for x in ret]
        return ret